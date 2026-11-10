# Tareas 001 — Django Project Foundation

## 1. Identificación

| Campo | Valor |
|---|---|
| Funcionalidad | 001 — Django Project Foundation |
| Artefacto | `specs/001-django-project-foundation/tasks.md` |
| Versión | 1.5 — RC-4 APROBADO; cierre de T-13, T-14, T-15 y T-16 |
| Estado | **La v1.0 fue APROBADA en RC-1; la v1.1, v1.2 y v1.3 en revisión delta. RC-3 APROBADO para T-06–T-12. RC-4 APROBADO para T-13–T-16, incluida la corrección del favicon y CA-13 en PASS.** |
| Historial | v1.0: APROBADO en RC-1. v1.1: APROBADO en revisión delta. v1.2: APROBADO en revisión delta. v1.3: APROBADO en revisión delta (i18n). v1.4 (2026-11-09): documentación T-15, versionado de `specs/001` y preparación de T-16; RC-4 pendiente. v1.5 (2026-11-10): RC-4 APROBADO; T-13–T-16 cerradas. |
| Especificación | `spec.md` v1.1 aprobada |
| Plan | `plan.md` v1.5 (RC-4 APROBADO) |
| Fecha | 2026-11-10 |
| Responsable | Planner |

## 2. Convenciones

- `[ ]` pendiente; `[x]` completada; `[~]` en curso; `[!]` bloqueada.
- Cada tarea es pequeña, ordenada y verificable.
- Ninguna tarea se ejecuta sin los gates del plan §12.
- Las evidencias no contienen contraseñas, tokens ni datos personales.
- Los comandos con conexión MySQL solo usan `nexopyme_bootstrap_dev` en `127.0.0.1:3306`.
- La suite completa de pytest no se ejecuta.
- **Git:** un commit por tarea con archivos versionables, creado solo tras el APROBADO individual del Reviewer en RC-2, RC-3, RC-4 o T-17 (T-18 se ampara en el APROBADO de T-17); `git add` exclusivamente de los archivos de esa tarea; Conventional Commits en inglés; Build verifica la correspondencia y ejecuta `git push`.
- Implementer solo commitea después de ejecutar las pruebas correspondientes, obtener Ruff sin errores y verificar que no existen cambios ajenos a la tarea. Build vuelve a verificar el alcance del commit antes del push.
- Las correcciones `fix:` requieren un nuevo APROBADO del Reviewer en el checkpoint donde se detectó el defecto; no se reutiliza la aprobación anterior.
- Las tareas sin archivos versionables no generan commit; su evidencia es el informe. T-14 no tiene commit propio; si Ruff exige correcciones, se commitean bajo la tarea afectada con `fix:`.
- T-18 commitea solo `MEMORY.md`; Build verifica su contenido contra el alcance documental antes del commit.

## 3. Prerrequisitos ejecutados

| ID | Prerrequisito | Estado | Evidencia |
|---|---|---|---|
| P-01 | Consolidar `spec.md` v1.0 y enmienda v1.1 aprobadas | `[x]` | `specs/001-django-project-foundation/spec.md` |
| P-02 | Renumerar productos D-06 preservando contenido | `[x]` | `specs/002-productos-inventario/spec.md`; SHA-256 `DBDFB6A1FF5342F54F42BC1D6B73F3D3E89216504750F290B9238D2CB0AE923E` |

## 4. Resumen de tareas

| ID | Título | Fase | Depende de | Gate | Estado |
|---|---|---|---|---|---|
| T-01 | Instalar Unfold y verificar compatibilidad | 1 | Plan aprobado | G-1, G-2 | `[x]` |
| T-02 | Crear estructura y `apps/core` | 2 | T-01 | G-1 | `[x]` |
| T-03 | Configurar `settings.py` | 2 | T-01, T-02 | G-1 | `[x]` |
| T-04 | Configurar URLs y vista home | 2 | T-02, T-03 | G-1 | `[x]` |
| T-05 | Re-registrar `User`/`Group` con Unfold | 2 | T-01, T-02, T-03 | G-1 | `[x]` |
| T-06 | Verificar e instalar `frontend-design` | 3 | Plan aprobado | G-4 | `[x]` |
| T-07 | Crear `base.html` y componentes | 3 | T-03, T-06 | G-1 | `[x]` |
| T-08 | Crear `home.html` | 3 | T-07 | G-1 | `[x]` |
| T-09 | Crear `main.css` | 3 | T-06, T-07 | G-1 | `[x]` |
| T-10 | Ejecutar `migrate --check` | 4 | T-03 | G-3 | `[x]` |
| T-11 | Crear superusuario local | 4 | T-05, T-10 | G-3 | `[x]` |
| T-12 | Ejecutar `runserver` y verificar | 4 | T-04, T-05, T-08, T-09, T-11 | G-3 | `[x]` |
| T-13 | Pruebas automatizadas DB-free | 5 | T-02–T-09 | G-1 | `[x]` |
| T-14 | Ejecutar Ruff | 5 | T-01–T-13 | G-1 | `[x]` |
| T-15 | Actualizar documentación | 6 | T-12, T-13, T-14, T-16 | G-1 | `[x]` |
| T-16 | Validación visual y evidencias | 5 | T-09 (home), T-12 (Admin) | G-3 solo para Admin | `[x]` |
| T-17 | Revisión final del Reviewer | 6 | T-01–T-16 | — | `[ ]` |
| T-18 | Cierre documental y verificación Git | 6 | T-17 APROBADO y commits/push de T-01–T-16 | G-6 | `[ ]` |

`[x]` tarea completada y aprobada (el commit se ejecuta bajo G-6 después del APROBADO, cuando la tarea tiene archivos versionables); `[~]` implementada y pendiente de aprobación o commit; `[ ]` no iniciada.

