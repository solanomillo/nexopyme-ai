"""Rutas del panel comercial de NexoPyme AI (T-11)."""

from django.urls import path

from .views import PanelLoginView, PanelLogoutView, panel_home

app_name = "accounts"

urlpatterns = [
    path("login/", PanelLoginView.as_view(), name="login"),
    path("logout/", PanelLogoutView.as_view(), name="logout"),
    path("panel/", panel_home, name="panel"),
]
