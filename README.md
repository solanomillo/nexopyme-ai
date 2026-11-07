# NexoPyme AI

Plataforma de gestión empresarial para pequeños negocios: productos, inventario,
compras, ventas, clientes, finanzas básicas y reportes, con un asistente de IA
para apoyar las operaciones del negocio.

Este repositorio contiene el **Bootstrap 000**: entorno local reproducible,
configuración Django, MySQL 8.x, migraciones iniciales, suite de pruebas y
endpoint de salud. El MVP de negocio todavía no está implementado.

## Estado del Bootstrap 000

- Especificación 000 v1.4 aprobada.
- T-01–T-13 completadas; Bootstrap 000 cerrado documentalmente.
- Sin módulos de negocio, agentes de IA, checkpointer ni despliegue remoto.
- V1 local, sin microservicios, Redis, RAG ni bases vectoriales.

## Versiones verificadas

- Python 3.14.10 (Windows 10 x64; Windows 11 no se probó independientemente).
- Django 6.0.9.
- mysqlclient 2.3.0.
- pytest 9.2.0 y pytest-django 4.14.0.
- Ruff 0.17.4.
- Pydantic 2.14.3.
- LangChain 1.4.9, LangGraph 1.2.20 y `langchain-deepseek` 1.1.1.
- MySQL 8.0.36.

La evidencia detallada de resolución, metadata y ejecución está en
`specs/000-project-bootstrap/tasks.md` y `plan.md`.

## Requisitos

- Python 3.14.10.
- MySQL 8.0.x local; el servidor autorizado es 8.0.36 en `127.0.0.1:3306`.
- Git.

## Instalación

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

## Variables de entorno

`.env` **no se carga automáticamente**: exportá las variables en el proceso
antes de ejecutar `manage.py` o pytest. `.env` está excluido por Git;
`.env.example` solo contiene nombres y placeholders no utilizables.

Variables obligatorias:

- `DJANGO_SECRET_KEY`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

Variables opcionales:

- `DJANGO_DEBUG` (por defecto `False`)
- `DJANGO_ALLOWED_HOSTS` (por defecto vacío; para local usar
  `127.0.0.1,localhost`)

Variables de pruebas:

- `MYSQL_TEST_USER`
- `MYSQL_TEST_PASSWORD`

No se deben commitear credenciales ni valores reales.

## Base de datos y migraciones

- Desarrollo: `nexopyme_bootstrap_dev`.
- Pruebas: `nexopyme_bootstrap_test` (la crea y elimina pytest).
- No se usa SQLite como base operativa.

Comandos:

```powershell
python manage.py migrate
python manage.py migrate --check
```

Las migraciones iniciales aplicadas son las de `contenttypes`, `auth`, `admin`
y `sessions` (18 en total). El detalle está en `plan.md` y `tasks.md`.

## Pruebas y calidad

```powershell
python -m pytest
python -m ruff check .
```

- pytest usa `config.settings_test` y la base `nexopyme_bootstrap_test`.
- `config/settings_test.py` y `conftest.py` bloquean el uso de la base de
  desarrollo, `TEST.MIRROR`, el paralelismo, `--no-migrations`, `--reuse-db` y
  `--create-db`.
- La suite de T-10 verificó que la conexión apunta a `nexopyme_bootstrap_test`
  y que la base se elimina al finalizar.
- No se autoriza `manage.py test` como vía de pruebas.

## Endpoint de salud

```powershell
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:DJANGO_DEBUG = "False"
python manage.py runserver 127.0.0.1:8000
curl -i http://127.0.0.1:8000/health/
```

`GET /health/` responde HTTP 200, `Content-Type: text/plain` y cuerpo `ok`, sin
lógica de negocio ni llamadas a IA. La validación de T-12 se realizó con
`wsgiref.simple_server` en lugar de `runserver` porque `runserver` ejecuta
`check_migrations()` y habría abierto una conexión MySQL, prohibida en esa
validación. Ver `plan.md` y `tasks.md`.

## Evidencias y limitaciones

- Evidencia de ejecución en `specs/000-project-bootstrap/plan.md` y
  `tasks.md`: preflight MySQL, migraciones, `migrate --check`, pytest, Ruff y
  endpoint.
- Windows 10 x64 es el entorno efectivamente verificado. Windows 11 no se probó
  independientemente y no se afirma compatibilidad universal.
- pytest reportó 13 warnings de `langsmith`
  (`DeprecationWarning: asyncio.iscoroutinefunction`), no bloqueantes y sin
  relación con Django/MySQL.
- `specs/001-productos-inventario/` está fuera de este bootstrap y no se
  modifica.

## Documentación

- `CONSTITUTION.md`: principios aprobados.
- `AGENTS.md`: instrucciones de trabajo.
- `specs/000-project-bootstrap/spec.md`: especificación v1.4.
- `specs/000-project-bootstrap/plan.md`: plan técnico y evidencias.
- `specs/000-project-bootstrap/tasks.md`: tareas, trazabilidad y checklist.