## 5. Tareas detalladas

### T-01 — Instalar Unfold y verificar compatibilidad

- **Objetivo:** instalar exactamente `django-unfold==0.110.1` y confirmar compatibilidad con Django 6.0.9 y Python 3.14.10.
- **Alcance:** `requirements.txt`, entorno `.venv`.
- **Dependencias:** plan aprobado; gates G-1 y G-2.
- **Pasos:**
  1. Verificar `python --version` (3.14.10) y que `sys.prefix` está bajo `.venv`.
  2. Añadir `django-unfold==0.110.1` a `requirements.txt` con comentario de etapa.
  3. Ejecutar `python -m pip install -r requirements.txt`.
  4. Ejecutar `python -m pip check`.
  5. Ejecutar `python -m pip show django-unfold`.
  6. Ejecutar `python -c "from importlib.metadata import version; print(version('django-unfold'))"`.
  7. Ejecutar `python -c "import unfold, unfold.admin, unfold.forms; from unfold.admin import ModelAdmin; from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm"`.
- **Verificación:** versión exacta, sin conflictos, import de paquete y submódulos correcto.
- **Evidencia:** salidas de los comandos, sin secretos.
- **Trazabilidad:** RF-06, RNF-01, RNF-08 → CA-06.
- **Prohibido:** instalar otras dependencias, cambiar versiones existentes, usar rangos abiertos.
- **Regularización (2026-11-09):** se añadió `python-dotenv==1.2.4` a `requirements.txt` para la carga local de `.env`. El commit `fix(T-01)` incluye **solo** `requirements.txt`; aprobado y publicado en RC-2.

### T-02 — Crear estructura y `apps/core`

- **Objetivo:** crear la estructura mínima y la app de infraestructura sin modelos.
- **Alcance:** `apps/__init__.py`, `apps/core/__init__.py`, `apps/core/apps.py`, `templates/`, `static/css/`, `docs/README.md`, `tests/`.
- **Dependencias:** T-01.
- **Pasos:**
  1. Crear directorios y archivos mínimos.
  2. Crear `CoreConfig` con `name = "apps.core"` y `verbose_name = "Infraestructura"`.
  3. No crear `models.py` ni `migrations/`.
  4. Crear `docs/README.md` con el índice inicial de la etapa.
  5. Añadir `.gitkeep` en los directorios que quedarán vacíos hasta T-07/T-09/T-13 para que sean versionables.
  6. Añadir `staticfiles/` a `.gitignore` si no está.
- **Verificación:** árbol de archivos; ausencia de modelos y migraciones; `from apps.core.apps import CoreConfig` con `assert CoreConfig.name == "apps.core"` (sin `django.setup()`, porque `apps.core` aún no está en `INSTALLED_APPS`). La carga efectiva de la app se verifica en T-03.
- **Evidencia:** listado de estructura.
- **Trazabilidad:** RF-01 → CA-01.
- **Prohibido:** crear aplicaciones funcionales, modelos o migraciones.

### T-03 — Configurar `settings.py`

- **Objetivo:** habilitar Unfold, `apps/core`, plantillas y estáticos globales.
- **Alcance:** `config/settings.py`.
- **Dependencias:** T-01, T-02.
- **Pasos:**
  1. Añadir `"unfold"` antes de `"django.contrib.admin"`.
  2. Añadir `"apps.core"` al final de `INSTALLED_APPS`, después de las apps de Django.
  3. Configurar `TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]`.
  4. Configurar `STATICFILES_DIRS = [BASE_DIR / "static"]` y `STATIC_ROOT = BASE_DIR / "staticfiles"`.
  5. Definir `UNFOLD` con `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER` y `SITE_URL`.
  6. Mantener `DEBUG` default `False`, `ALLOWED_HOSTS`, `DATABASES`, `SECRET_KEY` y `MIDDLEWARE`.
  7. Verificar la carga de la app con `$env:DJANGO_SETTINGS_MODULE='config.settings'; python -c "import django; django.setup(); from django.apps import apps; assert apps.get_app_config('core').name == 'apps.core'"`.
  8. Cargar `.env` con `load_dotenv(BASE_DIR / ".env", override=False)`, sin sobrescribir variables ya definidas; mantener las validaciones `_get_required_env` y no versionar `.env`.
- **Verificación:** `python manage.py check` sin errores; `apps.core` cargada; `.env` ignorado; revisión de diffs limitados.
- **Evidencia:** salida de `check`; fragmentos de configuración; `git check-ignore .env`.
- **Trazabilidad:** RF-02, RF-06, RF-07, RNF-08 → CA-02, CA-06, CA-07.
- **Prohibido:** módulos `unfold.contrib.*`, cambios de base de datos o de secretos, versionar `.env` o exponer credenciales.
- **Regularización (2026-11-09):** `config/settings.py` incorpora `load_dotenv(..., override=False)`. El commit `fix(T-03)` de esa regularización incluyó solo `config/settings.py`; la dependencia `python-dotenv==1.2.4` se commiteó en `fix(T-01)` sobre `requirements.txt`.
- **Regularización i18n (2026-11-09):** `LANGUAGE_CODE=es-ar`, `TIME_ZONE=America/Argentina/Buenos_Aires`, `LOCALE_PATHS=[BASE_DIR / "locale"]`; catálogo mínimo `locale/es_AR/LC_MESSAGES/django.po|.mo` para el mensaje de logout de Unfold. El nuevo commit `fix(T-03)` incluye `config/settings.py` y el catálogo; aprobado y publicado en `dce246b`. No se modifican templates de Admin.

### T-04 — Configurar URLs y vista home

