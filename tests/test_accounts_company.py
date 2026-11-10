"""Pruebas de los modelos y servicios de cuentas (T-03, T-06)."""

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
from apps.accounts.services import (
    CapabilityDenied,
    CompanyAlreadyInitialized,
    CrossCompanyError,
    DuplicateEmailError,
    LastOwnerError,
    ServiceError,
    change_role,
    create_company_with_owner,
    create_employee,
    deactivate_membership,
    reactivate_membership,
    regenerate_temporary_password,
    update_company_name,
)
from apps.audit.models import AuditEvent


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


def _create_membership(
    company: Company,
    email: str,
    role: str,
) -> Membership:
    account = _create_account(email)
    return Membership.objects.create(
        account=account,
        company=company,
        role=role,
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


@pytest.mark.django_db
def test_create_company_with_owner_initializes_the_installation(
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        membership = create_company_with_owner(
            name="Almacén Central",
            email="duena@example.com",
            display_name="Dueña",
            password="Clave-Segura-2026",
        )
    assert membership.role == Role.DUENO.value
    assert membership.must_change_password is True
    assert Company.objects.filter(is_active=True).count() == 1
    assert Account.objects.filter(email="duena@example.com").exists()
    assert AuditEvent.objects.filter(action="company.initialized").exists()


@pytest.mark.django_db
def test_second_company_initialization_is_rejected(
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        create_company_with_owner(
            name="Almacén Central",
            email="duena@example.com",
            display_name="Dueña",
            password="Clave-Segura-2026",
        )
    with pytest.raises(CompanyAlreadyInitialized):
        create_company_with_owner(
            name="Otra empresa",
            email="otra@example.com",
            display_name="Otra",
            password="Clave-Segura-2026",
        )


@pytest.mark.django_db
def test_create_employee_returns_a_temporary_password(
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        membership, temporary_password = create_employee(
            actor=owner_membership,
            email="empleado@example.com",
            display_name="Empleado",
            role=Role.OPERADOR.value,
        )
    assert membership.role == Role.OPERADOR.value
    assert membership.must_change_password is True
    assert membership.account.user.check_password(temporary_password)
    assert AuditEvent.objects.filter(action="membership.created").exists()


@pytest.mark.django_db
def test_duplicate_email_is_rejected(
    owner_membership: Membership,
) -> None:
    create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    accounts_before = Account.objects.count()
    with pytest.raises(DuplicateEmailError):
        create_employee(
            actor=owner_membership,
            email="EMPLEADO@example.com",
            display_name="Otro",
            role=Role.CONSULTA.value,
        )
    assert Account.objects.count() == accounts_before


@pytest.mark.django_db
def test_cannot_create_another_owner(owner_membership: Membership) -> None:
    with pytest.raises(ServiceError):
        create_employee(
            actor=owner_membership,
            email="segundo@example.com",
            display_name="Segundo",
            role=Role.DUENO.value,
        )


@pytest.mark.django_db
def test_employee_cannot_manage_users(
    company: Company,
    owner_membership: Membership,
) -> None:
    encargado = _create_membership(company, "encargado@example.com", Role.ENCARGADO)
    with pytest.raises(CapabilityDenied):
        create_employee(
            actor=encargado,
            email="nuevo@example.com",
            display_name="Nuevo",
            role=Role.CONSULTA.value,
        )


@pytest.mark.django_db
def test_change_role_is_audited(
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    with django_capture_on_commit_callbacks(execute=True):
        change_role(
            actor=owner_membership,
            membership=employee,
            role=Role.CONSULTA.value,
        )
    employee.refresh_from_db()
    assert employee.role == Role.CONSULTA.value
    event = AuditEvent.objects.get(action="membership.role_changed")
    assert event.before == {"role": Role.OPERADOR.value}
    assert event.after == {"role": Role.CONSULTA.value}


@pytest.mark.django_db
def test_last_owner_cannot_change_own_role(owner_membership: Membership) -> None:
    with pytest.raises(LastOwnerError):
        change_role(
            actor=owner_membership,
            membership=owner_membership,
            role=Role.ENCARGADO.value,
        )


@pytest.mark.django_db
def test_cannot_assign_owner_role(owner_membership: Membership) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    with pytest.raises(ServiceError):
        change_role(
            actor=owner_membership,
            membership=employee,
            role=Role.DUENO.value,
        )


@pytest.mark.django_db
def test_cannot_change_membership_of_another_company(
    owner_membership: Membership,
) -> None:
    other_company = Company.objects.create(name="Otra empresa")
    other_membership = _create_membership(
        other_company,
        "otra@example.com",
        Role.OPERADOR,
    )
    with pytest.raises(CrossCompanyError):
        change_role(
            actor=owner_membership,
            membership=other_membership,
            role=Role.CONSULTA.value,
        )


@pytest.mark.django_db
def test_cross_company_mutations_are_rejected(
    owner_membership: Membership,
) -> None:
    other_company = Company.objects.create(name="Otra empresa")
    other_membership = _create_membership(
        other_company,
        "otra@example.com",
        Role.OPERADOR,
    )
    with pytest.raises(CrossCompanyError):
        deactivate_membership(
            actor=owner_membership,
            membership=other_membership,
        )
    with pytest.raises(CrossCompanyError):
        reactivate_membership(
            actor=owner_membership,
            membership=other_membership,
        )
    with pytest.raises(CrossCompanyError):
        regenerate_temporary_password(
            actor=owner_membership,
            membership=other_membership,
        )


@pytest.mark.django_db
def test_last_owner_cannot_be_deactivated(owner_membership: Membership) -> None:
    with pytest.raises(LastOwnerError):
        deactivate_membership(
            actor=owner_membership,
            membership=owner_membership,
        )


@pytest.mark.django_db
def test_employee_deactivation_and_reactivation(
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    with django_capture_on_commit_callbacks(execute=True):
        deactivate_membership(actor=owner_membership, membership=employee)
    employee.refresh_from_db()
    assert employee.is_active is False
    with django_capture_on_commit_callbacks(execute=True):
        temporary_password = reactivate_membership(
            actor=owner_membership,
            membership=employee,
        )
    employee.refresh_from_db()
    assert employee.is_active is True
    assert employee.must_change_password is True
    assert employee.account.user.check_password(temporary_password)


@pytest.mark.django_db
def test_cannot_deactivate_twice(
    owner_membership: Membership,
) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    deactivate_membership(actor=owner_membership, membership=employee)
    with pytest.raises(ServiceError):
        deactivate_membership(actor=owner_membership, membership=employee)


@pytest.mark.django_db
def test_regenerate_temporary_password(
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="empleado@example.com",
        display_name="Empleado",
        role=Role.OPERADOR.value,
    )
    with django_capture_on_commit_callbacks(execute=True):
        temporary_password = regenerate_temporary_password(
            actor=owner_membership,
            membership=employee,
        )
    employee.refresh_from_db()
    assert employee.must_change_password is True
    assert employee.account.user.check_password(temporary_password)
    assert AuditEvent.objects.filter(
        action="membership.password_regenerated"
    ).exists()


@pytest.mark.django_db
def test_company_name_requires_capability(
    company: Company,
    owner_membership: Membership,
) -> None:
    encargado = _create_membership(company, "encargado@example.com", Role.ENCARGADO)
    with pytest.raises(CapabilityDenied):
        update_company_name(actor=encargado, name="Nuevo nombre")


@pytest.mark.django_db
def test_update_company_name_is_audited(
    company: Company,
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    with django_capture_on_commit_callbacks(execute=True):
        update_company_name(actor=owner_membership, name="  Nuevo nombre  ")
    company.refresh_from_db()
    assert company.name == "Nuevo nombre"
    event = AuditEvent.objects.get(action="company.name_updated")
    assert event.before == {"name": "Almacén Central"}
    assert event.after == {"name": "Nuevo nombre"}
