"""Vistas del panel comercial de NexoPyme AI (T-11)."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ClassVar

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


class EmailAuthenticationForm(AuthenticationForm):
    """Formulario de acceso por correo con mensaje genérico."""

    username = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages: ClassVar[dict[str, str]] = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Correo o contraseña incorrectos.",
        "inactive": "Correo o contraseña incorrectos.",
    }

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            return
        for name in ("username", "password"):
            field = self[name]
            if field.errors:
                self.fields[name].widget.attrs.update(
                    {
                        "aria-invalid": "true",
                        "aria-describedby": f"{field.auto_id}-errors",
                    }
                )


class PanelLoginView(LoginView):
    """Acceso al panel con destino seguro y sin reautenticar sesiones."""

    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class PanelLogoutView(LogoutView):
    """Cierre de sesión por POST con retorno al acceso."""

    def get_default_redirect_url(self) -> str:
        return str(settings.LOGOUT_REDIRECT_URL)


def no_store(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """Impide que el navegador conserve respuestas autenticadas."""

    @wraps(view_func)
    def wrapper(
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        response = view_func(request, *args, **kwargs)
        response["Cache-Control"] = "no-store"
        return response

    return wrapper


@no_store
@login_required
def panel_home(request: HttpRequest) -> HttpResponse:
    """Muestra el panel comercial de la empresa activa."""

    return render(request, "accounts/panel.html")
