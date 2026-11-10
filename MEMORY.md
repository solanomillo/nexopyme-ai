# MEMORY.md — NexoPyme AI

## Estado
- Proyecto: NexoPyme AI, gestión empresarial para pequeños negocios con IA.
- Bootstrap 000: T-01–T-13 completadas; cerrado documentalmente; MVP no implementado.
- Etapa 001: CERRADA; T-01–T-18 completadas, aprobadas y publicadas el 2026-11-10.
- Constitución: `CONSTITUTION.md` existe y está aprobada.
- Base operativa: MySQL 8.0.36; `nexopyme_bootstrap_dev` (desarrollo) y `nexopyme_bootstrap_test` (pruebas, creada/eliminada por pytest).

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
- Spec 000 v1.4 aprobada; plan y tareas aprobados y versionados.
- Spec 001 v1.1 aprobada; plan y tareas v1.6 con T-17 APROBADO.
- `specs/002-productos-inventario/` está renumerada, sin aprobar ni implementar.

## Metodología
- SDD; Build coordina, Planner planifica, Implementer desarrolla, Reviewer revisa.
- El usuario autoriza especificación, plan e implementación.
- Engram conectado a OpenCode mediante MCP.

## Avances y próximos pasos
- RC-3, RC-4 y T-17 aprobados; suite DB-free 20 passed y `ruff check .` verde.
- Commits de la etapa: T-13 `a886e05`, T-16 `b37c164`, T-15 `5b25e03`, T-17 `b8017a6`.
- Limitaciones: suite completa NO EJECUTADA; deuda de `ruff format --check .`; `/favicon.ico` en Admin fuera de alcance.
- Próximo: esperar autorización del usuario para una nueva etapa.
