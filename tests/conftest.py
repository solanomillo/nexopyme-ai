"""Fixtures compartidas de la Etapa 003 (T-03)."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.capabilities import Role
from apps.accounts.models import (
    Account,
    Company,
    Membership,
    generate_username,
)

TEST_PASSWORD = "Clave-Segura-2026"


@pytest.fixture
def company(db: object) -> Company:
    """Empresa activa de prueba."""
    return Company.objects.create(name="Almacén Central")


@pytest.fixture
def owner_account(db: object) -> Account:
    """Cuenta del dueño, con correo normalizado."""
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    return Account.objects.create(
        user=user,
        email="dueno@example.com",
        display_name="Dueña",
    )


@pytest.fixture
def owner_membership(
    db: object,
    company: Company,
    owner_account: Account,
) -> Membership:
    """Membresía activa del dueño en la empresa de prueba."""
    return Membership.objects.create(
        account=owner_account,
        company=company,
        role=Role.DUENO,
    )
