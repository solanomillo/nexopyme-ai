# MEMORY.md — NexoPyme AI

## Estado
- Proyecto: NexoPyme AI, gestión empresarial para pequeños negocios con IA.
- Bootstrap 000: T-01–T-13 completadas; cerrado documentalmente; MVP no implementado.
- Constitución: `CONSTITUTION.md` existe y está aprobada.
- Base operativa: MySQL 8.0.36; dos bases separadas: `nexopyme_bootstrap_dev` (desarrollo) y `nexopyme_bootstrap_test` (pruebas, creada/eliminada por pytest).

## Stack
- Python 3.14.10, Django 6.0.9, mysqlclient 2.3.0.
- Django Templates, HTML, CSS y JavaScript.
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
- Spec 000 v1.4 aprobada; plan y tareas aprobados.
- `specs/001-productos-inventario/` está en borrador y fuera del Bootstrap 000.

## Metodología
- SDD; Build coordina, Planner planifica, Implementer desarrolla, Reviewer revisa.
- El usuario autoriza especificación, plan e implementación.

## Memoria
- Engram conectado a OpenCode mediante MCP.

## Avances y próximos pasos
- T-01–T-12 completadas; pytest 2/2, Ruff verde, `/health/` 200.
- Bootstrap 000 cerrado documentalmente; no iniciar producto sin autorización.
