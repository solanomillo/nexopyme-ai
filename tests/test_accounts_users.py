"""Pruebas del listado de usuarios del panel (T-14, T-15)."""

from __future__ import annotations

import re
from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

from apps.accounts.capabilities import Role
from apps.accounts.models import Account, Company, Membership, generate_username
from apps.audit.models import AuditEvent, SecurityEvent

TEST_PASSWORD = "Clave-Segura-2026"


def _create_membership(
    company: Company,
    email: str,
    *,
    display_name: str = "Empleado",
    role: str = Role.OPERADOR.value,
    is_active: bool = True,
) -> Membership:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=None,
    )
    account = Account.objects.create(
        user=user,
        email=email,
        display_name=display_name,
    )
    return Membership.objects.create(
        account=account,
        company=company,
        role=role,
        is_active=is_active,
    )


def test_user_list_route_is_registered() -> None:
    """La ruta del listado se resuelve con el namespace accounts (DB-free)."""

    assert reverse("accounts:user_list") == "/users/"


@pytest.mark.django_db
def test_user_list_requires_login(client: object) -> None:
    response = client.get("/users/")
    assert response.status_code == 302
    assert response.url == "/login/?next=/users/"


@pytest.mark.django_db
def test_user_list_requires_the_management_capability(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    consulta = _create_membership(
        company,
        "consulta@example.com",
        display_name="Consulta",
        role=Role.CONSULTA.value,
    )
    client.force_login(consulta.account.user)
    response = client.get("/users/")
    assert response.status_code == 403
    assert "No tenés permiso" in response.content.decode()
    assert owner_account.email not in response.content.decode()


@pytest.mark.django_db
def test_user_list_shows_only_the_active_company(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    employee = _create_membership(
        company,
        "empleado@example.com",
        display_name="Empleado Propio",
        role=Role.ENCARGADO.value,
    )
    other_company = Company.objects.create(name="Otra empresa", is_active=False)
    foreign = _create_membership(
        other_company,
        "ajeno@example.com",
        display_name="Cuenta Ajena",
    )

    client.force_login(owner_account.user)
    response = client.get("/users/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "accounts/user_list.html" in [
        template.name for template in response.templates
    ]
    assert owner_account.email in content
    assert employee.account.email in content
    assert employee.account.display_name in content
    assert "Encargado" in content
    assert foreign.account.email not in content
    assert foreign.account.display_name not in content
    assert response["Cache-Control"] == "no-store"
    assert content.count("<h1") == 1


@pytest.mark.django_db
def test_user_list_shows_state_and_last_access(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    active = _create_membership(company, "activo@example.com")
    inactive = _create_membership(
        company,
        "inactivo@example.com",
        display_name="Inactivo",
        is_active=False,
    )
    last_login = timezone.make_aware(
        datetime(2026, 3, 5, 12, 0),
        timezone.get_current_timezone(),
    )
    get_user_model().objects.filter(pk=active.account.user.pk).update(
        last_login=last_login
    )

    client.force_login(owner_account.user)
    content = client.get("/users/").content.decode()

    assert "Activa" in content
    assert "Inactiva" in content
    assert "05/03/2026 12:00" in content
    assert "Nunca" in content
    assert inactive.account.email in content
    assert TEST_PASSWORD not in content
    assert "pbkdf2" not in content


@pytest.mark.django_db
def test_user_list_template_renders_the_empty_state(
    rf: RequestFactory,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    request = rf.get("/users/")
    request.user = owner_account.user
    request.company = company
    request.membership = owner_membership
    request.account = owner_account
    request.resolver_match = None

    page_obj = Paginator([], 20).get_page(1)
    html = render_to_string(
        "accounts/user_list.html",
        {"page_obj": page_obj},
        request=request,
    )

    assert "No hay usuarios registrados en la empresa." in html
    assert "pagination" not in html


@pytest.mark.django_db
def test_user_list_paginates_twenty_memberships_per_page(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    for index in range(21):
        _create_membership(
            company,
            f"empleado{index:02d}@example.com",
            display_name=f"Empleado {index:02d}",
        )

    client.force_login(owner_account.user)
    first = client.get("/users/")
    second = client.get("/users/?page=2")

    assert first.status_code == 200
    assert second.status_code == 200
    first_content = first.content.decode()
    second_content = second.content.decode()
    assert first_content.count('scope="row"') == 20
    assert second_content.count('scope="row"') == 2
    assert "Página 1 de 2" in first_content
    assert "Página 2 de 2" in second_content
    assert 'rel="next"' in first_content
    assert 'rel="prev"' in second_content
    assert 'aria-label="Paginación de usuarios"' in first_content


@pytest.mark.django_db
def test_user_list_handles_an_invalid_page_number(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/users/?page=no-es-un-numero")
    assert response.status_code == 200
    assert owner_account.email in response.content.decode()


@pytest.mark.django_db
def test_user_create_requires_login(client: object) -> None:
    response = client.get("/users/new/")
    assert response.status_code == 302
    assert response.url == "/login/?next=/users/new/"


@pytest.mark.django_db
def test_user_create_requires_the_management_capability(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    consulta = _create_membership(
        company,
        "consulta@example.com",
        role=Role.CONSULTA.value,
    )
    client.force_login(consulta.account.user)
    response = client.post(
        "/users/new/",
        {
            "email": "nuevo@example.com",
            "display_name": "Nuevo",
            "role": Role.OPERADOR.value,
        },
    )
    assert response.status_code == 403
    assert not Account.objects.filter(email="nuevo@example.com").exists()


@pytest.mark.django_db
def test_user_create_renders_the_form_without_the_owner_role(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.get("/users/new/")
    assert response.status_code == 200
    content = response.content.decode()
    assert "accounts/user_form.html" in [
        template.name for template in response.templates
    ]
    assert response["Cache-Control"] == "no-store"
    choices = [value for value, _ in response.context["form"].fields["role"].choices]
    assert Role.DUENO.value not in choices
    assert 'value="dueno"' not in content
    assert content.count("<h1") == 1


@pytest.mark.django_db
def test_user_create_creates_the_employee_and_shows_the_password_once(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    client.force_login(owner_account.user)
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(
            "/users/new/",
            {
                "email": "nuevo@example.com",
                "display_name": "Nueva Persona",
                "role": Role.ENCARGADO.value,
            },
        )

    assert response.status_code == 200
    content = response.content.decode()
    match = re.search(r"<code>([^<]+)</code>", content)
    assert match is not None
    temporary_password = match.group(1)
    assert content.count(temporary_password) == 1
    assert "Nueva Persona" in content

    membership = Membership.objects.select_related("account__user").get(
        account__email="nuevo@example.com"
    )
    assert membership.company == company
    assert membership.role == Role.ENCARGADO.value
    assert membership.is_active is True
    assert membership.must_change_password is True
    assert membership.account.user.check_password(temporary_password)

    event = AuditEvent.objects.get(action="membership.created")
    assert event.company == company
    assert event.actor == owner_account.user
    assert temporary_password not in str(event.before)
    assert temporary_password not in str(event.after)

    later = client.get("/users/new/").content.decode()
    assert temporary_password not in later


@pytest.mark.django_db
def test_user_create_rejects_a_duplicate_email(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    django_capture_on_commit_callbacks: object,
) -> None:
    _create_membership(company, "repetido@example.com")
    client.force_login(owner_account.user)
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(
            "/users/new/",
            {
                "email": "  Repetido@Example.COM ",
                "display_name": "Duplicado",
                "role": Role.OPERADOR.value,
            },
        )

    assert response.status_code == 400
    assert "email" in response.context["form"].errors
    content = response.content.decode()
    assert "El correo ya está registrado." in content
    assert 'aria-invalid="true"' in content
    assert 'aria-describedby="id_email-errors"' in content
    assert Account.objects.filter(email="repetido@example.com").count() == 1
    assert Membership.objects.filter(company=company).count() == 2
    assert AuditEvent.objects.filter(action="membership.created").count() == 0
    assert get_user_model().objects.count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize("role", [Role.DUENO.value, "administrador"])
def test_user_create_rejects_an_invalid_role(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
    role: str,
) -> None:
    client.force_login(owner_account.user)
    response = client.post(
        "/users/new/",
        {
            "email": "nuevo@example.com",
            "display_name": "Nuevo",
            "role": role,
        },
    )
    assert response.status_code == 400
    assert "role" in response.context["form"].errors
    assert not Account.objects.filter(email="nuevo@example.com").exists()


@pytest.mark.django_db
def test_user_create_normalizes_the_email(
    client: object,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)
    response = client.post(
        "/users/new/",
        {
            "email": "  Nueva.Persona@Example.COM ",
            "display_name": "Nueva Persona",
            "role": Role.OPERADOR.value,
        },
    )
    assert response.status_code == 200
    assert Account.objects.filter(email="nueva.persona@example.com").exists()


@pytest.mark.django_db
def test_user_create_rejects_an_injected_company(
    client: object,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    other_company = Company.objects.create(name="Otra empresa", is_active=False)
    client.force_login(owner_account.user)
    response = client.post(
        "/users/new/",
        {
            "email": "nuevo@example.com",
            "display_name": "Nuevo",
            "role": Role.OPERADOR.value,
            "company": str(other_company.pk),
        },
    )
    assert response.status_code == 404
    assert not Account.objects.filter(email="nuevo@example.com").exists()
    assert SecurityEvent.objects.filter(action="company.scope.injected").exists()
