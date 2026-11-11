"""Pruebas de los modelos, servicios y vista de auditoría (T-04, T-05, T-18)."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from django.test import TransactionTestCase
from django.urls import reverse

from apps.accounts.capabilities import Role
from apps.accounts.models import (
    Account,
    Company,
    Membership,
    generate_username,
)
from apps.audit.models import (
    AuditEvent,
    ImmutableRecordError,
    SecurityEvent,
)
from apps.audit.services import record_audit, record_security


def _create_audit(company: Company) -> AuditEvent:
    return AuditEvent.objects.create(
        company=company,
        entity="Membership",
        entity_id="1",
        action="membership.created",
        result="success",
        before=None,
        after={"role": "operador"},
    )


@pytest.mark.django_db
def test_audit_event_is_created_with_expected_fields(company: Company) -> None:
    event = _create_audit(company)
    event.refresh_from_db()
    assert event.company == company
    assert event.entity == "Membership"
    assert event.action == "membership.created"
    assert event.after == {"role": "operador"}
    assert event.created_at is not None


@pytest.mark.django_db
def test_audit_event_cannot_be_saved_twice(company: Company) -> None:
    event = _create_audit(company)
    event.result = "failure"
    with pytest.raises(ImmutableRecordError):
        event.save()


@pytest.mark.django_db
def test_audit_event_cannot_be_deleted(company: Company) -> None:
    event = _create_audit(company)
    with pytest.raises(ImmutableRecordError):
        event.delete()


@pytest.mark.django_db
def test_audit_queryset_rejects_update_and_delete(company: Company) -> None:
    _create_audit(company)
    with pytest.raises(ImmutableRecordError):
        AuditEvent.objects.update(result="failure")
    with pytest.raises(ImmutableRecordError):
        AuditEvent.objects.all().delete()


@pytest.mark.django_db
def test_security_event_supports_missing_actor_and_company() -> None:
    event = SecurityEvent.objects.create(
        action="login.failed",
        result="denied",
        attempted_company_id=None,
    )
    event.refresh_from_db()
    assert event.actor is None
    assert event.company is None
    assert event.attempted_company_id is None


@pytest.mark.django_db
def test_security_event_is_immutable(company: Company) -> None:
    event = SecurityEvent.objects.create(
        company=company,
        action="access.denied",
        result="denied",
        attempted_company_id=42,
    )
    with pytest.raises(ImmutableRecordError):
        event.save()
    with pytest.raises(ImmutableRecordError):
        event.delete()
    with pytest.raises(ImmutableRecordError):
        SecurityEvent.objects.update(result="allowed")
    with pytest.raises(ImmutableRecordError):
        SecurityEvent.objects.all().delete()


def test_audit_models_do_not_store_sensitive_fields() -> None:
    forbidden = ("password", "token", "secret", "email", "api_key")
    for model in (AuditEvent, SecurityEvent):
        field_names = {field.name.lower() for field in model._meta.get_fields()}
        offenders = {
            name for name in field_names if any(term in name for term in forbidden)
        }
        assert offenders == set(), f"{model.__name__} expone {offenders}"


@pytest.mark.django_db
def test_record_audit_persists_after_commit(
    company: Company,
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        record_audit(
            actor=None,
            company=company,
            entity="Membership",
            entity_id=1,
            action="membership.created",
            result="success",
            after={"role": "operador"},
        )
    assert AuditEvent.objects.filter(company=company).count() == 1


@pytest.mark.django_db
def test_record_audit_is_deferred_until_commit(
    company: Company,
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks() as callbacks:
        record_audit(
            actor=None,
            company=company,
            entity="Membership",
            entity_id=1,
            action="membership.created",
            result="success",
        )
        assert AuditEvent.objects.count() == 0
    assert len(callbacks) == 1


@pytest.mark.django_db
def test_record_audit_sanitizes_sensitive_values(
    company: Company,
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        record_audit(
            actor=None,
            company=company,
            entity="Membership",
            entity_id=1,
            action="membership.created",
            result="success",
            before={"password": "secreto", "role": "consulta"},
            after={"token": "abc", "nested": {"secret": "xyz", "ok": True}},
        )
    event = AuditEvent.objects.get()
    assert event.before == {"role": "consulta"}
    assert event.after == {"nested": {"ok": True}}


@pytest.mark.django_db
def test_record_audit_does_not_mutate_source_payloads(
    company: Company,
    django_capture_on_commit_callbacks: object,
) -> None:
    before = {"password": "secreto", "role": "consulta"}
    after = {"nested": {"token": "abc", "ok": True}}
    with django_capture_on_commit_callbacks(execute=True):
        record_audit(
            actor=None,
            company=company,
            entity="Membership",
            entity_id=1,
            action="membership.created",
            result="success",
            before=before,
            after=after,
        )
    assert before == {"password": "secreto", "role": "consulta"}
    assert after == {"nested": {"token": "abc", "ok": True}}


@pytest.mark.django_db
def test_record_security_persists_immediately(company: Company) -> None:
    record_security(
        action="access.denied",
        result="denied",
        company=company,
        attempted_company_id=9,
    )
    assert SecurityEvent.objects.filter(
        company=company,
        attempted_company_id=9,
    ).exists()


class SecurityEventBoundaryTests(TransactionTestCase):
    """El evento sobrevive al rechazo y se descarta si se escribe dentro."""

    def test_event_written_after_rollback_survives(self) -> None:
        try:
            with db_transaction.atomic():
                Company.objects.create(name="Temporal")
                raise RuntimeError("fallo simulado")
        except RuntimeError:
            record_security(action="operation.failed", result="denied")
        self.assertEqual(SecurityEvent.objects.count(), 1)

    def test_event_written_inside_rolled_back_transaction_is_discarded(self) -> None:
        with self.assertRaises(RuntimeError), db_transaction.atomic():
            record_security(action="inside.atomic", result="denied")
            raise RuntimeError("fallo simulado")
        self.assertEqual(SecurityEvent.objects.count(), 0)


def _create_membership(
    company: Company,
    email: str,
    role: str = Role.ENCARGADO.value,
) -> Membership:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=None,
    )
    account = Account.objects.create(
        user=user,
        email=email,
        display_name=f"Persona {email}",
    )
    return Membership.objects.create(
        account=account,
        company=company,
        role=role,
    )


def _audit_event(
    company: Company,
    *,
    actor: object | None = None,
    action: str = "membership.created",
    before: object | None = None,
    after: object | None = None,
) -> AuditEvent:
    return AuditEvent.objects.create(
        actor=actor,
        company=company,
        entity="Membership",
        entity_id="1",
        action=action,
        result="success",
        before=before,
        after=after,
    )


def _security_event(
    company: Company | None,
    *,
    actor: object | None = None,
    action: str = "access.denied",
    attempted_company_id: int | None = None,
) -> SecurityEvent:
    return SecurityEvent.objects.create(
        actor=actor,
        company=company,
        action=action,
        result="denied",
        attempted_company_id=attempted_company_id,
    )


def test_audit_list_route_is_registered() -> None:
    """La ruta de auditoría se resuelve con el namespace accounts (DB-free)."""

    assert reverse("accounts:audit_list") == "/audit/"


@pytest.mark.django_db
def test_audit_list_requires_login(client: object) -> None:
    response = client.get("/audit/")
    assert response.status_code == 302
    assert response.url == "/login/?next=/audit/"


@pytest.mark.django_db
def test_audit_list_requires_the_audit_capability(
    client: object,
    company: Company,
    owner_membership: Membership,
) -> None:
    encargado = _create_membership(company, "encargado@example.com")
    _audit_event(company, actor=encargado.account.user, action="membership.role_changed")
    client.force_login(encargado.account.user)

    response = client.get("/audit/")

    assert response.status_code == 403
    assert "membership.role_changed" not in response.content.decode()


@pytest.mark.django_db
def test_audit_list_shows_only_the_company_events_with_actor(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    other_company = Company.objects.create(name="Otra empresa", is_active=False)
    _audit_event(
        company,
        actor=owner_account.user,
        action="membership.role_changed",
        before={"role": "operador"},
        after={"role": "consulta"},
    )
    _audit_event(company, actor=None, action="membership.without_actor")
    _audit_event(
        other_company,
        actor=owner_account.user,
        action="membership.foreign_company",
    )

    client.force_login(owner_account.user)
    response = client.get("/audit/")

    assert response.status_code == 200
    assert response["Cache-Control"] == "no-store"
    content = response.content.decode()
    assert "accounts/audit_list.html" in [
        template.name for template in response.templates
    ]
    assert "membership.role_changed" in content
    assert owner_account.display_name in content
    assert "operador" in content
    assert "consulta" in content
    assert "membership.without_actor" not in content
    assert "membership.foreign_company" not in content
    assert content.count("<h1") == 1


@pytest.mark.django_db
def test_audit_list_shows_security_events_without_the_attempted_company(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    other_company = Company.objects.create(name="Otra empresa", is_active=False)
    _security_event(
        company,
        actor=owner_account.user,
        action="permission.denied",
        attempted_company_id=987654321,
    )
    _security_event(company, actor=None, action="security.without_actor")
    _security_event(
        other_company,
        actor=owner_account.user,
        action="security.foreign_company",
    )

    client.force_login(owner_account.user)
    content = client.get("/audit/").content.decode()

    assert "permission.denied" in content
    assert "security.without_actor" not in content
    assert "security.foreign_company" not in content
    assert "987654321" not in content
    assert "attempted_company_id" not in content


@pytest.mark.django_db
def test_audit_list_labels_an_actor_without_commercial_account(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    technical = get_user_model().objects.create_user(
        username="tecnico-sin-cuenta",
        password=None,
    )
    _audit_event(company, actor=technical, action="technical.operation")

    client.force_login(owner_account.user)
    content = client.get("/audit/").content.decode()

    assert "technical.operation" in content
    assert "Personal técnico" in content
    assert "tecnico-sin-cuenta" not in content


@pytest.mark.django_db
def test_audit_list_paginates_twenty_events_per_page(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    for index in range(21):
        _audit_event(company, actor=owner_account.user, action=f"audit.{index:02d}")

    client.force_login(owner_account.user)
    first = client.get("/audit/")
    second = client.get("/audit/?audit_page=2")

    assert first.status_code == 200
    assert second.status_code == 200
    first_content = first.content.decode()
    second_content = second.content.decode()
    assert first_content.count("audit.") == 20
    assert second_content.count("audit.") == 1
    assert "Página 1 de 2" in first_content
    assert "Página 2 de 2" in second_content
    assert 'rel="next"' in first_content
    assert 'rel="prev"' in second_content


@pytest.mark.django_db
def test_audit_list_paginates_security_events(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    for index in range(21):
        _security_event(
            company,
            actor=owner_account.user,
            action=f"security.{index:02d}",
        )

    client.force_login(owner_account.user)
    first = client.get("/audit/")
    second = client.get("/audit/?security_page=2")

    assert first.content.decode().count("security.") == 20
    assert second.content.decode().count("security.") == 1
    assert "security.08" in first.content.decode()
    assert "security.00" in second.content.decode()


@pytest.mark.django_db
def test_audit_list_rejects_post_requests(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    assert client.post("/audit/").status_code == 405


@pytest.mark.django_db
def test_audit_pagination_keeps_the_other_page_parameter(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    for index in range(21):
        _audit_event(company, actor=owner_account.user, action=f"audit.{index:02d}")
        _security_event(
            company,
            actor=owner_account.user,
            action=f"security.{index:02d}",
        )

    client.force_login(owner_account.user)
    content = client.get("/audit/?security_page=2").content.decode()

    assert "audit_page=2&amp;security_page=2" in content


@pytest.mark.django_db
def test_audit_list_renders_both_empty_states(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    content = client.get("/audit/").content.decode()

    assert "No hay operaciones auditadas." in content
    assert "No hay eventos de seguridad." in content
    assert "pagination" not in content
