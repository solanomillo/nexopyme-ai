"""Guardas de seguridad para la suite de pruebas (T-10)."""

import pytest
from django.conf import settings

# Mantener sincronizadas con config/settings_test.py.
AUTHORIZED_SETTINGS_MODULE = "config.settings_test"
AUTHORIZED_TEST_DATABASE = "nexopyme_bootstrap_test"
PROTECTED_DEVELOPMENT_DATABASE = "nexopyme_bootstrap_dev"
AUTHORIZED_TEST_USER = "nexopyme_test_user"
AUTHORIZED_HOST = "127.0.0.1"
AUTHORIZED_PORT = "3306"


def pytest_configure(config: pytest.Config) -> None:
    """Aborta antes de cualquier acceso a MySQL si la configuración no es segura."""
    problems = []

    if not settings.configured:
        pytest.exit("Django settings no configurados.", returncode=2)

    if getattr(settings, "SETTINGS_MODULE", None) != AUTHORIZED_SETTINGS_MODULE:
        pytest.exit(
            "La suite de pruebas exige DJANGO_SETTINGS_MODULE="
            f"{AUTHORIZED_SETTINGS_MODULE}.",
            returncode=2,
        )

    database = settings.DATABASES.get("default", {})
    test_settings = database.get("TEST", {}) or {}
    engine = database.get("ENGINE")
    host = database.get("HOST")
    port = database.get("PORT")
    name = database.get("NAME")
    user = database.get("USER")
    test_name = test_settings.get("NAME")
    mirror = test_settings.get("MIRROR")
    migrate = test_settings.get("MIGRATE")

    if set(settings.DATABASES) != {"default"}:
        problems.append("solo se admite el alias 'default'")
    if engine != "django.db.backends.mysql":
        problems.append("el motor debe ser MySQL")
    if host != AUTHORIZED_HOST or str(port) != AUTHORIZED_PORT:
        problems.append("el destino debe ser 127.0.0.1:3306")
    if name != PROTECTED_DEVELOPMENT_DATABASE:
        problems.append("la base de desarrollo no es nexopyme_bootstrap_dev")
    if test_name != AUTHORIZED_TEST_DATABASE:
        problems.append("la base de pruebas no es nexopyme_bootstrap_test")
    if test_name == name:
        problems.append("la base de pruebas coincide con la de desarrollo")
    if mirror:
        problems.append("TEST['MIRROR'] debe ser None")
    if migrate is not True:
        problems.append("TEST['MIGRATE'] debe ser True")
    if user != AUTHORIZED_TEST_USER:
        problems.append("el usuario de pruebas no es nexopyme_test_user")
    if getattr(config.option, "numprocesses", None) not in (None, 0):
        problems.append("no se permite ejecución paralela de pruebas")
    if getattr(config.option, "nomigrations", False):
        problems.append("no se permite --no-migrations/--nomigrations")
    if getattr(config.option, "reuse_db", False):
        problems.append("no se permite --reuse-db en T-10")
    if getattr(config.option, "create_db", False):
        problems.append("no se permite --create-db en T-10")

    if problems:
        pytest.exit(
            "Configuración de pruebas insegura: " + "; ".join(problems),
            returncode=2,
        )
