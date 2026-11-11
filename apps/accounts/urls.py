"""Rutas del panel comercial de NexoPyme AI (T-11, T-12)."""

from django.urls import path

from .views import (
    PanelLoginView,
    PanelLogoutView,
    panel_home,
    password_change,
    profile_detail,
    profile_redirect,
    user_list,
)

app_name = "accounts"

urlpatterns = [
    path("login/", PanelLoginView.as_view(), name="login"),
    path("logout/", PanelLogoutView.as_view(), name="logout"),
    path("panel/", panel_home, name="panel"),
    path("password/", password_change, name="password_change"),
    path("profile/", profile_redirect, name="profile"),
    path("profile/<int:pk>/", profile_detail, name="profile_detail"),
    path("users/", user_list, name="user_list"),
]
