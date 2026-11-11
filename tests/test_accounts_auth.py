"""Pruebas de autenticación comercial y técnica (T-10)."""

from __future__ import annotations

import pytest
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from apps.accounts.backends import (
    COMMERCIAL_LOGIN_FAILED,
    TECHNICAL_LOGIN_FAILED,
    EmailBackend,
    TechnicalAdminBackend,
)
from apps.accounts.models import Account, Company, Membership
from apps.audit.models import SecurityEvent

TEST_PASSWORD = "Clave-Segura-2026"


def _create_staff(username: str = "tecnico") -> object:
    return get_user_model().objects.create_user(
        username=username,
        password=TEST_PASSWORD,
        is_staff=True,
    )


def test_authentication_settings_are_configured() -> None:
    """Los backends y los destinos de acceso quedan configurados (DB-free)."""

    assert settings.AUTHENTICATION_BACKENDS == [
        "apps.accounts.backends.EmailBackend",
        "apps.accounts.backends.TechnicalAdminBackend",
    ]
    assert settings.LOGIN_URL == "/login/"
    assert settings.LOGIN_REDIRECT_URL == "/profile/"
    assert settings.LOGOUT_REDIRECT_URL == "/login/"


@pytest.mark.django_db
def test_active_commercial_account_authenticates(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    user = authenticate(username="dueno@example.com", password=TEST_PASSWORD)
    assert user == owner_account.user
    assert user.backend == "apps.accounts.backends.EmailBackend"


@pytest.mark.django_db
def test_email_is_normalized_before_lookup(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    user = authenticate(
        username="  DUENO@Example.COM ",
        password=TEST_PASSWORD,
    )
    assert user == owner_account.user


@pytest.mark.django_db
def test_invalid_password_is_rejected_and_recorded(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    assert authenticate(username="dueno@example.com", password="incorrecta") is None
    event = SecurityEvent.objects.get(action=COMMERCIAL_LOGIN_FAILED)
    assert event.result == "denied"
    assert event.actor == owner_account.user
    assert event.company is None


@pytest.mark.django_db
def test_unknown_email_is_rejected_without_revealing_existence() -> None:
    assert authenticate(username="nadie@example.com", password="x") is None
    event = SecurityEvent.objects.get(action=COMMERCIAL_LOGIN_FAILED)
    assert event.actor is None
    assert event.result == "denied"


@pytest.mark.django_db
def test_inactive_account_is_rejected(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    get_user_model().objects.filter(pk=owner_account.user.pk).update(is_active=False)
    assert authenticate(username="dueno@example.com", password=TEST_PASSWORD) is None
    assert SecurityEvent.objects.filter(action=COMMERCIAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_inactive_membership_is_rejected(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    Membership.objects.filter(pk=owner_membership.pk).update(is_active=False)
    assert authenticate(username="dueno@example.com", password=TEST_PASSWORD) is None
    assert SecurityEvent.objects.filter(action=COMMERCIAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_inactive_company_is_rejected(
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    Company.objects.filter(pk=company.pk).update(is_active=False)
    assert authenticate(username="dueno@example.com", password=TEST_PASSWORD) is None
    assert SecurityEvent.objects.filter(action=COMMERCIAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_staff_without_membership_authenticates_in_admin() -> None:
    staff = _create_staff()
    user = authenticate(username="tecnico", password=TEST_PASSWORD)
    assert user == staff
    assert user.backend == "apps.accounts.backends.TechnicalAdminBackend"


@pytest.mark.django_db
def test_commercial_account_cannot_authenticate_in_admin(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    backend = TechnicalAdminBackend()
    user = backend.authenticate(
        None,
        username=owner_account.user.username,
        password=TEST_PASSWORD,
    )
    assert user is None


@pytest.mark.django_db
def test_staff_with_commercial_account_is_rejected_everywhere(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    get_user_model().objects.filter(pk=owner_account.user.pk).update(
        is_staff=True,
        is_superuser=True,
    )
    assert (
        EmailBackend().authenticate(
            None,
            username="dueno@example.com",
            password=TEST_PASSWORD,
        )
        is None
    )
    assert (
        TechnicalAdminBackend().authenticate(
            None,
            username=owner_account.user.username,
            password=TEST_PASSWORD,
        )
        is None
    )


@pytest.mark.django_db
def test_technical_wrong_password_is_recorded() -> None:
    _create_staff()
    assert authenticate(username="tecnico", password="incorrecta") is None
    event = SecurityEvent.objects.get(action=TECHNICAL_LOGIN_FAILED)
    assert event.result == "denied"


@pytest.mark.django_db
def test_email_backend_ignores_non_email_identifiers() -> None:
    backend = EmailBackend()
    assert backend.authenticate(None, username="tecnico", password="x") is None
    assert SecurityEvent.objects.count() == 0


@pytest.mark.django_db
def test_unknown_technical_username_is_recorded() -> None:
    assert authenticate(username="fantasma", password="x") is None
    assert SecurityEvent.objects.filter(action=TECHNICAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_inactive_staff_is_rejected() -> None:
    staff = _create_staff()
    get_user_model().objects.filter(pk=staff.pk).update(is_active=False)
    assert authenticate(username="tecnico", password=TEST_PASSWORD) is None
    assert SecurityEvent.objects.filter(action=TECHNICAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_superuser_without_staff_is_rejected() -> None:
    user = get_user_model().objects.create_user(
        username="superusuario",
        password=TEST_PASSWORD,
        is_superuser=True,
    )
    assert (
        TechnicalAdminBackend().authenticate(
            None,
            username=user.username,
            password=TEST_PASSWORD,
        )
        is None
    )


@pytest.mark.django_db
def test_backends_load_only_their_own_sessions(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    staff = _create_staff()
    assert EmailBackend().get_user(owner_account.user.pk) == owner_account.user
    assert EmailBackend().get_user(staff.pk) is None
    assert TechnicalAdminBackend().get_user(staff.pk) == staff
    assert TechnicalAdminBackend().get_user(owner_account.user.pk) is None


@pytest.mark.django_db
def test_inactive_user_session_is_rejected(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    get_user_model().objects.filter(pk=owner_account.user.pk).update(is_active=False)
    assert EmailBackend().get_user(owner_account.user.pk) is None
