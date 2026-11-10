"""Catálogo único de roles y capacidades de NexoPyme AI.

Los nombres de capacidad son vinculantes y coinciden con la especificación
003 §4.3 y con `specs/002-productos-inventario/spec.md` §4.3. Cualquier módulo
futuro consume este catálogo y no redefine roles ni capacidades.
"""

from __future__ import annotations

from enum import StrEnum

from django.db import models


class Role(models.TextChoices):
    """Roles fijos de la V1."""

    DUENO = "dueno", "Dueño"
    ENCARGADO = "encargado", "Encargado"
    OPERADOR = "operador", "Operador"
    CONSULTA = "consulta", "Consulta"


class Capability(StrEnum):
    """Capacidades autorizables con el patrón ``recurso.accion``."""

    PRODUCTO_CONSULTAR = "producto.consultar"
    HISTORIAL_CONSULTAR = "historial.consultar"
    PRODUCTO_CREAR = "producto.crear"
    PRODUCTO_EDITAR = "producto.editar"
    PRODUCTO_DESACTIVAR = "producto.desactivar"
    MOVIMIENTO_ENTRADA = "movimiento.entrada"
    MOVIMIENTO_SALIDA = "movimiento.salida"
    MOVIMIENTO_AJUSTAR = "movimiento.ajustar"
    EXISTENCIA_INICIALIZAR = "existencia.inicializar"
    AUDITORIA_CONSULTAR = "auditoria.consultar"
    USUARIOS_GESTIONAR = "usuarios.gestionar"
    EMPRESA_CONFIGURAR = "empresa.configurar"


_CAPACIDADES_LECTURA = frozenset(
    {
        Capability.PRODUCTO_CONSULTAR,
        Capability.HISTORIAL_CONSULTAR,
    }
)

ROLE_CAPABILITIES: dict[str, frozenset[Capability]] = {
    Role.DUENO.value: frozenset(Capability),
    Role.ENCARGADO.value: _CAPACIDADES_LECTURA
    | frozenset(
        {
            Capability.PRODUCTO_CREAR,
            Capability.PRODUCTO_EDITAR,
            Capability.PRODUCTO_DESACTIVAR,
            Capability.MOVIMIENTO_ENTRADA,
            Capability.MOVIMIENTO_SALIDA,
            Capability.MOVIMIENTO_AJUSTAR,
            Capability.EXISTENCIA_INICIALIZAR,
        }
    ),
    Role.OPERADOR.value: _CAPACIDADES_LECTURA
    | frozenset(
        {
            Capability.MOVIMIENTO_ENTRADA,
            Capability.MOVIMIENTO_SALIDA,
        }
    ),
    Role.CONSULTA.value: _CAPACIDADES_LECTURA,
}


def has_capability(actor_role: object, capability: object) -> bool:
    """Devuelve si el rol indicado posee la capacidad solicitada.

    El defecto es denegar: un rol o una capacidad desconocidos devuelven
    ``False``. Acepta un valor de rol o un objeto con atributo ``role``.
    """

    role = getattr(actor_role, "role", actor_role)
    try:
        normalized_role = Role(role)
        normalized_capability = Capability(capability)
    except (TypeError, ValueError):
        return False
    return normalized_capability in ROLE_CAPABILITIES[normalized_role.value]
