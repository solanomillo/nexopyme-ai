# NexoPyme AI

Plataforma de gestión empresarial para pequeños negocios: productos, inventario,
compras, ventas, clientes, finanzas básicas y reportes, con un asistente de IA
para apoyar las operaciones del negocio.

Este repositorio contiene el **Bootstrap 000**, la **Etapa 001 — Django Project
Foundation**, la **Etapa 003 — Cuentas y multiempresa** y la **Etapa 004 —
Rediseño visual** cerrados. La etapa 004 aplica el sistema visual «Mostrador» a
las superficies P0 del panel, sin cambios de backend, copy verificado ni pruebas.
El MVP de negocio todavía no está implementado.

## Estado actual

- Bootstrap 000: cerrado documentalmente; T-01–T-13 completadas.
- Etapa 001: cerrada; T-01–T-18 completadas y aprobadas (RC-4, revisión final del 2026-11-10 y cierre documental en `bef5c58`).
- Etapa 003: CERRADA; T-01–T-26 completadas y aprobadas (2026-11-12).
- Etapa 004: CERRADA; T-01–T-11 completadas y aprobadas (2026-11-13); RC-10 aprobado.
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

## Etapa 003 — Cuentas y multiempresa

### Rutas del panel comercial

- `/login/` — acceso con correo y contraseña.
- `/logout/` — cierre de sesión por `POST` con token CSRF.
- `/panel/` — panel comercial de la empresa activa.
- `/profile/` y `/profile/<id>/` — perfil propio.
- `/password/` — cambio de contraseña, obligatorio en el primer acceso.
- `/users/`, `/users/new/`, `/users/<id>/role/`, `/users/<id>/deactivate/`,
  `/users/<id>/reactivate/` y `/users/<id>/password/` — gestión de usuarios.
- `/company/` — configuración de la empresa.
- `/audit/` — consulta de auditoría y de eventos de seguridad.

La Administración técnica sigue en `/admin/` y es independiente del panel
comercial: una cuenta comercial no puede iniciar sesión en el Admin y el personal
técnico no accede al panel sin membresía activa.

### Roles y capacidades

Roles fijos de la V1: dueño, encargado, operador y consulta. Las capacidades usan
el patrón `recurso.accion` y se definen en `apps/accounts/capabilities.py`: el
dueño posee todas; encargado agrega alta, edición y desactivación de productos,
movimientos y existencia inicial; operador consulta y registra entradas y salidas;
consulta solo lectura. El servidor valida cada vista y servicio con
`require_capability` y `has_capability`; ocultar un enlace no sustituye la
autorización, que sigue respondiendo 403.

### Comandos

```powershell
python manage.py init_company --name "Mi Empresa" --email dueno@example.com
python manage.py reset_owner_password --email dueno@example.com
```

`init_company` solicita la contraseña por consola con confirmación, es idempotente
y crea la empresa con su dueño. `reset_owner_password` genera una contraseña
temporal que se muestra una sola vez y obliga el cambio en el próximo acceso.
Ninguno acepta contraseñas como argumento ni las registra en logs o auditoría.

### Sesión, cookies y logging técnico

Variables opcionales (por defecto entre paréntesis):

- `DJANGO_SECURE_COOKIES` (`False`): marca las cookies de sesión y CSRF como
  `Secure` cuando el sitio se sirve por HTTPS.
- `DJANGO_SESSION_COOKIE_AGE` (`1209600`): duración de la sesión en segundos;
  debe ser mayor que cero.
- `DJANGO_LOG_LEVEL` (`INFO`): nivel del logging técnico por consola
  (`DEBUG`, `INFO`, `WARNING`, `ERROR` o `CRITICAL`). La auditoría de negocio es
  independiente y no escribe credenciales ni datos personales.

### Frontend del panel

- Pie único: `templates/components/footer.html` es el único pie y declara
  «Etapa 003 — Cuentas y multiempresa»; lo usan `base.html` y `base_panel.html`.
- Navegación por capacidad: «Usuarios», «Empresa» y «Auditoría» solo aparecen con
  la capacidad correspondiente, resuelta por el context processor
  `apps.accounts.context_processors.panel_navigation` a partir de la membresía ya
  cargada por el middleware.
- Recuperación de errores: el 403 de capacidad ofrece «Volver al panel»; el 403
  de contexto ofrece cerrar sesión con CSRF; el 404 autenticado ofrece volver al
  panel y el 404 anónimo, iniciar sesión. Las páginas de error usan una cabecera
  mínima sin navegación pública y conservan `Cache-Control: no-store`.

### Estrategia de pruebas

- Pruebas DB-free: no tocan base de datos y cubren estructura, settings, home,
  URLs, Admin y catálogo de capacidades.
