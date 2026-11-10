"""Autorización por capacidades para vistas (T-09)."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse

from .capabilities import Capability, has_capability


class MissingContextDenied(PermissionDenied):
    """La cuenta no tiene membresía o empresa activa."""


class MissingCapabilityDenied(PermissionDenied):
    """La cuenta no posee la capacidad requerida."""


def require_capability(capability: Capability) -> Callable[[Callable], Callable]:
    """Exige una capacidad en la vista, delegando en ``has_capability``."""

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
            membership = getattr(request, "membership", None)
            if membership is None:
                raise MissingContextDenied("No tenés acceso al panel.")
            if not has_capability(membership.role, capability):
                raise MissingCapabilityDenied(
                    "No tenés permiso para realizar esta operación."
                )
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
