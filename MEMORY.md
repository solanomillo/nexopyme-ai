# MEMORY.md — NexoPyme AI

## Estado
- Proyecto: NexoPyme AI, gestión empresarial para pequeños negocios con IA.
- Bootstrap 000: T-01–T-13 completadas; cerrado documentalmente; MVP no implementado.
- Etapa 001: CERRADA; T-01–T-18 completadas, aprobadas y publicadas el 2026-11-10.
- Etapa 003: CERRADA; T-01–T-26 completadas y aprobadas el 2026-11-12.
- Constitución: `CONSTITUTION.md` existe y está aprobada.
- Base operativa: MySQL 8.0.36; `nexopyme_bootstrap_dev` y `nexopyme_bootstrap_test`.

## Stack
- Python 3.14.10, Django 6.0.9, mysqlclient 2.3.0; Django Templates, HTML, CSS y JavaScript.
- django-unfold 0.110.1 y python-dotenv 1.2.4.
- LangChain 1.4.9, LangGraph 1.2.20 y `langchain-deepseek` 1.1.1.
- Pydantic 2.14.3, pytest 9.2.0, pytest-django 4.14.0 y Ruff 0.17.4.
- DeepSeek mediante adaptador desacoplado.

## Decisiones vigentes
- Interfaz en español por defecto; V1 local sin despliegue remoto.
- Agentes sin acceso directo a la BD; operaciones de IA con confirmación humana previa.
- Aislamiento entre empresas sin excepciones.
- SQLite solo para un futuro checkpointer LangGraph; nunca datos operativos.

## Documentación
- Jerarquía: `CONSTITUTION.md` → `AGENTS.md` → spec → plan/tareas.
- `MEMORY.md` es descriptivo y no normativo.
- Spec 000 v1.4, spec 001 v1.1 y spec 003 v1.0 aprobadas.
- Etapa 003: plan v1.4 y tasks v1.7 con T-26 cerrada; `docs/README.md` documenta la etapa.
- `specs/002-productos-inventario/` está renumerada, sin aprobar ni implementar.

## Metodología
- SDD; Build coordina, Planner planifica, Implementer desarrolla, Reviewer revisa.
- El usuario autoriza especificación, plan e implementación.
- Engram conectado a OpenCode mediante MCP.

## Avances y próximos pasos
- Etapa 003 cerrada: 337 pruebas (36 DB-free + 301 con base) y Ruff en verde.
- Commits de cierre: T-24 `6d70e7e`, T-25 `3611f7c`, T-26 (este commit).
- Limitaciones: BOM aceptado en `6d70e7e` sin reescribir historial; suite en un solo proceso; deuda de `ruff format`; `/favicon.ico` en Admin.
- Próximo: la Etapa 004 requiere especificación y aprobación humanas; no iniciada.
