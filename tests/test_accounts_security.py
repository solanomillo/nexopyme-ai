"""Pruebas de seguridad de sesión, CSRF, cookies y logging técnico (T-20)."""

from __future__ import annotations

import logging

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import Client, override_settings

from apps.accounts.capabilities import Role
from apps.accounts.models import (
    Account,
    Company,
    Membership,
    generate_username,
)
from apps.audit.models import AuditEvent
from config.settings import _get_int_env, _get_log_level, _get_positive_int_env

TEST_PASSWORD = "Clave-Segura-2026"
SECRET_PASSWORD = "No-Debe-Aparecer-2026"


def _create_membership(
    company: Company,
    email: str,
    role: str = Role.CONSULTA.value,
) -> Membership:
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


def test_session_cookie_is_hardened() -> None:
    assert settings.SESSION_COOKIE_HTTPONLY is True
    assert settings.SESSION_COOKIE_SAMESITE == "Lax"
    assert settings.SESSION_COOKIE_SECURE is settings.CSRF_COOKIE_SECURE
    assert isinstance(settings.SESSION_COOKIE_AGE, int)
    assert settings.SESSION_COOKIE_AGE > 0


def test_csrf_cookie_is_hardened() -> None:
    assert settings.CSRF_COOKIE_HTTPONLY is True
    assert settings.CSRF_COOKIE_SAMESITE == "Lax"


def test_logging_uses_console_without_files() -> None:
    handlers = settings.LOGGING["handlers"]
    assert handlers["console"]["class"] == "logging.StreamHandler"
    assert all("filename" not in handler for handler in handlers.values())
    assert settings.LOGGING["root"]["level"] in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }
    assert settings.LOGGING["loggers"]["django"]["handlers"] == ["console"]
    assert settings.LOGGING["loggers"]["django"]["propagate"] is False


def test_log_format_does_not_include_request_data() -> None:
    fmt = settings.LOGGING["formatters"]["console"]["format"].lower()
    for token in ("request", "body", "password", "email", "token", "cookie"):
        assert token not in fmt


def test_get_int_env_reads_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXOPYME_TEST_INT", "900")
    assert _get_int_env("NEXOPYME_TEST_INT", 60) == 900


def test_get_int_env_uses_the_default_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("NEXOPYME_TEST_INT", raising=False)
    assert _get_int_env("NEXOPYME_TEST_INT", 60) == 60


def test_get_int_env_rejects_a_non_numeric_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEXOPYME_TEST_INT", "mucho")
    with pytest.raises(ImproperlyConfigured):
        _get_int_env("NEXOPYME_TEST_INT", 60)


def test_get_positive_int_env_rejects_zero_and_negatives(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NEXOPYME_TEST_INT", "0")
    with pytest.raises(ImproperlyConfigured):
        _get_positive_int_env("NEXOPYME_TEST_INT", 60)
    monkeypatch.setenv("NEXOPYME_TEST_INT", "-5")
    with pytest.raises(ImproperlyConfigured):
        _get_positive_int_env("NEXOPYME_TEST_INT", 60)


def test_get_log_level_normalizes_an_invalid_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DJANGO_LOG_LEVEL", "verbose")
    assert _get_log_level() == "INFO"
    monkeypatch.setenv("DJANGO_LOG_LEVEL", "warning")
    assert _get_log_level() == "WARNING"


@override_settings(SESSION_COOKIE_SECURE=False, CSRF_COOKIE_SECURE=False)
def test_login_page_sets_a_hardened_csrf_cookie(client: Client) -> None:
    response = client.get("/login/")

    assert response.status_code == 200
    cookie = response.cookies["csrftoken"]
    assert cookie["httponly"] is True
    assert cookie["samesite"] == "Lax"
    assert not cookie["secure"]


@pytest.mark.django_db
def test_post_without_csrf_token_is_rejected() -> None:
    client = Client(enforce_csrf_checks=True)
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": SECRET_PASSWORD},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_post_with_csrf_token_is_accepted(
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client = Client(enforce_csrf_checks=True)
    page = client.get("/login/")
    token = page.cookies["csrftoken"].value

    response = client.post(
        "/login/",
        {
            "username": "dueno@example.com",
            "password": TEST_PASSWORD,
            "csrfmiddlewaretoken": token,
        },
    )

    assert response.status_code == 302
    assert response.url == "/profile/"


@pytest.mark.django_db
@override_settings(SESSION_COOKIE_SECURE=False, CSRF_COOKIE_SECURE=False)
def test_login_sets_a_hardened_session_cookie(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": TEST_PASSWORD},
    )

    assert response.status_code == 302
    cookie = response.cookies["sessionid"]
    assert cookie["httponly"] is True
    assert cookie["samesite"] == "Lax"
    assert not cookie["secure"]


@pytest.mark.django_db
@override_settings(SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True)
def test_secure_flag_follows_the_environment(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    response = client.post(
        "/login/",
        {"username": "dueno@example.com", "password": TEST_PASSWORD},
    )

    assert response.status_code == 302
    assert response.cookies["sessionid"]["secure"] is True


@pytest.mark.django_db
def test_failed_login_does_not_log_credentials(
    client: Client,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.DEBUG):
        response = client.post(
            "/login/",
            {"username": "dueno@example.com", "password": SECRET_PASSWORD},
        )

    assert response.status_code == 200
    assert SECRET_PASSWORD not in caplog.text
    assert "dueno@example.com" not in caplog.text


@pytest.mark.django_db
def test_audit_is_separate_from_technical_logs(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    caplog: pytest.LogCaptureFixture,
    django_capture_on_commit_callbacks: object,
) -> None:
    client.force_login(owner_account.user)
    with caplog.at_level(logging.DEBUG), django_capture_on_commit_callbacks(
        execute=True
    ):
        response = client.post("/company/", {"name": "Nombre Auditado"})

    assert response.status_code == 302
    assert AuditEvent.objects.filter(action="company.name_updated").exists()
    assert "Nombre Auditado" not in caplog.text
    assert "company.name_updated" not in caplog.text


@pytest.mark.django_db
def test_forbidden_response_is_not_cached(
    client: Client,
    company: Company,
    owner_membership: Membership,
) -> None:
    consulta = _create_membership(company, "consulta@example.com")
    client.force_login(consulta.account.user)

    response = client.get("/users/")

    assert response.status_code == 403
    assert response["Cache-Control"] == "no-store"


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_not_found_response_is_not_cached(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    response = client.get("/profile/999999/")

    assert response.status_code == 404
    assert response["Cache-Control"] == "no-store"
