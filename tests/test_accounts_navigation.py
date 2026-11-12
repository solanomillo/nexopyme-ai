"""Pruebas de navegación por capacidad y recuperación de errores (T-24)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client

from apps.accounts.capabilities import Role
from apps.accounts.context_processors import panel_navigation
from apps.accounts.models import Account, Company, Membership, generate_username

TEST_PASSWORD = "Clave-Segura-2026"
STAGE_LABEL = "Etapa 003 — Cuentas y multiempresa"
OLD_STAGE_LABEL = "Etapa 001 — Django Project Foundation"
MANAGEMENT_LINKS = ('href="/users/"', 'href="/company/"', 'href="/audit/"')

pytestmark = pytest.mark.django_db


def _create_membership(
    company: Company,
    email: str,
    role: str = Role.CONSULTA.value,
) -> Membership:
    """Crea una cuenta con membresía activa en la empresa indicada."""

    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    account = Account.objects.create(
        user=user,
        email=email,
        display_name="Persona",
    )
    return Membership.objects.create(
        account=account,
        company=company,
        role=role,
    )


def _template_source(relative: str) -> str:
    """Lee el código fuente de una plantilla del proyecto."""

    return (Path(settings.BASE_DIR) / "templates" / relative).read_text(
        encoding="utf-8"
    )


def test_panel_navigation_without_membership_disables_every_link() -> None:
    """Sin membresía resuelta no se habilita ningún enlace de gestión."""

    context = panel_navigation(SimpleNamespace())
    assert context == {
        "panel_nav": {"users": False, "company": False, "audit": False}
    }


@pytest.mark.parametrize(
    ("role", "expected"),
    [
        (Role.DUENO.value, {"users": True, "company": True, "audit": True}),
        (Role.ENCARGADO.value, {"users": False, "company": False, "audit": False}),
        (Role.OPERADOR.value, {"users": False, "company": False, "audit": False}),
        (Role.CONSULTA.value, {"users": False, "company": False, "audit": False}),
    ],
)
def test_panel_navigation_follows_the_role_capabilities(
    role: str,
    expected: dict[str, bool],
) -> None:
    """Solo el dueño posee las capacidades de gestión del panel."""

    membership = SimpleNamespace(role=role)
    context = panel_navigation(SimpleNamespace(membership=membership))
    assert context["panel_nav"] == expected


def test_owner_sees_the_management_links_and_a_single_footer(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    """El dueño ve Usuarios, Empresa y Auditoría con un pie único."""

    client.force_login(owner_account.user)
    response = client.get("/panel/")
    assert response.status_code == 200
    content = response.content.decode()
    for href in MANAGEMENT_LINKS:
        assert href in content, href
    assert content.count("<footer") == 1


@pytest.mark.parametrize("role", [Role.ENCARGADO.value, Role.CONSULTA.value])
def test_roles_without_management_capabilities_hide_the_links(
    client: Client,
    company: Company,
    owner_membership: Membership,
    role: str,
) -> None:
    """Encargado y consulta conservan el panel, el perfil y la salida."""

    membership = _create_membership(company, f"{role}@example.com", role)
    client.force_login(membership.account.user)
    response = client.get("/panel/")
    assert response.status_code == 200
    content = response.content.decode()
    for href in MANAGEMENT_LINKS:
        assert href not in content, href
    assert 'href="/panel/"' in content
    assert 'href="/profile/"' in content
    assert "Cerrar sesión" in content


def test_consulta_is_denied_by_the_server_without_caching(
    client: Client,
    company: Company,
    owner_membership: Membership,
) -> None:
    """La autorización del servidor sigue vigente aunque se oculte el enlace."""

    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    client.force_login(consulta.account.user)
    for path in ("/users/", "/company/", "/audit/"):
        response = client.get(path)
        assert response.status_code == 403, path
        assert response["Cache-Control"] == "no-store", path


def test_capability_403_offers_the_return_to_panel(
    client: Client,
    company: Company,
    owner_membership: Membership,
) -> None:
    """Un 403 de capacidad ofrece volver al panel y no cerrar sesión."""

    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    client.force_login(consulta.account.user)
    content = client.get("/users/").content.decode()
    assert "Volver al panel" in content
    assert 'href="/panel/"' in content
    assert 'action="/logout/"' not in content


def test_context_403_offers_logout_with_csrf(client: Client) -> None:
    """Un 403 de contexto permite cerrar sesión con token CSRF."""

    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    client.force_login(user)
    response = client.get("/panel/")
    assert response.status_code == 403
    content = response.content.decode()
    assert "Cerrar sesión" in content
    assert 'action="/logout/"' in content
    assert "csrfmiddlewaretoken" in content
    assert "Volver al panel" not in content


def test_authenticated_404_offers_the_return_to_panel(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    """Un 404 autenticado con contexto ofrece volver al panel."""

    client.force_login(owner_account.user)
    response = client.get("/profile/999999/")
    assert response.status_code == 404
    content = response.content.decode()
    assert "Volver al panel" in content
    assert 'href="/panel/"' in content
    assert response["Cache-Control"] == "no-store"


def test_anonymous_404_offers_login(client: Client) -> None:
    """Un 404 anónimo ofrece iniciar sesión y nunca el panel."""

    response = client.get("/no-existe/")
    assert response.status_code == 404
    content = response.content.decode()
    assert "Iniciar sesión" in content
    assert 'href="/login/"' in content
    assert "Volver al panel" not in content
    assert response["Cache-Control"] == "no-store"


def test_foreign_and_missing_404_are_identical(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    foreign_account: Account,
) -> None:
    """Un recurso ajeno y uno inexistente comparten el mismo 404."""

    client.force_login(owner_account.user)
    foreign = client.get(f"/profile/{foreign_account.pk}/")
    missing = client.get("/profile/999999/")
    assert foreign.status_code == missing.status_code == 404
    assert foreign.content == missing.content


def test_stage_label_is_current_in_every_page(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    """Login, panel, home, 403 y 404 muestran la etapa 003 en el pie único."""

    anonymous = Client()
    client.force_login(owner_account.user)
    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    capability_client = Client()
    capability_client.force_login(consulta.account.user)

    responses = [
        anonymous.get("/login/"),
        client.get("/panel/"),
        anonymous.get("/"),
        capability_client.get("/users/"),
        client.get("/profile/999999/"),
    ]
    for response in responses:
        assert response.status_code in {200, 403, 404}
        content = response.content.decode()
        assert STAGE_LABEL in content
        assert OLD_STAGE_LABEL not in content


def test_error_pages_hide_the_public_navigation(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    """Los errores no muestran la navegación pública ni la Administración."""

    client.force_login(owner_account.user)
    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    capability_client = Client()
    capability_client.force_login(consulta.account.user)

    contents = [
        capability_client.get("/users/").content.decode(),
        client.get("/profile/999999/").content.decode(),
    ]
    for content in contents:
        assert 'href="/admin/"' not in content
        assert "Administración" not in content


def test_base_panel_uses_capability_aware_links_and_shared_footer() -> None:
    """base_panel.html filtra por capacidad, usa url y comparte el pie."""

    source = _template_source("base_panel.html")
    assert '{% include "components/footer.html" %}' in source
    assert "<footer" not in source
    for tag in (
        "{% url 'accounts:user_list' %}",
        "{% url 'accounts:company_edit' %}",
        "{% url 'accounts:audit_list' %}",
    ):
        assert tag in source, tag
    for href in MANAGEMENT_LINKS:
        assert href not in source, href
    for flag in ("panel_nav.users", "panel_nav.company", "panel_nav.audit"):
        assert f"{{% if {flag} %}}" in source, flag


def test_base_template_exposes_the_site_header_block() -> None:
    """base.html declara el bloque de cabecera y el pie usa la etapa 003."""

    base = _template_source("base.html")
    assert "{% block site_header %}" in base
    assert '{% include "components/navbar.html" %}' in base
    footer = _template_source("components/footer.html")
    assert STAGE_LABEL in footer
