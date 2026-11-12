"""Pruebas de integración de extremo a extremo de la Etapa 003 (T-22).

Cubren los flujos completos de inicialización, acceso, alta, primer acceso,
cambio de rol, desactivación, reactivación y recuperación, junto con la
auditoría de cada uno y los errores uniformes con ``DEBUG=False``.
"""

from __future__ import annotations

import re
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.http import HttpResponse
from django.test import Client, override_settings

from apps.accounts.capabilities import Role
from apps.accounts.models import Account, Company, Membership, generate_username
from apps.audit.models import AuditEvent, SecurityEvent

TEST_PASSWORD = "Clave-Segura-2026"
INITIAL_PASSWORD = "Clave-Inicial-2026!"
NEW_PASSWORD = "Clave-Nueva-2026!"
EMPLOYEE_PASSWORD = "Clave-Empleado-2026!"
RECOVERED_PASSWORD = "Clave-Recuperada-2026!"
OWNER_EMAIL = "dueno@example.com"
EMPLOYEE_EMAIL = "empleado@example.com"
COMPANY_NAME = "Almacén Central"


def _initialize_company(
    monkeypatch: pytest.MonkeyPatch,
    capture: object,
    *,
    email: str = OWNER_EMAIL,
    password: str = INITIAL_PASSWORD,
) -> Membership:
    """Ejecuta ``init_company`` con la contraseña simulada por ``getpass``."""

    answers = iter([password, password])
    monkeypatch.setattr(
        "apps.accounts.management.commands.init_company.getpass.getpass",
        lambda prompt="": next(answers),
    )
    with capture(execute=True):
        call_command(
            "init_company",
            "--name",
            COMPANY_NAME,
            "--email",
            email,
            "--display-name",
            "Dueña",
            stdout=StringIO(),
        )
    return Membership.objects.select_related("account__user", "company").get()


def _login(client: Client, email: str, password: str) -> HttpResponse:
    return client.post(
        "/login/",
        {"username": email, "password": password},
    )


def _change_password(client: Client, old: str, new: str) -> HttpResponse:
    return client.post(
        "/password/",
        {
            "old_password": old,
            "new_password1": new,
            "new_password2": new,
        },
    )


def _temporary_password(response: HttpResponse) -> str:
    """Extrae la contraseña temporal mostrada una sola vez en el HTML."""

    match = re.search(r"<code>([^<]+)</code>", response.content.decode())
    assert match is not None
    return match.group(1).strip()


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


@pytest.mark.django_db
def test_initialization_and_first_access_flow(
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    django_capture_on_commit_callbacks: object,
) -> None:
    owner = _initialize_company(monkeypatch, django_capture_on_commit_callbacks)
    company = owner.company

    assert company.is_active is True
    assert owner.role == Role.DUENO.value
    assert owner.is_active is True
    assert owner.must_change_password is True
    assert owner.account.user.check_password(INITIAL_PASSWORD)

    login = _login(client, OWNER_EMAIL, INITIAL_PASSWORD)
    assert login.status_code == 302
    assert login.url == "/profile/"

    forced = client.get("/panel/")
    assert forced.status_code == 302
    assert forced.url == "/password/"
    assert client.get("/password/").status_code == 200

    with django_capture_on_commit_callbacks(execute=True):
        changed = _change_password(client, INITIAL_PASSWORD, NEW_PASSWORD)
    assert changed.status_code == 302
    assert changed.url == "/profile/"

    assert client.get("/panel/").status_code == 200
    owner.refresh_from_db()
    owner.account.user.refresh_from_db()
    assert owner.must_change_password is False
    assert owner.account.user.check_password(NEW_PASSWORD)

    initialized = AuditEvent.objects.get(action="company.initialized")
    assert initialized.company == company
    assert initialized.actor == owner.account.user
    assert INITIAL_PASSWORD not in str(initialized.after)

    password_event = AuditEvent.objects.get(action="password.changed")
    assert password_event.company == company
    assert password_event.actor == owner.account.user
    assert password_event.entity_id == str(owner.account.pk)
    assert INITIAL_PASSWORD not in str(password_event.before)
    assert NEW_PASSWORD not in str(password_event.after)

    assert _login(Client(), OWNER_EMAIL, INITIAL_PASSWORD).status_code == 200
    assert _login(Client(), OWNER_EMAIL, NEW_PASSWORD).status_code == 302


