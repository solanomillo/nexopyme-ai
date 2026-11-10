"""Servicios de auditoría y eventos de seguridad (T-05).

La auditoría de negocio se registra con ``transaction.on_commit`` para no
persistir operaciones que se revierten. Los eventos de seguridad se escriben en
el límite de rechazo, fuera del bloque atómico de negocio.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction

from .models import AuditEvent, SecurityEvent

_SENSITIVE_KEY_PARTS = ("password", "token", "secret", "api_key")


def _sanitize(value: Any) -> Any:
    """Elimina claves sensibles de forma recursiva."""

    if isinstance(value, dict):
        return {
            key: _sanitize(item)
            for key, item in value.items()
            if not any(part in str(key).lower() for part in _SENSITIVE_KEY_PARTS)
        }
    if isinstance(value, (list, tuple)):
        return [_sanitize(item) for item in value]
    return value


def record_audit(
    *,
    actor: Any | None,
    company: Any,
    entity: str,
    entity_id: object,
    action: str,
    result: str,
    before: Any | None = None,
    after: Any | None = None,
) -> None:
    """Registra una operación de negocio después de confirmar la transacción."""

    sanitized_before = _sanitize(before)
    sanitized_after = _sanitize(after)
    transaction.on_commit(
        lambda: AuditEvent.objects.create(
            actor=actor,
            company=company,
            entity=entity,
            entity_id=str(entity_id),
            action=action,
            result=result,
            before=sanitized_before,
            after=sanitized_after,
        )
    )


def record_security(
    *,
    action: str,
    result: str,
    actor: Any | None = None,
    company: Any | None = None,
    attempted_company_id: int | None = None,
) -> None:
    """Registra un rechazo de seguridad de forma inmediata e independiente."""

    SecurityEvent.objects.create(
        actor=actor,
        company=company,
        action=action,
        result=result,
        attempted_company_id=attempted_company_id,
    )
