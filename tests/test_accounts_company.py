"""Pruebas de los modelos de cuentas, empresa y membresía (T-03)."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.accounts.capabilities import Role
from apps.accounts.emails import clean_email, normalize_email
from apps.accounts.models import (
    Account,
    Company,
    Membership,
    generate_username,
)


def _create_account(email: str) -> Account:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password="Clave-Segura-2026",
    )
    return Account.objects.create(
        user=user,
        email=email,
        display_name="Empleado",
    )


@pytest.mark.django_db
def test_account_normalizes_email_on_save() -> None:
    account = _create_account("  Dueno@Example.COM ")
    account.refresh_from_db()
    assert account.email == "dueno@example.com"


@pytest.mark.django_db
def test_account_email_is_unique() -> None:
    _create_account("duplicado@example.com")
    with pytest.raises(IntegrityError), transaction.atomic():
        _create_account("DUPLICADO@example.com")


@pytest.mark.django_db
def test_account_accepts_a_254_character_email() -> None:
    email = ("a" * 242) + "@example.com"
    assert len(email) == 254
    account = _create_account(email)
    assert account.email == email


@pytest.mark.django_db
def test_membership_is_unique_per_account_and_company(
    company: Company,
    owner_account: Account,
) -> None:
    Membership.objects.create(
        account=owner_account,
        company=company,
        role=Role.DUENO,
    )
    with pytest.raises(IntegrityError), transaction.atomic():
        Membership.objects.create(
            account=owner_account,
            company=company,
            role=Role.ENCARGADO,
        )


@pytest.mark.django_db
def test_company_and_membership_defaults(
    company: Company,
    owner_account: Account,
) -> None:
    membership = Membership.objects.create(
        account=owner_account,
        company=company,
        role=Role.ENCARGADO,
    )
    assert company.is_active is True
    assert membership.is_active is True
    assert membership.must_change_password is False


def test_username_is_opaque_and_unique() -> None:
    usernames = {generate_username() for _ in range(100)}
    assert len(usernames) == 100
    for username in usernames:
        assert username.startswith("u")
        assert len(username) <= 150


def test_normalize_email_strips_and_casefolds() -> None:
    assert normalize_email("  Usuario@Ejemplo.COM ") == "usuario@ejemplo.com"


def test_clean_email_rejects_invalid_and_oversized_values() -> None:
    with pytest.raises(ValidationError):
        clean_email("")
    with pytest.raises(ValidationError):
        clean_email("sin-arroba")
    with pytest.raises(ValidationError):
        clean_email(("a" * 250) + "@example.com")