@pytest.mark.django_db
def test_employee_creation_and_first_access_flow(
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    django_capture_on_commit_callbacks: object,
) -> None:
    owner = _initialize_company(monkeypatch, django_capture_on_commit_callbacks)
    _login(client, OWNER_EMAIL, INITIAL_PASSWORD)
    with django_capture_on_commit_callbacks(execute=True):
        _change_password(client, INITIAL_PASSWORD, NEW_PASSWORD)

    with django_capture_on_commit_callbacks(execute=True):
        created = client.post(
            "/users/new/",
            {
                "email": EMPLOYEE_EMAIL,
                "display_name": "Empleado",
                "role": Role.OPERADOR.value,
            },
        )

    assert created.status_code == 200
    temporary = _temporary_password(created)
    employee = Membership.objects.select_related("account__user").get(
        account__email=EMPLOYEE_EMAIL
    )
    assert employee.company == owner.company
    assert employee.role == Role.OPERADOR.value
    assert employee.is_active is True
    assert employee.must_change_password is True
    assert employee.account.user.check_password(temporary)

    employee_client = Client()
    login = _login(employee_client, EMPLOYEE_EMAIL, temporary)
    assert login.status_code == 302
    forced = employee_client.get("/panel/")
    assert forced.status_code == 302
    assert forced.url == "/password/"

    with django_capture_on_commit_callbacks(execute=True):
        changed = _change_password(employee_client, temporary, EMPLOYEE_PASSWORD)
    assert changed.status_code == 302

    assert employee_client.get("/panel/").status_code == 200
    assert employee_client.get("/users/").status_code == 403
    employee.refresh_from_db()
    assert employee.must_change_password is False

    created_event = AuditEvent.objects.get(action="membership.created")
    assert created_event.company == owner.company
    assert created_event.actor == owner.account.user
    assert created_event.entity_id == str(employee.pk)
    assert temporary not in str(created_event.after)


@pytest.mark.django_db
def test_role_change_deactivation_and_reactivation_flow(
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    django_capture_on_commit_callbacks: object,
) -> None:
    _initialize_company(monkeypatch, django_capture_on_commit_callbacks)
    _login(client, OWNER_EMAIL, INITIAL_PASSWORD)
    with django_capture_on_commit_callbacks(execute=True):
        _change_password(client, INITIAL_PASSWORD, NEW_PASSWORD)

    with django_capture_on_commit_callbacks(execute=True):
        created = client.post(
            "/users/new/",
            {
                "email": EMPLOYEE_EMAIL,
                "display_name": "Empleado",
                "role": Role.OPERADOR.value,
            },
        )
    temporary = _temporary_password(created)
    employee = Membership.objects.select_related("account__user").get(
        account__email=EMPLOYEE_EMAIL
    )

    employee_client = Client()
    _login(employee_client, EMPLOYEE_EMAIL, temporary)
    with django_capture_on_commit_callbacks(execute=True):
        _change_password(employee_client, temporary, EMPLOYEE_PASSWORD)
    assert employee_client.get("/panel/").status_code == 200

    with django_capture_on_commit_callbacks(execute=True):
        role_response = client.post(
            f"/users/{employee.pk}/role/",
            {"role": Role.CONSULTA.value},
        )
    assert role_response.status_code == 200
    employee.refresh_from_db()
    assert employee.role == Role.CONSULTA.value
    assert employee_client.get("/panel/").status_code == 200
    assert employee_client.get("/users/").status_code == 403

    with django_capture_on_commit_callbacks(execute=True):
        deactivated = client.post(f"/users/{employee.pk}/deactivate/")
    assert deactivated.status_code == 200
    employee.refresh_from_db()
    assert employee.is_active is False
    assert employee_client.get("/panel/").status_code == 403
    assert _login(Client(), EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD).status_code == 200

    with django_capture_on_commit_callbacks(execute=True):
        reactivated = client.post(f"/users/{employee.pk}/reactivate/")
    assert reactivated.status_code == 200
    new_temporary = _temporary_password(reactivated)
    employee.refresh_from_db()
    employee.account.user.refresh_from_db()
    assert employee.is_active is True
    assert employee.must_change_password is True
    assert employee.account.user.check_password(new_temporary)
    assert not employee.account.user.check_password(EMPLOYEE_PASSWORD)

    restored = Client()
    assert _login(restored, EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD).status_code == 200
    assert _login(restored, EMPLOYEE_EMAIL, new_temporary).status_code == 302
    assert restored.get("/panel/").url == "/password/"
    with django_capture_on_commit_callbacks(execute=True):
        assert _change_password(
            restored,
            new_temporary,
            EMPLOYEE_PASSWORD,
        ).status_code == 302
    assert restored.get("/panel/").status_code == 200

    audit = client.get("/audit/").content.decode()
    assert "membership.created" in audit
    assert "membership.role_changed" in audit
    assert "membership.deactivated" in audit
    assert "membership.reactivated" in audit
    assert temporary not in audit
    assert new_temporary not in audit
    assert "Dueña" in audit

    role_event = AuditEvent.objects.get(action="membership.role_changed")
    assert role_event.before == {"role": Role.OPERADOR.value}
    assert role_event.after == {"role": Role.CONSULTA.value}
    deactivated_event = AuditEvent.objects.get(action="membership.deactivated")
    assert deactivated_event.after == {"is_active": False}
    reactivated_event = AuditEvent.objects.get(action="membership.reactivated")
    assert reactivated_event.after == {"is_active": True}


