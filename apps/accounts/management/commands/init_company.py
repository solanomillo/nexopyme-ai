"""Inicialización idempotente de la empresa y su dueño (T-13)."""

from __future__ import annotations

import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from apps.accounts.capabilities import Role
from apps.accounts.emails import clean_email
from apps.accounts.models import Company, Membership
from apps.accounts.services import (
    CompanyAlreadyInitialized,
    ServiceError,
    create_company_with_owner,
)


class Command(BaseCommand):
    """Crea la empresa activa y su dueño una sola vez.

    La contraseña inicial se solicita de forma interactiva y nunca se acepta
    como argumento ni se registra en la salida, los logs o la auditoría.
    """

    help = (
        "Crea la empresa activa y su dueño. La contraseña se solicita de forma "
        "interactiva y no se acepta como argumento."
    )

    def add_arguments(self, parser: object) -> None:
        parser.add_argument("--name", required=True, help="Nombre del negocio.")
        parser.add_argument("--email", required=True, help="Correo del dueño.")
        parser.add_argument(
            "--display-name",
            default=None,
            help=(
                "Nombre visible del dueño; por defecto, la parte local del "
                "correo."
            ),
        )

    def handle(self, *args: object, **options: object) -> None:
        try:
            email = clean_email(str(options["email"]))
        except ValidationError as exc:
            raise CommandError(" ".join(exc.messages)) from exc

        display_name = str(
            options["display_name"] or email.split("@", 1)[0]
        ).strip()
        if self._existing_owner(email) is not None:
            self.stdout.write(
                self.style.SUCCESS(
                    "La instalación ya está inicializada; no se modificó nada."
                )
            )
            return

        password = self._prompt_password()
        try:
            validate_password(password)
        except ValidationError as exc:
            raise CommandError(" ".join(exc.messages)) from exc

        try:
            create_company_with_owner(
                name=str(options["name"]),
                email=email,
                display_name=display_name,
                password=password,
            )
        except CompanyAlreadyInitialized as exc:
            raise CommandError(str(exc)) from exc
        except ServiceError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.SUCCESS("Instalación inicializada."))

    def _existing_owner(self, email: str) -> Membership | None:
        """Devuelve el dueño existente o falla si el estado es inconsistente."""

        active_companies = Company.objects.filter(is_active=True)
        count = active_companies.count()
        if count == 0:
            return None
        if count > 1:
            raise CommandError(
                "Estado inconsistente: hay más de una empresa activa."
            )

        company = active_companies.first()
        owners = Membership.objects.select_related("account").filter(
            company=company,
            role=Role.DUENO.value,
            is_active=True,
        )
        owner_count = owners.count()
        if owner_count != 1:
            raise CommandError(
                "Estado inconsistente: la empresa no tiene un único dueño activo."
            )

        owner = owners.first()
        if owner.account.email != email:
            raise CommandError(
                "La instalación ya está inicializada con otro dueño."
            )
        return owner

    def _prompt_password(self) -> str:
        password = getpass.getpass("Contraseña inicial: ")
        confirmation = getpass.getpass("Repetí la contraseña inicial: ")
        if not password:
            raise CommandError("La contraseña es obligatoria.")
        if password != confirmation:
            raise CommandError("Las contraseñas no coinciden.")
        return password
