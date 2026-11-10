"""Configuración de la app de cuentas y multiempresa."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuración de la app de cuentas, empresa y permisos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Cuentas y empresa"
