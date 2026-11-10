"""Pruebas DB-free de la configuración de la fundación (T-13)."""

import os

from django.conf import settings

GUARD_ENV_VARIABLES = (
    "DJANGO_SECRET_KEY",
    "MYSQL_DATABASE",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_TEST_USER",
    "MYSQL_TEST_PASSWORD",
)


def test_installed_apps_enable_unfold_before_admin() -> None:
    """Unfold precede al Admin y apps.core queda al final de INSTALLED_APPS."""
    installed_apps = list(settings.INSTALLED_APPS)
    assert "unfold" in installed_apps
    assert "django.contrib.admin" in installed_apps
    assert installed_apps.index("unfold") < installed_apps.index("django.contrib.admin")
    assert installed_apps[-1] == "apps.core"


def test_templates_include_project_templates_dir() -> None:
    """TEMPLATES[0]['DIRS'] incluye el directorio global de plantillas."""
    template_dirs = settings.TEMPLATES[0]["DIRS"]
    assert settings.BASE_DIR / "templates" in template_dirs


def test_static_files_configuration() -> None:
    """STATICFILES_DIRS y STATIC_ROOT apuntan a los directorios de la etapa."""
    # Django normaliza STATIC_URL agregando la barra inicial si falta.
    assert settings.STATIC_URL in {"static/", "/static/"}
    assert settings.BASE_DIR / "static" in settings.STATICFILES_DIRS
    assert settings.STATIC_ROOT == settings.BASE_DIR / "staticfiles"


def test_unfold_identity_configuration() -> None:
    """UNFOLD define la identidad mínima de NexoPyme AI."""
    unfold_settings = settings.UNFOLD
    assert unfold_settings["SITE_TITLE"] == "NexoPyme AI"
    assert unfold_settings["SITE_HEADER"] == "NexoPyme AI"
    assert unfold_settings["SITE_SUBHEADER"] == "Administración"
    assert unfold_settings["SITE_URL"] == "/"


def test_localization_configuration() -> None:
    """La localización usa español de Argentina y el catálogo del proyecto."""
    assert settings.LANGUAGE_CODE == "es-ar"
    assert settings.TIME_ZONE == "America/Argentina/Buenos_Aires"
    assert settings.BASE_DIR / "locale" in settings.LOCALE_PATHS


def test_settings_test_guard_variables_are_present() -> None:
    """Las guardas de settings_test disponen de sus variables sin abrir base."""
    missing = [name for name in GUARD_ENV_VARIABLES if not os.environ.get(name)]
    assert missing == [], f"Faltan variables de guarda: {missing}"
    assert os.environ["MYSQL_USER"] != os.environ["MYSQL_TEST_USER"]

    database = settings.DATABASES["default"]
    assert database["NAME"] == "nexopyme_bootstrap_dev"
    assert database["HOST"] == "127.0.0.1"
    assert str(database["PORT"]) == "3306"
    assert database["TEST"]["NAME"] == "nexopyme_bootstrap_test"
    assert database["USER"] == "nexopyme_test_user"