- **Objetivo:** registrar `/admin/`, `/` y conservar `/health/`.
- **Alcance:** `config/urls.py`, `config/views.py`.
- **Dependencias:** T-02, T-03.
- **Pasos:**
  1. Implementar `home(request)` con `render(request, "home.html")`.
  2. Conservar `health(request)` sin cambios funcionales.
  3. Registrar `path("admin/", admin.site.urls)`, `path("", home, name="home")` y `path("health/", health, name="health")`.
- **Verificación:** `python manage.py check`; resolución de las tres rutas (el render de `/` se verifica en T-08 y T-13).
- **Evidencia:** salida de `check`; diff de URLs.
- **Trazabilidad:** RF-04, RF-05 → CA-04, CA-05; CA-03 se evidencia en T-08 y T-13.
- **Prohibido:** lógica de negocio, consultas a base o rutas adicionales.

### T-05 — Re-registrar `User`/`Group` con Unfold

- **Objetivo:** aplicar estilos de Unfold a los modelos de autenticación.
- **Alcance:** `apps/core/admin.py`.
- **Dependencias:** T-01, T-02, T-03 (T-03 añade `"apps.core"` a `INSTALLED_APPS`, sin lo cual `autodiscover` no importa `apps/core/admin.py` y la verificación sería vacía).
- **Pasos:**
  1. Importar `User`, `Group`, `unfold.admin.ModelAdmin` y `unfold.forms`.
  2. Desregistrar y re-registrar `User` y `Group`.
  3. Usar `UserChangeForm`, `UserCreationForm` y `AdminPasswordChangeForm`.
  4. No añadir modelos ni personalizaciones adicionales.
  5. Confirmar con `python manage.py check` que `apps/core/admin.py` se importa y registra.
- **Verificación:** `python manage.py check`; aserción sin base con `python manage.py shell -c "from django.contrib import admin; from django.contrib.auth.models import Group, User; from unfold.admin import ModelAdmin; assert isinstance(admin.site._registry[User], ModelAdmin); assert isinstance(admin.site._registry[Group], ModelAdmin)"`.
- **Evidencia:** salida de `check`; fragmento de `admin.py`.
- **Trazabilidad:** RF-08 → CA-08.
- **Prohibido:** personalizar plantillas de Unfold o añadir módulos `contrib`.

### T-06 — Verificar e instalar `frontend-design`

- **Objetivo:** incorporar la skill `frontend-design` a nivel de proyecto y detectada por OpenCode, antes de diseñar el frontend, sin alterar configuraciones globales.
- **Alcance:** `.agents/skills/frontend-design/` y `skills-lock.json` en la raíz del repositorio; sin cambios de código, configuración global ni dependencias Python.
- **Dependencias:** Plan aprobado; gate G-4.
- **Pasos:**
  1. Verificar `node`/`npx` y que `frontend-design` no está instalada ni a nivel de proyecto ni global.
  2. Ejecutar desde la raíz del repositorio, sin `-g` y sin flags globales, el comando oficial publicado por la página de skills.sh: `npx skills add https://github.com/anthropics/skills --skill frontend-design --agent opencode --copy -y`.
  3. Si la CLI solicita agente o alcance, seleccionar **OpenCode** y **proyecto**; nunca instalar globalmente y no usar `-g`.
  4. Verificar que los archivos quedaron dentro del proyecto en `.agents/skills/frontend-design/SKILL.md` y `LICENSE.txt`, y que `skills-lock.json` está en la raíz; confirmar que no se escribió en `~/.config/opencode/skills` ni en otra ubicación global.
  5. Verificar que OpenCode detecta la skill: aparece como disponible y el `skill` tool la carga por el ID `frontend-design`.
  6. Registrar la versión, el `computedHash` y la fuente que reporte `skills-lock.json`; si no se puede fijar, documentar el riesgo de deriva.
  7. Revisar `SKILL.md` antes de usarla, confirmar que no incorpora dependencias no aprobadas y registrar origen (`anthropics/skills`) y licencia (Apache 2.0, `LICENSE.txt`).
  8. No modificar la configuración de OpenCode; si fuera imprescindible, detenerse y consultar.
  9. No instalar otras skills ni modificar configuraciones globales.
  10. Si la CLI genera archivos de manifiesto o lock distintos de `skills-lock.json`, o archivos fuera de `.agents/skills/frontend-design/` y `skills-lock.json`, detenerse y consultar antes de incluirlos o modificarlos.
  11. Si falla, documentar y continuar con la dirección visual de la especificación.
- **Verificación:** skill presente en `.agents/skills/frontend-design/`, `skills-lock.json` en la raíz y detectada por OpenCode, o fallo documentado sin instalación global.
- **Nota:** la URL individual de skills.sh no expone el catálogo que consume la CLI; su página publica como comando oficial el de `https://github.com/anthropics/skills --skill frontend-design`. La tabla §13.1 de `spec.md` conserva el dato observado anterior como descriptivo y no normativo.
- **Commit:** incluir `.agents/skills/frontend-design/` y `skills-lock.json`; excluir `.opencode/agents/` y cualquier archivo ajeno.
- **Evidencia:** comandos, ruta dentro del proyecto, confirmación de detección, `computedHash`, origen y licencia; sin secretos.
- **Trazabilidad:** RF-12 (orientación), RNF-04, RNF-05 → CA-13.
- **Prohibido:** usar `-g`, instalar globalmente, instalar otras skills, declararla en `requirements.txt`, instalar dependencias frontend, modificar configuración global o el stack, o incluir en el commit archivos ajenos a `.agents/skills/frontend-design/` y `skills-lock.json` (por ejemplo `.opencode/agents/`).

### T-07 — Crear `base.html` y componentes

