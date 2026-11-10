# Documentación — NexoPyme AI

Guía de la **Etapa 001 — Django Project Foundation** y de la fundación técnica
del proyecto. El Bootstrap 000 permanece cerrado y no se modifica.

## Contenido

- `specs/000-project-bootstrap/spec.md`, `plan.md`, `tasks.md`: Bootstrap 000
  cerrado y versionado.
- `specs/001-django-project-foundation/spec.md`: especificación v1.1 aprobada.
- `specs/001-django-project-foundation/plan.md`: plan técnico v1.5.
- `specs/001-django-project-foundation/tasks.md`: tareas v1.5 y trazabilidad.
- `specs/002-productos-inventario/spec.md`: especificación renumerada, no
  aprobada ni implementada.

Los artefactos de la Etapa 001 forman parte del alcance versionable de T-15. Los
artefactos de la Etapa 000 ya estaban versionados en `144056c` y se verificaron
sin modificar su contenido.

## Estructura de la etapa

```text
apps/
├── __init__.py
└── core/
    ├── __init__.py
    ├── admin.py           # Re-registro Unfold de User/Group
    └── apps.py            # CoreConfig, sin modelos
config/
├── settings.py            # TEMPLATES, STATIC*, INSTALLED_APPS, UNFOLD, i18n
├── urls.py                # admin/, home, health/
└── views.py               # home y health
docs/
└── README.md              # Esta guía
locale/
└── es_AR/LC_MESSAGES/     # Catálogo mínimo del logout
specs/
├── 000-project-bootstrap/
├── 001-django-project-foundation/
└── 002-productos-inventario/
static/
├── css/main.css
└── img/favicon.svg
templates/
├── base.html
├── home.html
└── components/
    ├── navbar.html
    └── footer.html
tests/
├── test_db_guards.py      # Guarda existente; no modificar
├── test_project_structure.py
├── test_settings_foundation.py
├── test_home_view.py
├── test_urls.py
└── test_admin_unfold.py
```

`apps/core` es una aplicación de infraestructura sin modelos, migraciones ni
servicios de negocio. No se crearon aplicaciones funcionales.

## Configuración aplicada

### Plantillas y estáticos

- `TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]`.
- `STATICFILES_DIRS = [BASE_DIR / "static"]`.
- `STATIC_ROOT = BASE_DIR / "staticfiles"` (no versionado).
- `STATIC_URL = "static/"`.

### Admin y Unfold

- `django-unfold==0.110.1` en `requirements.txt`.
- `"unfold"` antes de `"django.contrib.admin"` en `INSTALLED_APPS`.
- `"apps.core"` al final para que `apps/core/admin.py` se autodescubra.
- `UNFOLD` con `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER` y `SITE_URL`.
- `User` y `Group` re-registrados con `unfold.admin.ModelAdmin` y los formularios
  `AdminPasswordChangeForm`, `UserChangeForm` y `UserCreationForm`.
- Sin módulos `unfold.contrib.*` ni overrides de plantillas del Admin.

### Internacionalización

- `LANGUAGE_CODE = "es-ar"`.
- `TIME_ZONE = "America/Argentina/Buenos_Aires"`.
- `USE_I18N = True` y `USE_TZ = True`.
- `LOCALE_PATHS = [BASE_DIR / "locale"]`.
- Catálogo mínimo `locale/es_AR/LC_MESSAGES/django.po|.mo` con la traducción de
  «You have been successfully logged out from the administration» a «Has cerrado
  sesión correctamente en la administración». No se modificaron plantillas del
  Admin.

### Carga de `.env`

`config/settings.py` ejecuta `load_dotenv(BASE_DIR / ".env", override=False)`:

- `.env` se carga automáticamente al iniciar los settings;
- las variables ya exportadas en el proceso tienen prioridad;
- `.env` está ignorado por Git y no se versiona;
- `.env.example` solo contiene nombres y placeholders vacíos.

## Superusuario local

Creación interactiva:

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

No se registran identidad, correo, contraseña ni hash. La verificación de T-11
confirmó `superuser_count=1`, `staff_count=1`, `is_staff=True` e
`is_superuser=True`; T-12 confirmó el login y el logout.

## Ejecución local

```powershell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
python manage.py runserver 127.0.0.1:8000
```

`DJANGO_DEBUG=True` es exclusivamente local para que `runserver` sirva estáticos.
El default del repositorio permanece `False`; no se usa `collectstatic` ni
`runserver --insecure` como estrategia principal.

Rutas:

- `http://127.0.0.1:8000/` — portada informativa.
- `http://127.0.0.1:8000/health/` — HTTP 200 `text/plain`, cuerpo `ok`.
- `http://127.0.0.1:8000/admin/` — login y panel con Unfold.

## Pruebas y calidad

### Pruebas DB-free

```powershell
python -m pytest tests/test_project_structure.py tests/test_settings_foundation.py tests/test_home_view.py tests/test_urls.py tests/test_admin_unfold.py
```

