"""Capacidades de navegación del panel expuestas a las plantillas (T-24)."""

from __future__ import annotations

from django.http import HttpRequest

from .capabilities import Capability, has_capability


def panel_navigation(request: HttpRequest) -> dict[str, dict[str, bool]]:
    """Devuelve los enlaces del panel habilitados para la membresía actual."""
    membership = getattr(request, "membership", None)
    role = getattr(membership, "role", None)
    return {
        "panel_nav": {
            "users": has_capability(role, Capability.USUARIOS_GESTIONAR),
            "company": has_capability(role, Capability.EMPRESA_CONFIGURAR),
            "audit": has_capability(role, Capability.AUDITORIA_CONSULTAR),
        }
    }
