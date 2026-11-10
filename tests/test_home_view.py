"""Pruebas DB-free de la vista home (T-13)."""

from pathlib import Path

from django.conf import settings
from django.test import Client, override_settings

HOME_TEMPLATE_FILES = (
    "templates/base.html",
    "templates/home.html",
    "templates/components/navbar.html",
    "templates/components/footer.html",
)

FORBIDDEN_TEMPLATE_TOKENS = ("request.user", "perms", "messages")


@override_settings(ALLOWED_HOSTS=["testserver"])
def test_home_returns_200_with_home_template() -> None:
    """GET / responde 200 y renderiza templates/home.html."""
    response = Client().get("/")
    assert response.status_code == 200
    template_names = [template.name for template in response.templates]
    assert "home.html" in template_names


@override_settings(ALLOWED_HOSTS=["testserver"])
def test_home_shows_identity_and_admin_link() -> None:
    """La home muestra NexoPyme AI, un único h1 y el enlace al Admin."""
    response = Client().get("/")
    content = response.content.decode("utf-8")
    assert "NexoPyme AI" in content
    assert 'href="/admin/"' in content
    assert content.count("<h1") == 1


@override_settings(ALLOWED_HOSTS=["testserver"])
def test_home_lists_modules_as_pending() -> None:
    """La home presenta los módulos como pendientes, sin datos ficticios."""
    response = Client().get("/")
    content = response.content.decode("utf-8")
    assert "Pendiente de especificación" in content
    for marker in ("Lorem ipsum", "TODO", "dato de ejemplo"):
        assert marker not in content


def test_home_templates_do_not_touch_session_context() -> None:
    """Las plantillas de la home no acceden a usuario, permisos ni mensajes."""
    base_dir = Path(settings.BASE_DIR)
    for relative in HOME_TEMPLATE_FILES:
        text = (base_dir / relative).read_text(encoding="utf-8")
        for token in FORBIDDEN_TEMPLATE_TOKENS:
            assert token not in text, f"{relative} accede a {token}"
