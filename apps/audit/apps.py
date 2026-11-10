"""Configuración de la app de auditoría compartida."""

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Configuración de la app de auditoría y eventos de seguridad."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    verbose_name = "Auditoría"
