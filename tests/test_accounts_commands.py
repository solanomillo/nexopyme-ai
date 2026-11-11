"""Pruebas de los comandos de inicialización y recuperación (T-13)."""

from __future__ import annotations

import logging
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.accounts.capabilities import Role
from apps.accounts.models import Account, Company, Membership, generate_username
from apps.audit.models import AuditEvent

INITIAL_PASSWORD = "Clave-Inicial-2026!"
OWNER_PASSWORD = "Clave-Segura-2026"


def _prompt_with(
    monkeypatch: pytest.MonkeyPatch,
    password: str,
    confirmation: str | None = None,
) -> None:
    answers = iter([password, password if confirmation is None else confirmation])
    monkeypatch.setattr(
        "apps.accounts.management.commands.init_company.getpass.getpass",
        lambda prompt="": next(answers),
    )


def _fail_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    def _prompt(prompt: str = "") -> str:
        raise AssertionError("No se debe solicitar la contraseña.")

    monkeypatch.setattr(
        "apps.accounts.management.commands.init_company.getpass.getpass",
        _prompt,
    )


def _create_employee(company: Company, email: str) -> Membership:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=OWNER_PASSWORD,
    )
    account = Account.objects.create(
        user=user,
        email=email,
        display_name="Empleado",
    )
    return Membership.objects.create(
        account=account,
        company=company,
        role=Role.OPERADOR,
    )


@pytest.mark.django_db
def test_init_company_creates_one_company_and_owner(
    monkeypatch: pytest.MonkeyPatch,
    django_capture_on_commit_callbacks: object,
) -> None:
    _prompt_with(monkeypatch, INITIAL_PASSWORD)
    out = StringIO()
    with django_capture_on_commit_callbacks(execute=True):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "Dueno@Example.com",
            stdout=out,
        )

    assert Company.objects.filter(is_active=True).count() == 1
    company = Company.objects.get()
    assert company.name == "Almacén Central"
    membership = Membership.objects.select_related("account__user").get()
    assert membership.role == Role.DUENO.value
    assert membership.is_active is True
    assert membership.must_change_password is True
    assert membership.account.email == "dueno@example.com"
    assert membership.account.display_name == "dueno"
    assert membership.account.user.check_password(INITIAL_PASSWORD)
    assert INITIAL_PASSWORD not in out.getvalue()

    event = AuditEvent.objects.get(action="company.initialized")
    assert event.company == company
    assert event.actor == membership.account.user
    assert INITIAL_PASSWORD not in str(event.before)
    assert INITIAL_PASSWORD not in str(event.after)


@pytest.mark.django_db
def test_init_company_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
    django_capture_on_commit_callbacks: object,
) -> None:
    _prompt_with(monkeypatch, INITIAL_PASSWORD)
    with django_capture_on_commit_callbacks(execute=True):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "dueno@example.com",
            stdout=StringIO(),
        )

    _fail_prompt(monkeypatch)
    out = StringIO()
    call_command(
        "init_company",
        "--name",
        "Otro nombre",
        "--email",
        "dueno@example.com",
        stdout=out,
    )

    assert Company.objects.count() == 1
    assert Membership.objects.count() == 1
    assert Company.objects.get().name == "Almacén Central"
    assert "no se modificó nada" in out.getvalue()
    assert AuditEvent.objects.filter(action="company.initialized").count() == 1


@pytest.mark.django_db
def test_init_company_rejects_company_without_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    Company.objects.create(name="Huérfana")
    _fail_prompt(monkeypatch)

    with pytest.raises(CommandError, match="único dueño"):
        call_command(
            "init_company",
            "--name",
            "Otra",
            "--email",
            "dueno@example.com",
            stdout=StringIO(),
        )

    assert Company.objects.count() == 1
    assert Membership.objects.count() == 0