Resultado registrado en T-13: **20 passed**. La ejecución con `--setup-show` y la
misma lista no mostró `django_db_setup` ni fixtures de base de datos.

La suite completa de pytest está **NO EJECUTADA** porque usaría
`nexopyme_bootstrap_test`, base prohibida en esta etapa. `tests/test_db_guards.py`
no se modificó y su prueba con `django_db` quedó **NO EJECUTADA**.

### Ruff

```powershell
ruff check .
```

Resultado registrado en T-14: **All checks passed**. `ruff format --check .`
señala solo deuda de formato preexistente del Bootstrap 000 en
`config/settings.py` y `config/settings_test.py`; no se reformateó fuera de
alcance.

### Comprobaciones Django

```powershell
python manage.py check
python manage.py migrate --check
```

Resultados registrados: `check` sin errores; `migrate --check` exit 0, sin
migraciones pendientes. Las 18 migraciones iniciales son del 2026-11-07
(Bootstrap 000). El `migrate` accidental del 2026-11-09 fue un no-op.

## Validación visual T-16

T-16 fue **revisada y aprobada explícitamente por el usuario** el 2026-11-10. La
batería automatizada con Chrome DevTools MCP sobre una instancia aislada de Brave
cubrió 320, 375, 768, 1440 y 1920 px, además de teclado, foco, skip link,
movimiento reducido, Admin y separación de assets. CA-13 queda en PASS.

### Preparación

1. Build inicia el servidor en `http://127.0.0.1:8000` con `DJANGO_DEBUG=True`.
2. Abrir la portada y el Admin en el navegador.
3. Usar las herramientas de desarrollo (F12) para el modo responsive.
4. No capturar identidad, correo ni contraseña del superusuario.

### Viewports

Revisar la portada en:

- 320 px
- 375 px
- 768 px
- 1440 px
- 1920 px

En cada ancho comprobar:

- [ ] No hay desplazamiento horizontal
      (`document.documentElement.scrollWidth <= window.innerWidth`).
- [ ] La navbar, el contenido y el footer permanecen visibles y legibles.
- [ ] El texto no se solapa ni se corta.
- [ ] El enlace «Abrir Administración» sigue siendo accesible.

### Portada y contenido

- [ ] `lang="es"` en el elemento `html`.
- [ ] Un solo `h1` con «NexoPyme AI».
- [ ] Se muestra «Etapa 001 — Django Project Foundation».
- [ ] Los próximos pasos aparecen como «Pendiente de especificación».
- [ ] No hay métricas, gráficos, tablas ni datos ficticios.
- [ ] El footer muestra la identidad, la etapa y el año.

### Navegación, teclado y foco

- [ ] El primer `Tab` desde la barra de direcciones muestra el enlace «Saltar al
      contenido principal».
- [ ] `Enter` sobre el skip link lleva el foco al contenido principal.
- [ ] El orden de tabulación es: skip link → marca → Inicio → Administración →
      Abrir Administración → footer.
- [ ] Cada elemento enfocado muestra un indicador de foco visible.
- [ ] `Shift+Tab` recorre el orden inverso sin perder el foco.

### Movimiento reducido

- [ ] En DevTools → Rendering → «Emulate CSS media feature
      prefers-reduced-motion: reduce», la página sigue siendo usable y no hay
      animaciones esenciales.
- [ ] No hay transiciones o animaciones que impidan leer o navegar.

### Admin Unfold

- [ ] `GET /admin/` sin sesión muestra el login.
- [ ] El login y el panel usan los estilos de Unfold.
- [ ] El título y el encabezado muestran «NexoPyme AI» y no «Django
      administration».
- [ ] `GET /admin/auth/user/` responde 200 con estilos de Unfold.
- [ ] `GET /admin/auth/group/` responde 200 con estilos de Unfold.
- [ ] El logout funciona y muestra «Has cerrado sesión correctamente en la
      administración».

### Separación Admin/frontend

- [ ] La portada no carga assets de `unfold/` (revisar la pestaña Network).
- [ ] El Admin no carga `static/css/main.css` (revisar la pestaña Network).
- [ ] Las plantillas y estilos propios no extienden ni importan Unfold.

### Hallazgo y corrección (2026-11-10)

- `/favicon.ico` devolvía 404 en todos los anchos y generaba un error de consola.
  Se agregó `static/img/favicon.svg` y su `rel="icon"` con `{% static %}` en
  `templates/base.html`; la portada ya no solicita `/favicon.ico` y la consola
  queda sin mensajes.
- Las páginas de Admin (Unfold) no usan `base.html` y conservan la solicitud de
  `/favicon.ico`; corregirlo exigiría modificar plantillas de Unfold o agregar una
  ruta, fuera del alcance aprobado.
- La alineación variable de «Pendiente de especificación» en 320 px se acepta como
  cosmética. Los textos en inglés y el acento violeta de Unfold se registran como
  mejora futura fuera del alcance actual.

### Registro de resultados