- **Objetivo:** establecer el layout global propio.
- **Alcance:** `templates/base.html`, `templates/components/navbar.html`, `templates/components/footer.html`.
- **Dependencias:** T-03, T-06.
- **Pasos:**
  1. Crear HTML5 con `lang="es"`, viewport, título y descripción.
  2. Cargar `main.css` con `{% static %}`.
  3. Añadir skip link, `header`, `main` y `footer`.
  4. Incluir navbar y footer.
  5. Definir bloques `title`, `description`, `content` y `scripts`.
  6. No acceder a `request.user`, `perms` ni `messages` en la home, para preservar la prueba DB-free.
- **Verificación:** carga de plantilla sin errores; estructura semántica.
- **Evidencia:** archivos y revisión visual posterior.
- **Trazabilidad:** RF-12, RNF-04, RNF-05, RNF-06 → CA-12, CA-13.
- **Prohibido:** assets o clases de Unfold, frameworks o datos ficticios.

### T-08 — Crear `home.html`

- **Objetivo:** página informativa de NexoPyme AI sin lógica de negocio.
- **Alcance:** `templates/home.html`.
- **Dependencias:** T-07.
- **Pasos:**
  1. Extender `base.html`.
  2. Definir un único `h1`.
  3. Describir la etapa actual y el enlace a Administración; no enlazar documentación si no existe una ruta que la sirva.
  4. Listar próximos pasos como pendientes de especificación.
  5. No incluir métricas, gráficos ni datos de ejemplo.
  6. No acceder a `request.user`, `perms` ni `messages`.
- **Verificación:** render correcto; sin consultas a base; contenido coherente.
- **Evidencia:** captura y prueba DB-free.
- **Trazabilidad:** RF-03, RF-12, RNF-06 → CA-03, CA-12.
- **Prohibido:** dashboard, indicadores inventados o módulos no implementados.

### T-09 — Crear `main.css`

- **Objetivo:** sistema visual inicial responsive y accesible.
- **Alcance:** `static/css/main.css`.
- **Dependencias:** T-06, T-07.
- **Pasos:**
  1. Definir variables de color, espaciado y tipografía.
  2. Aplicar reset mínimo y estilos de layout.
  3. Estilizar navbar, footer, tarjetas y enlaces.
  4. Añadir breakpoints para 320 px, 768 px, 1440 px y 1920 px.
  5. Añadir `:focus-visible`, skip link y `prefers-reduced-motion`.
- **Verificación:** sin desbordamiento; foco visible; contraste suficiente.
- **Evidencia:** revisión visual en T-16.
- **Trazabilidad:** RF-12, RNF-04, RNF-05, RNF-06 → CA-12, CA-13.
- **Prohibido:** frameworks, fuentes externas o animaciones esenciales.

### T-10 — Ejecutar `migrate --check`

- **Objetivo:** confirmar que no existen migraciones pendientes en la base de desarrollo.
- **Alcance:** ninguna modificación de archivos; conexión a `nexopyme_bootstrap_dev`.
- **Dependencias:** T-03; gate G-3.
- **Pasos:**
  1. Verificar `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306` y `DJANGO_SETTINGS_MODULE=config.settings`.
  2. Ejecutar `python manage.py migrate --check`.
  3. Si no hay pendientes, registrar el resultado.
  4. Si hay pendientes, detenerse, documentar y solicitar G-5; no ejecutar `migrate`.
- **Verificación:** salida sin migraciones pendientes o bloqueo documentado.
- **Evidencia:** comando y salida; identidad de base confirmada sin credenciales.
- **Trazabilidad:** RF-11, RNF-09 → CA-11.
- **Evidencia T-10:** identidad dev verificada (`nexopyme_bootstrap_dev`, `127.0.0.1`, `3306`); `python manage.py migrate --check` exit 0; 18 filas de `django_migrations` fechadas el 2026-11-07; sin acceso a `nexopyme_bootstrap_test`.
- **Prohibido:** `migrate` sin G-5, acceder a `nexopyme_bootstrap_test`, modificar permisos.
- **Desviación controlada (2026-11-09):** durante T-11 se ejecutó accidentalmente `python manage.py migrate` en `nexopyme_bootstrap_dev`. Verificación de `django_migrations`: las 18 filas (`admin`, `auth`, `contenttypes`, `sessions`) son del **2026-11-07** (Bootstrap 000); el comando del 2026-11-09 fue un **no-op** y no aplicó migraciones nuevas. `migrate --check` posterior exit 0; no se revierte, no se ejecutan nuevas migraciones y no se accedió a `nexopyme_bootstrap_test`. G-5 queda regularizado por instrucción del usuario.

### T-11 — Crear superusuario local

- **Objetivo:** crear la cuenta administrativa local de forma interactiva y segura.
- **Alcance:** base `nexopyme_bootstrap_dev`; sin archivos versionados.
- **Dependencias:** T-05, T-10; gate G-3.
- **Pasos:**
  1. Confirmar la identidad de la base de desarrollo y `DJANGO_SETTINGS_MODULE=config.settings`.
  2. Ejecutar `python manage.py createsuperuser`.
  3. Introducir usuario, correo y contraseña de forma interactiva.
  4. Verificar `is_staff` e `is_superuser` sin mostrar el hash ni el correo.
  5. No registrar la contraseña en comandos, archivos ni capturas.
- **Verificación:** cuenta creada; flags correctos; login validado en T-12.
- **Evidencia:** comando y resultado; captura enmascarada; confirmación de ausencia de secretos.
- **Trazabilidad:** RF-09, RNF-02 → CA-09, CA-10.
- **Prohibido:** `DJANGO_SUPERUSER_PASSWORD`, fixtures, scripts, contraseñas en argumentos.
- **Registro de ejecución (2026-11-09):** superusuario creado y verificado por el usuario; `superuser_count=1`, `staff_count=1`, `is_staff=True`, `is_superuser=True`. No se registraron usuario, correo ni contraseña; el login se valida en T-12.

