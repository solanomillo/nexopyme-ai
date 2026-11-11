"""Recuperación técnica del dueño mediante contraseña temporal (T-13)."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.capabilities import Role
from apps.accounts.emails import clean_email
from apps.accounts.models import Membership
from apps.accounts.services import generate_temporary_password
from apps.audit.services import record_audit


class Command(BaseCommand):
    """Genera una contraseña temporal para el dueño activo.

    La contraseña se muestra una sola vez en la salida estándar, activa el
    cambio obligatorio y queda auditada sin registrar su valor.
    """

    help = (
        "Genera una contraseña temporal para el dueño. Se muestra una sola vez "
        "y exige el cambio en el siguiente acceso."
    )

    def add_arguments(self, parser: object) -> None:
        parser.add_argument("--email", required=True, help="Correo del dueño.")

    def handle(self, *args: object, **options: object) -> None:
        try:
            email = clean_email(str(options["email"]))
        except ValidationError as exc:
            raise CommandError(" ".join(exc.messages)) from exc

        membership = (
            Membership.objects.select_related("account__user", "company")
            .filter(
                account__email=email,
                role=Role.DUENO.value,
                is_active=True,
                company__is_active=True,
            )
            .first()
        )
        if membership is None:
            raise CommandError("No existe un dueño activo con ese correo.")

        temporary_password = generate_temporary_password()
        with transaction.atomic():
            user = membership.account.user
            user.set_password(temporary_password)
            user.save(update_fields=["password"])
            membership.must_change_password = True
            membership.save(
                update_fields=["must_change_password", "updated_at"]
            )
            record_audit(
                actor=None,
                company=membership.company,
                entity="Membership",
                entity_id=membership.pk,
                action="membership.owner_password_reset",
                result="success",
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Contraseña temporal generada. Se muestra una sola vez:"
            )
        )
        self.stdout.write(temporary_password)
