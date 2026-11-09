"""Vistas básicas del proyecto NexoPyme AI (bootstrap 000)."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Renderiza la página informativa de NexoPyme AI."""
    return render(request, "home.html")


def health(request: HttpRequest) -> HttpResponse:
    """Devuelve HTTP 200 si Django puede atender la solicitud."""
    return HttpResponse("ok", content_type="text/plain")
