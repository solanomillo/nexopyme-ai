# Plan técnico 001 — Django Project Foundation

## 1. Identificación y estado

| Campo | Valor |
|---|---|
| Funcionalidad | 001 — Django Project Foundation |
| Artefacto | `specs/001-django-project-foundation/plan.md` |
| Versión | 1.5 — RC-4 APROBADO; cierre de T-13 a T-16 |
| Estado | **La v1.0 fue APROBADA en RC-1; la v1.1, v1.2 y v1.3 en revisión delta. RC-3 APROBADO para T-06–T-12. RC-4 APROBADO para T-13–T-16, incluida la corrección del favicon y CA-13 en PASS.** |
| Historial | v1.0: APROBADO en RC-1. v1.1: APROBADO en revisión delta. v1.2: APROBADO en revisión delta. v1.3: APROBADO en revisión delta (i18n). v1.4 (2026-11-09): documentación T-15, versionado de `specs/001` y preparación de T-16; RC-4 pendiente. v1.5 (2026-11-10): RC-4 APROBADO; T-13–T-16 cerradas. |
| Especificación de referencia | `specs/001-django-project-foundation/spec.md` v1.1 aprobada |
| Tareas | `specs/001-django-project-foundation/tasks.md` v1.5 |
| Fecha | 2026-11-10 |
| Responsable | Planner |
| Fase SDD | 8: implementación de la Etapa 001 completada hasta T-16; T-17 y T-18 pendientes |
| Prelación normativa | `CONSTITUTION.md` → `AGENTS.md` → `spec.md` → este plan → `tasks.md` |

Este plan no implementa, no instala dependencias, no accede a MySQL, no crea el superusuario, no ejecuta `runserver` y no realiza commits ni push. Su ejecución requiere la aprobación humana del plan y la autorización explícita de implementación.

## 2. Objetivo del plan

Convertir la especificación aprobada en una secuencia técnica ejecutable, verificable y reversible, con tareas pequeñas, dependencias explícitas, puntos de autorización y evidencias definidas. El resultado esperado es una fundación Django operativa con:

- estructura modular mínima;
- `apps/core` como app de infraestructura sin modelos;
- Django Admin con Unfold;
- superusuario local creado de forma interactiva;
- `runserver` verificado contra `nexopyme_bootstrap_dev`;
- página inicial informativa y sistema visual responsive;
- pruebas DB-free y validación manual del Admin;
- documentación reproducible.

## 3. Estado de partida

| Elemento | Estado |
|---|---|
| Bootstrap 000 | Cerrado y publicado; tareas del Bootstrap T-01–T-13 completadas |
| Python | 3.14.10 en `.venv` |
| Django | `6.0.9` |
| MySQL | 8.0.36; `nexopyme_bootstrap_dev` en `127.0.0.1:3306` |
| Driver | `mysqlclient==2.3.0` |
| Estructura | `config/`, `apps/`, `templates/`, `static/`, `docs/`, `tests/`, `specs/`, `README.md`; estructura creada en T-02/T-07/T-09 |
| Admin | Admin con Unfold configurado; `User`/`Group` re-registrados en T-03/T-05 |
| Estáticos | `STATICFILES_DIRS`, `STATIC_ROOT` y `static/css/main.css` (T-03/T-09) |
| URLs | `admin/`, `home` y `health/` (T-04) |
| Internacionalización | `LANGUAGE_CODE=es-ar`; `TIME_ZONE=America/Argentina/Buenos_Aires`; `LOCALE_PATHS=[BASE_DIR / "locale"]`; catálogo mínimo para el logout de Unfold (T-03) |
| Carga local de entorno | `python-dotenv==1.2.4`; `load_dotenv(BASE_DIR / ".env", override=False)` (regularización T-03) |
| Migraciones iniciales | 18 migraciones de Django presentes desde el 2026-11-07 (Bootstrap 000); el `migrate` accidental del 2026-11-09 fue un no-op; sin revertir |
| Superusuario | Creado y verificado en T-11; identidad y credenciales no registradas |
| Pruebas | Guardas activas; 20 pruebas DB-free en verde (T-13); suite completa exige `nexopyme_bootstrap_test` (prohibida) y se registra `NO EJECUTADA` |
| Ruff | `ruff check .` verde (T-14); deuda de formato preexistente documentada |
| Documentación | T-15: `README.md`, `docs/README.md`, `.env.example` y artefactos de `specs/001` actualizados; RC-4 APROBADO |
| Validación visual | T-16 APROBADA por el usuario: 320/375/768/1440/1920 sin desbordamiento, teclado, foco, skip link, reduced motion, Admin y separación de assets; CA-13 en PASS |
| Renumeración D-06 | Ejecutada: `specs/002-productos-inventario/spec.md` con SHA-256 idéntico |
| Spec 001 | v1.1 aprobada (incluye `python-dotenv==1.2.4`) |