### T-12 — Ejecutar `runserver` y verificar

- **Objetivo:** validar el servidor local, las rutas y el Admin contra MySQL de desarrollo.
- **Alcance:** ejecución local; sin cambios de código salvo correcciones menores aprobadas.
- **Dependencias:** T-04, T-05, T-08, T-09, T-11; gate G-3.
- **Pasos:**
  1. Verificar `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306` y `DJANGO_SETTINGS_MODULE=config.settings`.
  2. Confirmar la configuración efectiva sin credenciales: `python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); django.setup(); from django.conf import settings; db=settings.DATABASES['default']; print(db['ENGINE'], db['HOST'], db['PORT'], db['NAME'])"`, comprobando `127.0.0.1`, `3306` y `nexopyme_bootstrap_dev`.
  3. Configurar `DJANGO_DEBUG=True` y `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost` solo en el entorno local.
  4. Ejecutar `python manage.py runserver 127.0.0.1:8000`.
  5. Verificar `GET /` → 200 y contenido de la home.
  6. Verificar `GET /health/` → 200 `ok`.
  7. Verificar `GET /admin/` → login; autenticar; panel; `GET /admin/auth/user/` y `GET /admin/auth/group/` → 200; logout.
  8. Verificar en el HTML autenticado del Admin que aparecen `SITE_TITLE` y `SITE_HEADER` configurados y no el branding por defecto «Django administration».
  9. Verificar carga de `main.css` y de assets de Unfold.
  10. Detener el servidor y registrar resultados.
- **Verificación:** rutas y Admin funcionan; títulos de Unfold correctos; sin errores de plantilla o estáticos.
- **Evidencia:** estados HTTP, log del servidor y capturas enmascaradas.
- **Trazabilidad:** RF-05, RF-09, RF-10, RF-11, RNF-01, RNF-09 → CA-05, CA-06, CA-07, CA-08, CA-09, CA-11.
- **Prohibido:** base de pruebas, `--insecure` como estrategia principal, dejar el servidor activo.
- **Registro de ejecución (2026-11-09): PASS del usuario.** Seis comprobaciones: `/` 200, `/health/` 200, login/panel de Admin, `/admin/auth/user/` 200, `/admin/auth/group/` 200 y logout funcional con mensaje en español («Has cerrado sesión correctamente en la administración»). Servidor detenido de forma controlada. T-12 cerrada.

### T-13 — Pruebas automatizadas DB-free

- **Objetivo:** cubrir la fundación sin abrir conexión MySQL.
- **Alcance:** `tests/test_project_structure.py`, `test_settings_foundation.py`, `test_home_view.py`, `test_urls.py`, `test_admin_unfold.py`. `tests/test_db_guards.py` es una guarda existente y no se modifica.
- **Dependencias:** T-02–T-09.
- **Pasos:**
  1. Crear las cinco pruebas.
  2. No usar `django_db`, `db`, `transactional_db` ni `django_db_setup`.
  3. Usar `override_settings(ALLOWED_HOSTS=["testserver"])` en la prueba de home.
  4. No acceder a `request.user`, `perms` ni `messages` en las plantillas de la home.
  5. Verificar que las variables de `settings_test` están presentes: `DJANGO_SECRET_KEY`, `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306`, `MYSQL_TEST_USER=nexopyme_test_user` y `MYSQL_TEST_PASSWORD`, con `MYSQL_USER != MYSQL_TEST_USER`. Un valor distinto de `nexopyme_test_user` hace abortar a la guarda.
  6. Ejecutar solo esos archivos con la configuración y guardas existentes.
  7. Incluir aserciones de separación Admin/frontend en `test_project_structure.py`: las plantillas y el CSS propios no referencian `unfold`, y las plantillas de Admin no incluyen `main.css`.
  8. Ejecutar `python -m pytest --setup-show` con la lista explícita de los cinco archivos de la etapa (nunca sin filtro, para no colectar `tests/test_db_guards.py`) y confirmar que no aparece `django_db_setup` ni fixtures de base.
  9. Registrar la suite completa y la prueba `django_db` de `test_db_guards.py` como `NO EJECUTADAS`.
- **Verificación:** pruebas en verde; sin conexión; guardas intactas.
- **Evidencia:** salida de pytest, salida de `--setup-show` y registro de `NO EJECUTADA`.
- **Trazabilidad:** RF-14, RNF-07 → CA-15, CA-16; cobertura adicional de CA-01, CA-02, CA-03, CA-06, CA-08, CA-12 y CA-14.
- **Prohibido:** modificar `conftest.py`, `pytest.ini`, `settings_test.py` o `tests/test_db_guards.py`; ejecutar la suite completa.
- **Registro de ejecución (2026-11-09):** 5 archivos creados; `pytest` con lista explícita → **20 passed**; `pytest --setup-show` sin `django_db_setup` ni fixtures de base; suite completa y `test_db_guards.py::test_connection_targets_test_database` registradas como `NO EJECUTADAS`. Guardas intactas; sin acceso a MySQL. RC-4 APROBADO (2026-11-10); commit por tarea conforme al plan §12.

### T-14 — Ejecutar Ruff

- **Objetivo:** asegurar calidad estática del código modificado.
- **Alcance:** archivos Python de la etapa.
- **Dependencias:** T-01–T-13.
- **Pasos:**
  1. Ejecutar `ruff check .`.
  2. Corregir solo errores introducidos por la etapa.
  3. Si existen errores preexistentes, documentarlos y no corregirlos fuera de alcance.
  4. Ejecutar `ruff format --check .` si el proyecto lo admite.
