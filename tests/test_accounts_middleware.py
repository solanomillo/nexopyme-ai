"""Pruebas del middleware de contexto de empresa (T-08)."""

from __future__ import annotations

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import override_settings
from django.urls import path

from apps.accounts.models import Company, Membership
from apps.audit.models import SecurityEvent


def panel_view(request: HttpRequest) -> HttpResponse:
    """Vista mínima que expone el contexto resuelto por el middleware."""

    company = getattr(request, "company", None)
    membership = getattr(request, "membership", None)
    company_id = company.pk if company else "none"
    membership_id = membership.pk if membership else "none"
    return HttpResponse(f"{company_id}:{membership_id}")


urlpatterns = [path("panel/", panel_view)]

pytestmark = pytest.mark.django_db


@override_settings(ROOT_URLCONF=__name__)
def test_authenticated_user_receives_company_context(
    client: object,
    owner_account: object,
    owner_membership: Membership,
    django_assert_max_num_queries: object,
) -> None:
    client.force_login(owner_account.user)
    with django_assert_max_num_queries(3):
        response = client.get("/panel/")
    assert response.status_code == 200
    assert response.content.decode() == (
        f"{owner_membership.company_id}:{owner_membership.pk}"
    )
    assert response.wsgi_request.must_change_password is False


@override_settings(ROOT_URLCONF=__name__)
def test_anonymous_user_has_no_context(client: object) -> None:
    response = client.get("/panel/")
    assert response.status_code == 200
    assert response.content.decode() == "none:none"


@override_settings(ROOT_URLCONF=__name__)
def test_inactive_membership_is_denied(
    client: object,
    owner_account: object,
    owner_membership: Membership,
) -> None:
    Membership.objects.filter(pk=owner_membership.pk).update(is_active=False)
    client.force_login(owner_account.user)
    response = client.get("/panel/")
    assert response.status_code == 403


@override_settings(ROOT_URLCONF=__name__)
def test_inactive_company_is_denied(
    client: object,
    owner_account: object,
    owner_membership: Membership,
    company: Company,
) -> None:
    Company.objects.filter(pk=company.pk).update(is_active=False)
    client.force_login(owner_account.user)
    response = client.get("/panel/")
    assert response.status_code == 403


def test_excluded_paths_are_not_affected(
    client: object,
    owner_account: object,
) -> None:
    client.force_login(owner_account.user)
    assert client.get("/health/").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/admin/login/").status_code == 200


def test_excluded_paths_helper_covers_every_declared_route() -> None:
    from apps.accounts.middleware import _is_excluded

    excluded = (
        "/",
        "/health/",
        "/favicon.ico",
        "/login/",
        "/logout/",
        "/password/",
        "/static/css/main.css",
        "/admin/",
    )
    for route in excluded:
        assert _is_excluded(route), route
    assert not _is_excluded("/panel/")


@override_settings(ROOT_URLCONF=__name__)
def test_injected_company_identifier_is_rejected(
    client: object,
    owner_account: object,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/panel/?company=999")
    assert response.status_code == 404
    assert SecurityEvent.objects.filter(
        action="company.scope.injected",
        attempted_company_id=999,
    ).exists()


@override_settings(ROOT_URLCONF=__name__)
def test_injected_company_identifier_in_post_is_rejected(
    client: object,
    owner_account: object,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.post("/panel/", {"company": "999"})
    assert response.status_code == 404
    assert SecurityEvent.objects.filter(
        action="company.scope.injected",
        attempted_company_id=999,
    ).exists()


@override_settings(ROOT_URLCONF=__name__)
def test_matching_company_identifier_is_ignored(
    client: object,
    owner_account: object,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get(f"/panel/?company={owner_membership.company_id}")
    assert response.status_code == 200
    assert response.content.decode() == (
        f"{owner_membership.company_id}:{owner_membership.pk}"
    )
    assert not SecurityEvent.objects.filter(
        action="company.scope.injected",
    ).exists()