@pytest.mark.django_db
def test_owner_recovery_flow(
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    django_capture_on_commit_callbacks: object,
) -> None:
    owner = _initialize_company(monkeypatch, django_capture_on_commit_callbacks)
    _login(client, OWNER_EMAIL, INITIAL_PASSWORD)
    with django_capture_on_commit_callbacks(execute=True):
        _change_password(client, INITIAL_PASSWORD, NEW_PASSWORD)
    client.post("/logout/")

    out = StringIO()
    with django_capture_on_commit_callbacks(execute=True):
        call_command(
            "reset_owner_password",
            "--email",
            "Dueno@Example.com",
            stdout=out,
        )
    temporary = out.getvalue().strip().splitlines()[-1]

    owner.refresh_from_db()
    owner.account.user.refresh_from_db()
    assert owner.must_change_password is True
    assert owner.account.user.check_password(temporary)
    assert not owner.account.user.check_password(NEW_PASSWORD)

    fresh = Client()
    assert _login(fresh, OWNER_EMAIL, NEW_PASSWORD).status_code == 200
    assert _login(fresh, OWNER_EMAIL, temporary).status_code == 302
    assert fresh.get("/panel/").url == "/password/"
    with django_capture_on_commit_callbacks(execute=True):
        assert _change_password(
            fresh,
            temporary,
            RECOVERED_PASSWORD,
        ).status_code == 302
    assert fresh.get("/panel/").status_code == 200

    owner.refresh_from_db()
    owner.account.user.refresh_from_db()
    assert owner.must_change_password is False
    assert owner.account.user.check_password(RECOVERED_PASSWORD)

    event = AuditEvent.objects.get(action="membership.owner_password_reset")
    assert event.actor is None
    assert event.company == owner.company
    assert event.entity_id == str(owner.pk)
    assert temporary not in str(event.before)
    assert temporary not in str(event.after)


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_uniform_errors_with_debug_disabled(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    foreign = client.get(f"/profile/{foreign_account.pk}/")
    missing = client.get("/profile/999999/")
    assert foreign.status_code == 404
    assert missing.status_code == 404
    assert foreign.content == missing.content
    assert foreign["Cache-Control"] == "no-store"
    assert foreign_account.email not in foreign.content.decode()
    assert foreign_account.display_name not in foreign.content.decode()
    assert SecurityEvent.objects.filter(action="company.scope.foreign").exists()

    consulta = _create_membership(company, "consulta@example.com")
    capability_client = Client()
    capability_client.force_login(consulta.account.user)
    capability = capability_client.get("/users/")
    assert capability.status_code == 403
    assert "No tenés permiso" in capability.content.decode()
    assert capability["Cache-Control"] == "no-store"

    outsider_user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    outsider = Client()
    outsider.force_login(outsider_user)
    context_denied = outsider.get("/panel/")
    assert context_denied.status_code == 403
    assert "Tu cuenta no tiene acceso al panel" in context_denied.content.decode()
    assert context_denied["Cache-Control"] == "no-store"
    assert capability.content != context_denied.content
    assert owner_account.email not in context_denied.content.decode()
