"""Vistas del panel comercial de NexoPyme AI (T-11 a T-15)."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ClassVar

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.audit.services import record_audit

from .capabilities import Capability
from .decorators import require_capability
from .forms import EmployeeCreateForm
from .models import Membership
from .services import DuplicateEmailError, ServiceError, create_employee

USERS_PER_PAGE = 20


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


class PanelPasswordChangeForm(PasswordChangeForm):
    """Cambio de contraseña con contraseña actual y política vigente."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Contraseña actual"
        self.fields["old_password"].widget.attrs.update(
            {"autocomplete": "current-password", "autofocus": True}
        )
        self.fields["new_password1"].label = "Nueva contraseña"
        self.fields["new_password1"].widget.attrs.update(
            {"autocomplete": "new-password"}
        )
        self.fields["new_password2"].label = "Confirmar nueva contraseña"
        self.fields["new_password2"].widget.attrs.update(
            {"autocomplete": "new-password"}
        )
        if not self.is_bound:
            return
        for name in ("old_password", "new_password1", "new_password2"):
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


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
def user_list(request: HttpRequest) -> HttpResponse:
    """Lista las membresías de la empresa activa con paginación."""

    memberships = (
        Membership.objects.select_related("account__user")
        .filter(company=request.company)
        .order_by("account__display_name", "pk")
    )
    paginator = Paginator(memberships, USERS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "accounts/user_list.html",
        {"page_obj": page_obj},
    )


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
@require_http_methods(["GET", "POST"])
def user_create(request: HttpRequest) -> HttpResponse:
    """Crea un empleado y muestra su contraseña temporal una sola vez."""

    form = EmployeeCreateForm(
        data=request.POST if request.method == "POST" else None,
    )
    if request.method == "POST" and form.is_valid():
        try:
            membership, temporary_password = create_employee(
                actor=request.membership,
                email=form.cleaned_data["email"],
                display_name=form.cleaned_data["display_name"],
                role=form.cleaned_data["role"],
            )
        except DuplicateEmailError:
            form.add_error("email", "El correo ya está registrado.")
            form.apply_error_attributes()
        except ServiceError as exc:
            form.add_error(None, str(exc))
            form.apply_error_attributes()
        else:
            return render(
                request,
                "accounts/user_form.html",
                {
                    "created_membership": membership,
                    "temporary_password": temporary_password,
                },
            )

    status = 400 if request.method == "POST" else 200
    return render(
        request,
        "accounts/user_form.html",
        {"form": form},
        status=status,
    )


@no_store
@login_required
@require_http_methods(["GET", "POST"])
def password_change(request: HttpRequest) -> HttpResponse:
    """Cambia la contraseña propia y limpia el cambio obligatorio."""

    form = PanelPasswordChangeForm(
        user=request.user,
        data=request.POST if request.method == "POST" else None,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save()
            membership = request.membership
            membership.must_change_password = False
            membership.save(
                update_fields=["must_change_password", "updated_at"]
            )
            record_audit(
                actor=user,
                company=request.company,
                entity="account",
                entity_id=request.account.pk,
                action="password.changed",
                result="success",
            )
        update_session_auth_hash(request, user)
        messages.success(request, "Contraseña actualizada.")
        return redirect("accounts:profile")
    return render(request, "accounts/password_change.html", {"form": form})


@no_store
@login_required
def profile_redirect(request: HttpRequest) -> HttpResponse:
    """Redirige al perfil de la cuenta autenticada."""

    return redirect("accounts:profile_detail", pk=request.account.pk)


@no_store
@login_required
def profile_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Muestra el perfil propio y aísla las cuentas ajenas."""

    membership = (
        Membership.objects.select_related("account")
        .filter(company=request.company, account_id=pk)
        .first()
    )
    if membership is None:
        raise Http404("Recurso no encontrado.")
    if membership.account_id != request.account.pk:
        raise PermissionDenied("No tenés permiso para ver este perfil.")
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_account": membership.account,
            "profile_membership": membership,
        },
    )
