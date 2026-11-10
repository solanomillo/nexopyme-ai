"""Pruebas DB-free del registro de Admin con Unfold (T-13)."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin


def test_user_and_group_use_unfold_model_admin() -> None:
    """User y Group están registrados con unfold.admin.ModelAdmin."""
    assert isinstance(admin.site._registry[User], ModelAdmin)
    assert isinstance(admin.site._registry[Group], ModelAdmin)


def test_no_unfold_contrib_modules_are_installed() -> None:
    """No se incorporan módulos unfold.contrib.* en INSTALLED_APPS."""
    contrib_apps = [
        app for app in settings.INSTALLED_APPS if app.startswith("unfold.contrib")
    ]
    assert contrib_apps == []
