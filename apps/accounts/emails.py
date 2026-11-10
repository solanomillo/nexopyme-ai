"""Normalización y validación del correo de acceso."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

MAX_EMAIL_LENGTH = 254


def normalize_email(value: str) -> str:
    """Normaliza el correo: sin espacios laterales y sin distinguir mayúsculas."""

    return value.strip().casefold()


def clean_email(value: str) -> str:
    """Devuelve el correo normalizado o lanza ``ValidationError``."""

    normalized = normalize_email(value)
    if not normalized:
        raise ValidationError("El correo es obligatorio.")
    if len(normalized) > MAX_EMAIL_LENGTH:
        raise ValidationError("El correo supera la longitud máxima admitida.")
    validate_email(normalized)
    return normalized
