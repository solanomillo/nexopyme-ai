# NexoPyme AI

Plataforma de gestión empresarial para pequeños negocios: productos, inventario,
compras, ventas, clientes, finanzas básicas y reportes, con un asistente de IA
para apoyar las operaciones del negocio.

Este repositorio contiene el **Bootstrap 000** cerrado y la **Etapa 001 — Django
Project Foundation** en implementación. La etapa 001 establece la estructura
Django, el Admin con Django Unfold, la fundación visual propia y las pruebas
DB-free. El MVP de negocio todavía no está implementado.

## Estado actual

- Bootstrap 000: cerrado documentalmente; T-01–T-13 completadas.
- Etapa 001: T-01–T-16 completadas; T-13–T-16 aprobadas en RC-4 (2026-11-10); T-17 y T-18 pendientes.
- Sin módulos de negocio, agentes de IA, checkpointer ni despliegue remoto.
- V1 local, sin microservicios, Redis, RAG ni bases vectoriales.

## Versiones verificadas

- Python 3.14.10 (Windows 10 x64; Windows 11 no se probó independientemente).
- Django 6.0.9.
- mysqlclient 2.3.0.
- django-unfold 0.110.1.
- python-dotenv 1.2.4.
- pytest 9.2.0 y pytest-django 4.14.0.
- Ruff 0.17.4.
- Pydantic 2.14.3.
- LangChain 1.4.9, LangGraph 1.2.20 y `langchain-deepseek` 1.1.1.
- MySQL 8.0.36.

La evidencia detallada del Bootstrap 000 está en
`specs/000-project-bootstrap/tasks.md` y `plan.md`. La evidencia de la Etapa 001
está en `specs/001-django-project-foundation/tasks.md` y `plan.md`.

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

`.env` **se carga automáticamente** al iniciar `config.settings` mediante
`python-dotenv` y `load_dotenv(BASE_DIR / ".env", override=False)`. Las variables
ya exportadas en el proceso tienen prioridad sobre `.env`. El archivo `.env`
está excluido por Git y no se versiona; `.env.example` solo contiene nombres y
placeholders vacíos.

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

No se deben commitear credenciales ni valores reales. `DJANGO_SECRET_KEY` local
se provee fuera de Git, mediante `.env` o el entorno del proceso.

## Base de datos y migraciones

- Desarrollo: `nexopyme_bootstrap_dev` en `127.0.0.1:3306`.
- Pruebas: `nexopyme_bootstrap_test` (la crea y elimina pytest).
- No se usa SQLite como base operativa.
- No se ejecutan migraciones reales sin justificación y autorización.

Comandos de comprobación:

```powershell
python manage.py migrate --check
```

Resultado registrado en T-10: sin migraciones pendientes (exit 0). Las 18
migraciones iniciales son del Bootstrap 000 (2026-11-07). El `migrate` accidental
del 2026-11-09 fue un no-op y no se revirtió ni repitió.

## Ejecución local

Para desarrollo local, `DJANGO_DEBUG=True` permite que `runserver` sirva los
estáticos. El default del repositorio permanece `False`.

```powershell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
python manage.py runserver 127.0.0.1:8000
```

Rutas principales:

- `http://127.0.0.1:8000/` — portada informativa.
- `http://127.0.0.1:8000/health/` — salud, HTTP 200 `ok`.
- `http://127.0.0.1:8000/admin/` — Django Admin con Unfold.

La validación de T-12 se realizó con `runserver` contra
`nexopyme_bootstrap_dev` y sesión de superusuario. No se accedió a
`nexopyme_bootstrap_test`.

## Admin y Unfold

- `django-unfold==0.110.1` está declarado en `requirements.txt`.
- `"unfold"` se declara antes de `"django.contrib.admin"` en `INSTALLED_APPS`.
- `UNFOLD` define `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER` y `SITE_URL`.
- `User` y `Group` se re-registran en `apps/core/admin.py` con
  `unfold.admin.ModelAdmin` y los formularios de `unfold.forms`.
- No se usan módulos `unfold.contrib.*` ni se personalizan plantillas del Admin.
- La interfaz está en español de Argentina (`LANGUAGE_CODE=es-ar`, zona horaria
  `America/Argentina/Buenos_Aires`). El catálogo mínimo
  `locale/es_AR/LC_MESSAGES/django.po|.mo` traduce el mensaje de logout de Unfold.

### Superusuario local

Creación interactiva, sin contraseña en argumentos ni variables versionadas:

```powershell
python manage.py createsuperuser
```

Recuperación:

```powershell
python manage.py changepassword <usuario>
```

Si se perdió el acceso, se puede crear otro superusuario con `createsuperuser` o
usar `python manage.py shell` de forma interactiva para marcar `is_staff` e
`is_superuser` y ejecutar `set_password()`, sin escribir la contraseña en el
comando. No se elimina ni recrea la base para recuperar acceso.

La identidad, el correo y la contraseña del superusuario no se registran en
documentación, capturas ni evidencias.

## Frontend propio

- `templates/base.html`: HTML5, `lang="es"`, viewport, metadatos, skip link,
  navbar, `main`, footer y carga de `static/css/main.css`.
