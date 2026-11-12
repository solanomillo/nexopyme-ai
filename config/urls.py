"""Rutas URL del proyecto NexoPyme AI (bootstrap 000)."""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path

from apps.accounts.decorators import MissingContextDenied
from apps.audit.services import record_security

from .views import health, home


def _is_signed_in(request: HttpRequest) -> bool:
    """Indica si la solicitud corresponde a una sesión autenticada."""

    user = getattr(request, "user", None)
    return bool(user is not None and user.is_authenticated)


def handler403(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Renderiza el 403 con el mensaje correspondiente al motivo."""

    is_context_denial = isinstance(exception, MissingContextDenied)
    user = getattr(request, "user", None)
    if not is_context_denial and user is not None and user.is_authenticated:
        record_security(
            actor=user,
            company=getattr(request, "company", None),
            action="permission.denied",
            result="denied",
        )
    reason = "context" if is_context_denial else "capability"
    signed_in = _is_signed_in(request)
    can_return_to_panel = (
        signed_in
        and reason != "context"
        and getattr(request, "account", None) is not None
    )
    response = render(
        request,
        "errors/403.html",
        {
            "reason": reason,
            "signed_in": signed_in,
            "can_return_to_panel": can_return_to_panel,
        },
        status=403,
    )
    response["Cache-Control"] = "no-store"
    return response


def handler404(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Renderiza el 404 uniforme para recursos ajenos o inexistentes."""

    response = render(
        request,
        "errors/404.html",
        {
            "signed_in": _is_signed_in(request),
            "can_return_to_panel": getattr(request, "account", None) is not None,
        },
        status=404,
    )
    response["Cache-Control"] = "no-store"
    return response


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("", home, name="home"),
    path("health/", health, name="health"),
]
