"""Pruebas de los modelos y servicios de auditoría (T-04, T-05)."""

from __future__ import annotations

import pytest
from django.db import transaction as db_transaction
from django.test import TransactionTestCase

from apps.accounts.models import Company
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
