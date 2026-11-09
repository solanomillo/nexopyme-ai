from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuración de la app de infraestructura del proyecto."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Infraestructura"
