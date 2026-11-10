"""Modelos de auditoría y eventos de seguridad (T-04).

Ambos modelos son de solo adición: no se actualizan ni se eliminan desde la
aplicación. Los servicios de T-05 son la única vía de escritura.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class ImmutableRecordError(Exception):
    """Se intentó modificar o eliminar un registro inmutable."""


class ImmutableQuerySet(models.QuerySet):
    """Impide las mutaciones masivas sobre registros de auditoría."""

    def update(self, **kwargs: object) -> int:
        raise ImmutableRecordError("Los registros de auditoría no se actualizan.")

    def delete(self) -> tuple[int, dict[str, int]]:
        raise ImmutableRecordError("Los registros de auditoría no se eliminan.")


class AuditEvent(models.Model):
    """Operación de negocio relevante, con valores anterior y nuevo."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="audit_events",
    )
    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.PROTECT,
        related_name="audit_events",
    )
    entity = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=64)
    action = models.CharField(max_length=100)
    result = models.CharField(max_length=20)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImmutableQuerySet.as_manager()

    class Meta:
        verbose_name = "evento de auditoría"
        verbose_name_plural = "eventos de auditoría"
        indexes = [  # noqa: RUF012
            models.Index(
                fields=["company", "created_at"],
                name="audit_company_created_idx",
            )
        ]

    def save(self, *args: object, **kwargs: object) -> None:
        if not self._state.adding:
            raise ImmutableRecordError("Los registros de auditoría no se actualizan.")
        super().save(*args, **kwargs)

    def delete(self, *args: object, **kwargs: object) -> tuple[int, dict[str, int]]:
        raise ImmutableRecordError("Los registros de auditoría no se eliminan.")

    def __str__(self) -> str:
        return f"{self.action} · {self.entity} · {self.entity_id}"


class SecurityEvent(models.Model):
    """Rechazo por aislamiento, capacidad o credenciales inválidas."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="security_events",
    )
    company = models.ForeignKey(
        "accounts.Company",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="security_events",
    )
    attempted_company_id = models.PositiveBigIntegerField(null=True, blank=True)
    action = models.CharField(max_length=100)
    result = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImmutableQuerySet.as_manager()

    class Meta:
        verbose_name = "evento de seguridad"
        verbose_name_plural = "eventos de seguridad"
        indexes = [  # noqa: RUF012
            models.Index(
                fields=["company", "created_at"],
                name="security_company_created_idx",
            )
        ]

    def save(self, *args: object, **kwargs: object) -> None:
        if not self._state.adding:
            raise ImmutableRecordError(
                "Los eventos de seguridad no se actualizan."
            )
        super().save(*args, **kwargs)

    def delete(self, *args: object, **kwargs: object) -> tuple[int, dict[str, int]]:
        raise ImmutableRecordError("Los eventos de seguridad no se eliminan.")

    def __str__(self) -> str:
        return f"{self.action} · {self.result}"
