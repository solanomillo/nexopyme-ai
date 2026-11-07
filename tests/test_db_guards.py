"""Pruebas mínimas de aislamiento de la base de datos de pruebas (T-10)."""

import pytest
from django.conf import settings
from django.db import connection

AUTHORIZED_TEST_DATABASE = "nexopyme_bootstrap_test"


def test_test_database_settings_are_isolated() -> None:
    """La configuración de pruebas apunta solo a la base de pruebas dedicada."""
    assert settings.SETTINGS_MODULE == "config.settings_test"
    database = settings.DATABASES["default"]
    assert database["TEST"]["NAME"] == AUTHORIZED_TEST_DATABASE
    assert database["TEST"]["MIRROR"] is None
    assert database["TEST"]["MIGRATE"] is True
    assert database["TEST"]["CHARSET"] == "utf8mb4"
    assert database["TEST"]["COLLATION"] == "utf8mb4_unicode_ci"
    assert database["USER"] == "nexopyme_test_user"
    assert database["ENGINE"] == "django.db.backends.mysql"
    assert database["HOST"] == "127.0.0.1"
    assert str(database["PORT"]) == "3306"


@pytest.mark.django_db
def test_connection_targets_test_database() -> None:
    """La conexión de pytest apunta efectivamente a nexopyme_bootstrap_test."""
    assert connection.settings_dict["NAME"] == AUTHORIZED_TEST_DATABASE
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE()")
        assert cursor.fetchone()[0] == AUTHORIZED_TEST_DATABASE