- **Verificación:** sin errores en los archivos de la etapa.
- **Evidencia:** salida de Ruff.
- **Trazabilidad:** RNF-07 → CA-15.
- **Registro de ejecución (2026-11-09):** `ruff check .` → **All checks passed**, exit 0. `ruff format --check .` señala únicamente deuda preexistente del Bootstrap 000 en `config/settings.py` y `config/settings_test.py`; se documenta y no se reformatea (este último está prohibido de modificar). Sin cambios de archivos; sin commit propio.

### T-15 — Actualizar documentación

- **Objetivo:** dejar la etapa reproducible y comprensible. `MEMORY.md` se actualiza aquí pero se commitea en T-18.
- **Alcance:** `README.md`, `docs/README.md`, `.env.example`, `MEMORY.md` y los artefactos aprobados de `specs/001-django-project-foundation/` (`spec.md`, `plan.md`, `tasks.md`). Los artefactos de `specs/000-project-bootstrap/` ya están versionados y no se modifican.
- **Dependencias:** T-12, T-13, T-14, T-16.
- **Pasos:**
  1. Documentar estructura y versiones.
  2. Documentar Admin, Unfold y re-registro de auth.
  3. Documentar creación y recuperación del superusuario sin secretos.
  4. Documentar variables de entorno, `DJANGO_DEBUG=True` local y ejecución. Explicar que `.env` se carga automáticamente con `load_dotenv(..., override=False)`, que las variables ya exportadas tienen prioridad y que `.env` no se versiona. Documentar que `DJANGO_SECRET_KEY` local se provee fuera de Git y que `.env.example` permanece sin valores reales.
  5. Documentar pruebas DB-free y suite completa `NO EJECUTADA`. Reemplazar explícitamente en `README.md` la instrucción vigente `python -m pytest` y la referencia al uso de `nexopyme_bootstrap_test`.
  6. Corregir en `README.md` y `.env.example` toda afirmación que diga que `.env` no se carga automáticamente.
  7. Registrar comandos, resultados, checklist visual y limitaciones de T-16.
  8. Añadir una tabla `CA-01…CA-18` con el comando/resultado o `NO EJECUTADO` de cada criterio.
  9. Actualizar referencias obsoletas a `specs/001-productos-inventario/` en `README.md`, `docs/README.md` y `MEMORY.md` por `specs/002-productos-inventario/`, sin aprobar ni implementar productos. Registrar en `docs/README.md` como limitaciones aceptadas que `specs/000-project-bootstrap/spec.md` conserva una referencia histórica a `specs/001-productos-inventario/` (R-01 prohíbe modificar el Bootstrap 000) y que `specs/002-productos-inventario/spec.md` conserva internamente el título «Especificación funcional 001» por exigencia de contenido íntegro de D-06.
  10. Verificar ausencia de secretos: escanear también archivos nuevos con `git grep --untracked -n -I -E "(SECRET_KEY|PASSWORD|TOKEN)\s*="` (o `grep -R` sobre `apps/`, `templates/`, `static/`, `docs/`, `tests/`, `config/`, `.env.example`) y confirmar con `git ls-files --others --exclude-standard` los archivos que se versionarán. Documentar que las coincidencias de `.env.example` son placeholders vacíos y no secretos; usar `git ls-files` para confirmar que `.env` y `staticfiles/` no están versionados.
  11. Incorporar al control de versiones los artefactos aprobados de `specs/001-django-project-foundation/` (`spec.md`, `plan.md`, `tasks.md`), verificando su contenido y trazabilidad. Verificar que `specs/000-project-bootstrap/` ya está versionado (`144056c`) y no requiere cambios.
- **Verificación:** documentación coherente, sin secretos ni datos personales; tabla CA completa; `specs/001` versionable y trazable.
- **Evidencia:** archivos actualizados, revisión de enlaces y `git ls-files --others --exclude-standard`.
- **Trazabilidad:** RF-13, RNF-02, RNF-10 → CA-10, CA-17.
- **Registro de ejecución (2026-11-09):** `README.md`, `docs/README.md`, `.env.example` y `MEMORY.md` actualizados; tabla `CA-01…CA-18` y checklist de T-16 incorporados; `specs/001` incorporado al alcance versionable; `specs/000` verificado como ya versionado. RC-4 APROBADO (2026-11-10); commit por tarea conforme al plan §12; `MEMORY.md` se commitea en T-18.

### T-16 — Validación visual y evidencias

- **Objetivo:** validar la interfaz propia y la separación respecto de Admin.
- **Alcance:** home, navbar, footer, CSS, Admin y, por la corrección del favicon, `templates/base.html` y `static/img/favicon.svg`.
- **Dependencias:** home/CSS: T-09 (sin G-3); Admin: T-12 (con G-3 y confirmación de identidad MySQL).
- **Pasos:**
  1. Validación de home/CSS (sin G-3): servir la home y `main.css` sin MySQL mediante `wsgiref.simple_server` + `StaticFilesHandler` con `DEBUG=True` (mecanismo válido aunque el Bootstrap 000 solo usó `wsgiref` + `get_wsgi_application()`) o, si G-3 ya está vigente, con `runserver`. Revisar 320 px, 375 px, 768 px, 1440 px y 1920 px sin desbordamiento; navegación por teclado y foco; `lang="es"`, un `h1`, jerarquía y contraste.
  2. Verificar que la home no usa assets de Unfold y que no muestra datos ficticios.
  3. Validación de Admin (con G-3): verificar `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306` y `DJANGO_SETTINGS_MODULE=config.settings`.
  4. Verificar `GET /admin/auth/user/` y `GET /admin/auth/group/` con estilos de Unfold.
  5. Verificar en el HTML del Admin `SITE_TITLE` y `SITE_HEADER` configurados y ausencia de «Django administration».
  6. Verificar que Admin no usa `main.css`.
  7. Capturar evidencias sin identidad ni datos personales.
  8. Registrar hallazgos y correcciones.
  9. Publicar en `docs/README.md` el checklist y las instrucciones para la validación manual del usuario; no marcar PASS sin su confirmación.