## 4. Decisiones aplicadas

| ID | Resolución | Efecto en el plan |
|---|---|---|
| D-01 | Cambios mínimos en `config/` y `README.md`; sin tocar `specs/000` ni guardas | T-03, T-04, T-15 |
| D-02 | `apps/core` como app de infraestructura sin modelos | T-02, T-05 |
| D-03 | `DJANGO_DEBUG=True` solo en local; default `False` | T-12, T-15 |
| D-04 | No exponer identidad ni datos personales del superusuario | T-11, T-16 |
| D-05 | `frontend-design` tras verificar instalación y antes de diseñar | T-06 antes de T-07–T-09 |
| D-06 | Renumeración preservando contenido | Prerrequisito ejecutado |
| D-07 | Instalación de Unfold al inicio de la implementación | T-01, gate G-2 |
| D-08 | Guardas intactas; solo pruebas DB-free; suite completa `NO EJECUTADA` | T-13 |
| D-09 | Solo `unfold`, sin módulos `contrib` | T-03 |
| D-10 | Home informativa con próximos pasos, sin datos ficticios | T-08 |
| D-11 | `migrate --check` inicial; migraciones reales con justificación | T-10, gate G-5 |
| D-12 | Datos del superusuario elegidos interactivamente | T-11 |

## 5. Estrategia general y fases

| Fase | Objetivo | Tareas | Gate de salida |
|---|---|---|---|
| 0 | Prerrequisitos documentales | Spec v1.1 y renumeración | Completados |
| 1 | Dependencia Unfold | T-01 | `pip check` y `manage.py check` |
| 2 | Estructura y configuración | T-02, T-03, T-04, T-05 | `manage.py check` sin errores |
| 3 | Skill y fundación visual | T-06, T-07, T-08, T-09 | Plantillas y CSS revisables |
| 4 | MySQL, Admin y servidor | T-10, T-11, T-12 | Rutas y Admin verificados |
| 5 | Pruebas y validación | T-13, T-14, T-16 | pytest DB-free, Ruff y checklist visual |
| 6 | Documentación y cierre | T-15, T-17, T-18 | Reviewer APROBADO, commits por tarea y push |

La secuencia no es paralelizable en su mayor parte: la instalación y la configuración preceden al Admin; la skill precede al diseño; MySQL precede al superusuario y a `runserver`; las pruebas y la documentación cierran.

## 6. Dependencias y orden de ejecución

| Tarea | Depende de | Autorización específica |
|---|---|---|
| T-01 Instalar y verificar Unfold | Plan aprobado + autorización de implementación | G-1, G-2 |
| T-02 Crear estructura y `apps/core` | T-01 | G-1 |
| T-03 Configurar `settings.py` | T-01, T-02 | G-1 |
| T-04 Configurar URLs y vista home | T-02, T-03 | G-1 |
| T-05 Re-registrar auth con Unfold | T-01, T-02, T-03 | G-1 |
| T-06 Verificar/instalar `frontend-design` | Plan aprobado | G-4 |
| T-07 Crear `base.html` y componentes | T-03, T-06 | G-1 |
| T-08 Crear `home.html` | T-07 | G-1 |
| T-09 Crear `main.css` | T-06, T-07 | G-1 |
| T-10 Ejecutar `migrate --check` | T-03 | G-3 |
| T-11 Crear superusuario | T-05, T-10 | G-3 |
| T-12 Ejecutar `runserver` y verificar | T-04, T-05, T-08, T-09, T-11 | G-3 |
| T-13 Pruebas DB-free | T-02–T-09 | G-1 |
| T-14 Ruff | T-01–T-13 | G-1 |
| T-15 Documentación | T-12, T-13, T-14, T-16 | G-1 |
| T-16 Validación visual y evidencias | T-09 (home), T-12 (Admin) | G-3 solo para la validación de Admin |
| T-17 Revisión final del Reviewer | T-01–T-16 | — |
| T-18 Cierre documental y verificación Git | T-17 APROBADO y commits/push de T-01–T-16 | G-6 |

