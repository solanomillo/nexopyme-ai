"""Pruebas de autorización y errores uniformes (T-09)."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.test import override_settings
from django.urls import path

from apps.accounts.capabilities import Capability, Role, has_capability
from apps.accounts.decorators import (
    MissingCapabilityDenied,
    require_capability,
)
from apps.accounts.models import Account, Company, Membership, generate_username
from apps.audit.models import SecurityEvent
from config.urls import handler403, handler404  # noqa: F401


@require_capability(Capability.USUARIOS_GESTIONAR)
def guarded_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok")


def resource_view(request: HttpRequest, pk: int) -> HttpResponse:
    membership = get_object_or_404(Membership, pk=pk, company=request.company)
    if not has_capability(request.membership.role, Capability.USUARIOS_GESTIONAR):
        raise MissingCapabilityDenied(
            "No tenés permiso para realizar esta operación."
        )
    return HttpResponse(f"membership:{membership.pk}")


urlpatterns = [
    path("", lambda request: HttpResponse("home"), name="home"),
    path("guarded/", guarded_view),
    path("resource/<int:pk>/", resource_view),
]

pytestmark = pytest.mark.django_db


def _create_membership(company: Company, email: str, role: str) -> Membership:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password="Clave-Segura-2026",
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


@override_settings(ROOT_URLCONF=__name__)
def test_owner_with_capability_is_allowed(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/guarded/")
    assert response.status_code == 200
    assert response.content == b"ok"


@override_settings(ROOT_URLCONF=__name__)
def test_missing_capability_returns_capability_message(
    client: object,
    company: Company,
    owner_membership: Membership,
) -> None:
    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    client.force_login(consulta.account.user)
    response = client.get("/guarded/")
    assert response.status_code == 403
    assert "No tenés permiso" in response.content.decode()
    assert SecurityEvent.objects.filter(action="permission.denied").exists()


@override_settings(ROOT_URLCONF=__name__)
def test_missing_context_returns_access_denied_page(client: object) -> None:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password="Clave-Segura-2026",
    )
    client.force_login(user)
    response = client.get("/guarded/")
    assert response.status_code == 403
    assert "Cerrar sesión" in response.content.decode()
    assert client.session.get("_auth_user_id") == str(user.pk)


@override_settings(ROOT_URLCONF=__name__)
def test_foreign_and_missing_resources_share_the_same_404(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    foreign_company = Company.objects.create(name="Otra empresa")
    foreign_membership = _create_membership(
        foreign_company,
        "ajena@example.com",
        Role.OPERADOR,
    )
    client.force_login(owner_account.user)
    foreign_response = client.get(f"/resource/{foreign_membership.pk}/")
    missing_response = client.get("/resource/999999/")
    assert foreign_response.status_code == 404
    assert missing_response.status_code == 404
    assert foreign_response.content == missing_response.content


@override_settings(ROOT_URLCONF=__name__)
def test_isolation_is_checked_before_capability(
    client: object,
    company: Company,
    owner_membership: Membership,
) -> None:
    consulta = _create_membership(company, "consulta@example.com", Role.CONSULTA)
    foreign_company = Company.objects.create(name="Otra empresa")
    foreign_membership = _create_membership(
        foreign_company,
        "ajena@example.com",
        Role.OPERADOR,
    )
    client.force_login(consulta.account.user)
    foreign_response = client.get(f"/resource/{foreign_membership.pk}/")
    own_response = client.get(f"/resource/{consulta.pk}/")
    assert foreign_response.status_code == 404
    assert own_response.status_code == 403


@override_settings(ROOT_URLCONF=__name__)
def test_injected_company_uses_the_uniform_404(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/guarded/?company=999")
    assert response.status_code == 404
    assert "Recurso no encontrado" in response.content.decode()
    missing_response = client.get("/resource/999999/")
    assert response.content == missing_response.content
    assert SecurityEvent.objects.filter(
        action="company.scope.injected",
    ).exists()
