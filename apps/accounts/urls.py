"""Rutas del panel comercial de NexoPyme AI (T-11 a T-18)."""

from django.urls import path

from .views import (
    PanelLoginView,
    PanelLogoutView,
    audit_list,
    company_edit,
    panel_home,
    password_change,
    profile_detail,
    profile_redirect,
    user_change_role,
    user_create,
    user_deactivate,
    user_list,
    user_reactivate,
    user_regenerate_password,
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
    path("users/new/", user_create, name="user_create"),
    path("users/<int:pk>/role/", user_change_role, name="user_change_role"),
    path("users/<int:pk>/deactivate/", user_deactivate, name="user_deactivate"),
    path("users/<int:pk>/reactivate/", user_reactivate, name="user_reactivate"),
    path(
        "users/<int:pk>/password/",
        user_regenerate_password,
        name="user_regenerate_password",
    ),
    path("company/", company_edit, name="company_edit"),
    path("audit/", audit_list, name="audit_list"),
]