- Pruebas con base: usan exclusivamente `nexopyme_bootstrap_test` (`DA-07`) con
  fixtures de `tests/conftest.py`; cubren autenticación, autorización,
  aislamiento entre empresas, usuarios, empresa, auditoría, seguridad, comandos e
  integración de extremo a extremo.
- `tests/test_db_guards.py` protege que la configuración de pruebas no apunte a la
  base de desarrollo.
- Limitación conocida: ejecutar toda la suite en un único proceso hace fallar la
  guarda preexistente `test_settings_foundation.py::test_settings_test_guard_variables_are_present`
  porque pytest-django cambia `DATABASES["default"]["NAME"]` al preparar la base;
  la evidencia válida se obtiene en dos invocaciones (DB-free primero y con base
  después), sin modificar las guardas de la Etapa 001.
- Evidencia de T-25: 278 pruebas en la ejecución objetivo de 12 archivos y 337 en
  la suite completa (36 DB-free + 301 con base autorizada), todas en verde.
- Evidencia de T-26: `MEMORY.md` actualizado a 40 líneas, consistencia de
  `spec.md`, `plan.md`, `tasks.md` y documentación verificada, y **337 pruebas**
  en verde en la suite final; Ruff, `manage.py check` y
  `makemigrations --check` sin errores.

## Etapa 004 — Rediseño visual

La Etapa 004 aplica el sistema visual «Mostrador» a las superficies P0 de la
Etapa 003 sin modificar backend, copy verificado, permisos ni pruebas. Cierra con
T-01 a T-11 y el checkpoint RC-10 APROBADO; la home pública (P2), el menú móvil y
el login de dos columnas quedan fuera de alcance.

### Alcance y sistema visual

- Superficies P0: shell público y de panel, login, panel, listado/alta/confirmación
  de usuarios, empresa, auditoría, perfil, cambio de contraseña, 403 y 404.
- Paleta «Mostrador» de 28 colores, Candara + Segoe UI + Consolas, escala de
  espaciado, contenedor 72/80 rem, hojas 24/32, tablas con `caption`, `scope` y
  `.table-scroll` enfocable, recibo discontinuo, foco doble,
  `prefers-reduced-motion` y `forced-colors`.
- `base.html` y `base_panel.html` comparten el pie único «Etapa 003 — Cuentas y
  multiempresa»; el Admin conserva Unfold y no carga `main.css`.
- Sin JavaScript nuevo, frameworks CSS, fuentes externas ni recursos remotos. La
  home pública P2 se conserva con su bloque de compatibilidad y sin ámbar como
  texto.

### Validación T-10 y RC-10

- 320/375/768/1440/1920 px y zoom 200 % sin scroll horizontal de página; el único
  scroll lateral es el interno de `.table-scroll`.
- 23 pares de contraste medidos (21 de `spec.md` §5.2 más dos sobre `surface`), con
  umbral 4,5:1 para texto y 3:1 para componentes no textuales.
- Teclado, skip link, foco visible, `aria-current`, `aria-invalid`/
  `aria-describedby`, `aria-busy`, `prefers-reduced-motion` y `forced-colors`
  verificados; un solo `h1` y `lang="es"` en las superficies medidas.
- Estados vacío, carga, error, éxito y confirmación; aviso de contraseña temporal;
  403 de contexto; 404 propia con `DEBUG=False`; recibo con un único `<code>`;
  nombre de empresa de 150 caracteres truncado; home 1440/1920 sin regresión.
