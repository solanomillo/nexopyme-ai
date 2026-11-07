"""Rutas URL del proyecto NexoPyme AI (bootstrap 000)."""

from django.urls import path

from .views import health

urlpatterns = [
    path("health/", health, name="health"),
]
