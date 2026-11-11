"""Pruebas de la separación entre Django Admin y el panel comercial (T-19)."""

from __future__ import annotations

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.test import RequestFactory
from django.urls import reverse

from apps.accounts.models import Account, Company, Membership
from apps.audit.models import AuditEvent, SecurityEvent

TECHNICAL_PASSWORD = "Clave-Tecnica-2026!"


def _create_superuser():
    return get_user_model().objects.create_superuser(
        username="tecnico",
        email="tecnico@example.com",
        password=TECHNICAL_PASSWORD,
    )


def test_user_admin_is_read_only() -> None:
    request = RequestFactory().get("/admin/auth/user/")
    user_admin = admin.site._registry[User]

    assert user_admin.has_add_permission(request) is False
    assert user_admin.has_change_permission(request) is False
    assert user_admin.has_delete_permission(request) is False
    assert "password" not in user_admin.readonly_fields
    assert "username" in user_admin.readonly_fields


def test_group_admin_is_read_only() -> None:
    request = RequestFactory().get("/admin/auth/group/")
    group_admin = admin.site._registry[Group]

    assert group_admin.has_add_permission(request) is False
    assert group_admin.has_change_permission(request) is False
    assert group_admin.has_delete_permission(request) is False
    assert "name" in group_admin.readonly_fields


def test_business_and_audit_models_are_not_registered() -> None:
    registered = set(admin.site._registry)

    for model in (Account, Company, Membership, AuditEvent, SecurityEvent):
        assert model not in registered, f"{model.__name__} está registrado en Admin"


@pytest.mark.django_db
def test_commercial_account_is_redirected_from_admin(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/admin/")

    assert response.status_code == 302
    assert response.url == "/admin/login/?next=/admin/"
    assert "accounts/panel" not in response.url


@pytest.mark.django_db
def test_commercial_account_cannot_open_admin_models(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    assert owner_account.user.is_staff is False
    assert owner_account.user.is_superuser is False
    client.force_login(owner_account.user)
    response = client.get(reverse("admin:auth_user_changelist"))

    assert response.status_code == 302
    assert response.url.startswith("/admin/login/")


@pytest.mark.django_db
def test_technical_superuser_without_membership_can_open_admin(
    client: object,
) -> None:
    _create_superuser()
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)
    superuser = get_user_model().objects.get(username="tecnico")

    assert not Membership.objects.filter(account__user=superuser).exists()
    response = client.get("/admin/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "NexoPyme AI" in content
    assert "Cuentas" not in content


@pytest.mark.django_db
def test_superuser_cannot_add_users(client: object) -> None:
    _create_superuser()
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)

    response = client.get(reverse("admin:auth_user_add"))

    assert response.status_code == 403
    count = get_user_model().objects.count()
    client.post(
        reverse("admin:auth_user_add"),
        {
            "username": "intruso",
            "password1": TECHNICAL_PASSWORD,
            "password2": TECHNICAL_PASSWORD,
        },
    )
    assert get_user_model().objects.count() == count


@pytest.mark.django_db
def test_superuser_cannot_change_users(client: object) -> None:
    _create_superuser()
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)
    superuser = get_user_model().objects.get(username="tecnico")
    url = reverse("admin:auth_user_change", args=[superuser.pk])

    response = client.post(
        url,
        {
            "username": "renombrado",
            "email": superuser.email,
            "is_active": "on",
            "is_staff": "on",
        },
    )

    assert response.status_code == 403
    superuser.refresh_from_db()
    assert superuser.username == "tecnico"
    assert superuser.is_staff is True


@pytest.mark.django_db
def test_superuser_can_view_users_in_read_only_mode(client: object) -> None:
    _create_superuser()
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)
    superuser = get_user_model().objects.get(username="tecnico")

    response = client.get(reverse("admin:auth_user_change", args=[superuser.pk]))

    assert response.status_code == 200
    content = response.content.decode()
    assert 'name="_save"' not in content
    assert superuser.password not in content
    assert "pbkdf2" not in content


@pytest.mark.django_db
def test_superuser_cannot_change_groups(client: object) -> None:
    _create_superuser()
    group = Group.objects.create(name="Operadores")
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)
    url = reverse("admin:auth_group_change", args=[group.pk])

    response = client.post(url, {"name": "Renombrado", "permissions": []})

    assert response.status_code == 403
    group.refresh_from_db()
    assert group.name == "Operadores"


@pytest.mark.django_db
def test_superuser_cannot_add_or_delete_groups(client: object) -> None:
    _create_superuser()
    group = Group.objects.create(name="Operadores")
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)

    assert client.get(reverse("admin:auth_group_add")).status_code == 403
    assert (
        client.get(reverse("admin:auth_group_delete", args=[group.pk])).status_code
        == 403
    )
    assert Group.objects.filter(pk=group.pk).exists()


@pytest.mark.django_db
def test_superuser_cannot_delete_users(client: object) -> None:
    _create_superuser()
    target = get_user_model().objects.create_user(
        username="eliminable",
        password=None,
    )
    assert client.login(username="tecnico", password=TECHNICAL_PASSWORD)
    url = reverse("admin:auth_user_delete", args=[target.pk])

    response = client.get(url)

    assert response.status_code == 403
    assert get_user_model().objects.filter(pk=target.pk).exists()
