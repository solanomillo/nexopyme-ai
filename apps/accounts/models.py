"""Modelos de cuentas, empresa y membresía (T-03)."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from .capabilities import Role
from .emails import MAX_EMAIL_LENGTH, normalize_email


def generate_username() -> str:
    """Genera un identificador técnico opaco para ``auth.User.username``.

    El nombre de usuario no se muestra ni se usa para autenticar; el acceso se
    resuelve por el correo de ``Account`` (D-15).
    """

    return f"u{uuid.uuid4().hex}"


class Company(models.Model):
    """Empresa propietaria de los datos; unidad de aislamiento."""

    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    """Cuenta comercial de una persona del negocio."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="account",
    )
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, unique=True)
    display_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "cuenta"
        verbose_name_plural = "cuentas"

    def save(self, *args: object, **kwargs: object) -> None:
        self.email = normalize_email(self.email)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email


class Membership(models.Model):
    """Vínculo entre una cuenta y una empresa, con un rol."""

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "membresía"
        verbose_name_plural = "membresías"
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["account", "company"],
                name="unique_membership_account_company",
            )
        ]
        indexes = [  # noqa: RUF012
            models.Index(
                fields=["company", "is_active"],
                name="membership_company_active_idx",
            ),
            models.Index(
                fields=["account", "is_active"],
                name="membership_account_active_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.account.email} · {self.company.name} · {self.role}"