## 7. Detalle técnico

### 7.1 Estructura final (T-02 crea el esqueleto; T-05 y T-07–T-09 añaden archivos)

```text
apps/
├── __init__.py
└── core/
    ├── __init__.py
    ├── apps.py
    └── admin.py
templates/
├── base.html
├── home.html
└── components/
    ├── navbar.html
    └── footer.html
static/
├── css/
│   └── main.css
└── img/
    └── favicon.svg
locale/
└── es_AR/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
docs/
└── README.md
tests/
├── test_project_structure.py
├── test_settings_foundation.py
├── test_home_view.py
├── test_urls.py
└── test_admin_unfold.py
```

Reglas:

- `apps/core` no contiene `models.py`, `migrations/`, `views.py` de negocio ni servicios.
- `apps/core/apps.py` declara `CoreConfig` con `name = "apps.core"` y `verbose_name` en español.
- No se crean aplicaciones funcionales.
- `staticfiles/` no se versiona; se añade a `.gitignore` si falta.

### 7.2 `apps/core` (T-02, T-05)

`apps/core/apps.py`:

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Infraestructura"
```

`apps/core/admin.py` contiene únicamente el re-registro de `User` y `Group` descrito en la especificación §9.4. No define modelos ni migraciones.

### 7.3 `config/settings.py` (T-03)

Cambios mínimos:

- Añadir `"unfold"` al inicio de `INSTALLED_APPS`.
- Añadir `"apps.core"` al final de `INSTALLED_APPS`, después de las apps de Django, para que el re-registro de auth ocurra tras `django.contrib.auth.admin`.
- Mantener el orden del resto de apps.
- `TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]`.
- `STATICFILES_DIRS = [BASE_DIR / "static"]`.
- `STATIC_ROOT = BASE_DIR / "staticfiles"`.
- `UNFOLD` con `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER` y `SITE_URL`.
- `load_dotenv(BASE_DIR / ".env", override=False)` al inicio: no sobrescribe variables de entorno ya definidas. `.env` permanece ignorado por Git y no se versiona; las validaciones `_get_required_env` se mantienen.
- Dependencia `python-dotenv==1.2.4` para la carga local de `.env`: `fix(T-01)` sobre `requirements.txt` y `fix(T-03)` sobre `config/settings.py`, aprobados y publicados en RC-2.
- Internacionalización: `LANGUAGE_CODE = "es-ar"`, `TIME_ZONE = "America/Argentina/Buenos_Aires"` y `LOCALE_PATHS = [BASE_DIR / "locale"]`. Catálogo mínimo `locale/es_AR/LC_MESSAGES/django.po|.mo` para el mensaje de logout de Unfold; no se modifican templates del Admin. El `fix(T-03)` incluye `config/settings.py` y el catálogo; aprobado y publicado en `dce246b`.
- No cambiar `DEBUG` default, `ALLOWED_HOSTS`, `DATABASES`, `SECRET_KEY` ni `MIDDLEWARE`.

Criterio de aceptación técnico: importar `config.settings` y ejecutar `python manage.py check` sin errores. Los warnings preexistentes o de seguridad se documentan; no se silencian ni se corrigen fuera de alcance. Si `ALLOWED_HOSTS` vacío produce un warning, se exporta `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost` durante la comprobación local.

### 7.4 URLs y vista home (T-04)

`config/views.py`:

```python
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Renderiza la página informativa de NexoPyme AI."""
    return render(request, "home.html")


def health(request: HttpRequest) -> HttpResponse:
    """Devuelve HTTP 200 si Django puede atender la solicitud."""
    return HttpResponse("ok", content_type="text/plain")
```

`config/urls.py` registra `admin/`, `""` y `health/`, conservando el nombre `health`.

### 7.5 Admin y Unfold (T-03, T-05)

- `"unfold"` antes de `"django.contrib.admin"`.
- Sin `unfold.contrib.*` (D-09).
- `UNFOLD` mínimo, sin dashboard callback ni widgets.
- Re-registro de `User`/`Group` con `unfold.admin.ModelAdmin` y `unfold.forms`.
- No se personalizan plantillas de Unfold.

### 7.6 Superusuario (T-11)

- `python manage.py createsuperuser` interactivo.
- Sin `DJANGO_SUPERUSER_PASSWORD`, fixtures ni scripts.
- Verificación de `is_staff` e `is_superuser` sin mostrar hash.
- Recuperación documentada con `changepassword` o `shell` interactivo.
- Evidencias con identidad enmascarada (D-04).

### 7.7 Estáticos (T-03, T-12)

- `STATIC_URL = "static/"`, `STATICFILES_DIRS`, `STATIC_ROOT`.
- `DJANGO_DEBUG=True` solo en el entorno local documentado.
- Default `False` intacto.
- No se usa `collectstatic` ni `--insecure` como estrategia principal.
- Unfold sirve sus propios assets con `DEBUG=True`.

### 7.8 `frontend-design` (T-06)

1. Verificar `node`/`npx` y que `frontend-design` no está instalada ni a nivel de proyecto ni global.
2. Ejecutar desde la raíz del repositorio, sin `-g` ni flags globales, el comando oficial publicado por la página de skills.sh: `npx skills add https://github.com/anthropics/skills --skill frontend-design --agent opencode --copy -y` tras G-4.
3. Si la CLI solicita agente o alcance, seleccionar **OpenCode** y **proyecto**; nunca instalar globalmente.
4. Verificar que los archivos quedaron dentro del proyecto en `.agents/skills/frontend-design/SKILL.md` y `LICENSE.txt`, y que `skills-lock.json` está en la raíz; no en `~/.config/opencode/skills` ni en otra ubicación global.
5. Verificar que OpenCode detecta la skill por el ID `frontend-design`.
6. Registrar la versión, `computedHash` y fuente de `skills-lock.json`; si no se puede fijar, documentar el riesgo de deriva.
7. Revisar `SKILL.md`, confirmar que no incorpora dependencias no aprobadas y registrar origen (`anthropics/skills`) y licencia (Apache 2.0, `LICENSE.txt`).
8. No modificar la configuración de OpenCode salvo que sea imprescindible; si lo es, detenerse y consultar.
9. No instalar otras skills ni modificar configuraciones globales.
10. Si la CLI genera archivos de manifiesto o lock distintos de `skills-lock.json`, o fuera de `.agents/skills/frontend-design/` y `skills-lock.json`, detenerse y consultar antes de incluirlos o modificarlos.
11. Si la instalación falla, documentarlo y continuar con la dirección visual de la especificación; no bloquea la aceptación técnica.
12. No añadir dependencias Python ni frontend.

**Nota:** la URL individual de skills.sh no expone el catálogo que consume la CLI; su página publica como comando oficial el de `https://github.com/anthropics/skills --skill frontend-design`. La tabla §13.1 de `spec.md` conserva el dato observado anterior como descriptivo y no normativo.

### 7.9 Fundación visual (T-07, T-08, T-09)

- `base.html`: HTML5, `lang="es"`, viewport, título, descripción, `main.css`, skip link, navbar, `main`, footer, bloques.
- `navbar.html`: marca, enlace Inicio, enlace Administración.
- `footer.html`: NexoPyme AI, etapa actual, año.
- `home.html`: extiende `base.html`; un `h1`; descripción; etapa actual; enlace a Administración; próximos pasos como pendientes. No se enlaza documentación si no existe una ruta que la sirva.
- `main.css`: variables, reset mínimo, layout, componentes, breakpoints (incluido 1920 px), foco visible, `prefers-reduced-motion`.
- Sin Bootstrap, React, Vue, Node.js ni datos ficticios.

### 7.10 Pruebas DB-free (T-13)

Archivos y cobertura:

| Archivo | Cobertura |
|---|---|
| `test_project_structure.py` | Directorios y archivos; ausencia de apps funcionales; separación Admin/frontend (sin `unfold` en plantillas propias, sin `main.css` en Admin) |
| `test_settings_foundation.py` | `TEMPLATES`, `STATICFILES_DIRS`, `STATIC_ROOT`, `INSTALLED_APPS`, `UNFOLD` |
| `test_home_view.py` | `GET /` 200, plantilla usada, sin DB |
| `test_urls.py` | Resolución de `admin/`, `home`, `health` |
| `test_admin_unfold.py` | `User`/`Group` registrados con `unfold.admin.ModelAdmin` |

Reglas:

- Sin marcador `django_db` ni fixtures que abran conexión.
- `client` con `override_settings(ALLOWED_HOSTS=["testserver"])` cuando corresponda.
- `config.settings_test` y guardas intactas.
- Variables `MYSQL_TEST_*` presentes si la guarda las exige, sin conexión.
- Suite completa registrada como `NO EJECUTADA`.
- No se ejecutan `--reuse-db`, `--create-db`, `-n` ni `--nomigrations`.

### 7.11 Documentación (T-15)

`README.md` y `docs/README.md` deben incluir:

- estructura del proyecto;
- versiones y dependencia Unfold;
- configuración de Admin y Unfold;
- creación y recuperación del superusuario;
- variables de entorno y ejecución local;
- estrategia de estáticos con `DJANGO_DEBUG=True`;
- comandos de verificación y resultados;
- pruebas DB-free y suite completa `NO EJECUTADA`;
- evidencias y limitaciones.

La v1.4 incorpora al alcance versionable de T-15 los artefactos aprobados de la
Etapa 001 (`spec.md`, `plan.md`, `tasks.md`). Los artefactos de la Etapa 000 ya
estaban versionados en `144056c` y se verificaron sin modificarlos. La
documentación incluye la tabla `CA-01…CA-18`, el checklist de T-16 y las
limitaciones aceptadas de las referencias históricas a `specs/001-productos-inventario/`.
`MEMORY.md` se actualiza en T-15 pero se commitea en T-18, que es su alcance.

## 8. Operaciones que requieren MySQL

| Operación | Comando | Acceso | Tarea | Gate | Observaciones |
|---|---|---|---|---|---|
| Comprobación de sistema | `python manage.py check` | Sin conexión por defecto | T-03 | G-1 | No abre MySQL |
| Comprobación de migraciones | `python manage.py migrate --check` | Conexión de solo lectura/consulta de esquema | T-10 | G-3 | Solo `nexopyme_bootstrap_dev` |
| Migración real | `python manage.py migrate` | Escritura de esquema | T-10 (condicional) | G-5 | Solo si hay pendientes justificados |
| Migraciones iniciales (desviación T-10) | `python manage.py migrate` accidental | No-op; sin escritura nueva | T-10 | Regularizado por el usuario | Las 18 filas de `django_migrations` son del 2026-11-07 (Bootstrap 000); el `migrate` del 2026-11-09 no aplicó nada; sin revertir ni repetir |
| Creación de superusuario | `python manage.py createsuperuser` | Escritura en tablas `auth` | T-11 | G-3 | Interactivo; sin contraseña en argumentos |
| Servidor de desarrollo | `python manage.py runserver 127.0.0.1:8000` | Conexión y comprobación de migraciones | T-12 | G-3 | `DJANGO_DEBUG=True` local |
| Suite completa de pytest | `pytest` sin filtro | Crearía/usaría `nexopyme_bootstrap_test` | — | Prohibido | Se registra `NO EJECUTADA` |
| Pruebas DB-free | `pytest tests/...` sin `django_db` | Sin conexión | T-13 | G-1 | Guardas intactas |

**Regla de identidad:** antes de cualquier comando con conexión, verificar que `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_HOST=127.0.0.1` y `MYSQL_PORT=3306`. Si la identidad no coincide, detenerse sin conectar.

## 9. Estrategia de pruebas y guardas

### 9.1 Restricción estructural

`pytest.ini` fija `DJANGO_SETTINGS_MODULE=config.settings_test` y `conftest.py` aborta si:

- el módulo no es `config.settings_test`;
- la base de desarrollo no es `nexopyme_bootstrap_dev`;
- la base de pruebas no es `nexopyme_bootstrap_test`;
- el usuario de pruebas no es `nexopyme_test_user`;
- se usa paralelismo, `--reuse-db`, `--create-db` o `--nomigrations`.

Estas guardas no se modifican (D-08).

### 9.2 Pruebas DB-free

- Se ejecutan solo archivos concretos de `tests/`, sin marcador `django_db`.
- No se usan fixtures `db`, `transactional_db` ni `django_db_setup`.
- `client` no abre base para la home anónima; se configura `ALLOWED_HOSTS=["testserver"]` en la prueba.
- Las plantillas de la home no acceden a `request.user`, `perms` ni `messages`; si lo hicieran, podrían activar sesión y abrir MySQL.
- Variables requeridas por `settings_test`: `DJANGO_SECRET_KEY`, `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306`, `MYSQL_TEST_USER=nexopyme_test_user` y `MYSQL_TEST_PASSWORD`, con `MYSQL_USER != MYSQL_TEST_USER`. Su presencia satisface la guarda; no se abre conexión. Un `MYSQL_TEST_USER` distinto de `nexopyme_test_user` hace abortar la guarda.
- `config.settings_test` importa `config.settings`, por lo que `load_dotenv` también se ejecuta en pytest. Las guardas siguen validando base, host, puerto y usuario de pruebas; `.env` no debe contener valores de pruebas distintos de `nexopyme_test_user`.
- Verificación positiva: `python -m pytest --setup-show` **con la lista explícita de los cinco archivos de la etapa** (nunca sin filtro, porque colectaría `tests/test_db_guards.py` y activaría `django_db_setup`) no debe mostrar `django_db_setup` ni fixtures de base de datos; si aparecen, la prueba no es DB-free.
- Si una prueba intenta abrir base, se considera fallo de diseño y se corrige la prueba; no se habilita la base prohibida.
- `tests/test_db_guards.py` no se modifica; su prueba con `@pytest.mark.django_db` queda excluida y se registra como `NO EJECUTADA`.

### 9.3 Suite completa

- No se ejecuta.
- Se registra `NO EJECUTADA` con la causa y el alcance cubierto por las pruebas DB-free.
- No se usa `--ignore` para simular una suite completa.

### 9.4 Validación manual del Admin

- Se realiza contra `nexopyme_bootstrap_dev` con el superusuario local.
- Cubre login, panel, `User`, `Group`, logout y estilos de Unfold.
- No sustituye pruebas automatizadas, pero es evidencia obligatoria de CA-05 a CA-09.

## 10. Validación funcional y visual

### 10.1 Funcional

| Elemento | Verificación |
|---|---|
| `/` | HTTP 200, plantilla `home.html`, sin datos ficticios |
| `/health/` | HTTP 200, `text/plain`, cuerpo `ok` |
| `/admin/` | Login, panel autenticado, logout |
| `User`/`Group` | HTTP 200 con estilos de Unfold |
| Branding Unfold | `SITE_TITLE` y `SITE_HEADER` configurados; sin «Django administration» |
| Estáticos | `main.css` cargado; assets de Unfold cargados en Admin |
| Separación | Admin no usa `main.css`; home no usa assets de Unfold |

### 10.2 Visual

- 320 px, 768 px, 1440 px y 1920 px sin desbordamiento horizontal.
- Navegación por teclado y foco visible.
- `lang="es"`, un `h1`, jerarquía coherente.
- Contraste mínimo 4.5:1.
- Enlace de salto al contenido.
- Capturas sin identidad ni datos personales.

## 11. Riesgos y mitigaciones

| Riesgo | Mitigación | Tarea |
|---|---|---|
| Unfold falla en runtime | `pip check`, `manage.py check`, smoke test; detener y consultar | T-01, T-12 |
| Estáticos no servidos | `DJANGO_DEBUG=True` local documentado | T-12 |
| `User`/`Group` sin estilos | Re-registro con Unfold; verificación CA-08 | T-05, T-12 |
| Secretos en evidencias | Enmascarar; revisar archivos versionados | T-11, T-15, T-16 |
| Credenciales reales cargadas en el proceso | `.env` es secreto, no se imprime ni se versiona; `load_dotenv(override=False)`; no incluir valores reales en logs/evidencias | T-03, T-11, T-15 |
| Acceso a base de pruebas | No ejecutar suite completa; validar identidad | T-10, T-13 |
| Migraciones pendientes | `migrate --check`; no migrar sin G-5 | T-10 |
| `migrate` accidental sin G-5 | Desviación controlada: no-op verificado (18 filas del 2026-11-07), sin revertir, `migrate --check` exit 0, no repetir | T-10 |
| Carga de `.env` sobrescribe el entorno | `load_dotenv(..., override=False)`; validaciones intactas | T-03 |
| `.env` versionado por error | `.gitignore` + `git check-ignore`; no incluir en commits | T-03, T-15 |
| Pérdida de contenido al renumerar | Ya ejecutada con hash idéntico | Prerrequisito |
| Alcance hacia dashboard o negocio | Exclusiones y revisión del Reviewer | Todas |
| Mezcla Admin/frontend | Verificación CA-14 | T-16 |
| Pérdida de acceso al superusuario | Procedimiento de recuperación | T-11, T-15 |
| `ALLOWED_HOSTS` en pruebas | `override_settings` solo en test | T-13 |
| Deriva de Unfold | Pin exacto y `pip check` | T-01 |

## 12. Puntos de autorización y control

| Gate | Momento | Quién autoriza | Alcance |
|---|---|---|---|
| G-0 | Antes de implementar | Usuario | Aprobación del plan y las tareas |
| G-1 | Antes de T-01 | Usuario | Autorización explícita de implementación y flujo Git por tarea (`git add` solo de la tarea y `commit` por Implementer; `push` por Build) |
| G-2 | Antes de T-01 | Usuario | Instalación de `django-unfold==0.110.1` y `python-dotenv==1.2.4` (regularizado el 2026-11-09) |
| G-3 | Antes de T-10, T-11 y T-12, y antes de la parte de Admin de T-16 | Usuario | Alcance autorizado para MySQL dev; la ejecución requiere G-1 vigente y confirmación de identidad. La validación de home/CSS de T-16 no requiere G-3 |
| G-4 | Antes de T-06 | Usuario | Instalación de la skill `frontend-design` (D-05) |
| G-5 | Solo si `migrate --check` reporta pendientes; regularizado el 2026-11-09 para el `migrate` accidental no-op | Usuario | Migración real justificada; no se autorizan nuevas migraciones |
| G-6 | Por cada tarea aprobada en RC-2, RC-3, RC-4, T-17 y T-18 | Build (flujo §9) | Verificación del commit de esa tarea y `git push`; no requiere autorización adicional |

El silencio no constituye autorización. Si un gate no está resuelto, la tarea se detiene.

### 12.1 Política de Git por tarea (AGENTS.md §9)

- Un commit por tarea con archivos versionables. No existe un commit único de etapa.
- El commit se crea únicamente después de que el Reviewer emita APROBADO para esa tarea en el checkpoint que la cubre (RC-2, RC-3, RC-4 o T-17); el commit de cierre de T-18 se ampara en el APROBADO de T-17 y en el alcance documental aprobado.
- Implementer solo ejecuta el commit después de ejecutar las pruebas correspondientes, obtener Ruff sin errores y verificar que no existen cambios ajenos a la tarea.
- Implementer ejecuta `git add` limitado exclusivamente a los archivos de la tarea y `git commit` con Conventional Commit en inglés.
- Build vuelve a verificar el alcance del commit, que corresponde a su tarea, que el informe contiene pruebas y Ruff en verde y que existe APROBADO; después ejecuta `git push` a `main`. No se solicita autorización adicional por cada commit o push.
- Las tareas sin archivos versionables (T-10, T-11, T-12, T-14, T-17) no generan commit; su evidencia es el informe. T-06 se commitea porque instala la skill en `.agents/skills/` y genera `skills-lock.json`.
- T-16 commitea `templates/base.html` y `static/img/favicon.svg`, correspondientes a la corrección del favicon aprobada en RC-4.
- T-14 no tiene commit propio; si Ruff exige correcciones, se commitean bajo la tarea afectada con `fix:` tras el nuevo APROBADO.
- T-15 commitea `README.md`, `docs/README.md`, `.env.example` y los artefactos de `specs/001-django-project-foundation/` (`spec.md`, `plan.md`, `tasks.md`). `MEMORY.md` se actualiza en T-15 pero se commitea únicamente en T-18. Los artefactos de `specs/000-project-bootstrap/` ya están versionados y no se modifican.
- Las correcciones posteriores se revisan y aprueban en el checkpoint donde se detectan (RC-3, RC-4 o la re-revisión de T-17); ese nuevo APROBADO habilita un commit `fix:` bajo la tarea afectada. No se reutiliza el APROBADO original de la tarea y no se usa `amend`.
- T-18 commitea únicamente `MEMORY.md`, que es su alcance; Build verifica su contenido contra el alcance documental antes del commit. No agrupa cambios de otras tareas.

## 13. Revisión del Reviewer

| Checkpoint | Momento | Alcance | Veredicto |
|---|---|---|---|
| RC-1 | Antes de implementar | `plan.md` y `tasks.md` | APROBADO / CAMBIOS NECESARIOS |
| RC-2 | Tras T-01–T-05 | Instalación, estructura, configuración, Admin/Unfold | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-3 | Tras T-06–T-12 | Skill, frontend, MySQL dev, Admin y servidor | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-4 | Tras T-13–T-16 | Pruebas, Ruff, documentación y validación visual | APROBADO / CAMBIOS NECESARIOS por tarea |

En RC-2, RC-3 y RC-4 el Reviewer emite un veredicto individual por cada tarea incluida; solo las tareas con APROBADO pueden commitearse. T-17 revisa el conjunto completo.

El Reviewer no modifica archivos. Un veredicto APROBADO es técnico y no sustituye la aprobación humana.

## 14. Matriz de trazabilidad resumida

| Requisitos | CA | Tareas |
|---|---|---|
| RF-01, RNF-06 | CA-01, CA-12 | T-02, T-07, T-08, T-09, T-13 |
| RF-02 | CA-02 | T-03, T-13 |
| RF-03 | CA-03 | T-04 (ruta), T-08 (render), T-13 (prueba) |
| RNF-04, RNF-05 | CA-13 | T-09, T-16 |
| RF-04 | CA-04 | T-04, T-12, T-13 |
| RF-05, RF-10 | CA-05 | T-04, T-05, T-11, T-12 |
| RF-06, RNF-01, RNF-08 | CA-06 | T-01, T-03, T-05, T-12, T-13 |
| RF-07 | CA-07 | T-03, T-12, T-16 |
| RF-08 | CA-08 | T-05, T-12, T-13 |
| RF-09, RNF-02 | CA-09, CA-10 | T-11, T-12, T-15, T-16 |
| RF-11, RNF-09 | CA-11 | T-10, T-12 |
| RF-12 | CA-12, CA-13 | T-07, T-08, T-09, T-13, T-16 |
| RF-13, RNF-10 | CA-17 | T-15, T-16 |
| RF-14, RNF-07 | CA-15, CA-16 | T-13, T-14 |
| RF-15 | CA-18 | Prerrequisito D-06 |
| RNF-03 | CA-14 | T-07, T-09, T-13, T-16 |

La matriz detallada por tarea se encuentra en `tasks.md`.

## 15. Criterios de cierre

1. Plan y tareas aprobados por el usuario.
2. Autorización explícita de implementación emitida.
3. Todas las tareas T-01 a T-18 completadas con evidencia; cada tarea con archivos versionables tiene su commit y push.
4. Pruebas DB-free en verde; suite completa registrada como `NO EJECUTADA`.
5. Ruff sin errores sobre el código modificado.
6. Validación funcional y visual completada.
7. Reviewer con veredicto APROBADO.
8. Documentación actualizada y sin secretos.
9. `MEMORY.md` actualizado al cierre aprobado.
10. Commits por tarea y push realizados conforme a `AGENTS.md` §9; T-18 commitea solo `MEMORY.md`.

## 16. Fuera de alcance

- Aplicaciones, modelos, migraciones o servicios de negocio.
- Dashboard con datos ficticios.
- Bootstrap 5, React, Vue, Node.js o bundlers.
- Autenticación pública o gestión de usuarios fuera del Admin.
- Despliegue remoto, CI/CD, contenedores, Redis, RAG o bases vectoriales.
- Acceso a `nexopyme_bootstrap_test`, cambios de permisos MySQL o bases destructivas.
- Aprobación o implementación de productos e inventario.

## 17. Anexo: comandos previstos (no ejecutados)

```text
# Dependencia
python -m pip install -r requirements.txt
python -m pip check
python -m pip show django-unfold
python -c "from importlib.metadata import version; print(version('django-unfold'))"

# Comprobaciones Django
python manage.py check
python manage.py migrate --check

# Superusuario (interactivo)
python manage.py createsuperuser

# Servidor local (entorno local documentado)
python manage.py runserver 127.0.0.1:8000

# Pruebas DB-free (sin marcador django_db)
python -m pytest tests/test_project_structure.py tests/test_settings_foundation.py tests/test_home_view.py tests/test_urls.py tests/test_admin_unfold.py

# Calidad
ruff check .
```

Ninguno de estos comandos se ha ejecutado durante la elaboración de este plan.

---

**Fin del plan técnico v1.5.** La v1.0 fue aprobada en RC-1; la v1.1, v1.2 y v1.3 en revisión delta. RC-3 está aprobado. RC-4 está aprobado para T-13–T-16, incluida la corrección del favicon y CA-13 en PASS. Quedan T-17 y T-18. G-0/G-1 ya fueron concedidas.

