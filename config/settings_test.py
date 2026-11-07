"""Configuración de Django exclusiva para la suite de pruebas (T-10).

Deriva de `config.settings` y fuerza el uso exclusivo de la base de pruebas
`nexopyme_bootstrap_test` con el usuario `nexopyme_test_user`. No contiene
credenciales: las lee de variables de entorno del proceso.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .settings import *
from .settings import DATABASES, _get_required_env

TEST_DATABASE_NAME = "nexopyme_bootstrap_test"
DEVELOPMENT_DATABASE_NAME = "nexopyme_bootstrap_dev"
TEST_DATABASE_USER = "nexopyme_test_user"
AUTHORIZED_HOST = "127.0.0.1"
AUTHORIZED_PORT = "3306"

DATABASES["default"]["TEST"] = {
    "NAME": TEST_DATABASE_NAME,
    "CHARSET": "utf8mb4",
    "COLLATION": "utf8mb4_unicode_ci",
    "MIGRATE": True,
    "MIRROR": None,
}

DATABASES["default"]["USER"] = _get_required_env("MYSQL_TEST_USER")
DATABASES["default"]["PASSWORD"] = _get_required_env("MYSQL_TEST_PASSWORD")

if set(DATABASES) != {"default"}:
    raise ImproperlyConfigured(
        "La configuración de pruebas solo admite el alias 'default'."
    )

if DATABASES["default"]["ENGINE"] != "django.db.backends.mysql":
    raise ImproperlyConfigured(
        "La configuración de pruebas exige el backend MySQL."
    )

if (
    DATABASES["default"]["HOST"] != AUTHORIZED_HOST
    or str(DATABASES["default"]["PORT"]) != AUTHORIZED_PORT
):
    raise ImproperlyConfigured(
        "La configuración de pruebas exige el destino 127.0.0.1:3306."
    )

if DATABASES["default"]["NAME"] != DEVELOPMENT_DATABASE_NAME:
    raise ImproperlyConfigured(
        "La configuración de pruebas exige que MYSQL_DATABASE sea "
        f"{DEVELOPMENT_DATABASE_NAME}."
    )

if DATABASES["default"]["TEST"]["NAME"] != TEST_DATABASE_NAME:
    raise ImproperlyConfigured(
        f"La base de pruebas debe ser {TEST_DATABASE_NAME}."
    )

if DATABASES["default"]["TEST"]["NAME"] == DATABASES["default"]["NAME"]:
    raise ImproperlyConfigured(
        "La base de pruebas no puede coincidir con la base de desarrollo."
    )

if DATABASES["default"]["TEST"]["MIRROR"]:
    raise ImproperlyConfigured("TEST['MIRROR'] debe ser None.")

if DATABASES["default"]["TEST"]["MIGRATE"] is not True:
    raise ImproperlyConfigured("TEST['MIGRATE'] debe ser True.")

if DATABASES["default"]["TEST"]["CHARSET"] != "utf8mb4":
    raise ImproperlyConfigured("TEST['CHARSET'] debe ser utf8mb4.")

if DATABASES["default"]["TEST"]["COLLATION"] != "utf8mb4_unicode_ci":
    raise ImproperlyConfigured(
        "TEST['COLLATION'] debe ser utf8mb4_unicode_ci."
    )

if DATABASES["default"]["USER"] != TEST_DATABASE_USER:
    raise ImproperlyConfigured(
        f"El usuario de pruebas debe ser {TEST_DATABASE_USER}."
    )

if DATABASES["default"]["USER"] == os.environ.get("MYSQL_USER"):
    raise ImproperlyConfigured(
        "El usuario de pruebas no puede coincidir con el usuario de desarrollo."
    )