@pytest.mark.django_db
def test_init_company_rejects_a_different_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _prompt_with(monkeypatch, INITIAL_PASSWORD)
    call_command(
        "init_company",
        "--name",
        "Almacén Central",
        "--email",
        "dueno@example.com",
        stdout=StringIO(),
    )

    _fail_prompt(monkeypatch)
    with pytest.raises(CommandError, match="otro dueño"):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "otro@example.com",
            stdout=StringIO(),
        )

    assert Company.objects.count() == 1
    assert Membership.objects.count() == 1


@pytest.mark.django_db
def test_init_company_rejects_more_than_one_active_company(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    Company.objects.create(name="Primera")
    Company.objects.create(name="Segunda")
    _fail_prompt(monkeypatch)

    with pytest.raises(CommandError, match="más de una empresa activa"):
        call_command(
            "init_company",
            "--name",
            "Tercera",
            "--email",
            "dueno@example.com",
            stdout=StringIO(),
        )


@pytest.mark.django_db
def test_init_company_does_not_accept_the_password_as_argument() -> None:
    with pytest.raises(CommandError):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "dueno@example.com",
            "--password",
            INITIAL_PASSWORD,
            stdout=StringIO(),
        )

    assert Company.objects.count() == 0


@pytest.mark.django_db
def test_init_company_rejects_a_weak_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _prompt_with(monkeypatch, "123")

    with pytest.raises(CommandError):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "dueno@example.com",
            stdout=StringIO(),
        )

    assert Company.objects.count() == 0


@pytest.mark.django_db
def test_init_company_requires_matching_passwords(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _prompt_with(monkeypatch, INITIAL_PASSWORD, "Otra-Clave-2026!")

    with pytest.raises(CommandError, match="no coinciden"):
        call_command(
            "init_company",
            "--name",
            "Almacén Central",
            "--email",
            "dueno@example.com",
            stdout=StringIO(),
        )

    assert Company.objects.count() == 0


@pytest.mark.django_db
def test_reset_owner_password_generates_a_temporary_password(
    owner_account: Account,
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    out = StringIO()
    with django_capture_on_commit_callbacks(execute=True):
        call_command(
            "reset_owner_password",
            "--email",
            "Dueno@Example.com",
            stdout=out,
        )

    output = out.getvalue()
    temporary_password = output.strip().splitlines()[-1]
    assert output.count(temporary_password) == 1

    owner_account.user.refresh_from_db()
    owner_membership.refresh_from_db()
    assert owner_account.user.check_password(temporary_password)
    assert not owner_account.user.check_password(OWNER_PASSWORD)
    assert owner_membership.must_change_password is True
    assert temporary_password not in output.splitlines()[0]

    event = AuditEvent.objects.get(action="membership.owner_password_reset")
    assert event.actor is None
    assert event.company == owner_membership.company
    assert event.entity_id == str(owner_membership.pk)
    assert temporary_password not in str(event.before)
    assert temporary_password not in str(event.after)


@pytest.mark.django_db
def test_reset_owner_password_rejects_unknown_email() -> None:
    with pytest.raises(CommandError, match="dueño activo"):
        call_command(
            "reset_owner_password",
            "--email",
            "nadie@example.com",
            stdout=StringIO(),
        )


@pytest.mark.django_db
def test_reset_owner_password_rejects_a_non_owner(
    company: Company,
) -> None:
    _create_employee(company, "empleado@example.com")

    with pytest.raises(CommandError, match="dueño activo"):
        call_command(
            "reset_owner_password",
            "--email",
            "empleado@example.com",
            stdout=StringIO(),
        )


@pytest.mark.django_db
def test_reset_owner_password_does_not_log_the_password(
    owner_account: Account,
    owner_membership: Membership,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG)
    out = StringIO()
    call_command(
        "reset_owner_password",
        "--email",
        "dueno@example.com",
        stdout=out,
    )
    temporary_password = out.getvalue().strip().splitlines()[-1]
    assert temporary_password not in caplog.text
