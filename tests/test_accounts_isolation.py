"""Pruebas de aislamiento entre empresas (T-21).

La segunda empresa se crea por ORM, fuera de los servicios de negocio, y
permanece inactiva. Cada vista y cada servicio de la etapa tiene al menos un
caso de acceso cruzado.
"""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from apps.accounts.capabilities import Role
from apps.accounts.models import (
    Account,
    Company,
    Membership,
    generate_username,
)
from apps.accounts.services import (
    CrossCompanyError,
    change_role,
    create_employee,
    deactivate_membership,
    reactivate_membership,
    regenerate_temporary_password,
)
from apps.audit.models import AuditEvent, SecurityEvent

pytestmark = pytest.mark.django_db

TEST_PASSWORD = "Clave-Segura-2026"


def _create_membership(
    company: Company,
    email: str,
    role: str = Role.OPERADOR.value,
    *,
    is_active: bool = True,
) -> Membership:
    user = get_user_model().objects.create_user(
        username=generate_username(),
        password=TEST_PASSWORD,
    )
    account = Account.objects.create(
        user=user,
        email=email,
        display_name=f"Persona {email}",
    )
    return Membership.objects.create(
        account=account,
        company=company,
        role=role,
        is_active=is_active,
    )


def _create_audit(
    company: Company,
    action: str,
    actor: object,
) -> AuditEvent:
    return AuditEvent.objects.create(
        actor=actor,
        company=company,
        entity="Membership",
        entity_id="1",
        action=action,
        result="success",
    )


def _create_security(
    company: Company,
    action: str,
    actor: object,
) -> SecurityEvent:
    return SecurityEvent.objects.create(
        actor=actor,
        company=company,
        action=action,
        result="denied",
    )


