"""Vistas del panel comercial de NexoPyme AI (T-11 a T-18)."""

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

from apps.audit.models import AuditEvent, SecurityEvent
from apps.audit.services import record_audit

from .capabilities import Capability, Role
from .decorators import require_capability
from .forms import CompanyNameForm, EmployeeCreateForm
from .models import Membership
from .services import (
    DuplicateEmailError,
    ServiceError,
    change_role,
    create_employee,
    deactivate_membership,
    reactivate_membership,
    regenerate_temporary_password,
    update_company_name,
)

USERS_PER_PAGE = 20
AUDIT_PER_PAGE = 20


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
        {
            "page_obj": page_obj,
            "role_choices": [
                (role.value, role.label) for role in Role if role != Role.DUENO
            ],
        },
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


def _membership_of_company(request: HttpRequest, pk: int) -> Membership:
    """Devuelve la membresía de la empresa activa o responde 404 uniforme."""

    membership = (
        Membership.objects.select_related("account__user")
        .filter(company=request.company, pk=pk)
        .first()
    )
    if membership is None:
        raise Http404("Recurso no encontrado.")
    return membership


def _confirm(
    request: HttpRequest,
    *,
    title: str,
    message: str,
    membership: Membership,
    temporary_password: str | None = None,
    error: str | None = None,
) -> HttpResponse:
    """Renderiza la confirmación de una operación sobre una membresía."""

    return render(
        request,
        "accounts/user_confirm.html",
        {
            "title": title,
            "message": message,
            "target": membership,
            "temporary_password": temporary_password,
            "error": error,
        },
        status=400 if error else 200,
    )


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
@require_http_methods(["POST"])
def user_change_role(request: HttpRequest, pk: int) -> HttpResponse:
    """Cambia el rol de un empleado y audita los valores anterior y nuevo."""

    membership = _membership_of_company(request, pk)
    try:
        change_role(
            actor=request.membership,
            membership=membership,
            role=request.POST.get("role", ""),
        )
    except ServiceError as exc:
        return _confirm(
            request,
            title="No se pudo cambiar el rol",
            message="",
            membership=membership,
            error=str(exc),
        )
    return _confirm(
        request,
        title="Rol actualizado",
        message=(
            f"{membership.account.display_name} ahora tiene el rol "
            f"{membership.get_role_display()}. El cambio rige en su próxima "
            "solicitud."
        ),
        membership=membership,
    )


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
@require_http_methods(["POST"])
def user_deactivate(request: HttpRequest, pk: int) -> HttpResponse:
    """Desactiva un empleado y retira su acceso en la siguiente solicitud."""

    membership = _membership_of_company(request, pk)
    try:
        deactivate_membership(actor=request.membership, membership=membership)
    except ServiceError as exc:
        return _confirm(
            request,
            title="No se pudo desactivar",
            message="",
            membership=membership,
            error=str(exc),
        )
    return _confirm(
        request,
        title="Usuario desactivado",
        message=(
            f"{membership.account.display_name} ya no puede acceder al panel. "
            "Su historial y su auditoría se conservan."
        ),
        membership=membership,
    )


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
@require_http_methods(["POST"])
def user_reactivate(request: HttpRequest, pk: int) -> HttpResponse:
    """Reactiva un empleado con una contraseña temporal nueva."""

    membership = _membership_of_company(request, pk)
    try:
        temporary_password = reactivate_membership(
            actor=request.membership,
            membership=membership,
        )
    except ServiceError as exc:
        return _confirm(
            request,
            title="No se pudo reactivar",
            message="",
            membership=membership,
            error=str(exc),
        )
    return _confirm(
        request,
        title="Usuario reactivado",
        message=(
            f"{membership.account.display_name} puede volver a acceder con la "
            "contraseña temporal. Debe cambiarla en el primer acceso."
        ),
        membership=membership,
        temporary_password=temporary_password,
    )


@no_store
@login_required
@require_capability(Capability.USUARIOS_GESTIONAR)
@require_http_methods(["POST"])
def user_regenerate_password(request: HttpRequest, pk: int) -> HttpResponse:
    """Regenera la contraseña temporal de un empleado activo."""

    membership = _membership_of_company(request, pk)
    try:
        temporary_password = regenerate_temporary_password(
            actor=request.membership,
            membership=membership,
        )
    except ServiceError as exc:
        return _confirm(
            request,
            title="No se pudo regenerar la contraseña",
            message="",
            membership=membership,
            error=str(exc),
        )
    return _confirm(
        request,
        title="Contraseña temporal regenerada",
        message=(
            f"La contraseña anterior de {membership.account.display_name} quedó "
            "invalidada. La nueva se muestra una sola vez."
        ),
        membership=membership,
        temporary_password=temporary_password,
    )


@no_store
@login_required
@require_capability(Capability.EMPRESA_CONFIGURAR)
@require_http_methods(["GET", "POST"])
def company_edit(request: HttpRequest) -> HttpResponse:
    """Actualiza el nombre del negocio de la empresa activa."""

    form = CompanyNameForm(
        data=request.POST if request.method == "POST" else None,
        initial={"name": request.company.name},
    )
    if request.method == "POST" and form.is_valid():
        try:
            update_company_name(
                actor=request.membership,
                name=form.cleaned_data["name"],
            )
        except ServiceError as exc:
            form.add_error(None, str(exc))
        else:
            messages.success(request, "Nombre de la empresa actualizado.")
            return redirect("accounts:company_edit")

    status = 400 if request.method == "POST" else 200
    return render(
        request,
        "accounts/company_form.html",
        {"form": form},
        status=status,
    )


def _actor_label(event: object) -> str:
    """Nombre visible del actor; etiqueta genérica si no tiene cuenta."""

    account = getattr(event.actor, "account", None)
    return account.display_name if account is not None else "Personal técnico"


def _audit_row(event: AuditEvent) -> dict[str, object]:
    return {
        "created_at": event.created_at,
        "actor": _actor_label(event),
        "entity": event.entity,
        "entity_id": event.entity_id,
        "action": event.action,
        "result": event.result,
        "before": event.before,
        "after": event.after,
    }


def _security_row(event: SecurityEvent) -> dict[str, object]:
    """Fila de seguridad sin el identificador de empresa intentada."""

    return {
        "created_at": event.created_at,
        "actor": _actor_label(event),
        "action": event.action,
        "result": event.result,
    }


@no_store
@login_required
@require_capability(Capability.AUDITORIA_CONSULTAR)
@require_http_methods(["GET"])
def audit_list(request: HttpRequest) -> HttpResponse:
    """Lista la auditoría y los eventos de seguridad de la empresa activa."""

    audit_events = (
        AuditEvent.objects.select_related("actor__account")
        .filter(company=request.company, actor__isnull=False)
        .order_by("-created_at", "-pk")
    )
    security_events = (
        SecurityEvent.objects.select_related("actor__account")
        .filter(company=request.company, actor__isnull=False)
        .order_by("-created_at", "-pk")
    )
    audit_page = Paginator(audit_events, AUDIT_PER_PAGE).get_page(
        request.GET.get("audit_page")
    )
    security_page = Paginator(security_events, AUDIT_PER_PAGE).get_page(
        request.GET.get("security_page")
    )
    return render(
        request,
        "accounts/audit_list.html",
        {
            "audit_rows": [_audit_row(event) for event in audit_page.object_list],
            "audit_page": audit_page,
            "security_rows": [
                _security_row(event) for event in security_page.object_list
            ],
            "security_page": security_page,
        },
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
