"""Configuración de Django para NexoPyme AI (Etapa 001).

Toda la configuración sensible se lee de variables de entorno del proceso.
Este archivo no contiene credenciales, secretos ni valores reales.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar .env sin sobrescribir variables ya definidas (override=False).
load_dotenv(BASE_DIR / ".env", override=False)


def _get_required_env(name: str) -> str:
    """Devuelve una variable de entorno obligatoria o falla con un error claro."""
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(
            f"Falta la variable de entorno obligatoria {name}."
        )
    return value


def _get_bool_env(name: str, default: bool = False) -> bool:
    """Interpreta una variable de entorno booleana."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int_env(name: str, default: int) -> int:
    """Interpreta una variable de entorno entera, con valor por defecto."""
    value = os.environ.get(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ImproperlyConfigured(
            f"La variable de entorno {name} debe ser un número entero."
        ) from exc


def _get_positive_int_env(name: str, default: int) -> int:
    """Interpreta una variable entera positiva; rechaza cero y negativos."""
    value = _get_int_env(name, default)
    if value <= 0:
        raise ImproperlyConfigured(
            f"La variable de entorno {name} debe ser mayor que cero."
        )
    return value


SECRET_KEY = _get_required_env("DJANGO_SECRET_KEY")
DEBUG = _get_bool_env("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.accounts",
    "apps.audit",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.accounts.middleware.ActiveCompanyMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "apps.accounts.context_processors.panel_navigation",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": _get_required_env("MYSQL_DATABASE"),
        "USER": _get_required_env("MYSQL_USER"),
        "PASSWORD": _get_required_env("MYSQL_PASSWORD"),
        "HOST": _get_required_env("MYSQL_HOST"),
        "PORT": _get_required_env("MYSQL_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailBackend",
    "apps.accounts.backends.TechnicalAdminBackend",
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/profile/"
LOGOUT_REDIRECT_URL = "/login/"

# Cookies de sesión y CSRF (T-20). `Secure` se activa por entorno; las
# variables son opcionales y no obligatorias.
_COOKIE_SECURE = _get_bool_env("DJANGO_SECURE_COOKIES", default=False)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = _COOKIE_SECURE
SESSION_COOKIE_AGE = _get_positive_int_env(
    "DJANGO_SESSION_COOKIE_AGE", default=1209600
)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = _COOKIE_SECURE

# Logging técnico por consola, separado de la auditoría de negocio (T-20).
# No se registran cuerpos de solicitud, credenciales ni datos personales.
_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _get_log_level() -> str:
    """Normaliza el nivel de log configurado, con ``INFO`` como defecto."""
    level = os.environ.get("DJANGO_LOG_LEVEL", "INFO").strip().upper()
    return level if level in _LOG_LEVELS else "INFO"


_LOG_LEVEL = _get_log_level()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": _LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": _LOG_LEVEL,
            "propagate": False,
        },
    },
}

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

UNFOLD = {
    "SITE_TITLE": "NexoPyme AI",
    "SITE_HEADER": "NexoPyme AI",
    "SITE_SUBHEADER": "Administración",
    "SITE_URL": "/",
}