- **Verificación:** checklist completo; separación confirmada.
- **Evidencia:** checklist y capturas enmascaradas.
- **Trazabilidad:** RF-12, RNF-02, RNF-03, RNF-04, RNF-05 → CA-07, CA-10, CA-13, CA-14, CA-17.
- **Registro de ejecución (2026-11-09):** servidor preparado con `DJANGO_DEBUG=True` en `127.0.0.1:8000`; checklist de 320/375/768/1440/1920, teclado, foco, skip link, reduced motion, Admin y separación publicado en `docs/README.md`.
- **Validación (2026-11-10):** aprobada explícitamente por el usuario. Batería automatizada con Chrome DevTools MCP sobre Brave aislado en 320/375/768/1440/1920 px: sin desbordamiento horizontal, consola sin mensajes, un `h1`, `lang="es"`, CTA y footer visibles; teclado, foco, skip link y `prefers-reduced-motion` verificados; Admin con Unfold y sin `main.css`. Hallazgo corregido: `/favicon.ico` 404 sustituido por `static/img/favicon.svg` con `rel="icon"` en `templates/base.html`. **CA-13 en PASS.** El Admin (Unfold) conserva la solicitud de `/favicon.ico`; corregirlo queda fuera del alcance aprobado.

### T-17 — Revisión final del Reviewer

- **Objetivo:** obtener el veredicto técnico final y verificar que cada tarea con archivos versionables tenga su commit y push.
- **Alcance:** implementación, pruebas, Ruff, documentación, evidencias y trazabilidad Git.
- **Dependencias:** T-01–T-16.
- **Pasos:**
  1. Entregar al Reviewer el informe de implementación, las evidencias y la lista de commits por tarea.
  2. Verificar la trazabilidad RF/RNF → CA → tareas.
  3. Verificar que cada tarea con archivos versionables tiene su commit (solo con archivos de esa tarea) y su push, y que las tareas sin archivos no generan commit.
  4. Si hay hallazgos, el Implementer los corrige bajo la tarea afectada; el Reviewer emite un nuevo APROBADO en la re-revisión y solo entonces se commitean con `fix:`. No se reutiliza el APROBADO anterior.
  5. Repetir la revisión si el veredicto es CAMBIOS NECESARIOS.
- **Verificación:** veredicto APROBADO y commits/push por tarea completos.
- **Evidencia:** informe del Reviewer, hashes de commit por tarea y estado remoto.
- **Trazabilidad:** todos los requisitos y criterios.

### T-18 — Cierre documental y verificación Git

- **Objetivo:** cerrar la etapa actualizando `MEMORY.md` y verificando que todos los commits y push por tarea estén completos conforme a `AGENTS.md` §9.
- **Alcance:** `MEMORY.md` (commit propio) y verificación de Git; no incluye archivos de otras tareas.
- **Dependencias:** T-17 APROBADO y commits/push de T-01–T-16 completados; gate G-6.
- **Política de commits:** T-18 tiene un único commit propio que incluye solo `MEMORY.md`. No agrupa cambios de otras tareas ni sustituye los commits por tarea. El APROBADO de T-17 cubre el cierre documental de T-18; si el contenido de `MEMORY.md` excede ese alcance, detenerse y solicitar revisión.
- **Pasos:**
  1. Actualizar `MEMORY.md` con el estado final de la etapa y próximos pasos (máximo 40 líneas), incluida la referencia a `specs/002-productos-inventario/` y la eliminación de la referencia obsoleta a `specs/001-productos-inventario/`.
  2. Build verifica que el contenido de `MEMORY.md` corresponde al alcance documental de la etapa antes de autorizar su commit.
  3. Implementer ejecuta `git add MEMORY.md` y `git commit` con Conventional Commit en inglés.
  4. Build verifica que cada commit de T-01–T-16 corresponde a su tarea, que el informe contiene pruebas y Ruff en verde y que existe APROBADO, y confirma que ya fue publicado; si queda algún push pendiente, lo ejecuta a `main`.
  5. Verificar `git status`, `git log` y `origin/main...HEAD`; confirmar que no quedan cambios sin commitear.
  6. Informar el resultado al usuario.
- **Verificación:** `MEMORY.md` actualizado; commits por tarea y push completados; árbol limpio.
- **Evidencia:** hash del commit de T-18, lista de hashes por tarea, estado de rama e informe.
- **Trazabilidad:** todos los requisitos y criterios.
- **Prohibido:** `amend`, `force push`, operaciones destructivas, incluir archivos de otras tareas en el commit de T-18, agrupar la etapa en un único commit.

## 6. Puntos de revisión del Reviewer

| Checkpoint | Momento | Alcance | Resultado esperado |
|---|---|---|---|
| RC-1 | Antes de implementar | `plan.md` y `tasks.md` | APROBADO / CAMBIOS NECESARIOS |
| RC-2 | Tras T-01–T-05 | Instalación, estructura, settings, Admin/Unfold | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-3 | Tras T-06–T-12 | Skill, frontend, rutas, Admin, MySQL dev, estáticos | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-4 | Tras T-13–T-16 | Pruebas, Ruff, documentación y validación visual | APROBADO / CAMBIOS NECESARIOS por tarea |