- Evidencia detallada en `specs/004-rediseno-visual/tasks.md` (T-10 y RC-10) y en
  [`docs/README.md`](docs/README.md#etapa-004--rediseño-visual).

### Límites

- P1 (menú móvil, gestión por fila con `<details>`, login de dos columnas) y P2
  (home pública, parciales, iconografía, copy de producto) no se implementan.
- Sin cambios en `apps/**`, `config/**`, migraciones, Admin/Unfold ni la Etapa 003.
- La base de desarrollo no permite `DELETE`; los registros temporales de validación
  quedaron desactivados y no eliminados.

## Frontend propio

- `templates/base.html`: HTML5, `lang="es"`, viewport, metadatos, skip link,
  bloque `site_header` con la navbar, `main`, footer compartido y carga de
  `static/css/main.css`.
- `templates/base_panel.html`: shell del panel con barra superior, contexto de
  empresa y rol, navegación por capacidad, `aria-current` y pie compartido.
- `templates/components/navbar.html`: marca, Inicio y Administración.
- `templates/components/error_header.html`: cabecera mínima de las páginas de
  error, sin navegación pública.
- `templates/components/footer.html`: pie único con identidad, etapa y año.
- `templates/accounts/`: login, panel, usuarios, empresa, auditoría, perfil y
  contraseña con el sistema «Mostrador».
- `templates/errors/`: 403 y 404 con `.error-page` y acciones de recuperación.
- `templates/home.html`: portada informativa, un solo `h1`, enlace a
  Administración y próximos pasos marcados como pendientes.
- `static/css/main.css`: tokens «Mostrador», reset mínimo, layout, componentes,
  responsive, foco doble, `prefers-reduced-motion` y `forced-colors`.
- `static/img/favicon.svg`: icono propio en SVG con la paleta teal, enlazado
  desde `templates/base.html` con `rel="icon"`.

El frontend propio no usa assets de Unfold y el Admin no usa `main.css`. No se
incorporaron frameworks ni dependencias frontend adicionales. La portada no
muestra datos ficticios ni métricas inventadas.

## Pruebas y calidad

La estrategia de la Etapa 001 fueron pruebas DB-free sobre cinco archivos
concretos; la suite completa quedó fuera de alcance porque usaría
`nexopyme_bootstrap_test`, base prohibida en esa etapa. La Etapa 003 autorizó esa
base (`DA-07`) y su estrategia se describe en
[«Etapa 003 — Cuentas y multiempresa»](#etapa-003--cuentas-y-multiempresa).

Evidencia de la Etapa 001:

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
├── accounts/              # Cuentas, empresa, membresías, panel y comandos
├── audit/                 # Auditoría de negocio y eventos de seguridad
└── core/                  # Infraestructura, sin modelos ni migraciones
    ├── __init__.py
    ├── admin.py           # Re-registro Unfold de User/Group
    └── apps.py
config/                    # settings, urls, views, wsgi/asgi
docs/                      # Documentación de las etapas
locale/es_AR/LC_MESSAGES/  # Catálogo mínimo del logout
specs/                     # Especificaciones, planes y tareas
static/css/main.css        # Fundación visual propia y estilos del panel
static/img/favicon.svg     # Icono propio (rel="icon")
templates/                 # base, home, panel, cuentas, errores y componentes
tests/                     # Pruebas DB-free, con base y guardas existentes
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
- Evidencia de la Etapa 003 en `specs/003-cuentas-multiempresa/tasks.md`,
  `plan.md` y [`docs/README.md`](docs/README.md#etapa-003--cuentas-y-multiempresa):
  implementación por tarea, pruebas DB-free y con base autorizada, aislamiento
  entre empresas, validación visual T-23 y correcciones de T-24.
- Evidencia de la Etapa 004 en `specs/004-rediseno-visual/tasks.md`,
  `plan.md` y [`docs/README.md`](docs/README.md#etapa-004--rediseño-visual):
  sistema «Mostrador», correcciones puntuales de T-10, validación en cinco anchos,
  zoom 200 %, contraste, teclado, estados, 404 con `DEBUG=False`, recibo y home P2.
- Limitaciones de la Etapa 004: P1/P2 fuera de alcance; sin cambios de backend,
  copy verificado ni pruebas; `tfoot` y `aria-disabled` sin consumidor P0;
  `.container--wide` disponible sin uso; el vacío de usuarios no es alcanzable;
  la base de desarrollo no permite `DELETE` y los registros temporales de
  validación quedaron desactivados; la suite se ejecuta en dos invocaciones y el
  borde verde del login queda junto al encabezado (N-10, aceptado desde T-07/RC-9).
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
- `docs/README.md`: guía de las etapas 001, 003 y 004, checklist visual y tabla de CA.
- `specs/000-project-bootstrap/spec.md`: especificación v1.4.
- `specs/000-project-bootstrap/plan.md`: plan técnico y evidencias.
- `specs/000-project-bootstrap/tasks.md`: tareas, trazabilidad y checklist.
- `specs/001-django-project-foundation/spec.md`: especificación v1.1 aprobada.
- `specs/001-django-project-foundation/plan.md`: plan técnico v1.6.
- `specs/001-django-project-foundation/tasks.md`: tareas v1.6 y trazabilidad.
- `specs/002-productos-inventario/spec.md`: especificación renumerada, no
  aprobada ni implementada.
- `specs/003-cuentas-multiempresa/spec.md`: especificación v1.0 aprobada.
- `specs/003-cuentas-multiempresa/plan.md`: plan técnico v1.4.
- `specs/003-cuentas-multiempresa/tasks.md`: tareas y trazabilidad de la etapa.
- `specs/004-rediseno-visual/spec.md`: especificación v0.1 aprobada en G-0a.
- `specs/004-rediseno-visual/plan.md`: plan técnico v0.1 aprobado en G-0b.
- `specs/004-rediseno-visual/tasks.md`: tareas, trazabilidad y evidencia de T-10/RC-10.
