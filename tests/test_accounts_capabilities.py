"""Pruebas DB-free del catálogo de roles y capacidades (T-02)."""

from __future__ import annotations

import ast
from pathlib import Path

from django.conf import settings

from apps.accounts.capabilities import (
    ROLE_CAPABILITIES,
    Capability,
    Role,
    has_capability,
)

EXPECTED_MATRIX: dict[str, set[str]] = {
    Role.DUENO.value: {capability.value for capability in Capability},
    Role.ENCARGADO.value: {
        "producto.consultar",
        "historial.consultar",
        "producto.crear",
        "producto.editar",
        "producto.desactivar",
        "movimiento.entrada",
        "movimiento.salida",
        "movimiento.ajustar",
        "existencia.inicializar",
    },
    Role.OPERADOR.value: {
        "producto.consultar",
        "historial.consultar",
        "movimiento.entrada",
        "movimiento.salida",
    },
    Role.CONSULTA.value: {
        "producto.consultar",
        "historial.consultar",
    },
}

EXPECTED_CAPABILITIES = {
    "producto.consultar",
    "historial.consultar",
    "producto.crear",
    "producto.editar",
    "producto.desactivar",
    "movimiento.entrada",
    "movimiento.salida",
    "movimiento.ajustar",
    "existencia.inicializar",
    "auditoria.consultar",
    "usuarios.gestionar",
    "empresa.configurar",
}


def test_roles_are_the_four_approved_ones() -> None:
    assert {role.value for role in Role} == {
        "dueno",
        "encargado",
        "operador",
        "consulta",
    }


def test_capability_catalog_matches_the_specification() -> None:
    assert {capability.value for capability in Capability} == EXPECTED_CAPABILITIES


def test_role_capability_matrix_matches_the_specification() -> None:
    assert set(ROLE_CAPABILITIES) == {role.value for role in Role}
    for role, expected in EXPECTED_MATRIX.items():
        actual = {capability.value for capability in ROLE_CAPABILITIES[role]}
        assert actual == expected, f"Matriz incorrecta para {role}"


def test_owner_has_every_capability() -> None:
    assert all(has_capability(Role.DUENO, capability) for capability in Capability)


def test_operator_cannot_adjust_or_initialize_stock() -> None:
    assert has_capability(Role.OPERADOR, Capability.MOVIMIENTO_ENTRADA)
    assert not has_capability(Role.OPERADOR, Capability.MOVIMIENTO_AJUSTAR)
    assert not has_capability(Role.OPERADOR, Capability.EXISTENCIA_INICIALIZAR)


def test_consulta_role_is_read_only() -> None:
    assert has_capability(Role.CONSULTA, Capability.PRODUCTO_CONSULTAR)
    assert has_capability(Role.CONSULTA, Capability.HISTORIAL_CONSULTAR)
    assert not has_capability(Role.CONSULTA, Capability.PRODUCTO_CREAR)
    assert not has_capability(Role.CONSULTA, Capability.MOVIMIENTO_ENTRADA)


def test_unknown_role_or_capability_is_denied() -> None:
    assert not has_capability("administrador", Capability.PRODUCTO_CONSULTAR)
    assert not has_capability(None, Capability.PRODUCTO_CONSULTAR)
    assert not has_capability(Role.DUENO, "producto.borrar")
    assert not has_capability(Role.DUENO, None)


def test_has_capability_accepts_an_object_with_role_attribute() -> None:
    class Actor:
        role = Role.ENCARGADO.value

    assert has_capability(Actor(), Capability.PRODUCTO_CREAR)
    assert not has_capability(Actor(), Capability.USUARIOS_GESTIONAR)


def test_capability_catalog_is_defined_only_once() -> None:
    """CA-20: no existe otra definición de roles ni capacidades en apps/."""

    apps_dir = Path(settings.BASE_DIR) / "apps"
    allowed = apps_dir / "accounts" / "capabilities.py"
    offenders: list[str] = []
    for path in apps_dir.rglob("*.py"):
        if path == allowed:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in {"Role", "Capability"}:
                offenders.append(f"{path}: class {node.name}")
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "ROLE_CAPABILITIES"
                    ):
                        offenders.append(f"{path}: ROLE_CAPABILITIES")
    assert offenders == []
