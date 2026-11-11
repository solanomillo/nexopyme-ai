"""Backends de autenticación de NexoPyme AI (T-10).

Existen dos caminos disjuntos:

- ``EmailBackend`` autentica cuentas comerciales por correo y exige membresía y
  empresa activas. Rechaza al personal técnico y a los superusuarios.
- ``TechnicalAdminBackend`` autentica únicamente personal técnico con
  ``is_staff`` y sin cuenta comercial.

Ningún camino permite saltarse la membresía de negocio.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from apps.audit.services import record_security

from .emails import normalize_email
from .models import Account, Membership

COMMERCIAL_LOGIN_FAILED = "login.failed"
TECHNICAL_LOGIN_FAILED = "admin.login.failed"


def _record_failed_login(
    *,
    action: str = COMMERCIAL_LOGIN_FAILED,
    actor: Any | None = None,
) -> None:
    """Registra un intento fallido sin almacenar correo ni contraseña."""

    record_security(action=action, result="denied", actor=actor)


class EmailBackend(BaseBackend):
    """Autentica cuentas comerciales mediante correo electrónico."""

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> Any | None:
        raw_email = username or kwargs.get("email")
        if not raw_email or not password:
            return None
        # Un identificador sin forma de correo pertenece al Admin técnico.
        if "@" not in str(raw_email):
            return None

        email = normalize_email(str(raw_email))
        account = (
            Account.objects.select_related("user").filter(email=email).first()
        )
        if account is None:
            # Iguala el costo del hash para no revelar si la cuenta existe.
            get_user_model()().set_password(password)
            _record_failed_login()
            return None

        user = account.user
        password_ok = user.check_password(password)
        if user.is_staff or user.is_superuser:
            _record_failed_login(actor=user)
            return None
        if not password_ok:
            _record_failed_login(actor=user)
            return None
        if not user.is_active:
            _record_failed_login(actor=user)
            return None

        membership = (
            Membership.objects.select_related("company")
            .filter(
                account=account,
                is_active=True,
                company__is_active=True,
            )
            .first()
        )
        if membership is None:
            _record_failed_login(actor=user)
            return None
        return user

    def get_user(self, user_id: Any) -> Any | None:
        """Carga la cuenta comercial de una sesión activa."""

        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
        if not user.is_active:
            return None
        if user.is_staff or user.is_superuser:
            return None
        return user


class TechnicalAdminBackend(BaseBackend):
    """Autentica personal técnico con acceso a Django Admin."""

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> Any | None:
        identifier = username or kwargs.get("username")
        if not identifier or not password:
            return None

        user_model = get_user_model()
        try:
            user = user_model._default_manager.get_by_natural_key(str(identifier))
        except user_model.DoesNotExist:
            if "@" not in str(identifier):
                _record_failed_login(action=TECHNICAL_LOGIN_FAILED)
            user_model().set_password(password)
            return None
        if not user.is_staff:
            if "@" not in str(identifier):
                _record_failed_login(action=TECHNICAL_LOGIN_FAILED, actor=user)
            return None
        if Account.objects.filter(user=user).exists():
            return None
        if not user.is_active or not user.check_password(password):
            _record_failed_login(action=TECHNICAL_LOGIN_FAILED, actor=user)
            return None
        return user

    def get_user(self, user_id: Any) -> Any | None:
        """Carga el personal técnico de una sesión de Admin."""

        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
        if not user.is_active:
            return None
        if not user.is_staff:
            return None
        if Account.objects.filter(user=user).exists():
            return None
        return user
