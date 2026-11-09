"""Rutas URL del proyecto NexoPyme AI (bootstrap 000)."""

from django.contrib import admin
from django.urls import path

from .views import health, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("health/", health, name="health"),
]
