"""Contexto de empresa y membresía por solicitud (T-08)."""

from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse

from apps.audit.services import record_security

from .decorators import MissingContextDenied
from .models import Membership

EXCLUDED_EXACT_PATHS = frozenset(
    {
        "/",
        "/health/",
        "/favicon.ico",
        "/login/",
        "/logout/",
        "/password/",
    }
)
EXCLUDED_PREFIXES = ("/static/", "/admin/")


def _is_excluded(path: str) -> bool:
    return path in EXCLUDED_EXACT_PATHS or path.startswith(EXCLUDED_PREFIXES)


class ActiveCompanyMiddleware:
    """Resuelve membresía y empresa activa una vez por solicitud.

    Sin membresía activa o con empresa inactiva se deniega con 403. Un
    identificador de empresa enviado por el cliente que no coincida con el
    contexto produce 404 uniforme y un evento de seguridad.
    """

    def __init__(self, get_response: object) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.membership = None
        request.company = None
        request.must_change_password = False

        if _is_excluded(request.path):
            return self.get_response(request)

        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return self.get_response(request)

        membership = (
            Membership.objects.select_related("company")
            .filter(account__user=user, is_active=True)
            .first()
        )
        if membership is None:
            raise MissingContextDenied("No tenés acceso al panel.")
        if not membership.company.is_active:
            raise MissingContextDenied("La empresa no está activa.")

        request.membership = membership
        request.company = membership.company
        # Punto único de evaluación de must_change_password.
        # T-12 añade aquí la redirección a /password/ con sus excepciones.
        request.must_change_password = membership.must_change_password

        injected_company = request.POST.get("company") or request.GET.get("company")
        if injected_company is not None and str(injected_company) != str(
            membership.company_id
        ):
            attempted_id = (
                int(injected_company) if str(injected_company).isdigit() else None
            )
            record_security(
                actor=user,
                company=membership.company,
                action="company.scope.injected",
                result="denied",
                attempted_company_id=attempted_id,
            )
            raise Http404("Recurso no encontrado.")

        return self.get_response(request)
