"""Pruebas DB-free de la resolución de URLs (T-13)."""

from django.urls import resolve, reverse

from config.views import health, home


def test_home_url_resolves_to_home_view() -> None:
    """La raíz resuelve a la vista home y conserva su nombre."""
    match = resolve("/")
    assert match.func is home
    assert match.url_name == "home"
    assert reverse("home") == "/"


def test_health_url_resolves_to_health_view() -> None:
    """health/ resuelve a la vista health y conserva su nombre."""
    match = resolve("/health/")
    assert match.func is health
    assert match.url_name == "health"
    assert reverse("health") == "/health/"


def test_admin_url_is_registered_under_admin_namespace() -> None:
    """admin/ resuelve al índice del Admin en el namespace admin."""
    match = resolve("/admin/")
    assert match.app_name == "admin"
    assert "admin" in match.namespaces
    assert match.url_name == "index"
    assert reverse("admin:index") == "/admin/"
