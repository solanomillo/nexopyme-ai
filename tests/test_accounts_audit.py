"""Pruebas de los modelos de auditoría y eventos de seguridad (T-04)."""

from __future__ import annotations

import pytest

from apps.accounts.models import Company
from apps.audit.models import (
    AuditEvent,
    ImmutableRecordError,
    SecurityEvent,
)


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
