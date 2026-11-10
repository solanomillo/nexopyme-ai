"""Rutas URL del proyecto NexoPyme AI (bootstrap 000)."""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from apps.accounts.decorators import MissingContextDenied
from apps.audit.services import record_security

from .views import health, home


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
    return render(request, "errors/403.html", {"reason": reason}, status=403)


def handler404(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Renderiza el 404 uniforme para recursos ajenos o inexistentes."""

    return render(request, "errors/404.html", status=404)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("health/", health, name="health"),
]