Registrar por cada punto `PASS` o `FAIL`, el viewport y una nota breve. Si hay
`FAIL`, indicar el ancho, el elemento afectado y el comportamiento observado.
Las capturas deben estar enmascaradas y sin datos personales.

La batería automatizada del 2026-11-10 verificó los puntos de viewports, portada,
teclado, foco, skip link, movimiento reducido, Admin y separación de assets; el
usuario aprobó el resultado. Las casillas se mantienen como plantilla de revisión
manual.

## Criterios de aceptación

| CA | Estado | Evidencia (comando/resultado) |
|---|---|---|
| CA-01 | PASS | `pytest tests/test_project_structure.py` (5 pruebas) y `git ls-files`; estructura mínima sin apps funcionales ni modelos. |
| CA-02 | PASS | `pytest tests/test_settings_foundation.py` (6 pruebas) y `python manage.py check` sin errores. |
| CA-03 | PASS | `pytest tests/test_home_view.py`; `GET /` 200 con `home.html`, sin datos ficticios ni base. |
| CA-04 | PASS | `pytest tests/test_urls.py`; `GET /health/` 200 `text/plain`, cuerpo `ok`. |
| CA-05 | PASS | T-12: login, panel autenticado y logout verificados por el usuario. |
| CA-06 | PASS | `requirements.txt` con `django-unfold==0.110.1`; `INSTALLED_APPS` correcto; `pip check` y `manage.py check` sin errores. |
| CA-07 | PASS | T-12: Admin con `SITE_TITLE`/`SITE_HEADER` de NexoPyme AI y estilos de Unfold. |
| CA-08 | PASS | T-12: `/admin/auth/user/` y `/admin/auth/group/` 200 con Unfold. |
| CA-09 | PASS | T-11: superusuario con `is_staff=True` e `is_superuser=True`; T-12: login correcto; identidad no registrada. |
| CA-10 | PASS | Escaneo de secretos y `git ls-files`; `.env` no versionado y `.env.example` con placeholders vacíos. |
| CA-11 | PASS | `migrate --check` exit 0; `runserver` contra `nexopyme_bootstrap_dev`; sin acceso a `nexopyme_bootstrap_test`. |
| CA-12 | PASS | `pytest tests/test_project_structure.py`; plantillas y `main.css` presentes; sin frameworks adicionales. |
| CA-13 | PASS | T-16: validación visual 320/375/768/1440/1920 sin desbordamiento; teclado, foco, skip link y `prefers-reduced-motion` verificados; aprobada explícitamente por el usuario el 2026-11-10. |
| CA-14 | PASS | `pytest tests/test_project_structure.py`; portada sin Unfold y Admin sin `main.css`. |
| CA-15 | PASS | `pytest` DB-free: 20 passed; `ruff check .`: All checks passed. |
| CA-16 | NO EJECUTADO | Suite completa prohibida por `nexopyme_bootstrap_test`; estrategia DB-free aplicada y registrada. |
| CA-17 | PASS | `README.md` y este documento actualizados; tabla CA con evidencia y `NO EJECUTADO`. |
| CA-18 | PASS | `specs/002-productos-inventario/spec.md` con SHA-256 `DBDFB6A1FF5342F54F42BC1D6B73F3D3E89216504750F290B9238D2CB0AE923E`; `specs/001-productos-inventario/` no existe; sin aprobar ni implementar. |

## Limitaciones aceptadas

- `specs/000-project-bootstrap/spec.md` conserva una referencia histórica a
  `specs/001-productos-inventario/`; R-01 prohíbe modificar el Bootstrap 000. La
  referencia vigente es `specs/002-productos-inventario/`.
- `specs/002-productos-inventario/spec.md` conserva internamente el título
  «Especificación funcional 001» por la exigencia de contenido íntegro de D-06.
  No está aprobada ni implementada.
- La suite completa de pytest queda fuera de alcance por depender de la base de
  pruebas prohibida.
- `specs/001-django-project-foundation/spec.md` conserva en §1 y §17.2 el estado
  de la aprobación (RC-3 y T-12 pendientes). Es una instantánea no normativa del
  momento de aprobación; el estado operativo vigente se registra en `plan.md` y
  `tasks.md`.
- `ruff format --check .` mantiene deuda de formato preexistente del Bootstrap
  000; no se corrige fuera de alcance.
- Windows 11 no se probó independientemente.

## Evidencias

- T-12: home 200, health 200, login/panel, `User`/`Group` 200 y logout con
  mensaje en español; servidor detenido de forma controlada.
- T-13: 20 pruebas DB-free en verde; sin fixtures de base.
- T-14: Ruff sin errores; deuda de formato preexistente documentada.
- T-15: documentación actualizada; artefactos de la Etapa 001 incorporados al
  alcance versionable de la tarea.
- T-16: batería automatizada con Chrome DevTools MCP sobre Brave aislado en
  320/375/768/1440/1920 px sin desbordamiento, consola limpia y favicon SVG
  servido con 200; teclado, foco, skip link y movimiento reducido verificados;
  aprobada explícitamente por el usuario.