En RC-2, RC-3 y RC-4 el Reviewer emite un veredicto individual por cada tarea incluida; solo las tareas con APROBADO se commitean. T-17 revisa el conjunto completo.

## 7. Matriz de trazabilidad por tarea

| Tarea | RF/RNF | CA |
|---|---|---|
| P-02 | RF-15 | CA-18 |
| T-01 | RF-06, RNF-01, RNF-08 | CA-06 |
| T-02 | RF-01 | CA-01 |
| T-03 | RF-02, RF-06, RF-07, RNF-08 | CA-02, CA-06, CA-07 |
| T-04 | RF-04, RF-05 | CA-04, CA-05 |
| T-05 | RF-08 | CA-08 |
| T-06 | RF-12, RNF-04, RNF-05 | CA-13 |
| T-07 | RF-12, RNF-04, RNF-05, RNF-06 | CA-12, CA-13 |
| T-08 | RF-03, RF-12, RNF-06 | CA-03, CA-12 |
| T-09 | RF-12, RNF-04, RNF-05, RNF-06 | CA-12, CA-13 |
| T-10 | RF-11, RNF-09 | CA-11 |
| T-11 | RF-09, RNF-02 | CA-09, CA-10 |
| T-12 | RF-05, RF-09, RF-10, RF-11, RNF-01, RNF-09 | CA-05, CA-06, CA-07, CA-08, CA-09, CA-11 |
| T-13 | RF-14, RNF-07 | CA-01, CA-02, CA-03, CA-06, CA-08, CA-12, CA-14, CA-15, CA-16 |
| T-14 | RNF-07 | CA-15 |
| T-15 | RF-13, RNF-02, RNF-10 | CA-10, CA-17 |
| T-16 | RF-12, RNF-02, RNF-03, RNF-04, RNF-05 | CA-07, CA-10, CA-13, CA-14, CA-17 |
| T-17 | Todos | Todos |
| T-18 | Todos | Todos |

## 8. Orden de ejecución

```text
Plan aprobado
  ├─ T-01 ── T-02 ── T-03
  │                   ├─ T-04 ──────────┐
  │                   ├─ T-05 ──────────┤
  │                   └─ T-10 ── T-11 ──┤
  └─ T-06 ── T-07 ── T-08 ── T-09 ──────┤
T-04 + T-05 + T-08 + T-09 + T-11 ── T-12
T-02..T-09 ── T-13 ── T-14
T-09 + T-12 ── T-16 ── T-15 ── T-17 ── T-18
```

## 9. Autorizaciones requeridas

| Gate | Tareas afectadas | Estado |
|---|---|---|
| G-0 Aprobación del plan y tareas | Todas | Aprobado por el usuario el 2026-11-09 |
| G-1 Autorización de implementación | T-01–T-05, T-07–T-09, T-13–T-16 | Aprobado por el usuario el 2026-11-09; flujo Git por tarea |
| G-2 Instalación de dependencias | T-01 | Aprobado: `django-unfold==0.110.1` y `python-dotenv==1.2.4` (regularizado el 2026-11-09) |
| G-3 Operaciones MySQL dev | T-10, T-11, T-12, T-16 (solo la parte de Admin) | Alcance autorizado; T-10/T-11/T-12 ejecutadas y verificadas; T-16 (Admin) validada y aprobada por el usuario el 2026-11-10 |
| G-4 Instalación de `frontend-design` | T-06 | Aprobado; skill instalada en `.agents/skills/frontend-design` |
| G-5 Migración real | T-10 condicional | Regularizado el 2026-11-09 para el `migrate` accidental no-op; no autoriza nuevas migraciones |
| G-6 Commit y push por tarea | Tareas con archivos versionables en RC-2, RC-3, RC-4, T-17 y T-18 | Build verifica §9; no requiere autorización adicional |

## 10. Estado de las tareas

- `[x]` T-01–T-05: implementadas, aprobadas en RC-2, commitadas y publicadas (`b214669`, `3cd049a`, `c4c3098`, `55c7674`, `f126c1a`).
- `[x]` T-10: identidad dev verificada y `migrate --check` exit 0; `migrate` accidental del 2026-11-09 fue no-op.
- `[x]` T-11: superusuario creado y verificado (count 1, flags true), sin identidad registrada.
- `[x]` T-06–T-09: implementadas, aprobadas en RC-3, commitadas y publicadas (`064789e`, `1061db1`, `9eadf7a`, `fb810de`).
- `[x]` T-12: validación visual y funcional PASS del usuario; logout en español; servidor detenido.
- `[x]` T-13: 20 pruebas DB-free en verde; cinco archivos aprobados en RC-4 (2026-11-10); commit por tarea conforme al plan §12.
- `[x]` T-14: `ruff check .` verde; deuda de formato preexistente documentada, sin cambios.
- `[x]` T-15: documentación actualizada (`README.md`, `docs/README.md`, `.env.example`, `specs/001`); aprobada en RC-4 (2026-11-10); commit por tarea conforme al plan §12; `MEMORY.md` se commitea en T-18.
- `[x]` T-16: validación visual y funcional aprobada explícitamente por el usuario el 2026-11-10; favicon SVG corregido; CA-13 en PASS; commit por tarea conforme al plan §12.
- `[ ]` T-17–T-18: no iniciadas.
- P-01 y P-02 están completados.
- RC-3 aprobado; la regularización i18n está aprobada y publicada (`dce246b`).

---

**Fin de las tareas v1.5.** La v1.0 fue aprobada en RC-1; la v1.1, v1.2 y v1.3 en revisión delta. RC-3 está aprobado. RC-4 está aprobado para T-13–T-16, incluida la corrección del favicon y CA-13 en PASS. Quedan T-17 y T-18. G-0/G-1 ya fueron concedidas.

