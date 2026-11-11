"""Pruebas de autenticación y acceso al panel (T-10, T-11)."""

from __future__ import annotations

from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.test import override_settings
from django.urls import reverse

from apps.accounts.backends import (
    COMMERCIAL_LOGIN_FAILED,
    TECHNICAL_LOGIN_FAILED,
    EmailBackend,
    TechnicalAdminBackend,
)
from apps.accounts.models import Account, Company, Membership, generate_username
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


def test_panel_routes_are_registered() -> None:
    """Las rutas del panel se resuelven con el namespace accounts (DB-free)."""

    assert reverse("accounts:login") == "/login/"
    assert reverse("accounts:logout") == "/logout/"
    assert reverse("accounts:panel") == "/panel/"


def test_base_template_stays_free_of_panel_context() -> None:
    """base.html no incorpora contexto del panel (D-12, DB-free)."""

    content = (
        Path(settings.BASE_DIR) / "templates" / "base.html"
    ).read_text(encoding="utf-8")
    for token in ("request.user", "request.company", "request.membership"):
        assert token not in content


def test_login_template_implements_error_and_loading_states() -> None:
    """El acceso declara estados de error y carga (DB-free)."""

    content = (
        Path(settings.BASE_DIR) / "templates" / "accounts" / "login.html"
    ).read_text(encoding="utf-8")
    assert 'role="alert"' in content
    assert "aria-busy" in content


def test_panel_template_extends_independent_base_panel() -> None:
    """base_panel.html es independiente y panel.html lo extiende (DB-free)."""

    templates = Path(settings.BASE_DIR) / "templates"
    base_panel = (templates / "base_panel.html").read_text(encoding="utf-8")
    panel = (templates / "accounts" / "panel.html").read_text(encoding="utf-8")
    assert '{% extends "base.html" %}' not in base_panel
    assert '{% extends "base_panel.html" %}' in panel


@pytest.mark.django_db
def test_anonymous_panel_access_redirects_to_login(client: object) -> None:
    response = client.get("/panel/")
    assert response.status_code == 302
    assert response.url == "/login/?next=/panel/"


@pytest.mark.django_db
def test_login_page_renders_email_and_password_form(client: object) -> None:
    response = client.get("/login/")
    assert response.status_code == 200
    assert "accounts/login.html" in [template.name for template in response.templates]
    content = response.content.decode()
    assert 'type="email"' in content
    assert 'name="username"' in content
    assert 'name="password"' in content
    assert "csrfmiddlewaretoken" in content
    assert content.count("<h1") == 1


@pytest.mark.django_db
def test_field_errors_are_associated_with_the_control(client: object) -> None:
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": ""},
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert 'aria-invalid="true"' in content
    assert 'aria-describedby="id_password-errors"' in content


@pytest.mark.django_db
def test_username_errors_are_associated_with_the_control(client: object) -> None:
    response = client.post(
        "/login/",
        {"username": "no-es-correo", "password": "x"},
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert 'aria-invalid="true"' in content
    assert 'aria-describedby="id_username-errors"' in content


@pytest.mark.django_db
def test_login_with_valid_credentials_redirects_to_panel(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    response = client.post(
        "/login/",
        {
            "username": "dueno@example.com",
            "password": TEST_PASSWORD,
            "next": "/panel/",
        },
    )
    assert response.status_code == 302
    assert response.url == "/panel/"
    assert client.session["_auth_user_id"] == str(owner_account.user.pk)


@pytest.mark.django_db
def test_login_with_invalid_password_shows_generic_error(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": "incorrecta"},
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Correo o contraseña incorrectos." in content
    assert "incorrecta" not in content
    assert SecurityEvent.objects.filter(action=COMMERCIAL_LOGIN_FAILED).exists()


@pytest.mark.django_db
def test_unknown_email_and_wrong_password_share_the_same_message(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    known = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": "incorrecta"},
    )
    unknown = client.post(
        "/login/",
        {"username": "nadie@example.com", "password": "incorrecta"},
    )
    message = "Correo o contraseña incorrectos."
    assert known.status_code == unknown.status_code == 200
    assert message in known.content.decode()
    assert message in unknown.content.decode()


@pytest.mark.django_db
def test_inactive_account_gets_the_generic_login_message(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    get_user_model().objects.filter(pk=owner_account.user.pk).update(is_active=False)
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    assert "Correo o contraseña incorrectos." in response.content.decode()


@pytest.mark.django_db
def test_inactive_membership_gets_the_generic_login_message(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    Membership.objects.filter(pk=owner_membership.pk).update(is_active=False)
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    assert "Correo o contraseña incorrectos." in response.content.decode()


@pytest.mark.django_db
def test_inactive_company_gets_the_generic_login_message(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    company: Company,
) -> None:
    Company.objects.filter(pk=company.pk).update(is_active=False)
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    assert "Correo o contraseña incorrectos." in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "unsafe_next",
    ["https://evil.example/", "//evil.example/", "/\\evil.example/"],
)
def test_login_discards_unsafe_next(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    unsafe_next: str,
) -> None:
    response = client.post(
        "/login/",
        {
            "username": "dueno@example.com",
            "password": TEST_PASSWORD,
            "next": unsafe_next,
        },
    )
    assert response.status_code == 302
    assert response.url == settings.LOGIN_REDIRECT_URL


@pytest.mark.django_db
def test_authenticated_user_is_redirected_from_login(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/login/")
    assert response.status_code == 302
    assert response.url == settings.LOGIN_REDIRECT_URL


@pytest.mark.django_db
def test_panel_renders_company_context_without_caching(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    company: Company,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/panel/")
    assert response.status_code == 200
    template_names = [template.name for template in response.templates]
    assert "accounts/panel.html" in template_names
    assert "base_panel.html" in template_names
    content = response.content.decode()
    assert company.name in content
    assert owner_account.display_name in content
    assert "Dueño" in content
    assert content.count("<h1") == 1
    assert response["Cache-Control"] == "no-store"


@pytest.mark.django_db
def test_panel_denies_user_without_membership(client: object) -> None:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    client.force_login(user)
    response = client.get("/panel/")
    assert response.status_code == 403
    assert "Cerrar sesión" in response.content.decode()


@pytest.mark.django_db
def test_panel_denies_inactive_membership(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    Membership.objects.filter(pk=owner_membership.pk).update(is_active=False)
    client.force_login(owner_account.user)
    assert client.get("/panel/").status_code == 403


@pytest.mark.django_db
def test_panel_denies_inactive_company(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    company: Company,
) -> None:
    Company.objects.filter(pk=company.pk).update(is_active=False)
    client.force_login(owner_account.user)
    assert client.get("/panel/").status_code == 403


@pytest.mark.django_db
def test_home_does_not_expose_panel_context(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    company: Company,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/")
    assert response.status_code == 200
    assert company.name not in response.content.decode()


@pytest.mark.django_db
def test_logout_requires_post(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/logout/")
    assert response.status_code == 405
    assert client.session.get("_auth_user_id") == str(owner_account.user.pk)


@pytest.mark.django_db
def test_logout_clears_the_session(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.post("/logout/")
    assert response.status_code == 302
    assert response.url == settings.LOGOUT_REDIRECT_URL
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
@override_settings(LOGOUT_REDIRECT_URL="/salir/")
def test_logout_reads_the_redirect_at_request_time(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.post("/logout/")
    assert response.status_code == 302
    assert response.url == "/salir/"
