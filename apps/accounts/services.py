"""Servicios de empresa, membresía y cuentas (T-06).

Todas las mutaciones revalidan capacidad y empresa, y auditan el resultado.
Ningún servicio acepta un identificador de empresa enviado por el cliente.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils.crypto import get_random_string

from apps.audit.services import record_audit

from .capabilities import Capability, Role, has_capability
from .emails import clean_email
from .models import Account, Company, Membership, generate_username

TEMPORARY_PASSWORD_LENGTH = 20


class ServiceError(Exception):
    """Error de negocio de cuentas."""


class CapabilityDenied(ServiceError):
    """El actor no posee la capacidad requerida."""


class CrossCompanyError(ServiceError):
    """El recurso pertenece a otra empresa."""


class LastOwnerError(ServiceError):
    """La operación dejaría la empresa sin dueño activo."""


class DuplicateEmailError(ServiceError):
    """El correo ya está registrado en la instalación."""


class CompanyAlreadyInitialized(ServiceError):
    """La instalación ya tiene una empresa activa."""


def generate_temporary_password() -> str:
    """Genera una contraseña temporal de un solo uso."""

    return get_random_string(TEMPORARY_PASSWORD_LENGTH)


def _require_capability(actor: Membership, capability: Capability) -> None:
    if not has_capability(actor.role, capability):
        raise CapabilityDenied("No tenés permiso para realizar esta operación.")


def _require_same_company(actor: Membership, membership: Membership) -> None:
    if actor.company_id != membership.company_id:
        raise CrossCompanyError("El recurso no pertenece a tu empresa.")


def _active_owner_count(company_id: int) -> int:
    return Membership.objects.filter(
        company_id=company_id,
        role=Role.DUENO.value,
        is_active=True,
    ).count()


def _audit(
    *,
    actor_user: object,
    company: Company,
    entity: str,
    entity_id: object,
    action: str,
    before: object | None = None,
    after: object | None = None,
) -> None:
    record_audit(
        actor=actor_user,
        company=company,
        entity=entity,
        entity_id=entity_id,
        action=action,
        result="success",
        before=before,
        after=after,
    )


def create_company_with_owner(
    *,
    name: str,
    email: str,
    display_name: str,
    password: str,
) -> Membership:
    """Inicializa la instalación con una empresa activa y su dueño."""

    normalized_email = clean_email(email)
    clean_name = name.strip()
    if not clean_name:
        raise ServiceError("El nombre de la empresa es obligatorio.")
    if Company.objects.filter(is_active=True).exists():
        raise CompanyAlreadyInitialized("La empresa ya fue inicializada.")

    with transaction.atomic():
        company = Company.objects.create(name=clean_name)
        user = get_user_model().objects.create_user(
            username=generate_username(),
            password=password,
        )
        account = Account.objects.create(
            user=user,
            email=normalized_email,
            display_name=display_name.strip(),
        )
        membership = Membership.objects.create(
            account=account,
            company=company,
            role=Role.DUENO.value,
            must_change_password=True,
        )
        _audit(
            actor_user=user,
            company=company,
            entity="Company",
            entity_id=company.pk,
            action="company.initialized",
            after={"name": company.name},
        )
    return membership


def create_employee(
    *,
    actor: Membership,
    email: str,
    display_name: str,
    role: str,
) -> tuple[Membership, str]:
    """Crea una cuenta de empleado y devuelve su contraseña temporal."""

    _require_capability(actor, Capability.USUARIOS_GESTIONAR)
    try:
        role_value = Role(role)
    except ValueError as exc:
        raise ServiceError("Rol inválido.") from exc
    if role_value == Role.DUENO:
        raise ServiceError("No se puede crear otro dueño.")

    normalized_email = clean_email(email)
    temporary_password = generate_temporary_password()
    try:
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                username=generate_username(),
                password=temporary_password,
            )
            account = Account.objects.create(
                user=user,
                email=normalized_email,
                display_name=display_name.strip(),
            )
            membership = Membership.objects.create(
                account=account,
                company=actor.company,
                role=role_value.value,
                must_change_password=True,
            )
            _audit(
                actor_user=actor.account.user,
                company=actor.company,
                entity="Membership",
                entity_id=membership.pk,
                action="membership.created",
                after={"role": membership.role},
            )
    except IntegrityError as exc:
        raise DuplicateEmailError("El correo ya está registrado.") from exc
    return membership, temporary_password


def change_role(
    *,
    actor: Membership,
    membership: Membership,
    role: str,
) -> None:
    """Cambia el rol de una membresía de la misma empresa."""

    _require_same_company(actor, membership)
    _require_capability(actor, Capability.USUARIOS_GESTIONAR)
    try:
        role_value = Role(role)
    except ValueError as exc:
        raise ServiceError("Rol inválido.") from exc
    if role_value == Role.DUENO:
        raise ServiceError("No se puede asignar el rol de dueño.")

    with transaction.atomic():
        if (
            membership.role == Role.DUENO.value
            and membership.is_active
            and _active_owner_count(membership.company_id) <= 1
        ):
            raise LastOwnerError("La empresa debe conservar un dueño activo.")
        previous_role = membership.role
        membership.role = role_value.value
        membership.save(update_fields=["role", "updated_at"])
        _audit(
            actor_user=actor.account.user,
            company=actor.company,
            entity="Membership",
            entity_id=membership.pk,
            action="membership.role_changed",
            before={"role": previous_role},
            after={"role": membership.role},
        )


def deactivate_membership(*, actor: Membership, membership: Membership) -> None:
    """Desactiva una membresía, protegiendo al último dueño activo."""

    _require_same_company(actor, membership)
    _require_capability(actor, Capability.USUARIOS_GESTIONAR)
    if not membership.is_active:
        raise ServiceError("La membresía ya está inactiva.")

    with transaction.atomic():
        if (
            membership.role == Role.DUENO.value
            and membership.is_active
            and _active_owner_count(membership.company_id) <= 1
        ):
            raise LastOwnerError("La empresa debe conservar un dueño activo.")
        membership.is_active = False
        membership.save(update_fields=["is_active", "updated_at"])
        _audit(
            actor_user=actor.account.user,
            company=actor.company,
            entity="Membership",
            entity_id=membership.pk,
            action="membership.deactivated",
            before={"is_active": True},
            after={"is_active": False},
        )


def reactivate_membership(*, actor: Membership, membership: Membership) -> str:
    """Reactiva una membresía con una nueva contraseña temporal."""

    _require_same_company(actor, membership)
    _require_capability(actor, Capability.USUARIOS_GESTIONAR)
    if membership.is_active:
        raise ServiceError("La membresía ya está activa.")

    temporary_password = generate_temporary_password()
    with transaction.atomic():
        previous_flag = membership.must_change_password
        membership.is_active = True
        membership.must_change_password = True
        membership.save(update_fields=["is_active", "must_change_password", "updated_at"])
        user = membership.account.user
        user.set_password(temporary_password)
        user.save(update_fields=["password"])
        _audit(
            actor_user=actor.account.user,
            company=actor.company,
            entity="Membership",
            entity_id=membership.pk,
            action="membership.reactivated",
            before={"is_active": False, "must_change_password": previous_flag},
            after={"is_active": True, "must_change_password": True},
        )
    return temporary_password


def regenerate_temporary_password(
    *,
    actor: Membership,
    membership: Membership,
) -> str:
    """Regenera la contraseña temporal de un empleado activo."""

    _require_same_company(actor, membership)
    _require_capability(actor, Capability.USUARIOS_GESTIONAR)
    if membership.role == Role.DUENO.value:
        raise ServiceError(
            "La recuperación del dueño se realiza por comando técnico."
        )
    if not membership.is_active:
        raise ServiceError("La membresía está inactiva.")

    temporary_password = generate_temporary_password()
    with transaction.atomic():
        previous_flag = membership.must_change_password
        user = membership.account.user
        user.set_password(temporary_password)
        user.save(update_fields=["password"])
        membership.must_change_password = True
        membership.save(update_fields=["must_change_password", "updated_at"])
        _audit(
            actor_user=actor.account.user,
            company=actor.company,
            entity="Membership",
            entity_id=membership.pk,
            action="membership.password_regenerated",
            before={"must_change_password": previous_flag},
            after={"must_change_password": True},
        )
    return temporary_password


def update_company_name(*, actor: Membership, name: str) -> None:
    """Actualiza el nombre de la empresa del actor."""

    _require_capability(actor, Capability.EMPRESA_CONFIGURAR)
    clean_name = name.strip()
    if not clean_name:
        raise ServiceError("El nombre de la empresa es obligatorio.")

    company = actor.company
    with transaction.atomic():
        previous_name = company.name
        company.name = clean_name
        company.save(update_fields=["name", "updated_at"])
        _audit(
            actor_user=actor.account.user,
            company=company,
            entity="Company",
            entity_id=company.pk,
            action="company.name_updated",
            before={"name": previous_name},
            after={"name": company.name},
        )
