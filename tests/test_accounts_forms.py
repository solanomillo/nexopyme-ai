"""Pruebas DB-free de los formularios del panel (T-15)."""

from __future__ import annotations

from apps.accounts.capabilities import Role
from apps.accounts.forms import EmployeeCreateForm


def test_role_choices_exclude_the_owner() -> None:
    form = EmployeeCreateForm()
    values = [value for value, _ in form.fields["role"].choices]
    assert Role.DUENO.value not in values
    assert set(values) == {
        Role.ENCARGADO.value,
        Role.OPERADOR.value,
        Role.CONSULTA.value,
    }


def test_valid_form_normalizes_the_email_and_name() -> None:
    form = EmployeeCreateForm(
        data={
            "email": "  Empleado@Example.COM ",
            "display_name": "  Ana  ",
            "role": Role.OPERADOR.value,
        }
    )
    assert form.is_valid()
    assert form.cleaned_data["email"] == "empleado@example.com"
    assert form.cleaned_data["display_name"] == "Ana"


def test_invalid_email_is_rejected() -> None:
    form = EmployeeCreateForm(
        data={
            "email": "no-es-correo",
            "display_name": "Ana",
            "role": Role.OPERADOR.value,
        }
    )
    assert not form.is_valid()
    assert "email" in form.errors


def test_owner_role_is_rejected() -> None:
    form = EmployeeCreateForm(
        data={
            "email": "ana@example.com",
            "display_name": "Ana",
            "role": Role.DUENO.value,
        }
    )
    assert not form.is_valid()
    assert "role" in form.errors


def test_unknown_role_is_rejected() -> None:
    form = EmployeeCreateForm(
        data={
            "email": "ana@example.com",
            "display_name": "Ana",
            "role": "administrador",
        }
    )
    assert not form.is_valid()
    assert "role" in form.errors


def test_display_name_is_required() -> None:
    form = EmployeeCreateForm(
        data={
            "email": "ana@example.com",
            "display_name": "   ",
            "role": Role.OPERADOR.value,
        }
    )
    assert not form.is_valid()
    assert "display_name" in form.errors


def test_field_errors_are_associated_with_the_control() -> None:
    form = EmployeeCreateForm(data={"email": "", "display_name": "", "role": ""})
    assert not form.is_valid()
    rendered = str(form["email"])
    assert 'aria-invalid="true"' in rendered
    assert 'aria-describedby="id_email-errors"' in rendered