- `templates/components/navbar.html`: marca, Inicio y Administración.
- `templates/components/footer.html`: identidad, etapa y año.
- `templates/home.html`: portada informativa, un solo `h1`, enlace a
  Administración y próximos pasos marcados como pendientes.
- `static/css/main.css`: tokens, reset mínimo, layout, componentes, responsive,
  foco visible y `prefers-reduced-motion`.
- `static/img/favicon.svg`: icono propio en SVG con la paleta teal, enlazado
  desde `templates/base.html` con `rel="icon"`.

El frontend propio no usa assets de Unfold y el Admin no usa `main.css`. No se
incorporaron frameworks ni dependencias frontend adicionales. La portada no
muestra datos ficticios ni métricas inventadas.

## Pruebas y calidad

La suite completa de pytest está **NO EJECUTADA** porque usaría
`nexopyme_bootstrap_test`, base prohibida en esta etapa. La estrategia aprobada
son pruebas DB-free sobre cinco archivos concretos:

```powershell
python -m pytest tests/test_project_structure.py tests/test_settings_foundation.py tests/test_home_view.py tests/test_urls.py tests/test_admin_unfold.py
```

Resultado registrado en T-13: **20 passed**, sin `django_db_setup` ni fixtures de
base de datos. `pytest --setup-show` con la misma lista no mostró fixtures de
base. `tests/test_db_guards.py` no se modificó y su prueba con `django_db` quedó
**NO EJECUTADA**.

Calidad estática:

```powershell
ruff check .
```

Resultado registrado en T-14: **All checks passed**. `ruff format --check .`
señala únicamente deuda de formato preexistente del Bootstrap 000 en
`config/settings.py` y `config/settings_test.py`; no se reformateó fuera de
alcance.

## Estructura

```text
apps/
├── __init__.py
└── core/                  # Infraestructura, sin modelos ni migraciones
    ├── __init__.py
    ├── admin.py           # Re-registro Unfold de User/Group
    └── apps.py
config/                    # settings, urls, views, wsgi/asgi
docs/                      # Documentación de la etapa
locale/es_AR/LC_MESSAGES/  # Catálogo mínimo del logout
specs/                     # Especificaciones, planes y tareas
static/css/main.css        # Fundación visual propia
static/img/favicon.svg     # Icono propio (rel="icon")
templates/                 # base, home y componentes
tests/                     # Pruebas DB-free y guardas existentes
```

## Validación visual T-16

La validación visual fue **aprobada explícitamente por el usuario** el 2026-11-10
tras la batería automatizada en 320, 375, 768, 1440 y 1920 px. El checklist, las
URLs y los pasos están en
[`docs/README.md`](docs/README.md#validación-visual-t-16). CA-13 queda en PASS.

## Criterios de aceptación

La tabla `CA-01…CA-18` con el comando, resultado o `NO EJECUTADO` de cada
criterio está en
[`docs/README.md`](docs/README.md#criterios-de-aceptación). Resumen: 17 criterios
con evidencia registrada y CA-13 aprobado por el usuario; CA-16 corresponde a la
suite completa `NO EJECUTADA`.

## Evidencias y limitaciones

- Evidencia del Bootstrap 000 en `specs/000-project-bootstrap/plan.md` y
  `tasks.md`: preflight MySQL, migraciones, `migrate --check`, pytest, Ruff y
  endpoint.
- Evidencia de la Etapa 001 en `specs/001-django-project-foundation/plan.md` y
  `tasks.md`: Admin/Unfold, superusuario, `runserver`, pruebas DB-free, Ruff y
  validación visual.
- Windows 10 x64 es el entorno efectivamente verificado. Windows 11 no se probó
  independientemente y no se afirma compatibilidad universal.
- pytest reportó 13 warnings de `langsmith`
  (`DeprecationWarning: asyncio.iscoroutinefunction`), no bloqueantes y sin
  relación con Django/MySQL.
- `specs/002-productos-inventario/` conserva el contenido renumerado de la
  especificación de productos; no está aprobada ni implementada.
- `specs/000-project-bootstrap/spec.md` conserva una referencia histórica a
  `specs/001-productos-inventario/`; no se modifica por R-01. La referencia
  vigente es `specs/002-productos-inventario/`.

## Documentación

- `CONSTITUTION.md`: principios aprobados.
- `AGENTS.md`: instrucciones de trabajo.
- `MEMORY.md`: estado operativo resumido.
- `docs/README.md`: guía de la Etapa 001, checklist visual y tabla de CA.
- `specs/000-project-bootstrap/spec.md`: especificación v1.4.
- `specs/000-project-bootstrap/plan.md`: plan técnico y evidencias.
- `specs/000-project-bootstrap/tasks.md`: tareas, trazabilidad y checklist.
- `specs/001-django-project-foundation/spec.md`: especificación v1.1 aprobada.
- `specs/001-django-project-foundation/plan.md`: plan técnico v1.5.
- `specs/001-django-project-foundation/tasks.md`: tareas v1.5 y trazabilidad.
- `specs/002-productos-inventario/spec.md`: especificación renumerada, no
  aprobada ni implementada.