def test_second_company_is_inactive_and_built_outside_services(
    foreign_company: Company,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    assert foreign_company.is_active is False
    assert foreign_membership.company == foreign_company
    assert foreign_membership.account == foreign_account
    assert not AuditEvent.objects.filter(company=foreign_company).exists()


def test_user_with_only_foreign_membership_is_denied(
    client: Client,
    foreign_company: Company,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    client.force_login(foreign_account.user)

    response = client.get("/panel/")

    assert response.status_code == 403
    content = response.content.decode()
    assert foreign_company.name not in content
    assert foreign_account.email not in content


def test_panel_resolves_the_company_from_the_session(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
    foreign_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    response = client.get("/panel/")

    assert response.status_code == 200
    content = response.content.decode()
    assert company.name in content
    assert foreign_company.name not in content


def test_panel_resolves_the_context_once_per_request(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    django_assert_num_queries: object,
) -> None:
    client.force_login(owner_account.user)

    # Sesión, usuario y membresía con select_related: una sola resolución.
    with django_assert_num_queries(3):
        response = client.get("/panel/")

    assert response.status_code == 200


def test_profile_redirects_to_the_own_account(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    response = client.get("/profile/")

    assert response.status_code == 302
    assert response.url == f"/profile/{owner_account.pk}/"


def test_profile_of_a_foreign_account_is_uniform_404(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    foreign = client.get(f"/profile/{foreign_account.pk}/")
    missing = client.get("/profile/999999/")

    assert foreign.status_code == 404
    assert missing.status_code == 404
    assert foreign.content == missing.content
    content = foreign.content.decode()
    assert foreign_account.email not in content
    assert foreign_account.display_name not in content
    assert SecurityEvent.objects.filter(action="company.scope.foreign").exists()


def test_user_list_excludes_foreign_memberships(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    employee = _create_membership(company, "propio@example.com")
    client.force_login(owner_account.user)

    response = client.get("/users/")

    assert response.status_code == 200
    content = response.content.decode()
    assert employee.account.display_name in content
    assert foreign_account.display_name not in content
    assert foreign_account.email not in content
    assert response.context["page_obj"].paginator.count == 2


def test_user_list_accepts_out_of_range_pages(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
) -> None:
    for index in range(21):
        _create_membership(company, f"empleado{index:02d}@example.com")
    client.force_login(owner_account.user)

    below = client.get("/users/?page=0")
    above = client.get("/users/?page=999")

    assert below.status_code == 200
    assert above.status_code == 200
    # Django mapea páginas fuera de rango a la última página válida.
    assert below.context["page_obj"].paginator.num_pages == 2
    assert below.context["page_obj"].number == 2
    assert above.context["page_obj"].number == 2


def test_user_list_ignores_a_client_company_id(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    response = client.get(f"/users/?company_id={foreign_company.pk}")

    assert response.status_code == 200
    content = response.content.decode()
    assert company.name in content
    assert foreign_account.email not in content


def test_user_list_rejects_an_injected_company(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
) -> None:
    client.force_login(owner_account.user)

    response = client.get(f"/users/?company={foreign_company.pk}")

    assert response.status_code == 404
    event = SecurityEvent.objects.get(action="company.scope.injected")
    assert event.attempted_company_id == foreign_company.pk
    assert event.company == owner_membership.company


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/users/{pk}/role/", {"role": Role.CONSULTA.value}),
        ("/users/{pk}/deactivate/", {}),
        ("/users/{pk}/reactivate/", {}),
        ("/users/{pk}/password/", {}),
    ],
)
def test_user_actions_reject_a_foreign_membership(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    foreign_membership: Membership,
    path: str,
    payload: dict[str, str],
) -> None:
    password_before = foreign_membership.account.user.password
    active_before = foreign_membership.is_active
    client.force_login(owner_account.user)

    response = client.post(path.format(pk=foreign_membership.pk), payload)

    assert response.status_code == 404
    foreign_membership.refresh_from_db()
    foreign_membership.account.user.refresh_from_db()
    assert foreign_membership.role == Role.DUENO.value
    assert foreign_membership.is_active is active_before
    assert foreign_membership.must_change_password is False
    assert foreign_membership.account.user.password == password_before
    assert SecurityEvent.objects.filter(action="company.scope.foreign").exists()


def test_user_create_cannot_link_a_foreign_email(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    client.force_login(owner_account.user)

    response = client.post(
        "/users/new/",
        {
            "email": foreign_account.email,
            "display_name": "Intento ajeno",
            "role": Role.OPERADOR.value,
        },
    )

    assert response.status_code == 400
    assert "ya está registrado" in response.content.decode()
    assert not Membership.objects.filter(
        company=company,
        account=foreign_account,
    ).exists()
    assert Membership.objects.filter(company=foreign_membership.company).count() == 1


def test_create_employee_uses_the_actor_company(
    owner_membership: Membership,
    foreign_membership: Membership,
) -> None:
    employee, _ = create_employee(
        actor=owner_membership,
        email="nuevo@example.com",
        display_name="Nuevo",
        role=Role.OPERADOR.value,
    )

    assert employee.company == owner_membership.company
    assert employee.company != foreign_membership.company


def test_company_edit_rejects_an_injected_foreign_company(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
) -> None:
    client.force_login(owner_account.user)

    response = client.post(
        "/company/",
        {"name": "Nombre ajeno", "company": str(foreign_company.pk)},
    )

    assert response.status_code == 404
    company.refresh_from_db()
    foreign_company.refresh_from_db()
    assert company.name == "Almacén Central"
    assert foreign_company.name == "Empresa Ajena"
    assert SecurityEvent.objects.filter(action="company.scope.injected").exists()


def test_password_change_rejects_an_injected_company(
    client: Client,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
) -> None:
    client.force_login(owner_account.user)

    response = client.get(f"/password/?company={foreign_company.pk}")

    assert response.status_code == 404
    assert SecurityEvent.objects.filter(action="company.scope.injected").exists()


def test_audit_list_excludes_foreign_events(
    client: Client,
    company: Company,
    owner_account: Account,
    owner_membership: Membership,
    foreign_company: Company,
    foreign_account: Account,
    foreign_membership: Membership,
) -> None:
    _create_audit(company, "own.audit", owner_account.user)
    _create_audit(foreign_company, "foreign.audit", foreign_account.user)
    _create_security(company, "own.security", owner_account.user)
    _create_security(foreign_company, "foreign.security", foreign_account.user)
    client.force_login(owner_account.user)

    content = client.get("/audit/").content.decode()

    assert "own.audit" in content
    assert "own.security" in content
    assert "foreign.audit" not in content
    assert "foreign.security" not in content


@pytest.mark.parametrize(
    "operation",
    [
        "change_role",
        "deactivate",
        "reactivate",
        "regenerate",
    ],
)
def test_services_reject_cross_company_mutations(
    owner_membership: Membership,
    foreign_membership: Membership,
    operation: str,
) -> None:
    foreign_membership.is_active = False
    foreign_membership.save(update_fields=["is_active", "updated_at"])
    password_before = foreign_membership.account.user.password

    with pytest.raises(CrossCompanyError):
        if operation == "change_role":
            change_role(
                actor=owner_membership,
                membership=foreign_membership,
                role=Role.CONSULTA.value,
            )
        elif operation == "deactivate":
            deactivate_membership(
                actor=owner_membership,
                membership=foreign_membership,
            )
        elif operation == "reactivate":
            reactivate_membership(
                actor=owner_membership,
                membership=foreign_membership,
            )
        else:
            regenerate_temporary_password(
                actor=owner_membership,
                membership=foreign_membership,
            )

    foreign_membership.refresh_from_db()
    foreign_membership.account.user.refresh_from_db()
    assert foreign_membership.role == Role.DUENO.value
    assert foreign_membership.is_active is False
    assert foreign_membership.account.user.password == password_before
    event = SecurityEvent.objects.get(action="company.scope.foreign")
    assert event.actor == owner_membership.account.user
    assert event.company == owner_membership.company
    assert event.attempted_company_id is None


def test_services_check_isolation_before_capability(
    company: Company,
    owner_membership: Membership,
    foreign_membership: Membership,
) -> None:
    consulta = _create_membership(
        company,
        "consulta-servicio@example.com",
        Role.CONSULTA.value,
    )
    password_before = foreign_membership.account.user.password

    with pytest.raises(CrossCompanyError):
        deactivate_membership(
            actor=consulta,
            membership=foreign_membership,
        )

    foreign_membership.refresh_from_db()
    foreign_membership.account.user.refresh_from_db()
    assert foreign_membership.is_active is True
    assert foreign_membership.account.user.password == password_before
    assert SecurityEvent.objects.filter(action="company.scope.foreign").exists()
