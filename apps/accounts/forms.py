"""Formularios del panel comercial (T-15)."""

from __future__ import annotations

from django import forms

from .capabilities import Role
from .emails import clean_email


class EmployeeCreateForm(forms.Form):
    """Alta de empleado con correo, nombre y rol distinto de dueño."""

    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    display_name = forms.CharField(
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    role = forms.ChoiceField(label="Rol", choices=())

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            (role.value, role.label) for role in Role if role != Role.DUENO
        ]
        self.apply_error_attributes()

    def apply_error_attributes(self) -> None:
        """Asocia los errores de campo con su control para lectores de pantalla.

        Se vuelve a invocar tras ``add_error`` en la vista, porque los errores
        del servicio se agregan después de la validación del formulario.
        """

        for name in ("email", "display_name", "role"):
            field = self[name]
            if field.errors:
                self.fields[name].widget.attrs.update(
                    {
                        "aria-invalid": "true",
                        "aria-describedby": f"{field.auto_id}-errors",
                    }
                )

    def clean_email(self) -> str:
        return clean_email(self.cleaned_data["email"])
