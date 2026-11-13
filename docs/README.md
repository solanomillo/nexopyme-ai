# Documentación — NexoPyme AI

Guía de las etapas **001 — Django Project Foundation**, **003 — Cuentas y
multiempresa** y **004 — Rediseño visual**, y de la fundación técnica del
proyecto. El Bootstrap 000 permanece cerrado y no se modifica.

## Contenido

- `specs/000-project-bootstrap/spec.md`, `plan.md`, `tasks.md`: Bootstrap 000
  cerrado y versionado.
- `specs/001-django-project-foundation/spec.md`: especificación v1.1 aprobada.
- `specs/001-django-project-foundation/plan.md`: plan técnico v1.6.
- `specs/001-django-project-foundation/tasks.md`: tareas v1.6 y trazabilidad.
- `specs/002-productos-inventario/spec.md`: especificación renumerada, no
  aprobada ni implementada.
- `specs/003-cuentas-multiempresa/spec.md`: especificación v1.0 aprobada el
  2026-11-10.
- `specs/003-cuentas-multiempresa/plan.md`: plan técnico v1.4.
- `specs/003-cuentas-multiempresa/tasks.md`: tareas y trazabilidad de la etapa.
- `specs/004-rediseno-visual/spec.md`: especificación v0.1 aprobada en G-0a el
  2026-11-12.
- `specs/004-rediseno-visual/plan.md`: plan técnico v0.1 aprobado en G-0b.
- `specs/004-rediseno-visual/tasks.md`: tareas, trazabilidad y evidencia T-10/RC-10.

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

### Estructura de la Etapa 003

```text
apps/
├── accounts/
│   ├── capabilities.py        # Role, Capability, ROLE_CAPABILITIES
│   ├── context_processors.py  # panel_navigation (enlaces por capacidad)
│   ├── models.py              # Account, Company, Membership
│   ├── services.py            # Empresa, membresía y contraseñas
│   ├── emails.py              # Normalización y limpieza de correos
│   ├── forms.py               # Formularios del panel y de la empresa
│   ├── middleware.py          # ActiveCompanyMiddleware
│   ├── decorators.py          # require_capability y denegaciones
│   ├── backends.py            # EmailBackend y TechnicalAdminBackend
│   ├── views.py               # Panel comercial y gestión
│   ├── urls.py                # Rutas del namespace accounts
│   ├── admin.py               # Admin técnico acotado
│   ├── migrations/0001_initial.py
│   └── management/commands/   # init_company, reset_owner_password
└── audit/
    ├── models.py              # AuditEvent, SecurityEvent
    ├── services.py            # record_audit, record_security
    └── migrations/0001_initial.py
config/
├── settings.py                # Middleware, backends, cookies y logging
└── urls.py                    # handler403 y handler404 con no-store
templates/
├── base.html                  # Bloque site_header y pie compartido
├── base_panel.html            # Panel, navegación por capacidad
├── home.html                  # Portada con la etapa actual
├── accounts/                  # login, panel, perfil, usuarios, empresa, auditoría
├── components/
│   ├── footer.html            # Pie único de todas las plantillas
│   ├── navbar.html            # Navegación pública
│   └── error_header.html      # Cabecera mínima de errores
└── errors/                    # 403 y 404 con recuperación
tests/
├── conftest.py                # Fixtures de empresa, cuenta y membresía
├── test_accounts_*.py         # Capacidades, auth, autorización, aislamiento,
│                              # middleware, usuarios, empresa, auditoría,
│                              # seguridad, comandos, formularios e integración
├── test_accounts_navigation.py  # Navegación por capacidad y errores (T-24, T-25)
└── test_db_guards.py          # Guarda existente; no modificar
```

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
- [ ] Se muestra la etapa vigente: en la revisión de T-16 era «Etapa 001 —
      Django Project Foundation»; desde T-24 el pie único muestra «Etapa 003 —
      Cuentas y multiempresa».
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

## Validación visual T-23 — Cuentas y multiempresa

Fecha: 2026-11-12. Entorno: `nexopyme_bootstrap_dev` con datos ficticios
sembrados por ORM (`Bodega La Esquina` con dueña, encargado, operador, consulta
e inactivo; `Almacén Vacío` sin empleados ni auditoría). Servidores locales:
`127.0.0.1:8000` con `DJANGO_DEBUG=True` y `127.0.0.1:8001` con
`DJANGO_DEBUG=False --insecure`.

### Evidencias automatizadas

| Punto | Resultado |
|---|---|
| Viewports 320/375/768/1440/1920 px | PASS — 0 px de desbordamiento en `/login/`, `/panel/`, `/users/`, `/company/`, `/audit/`, `/profile/`, `/password/` y `/users/new/` |
| Zoom 200 % | PASS — 0 px de desbordamiento en `/users/` y `/audit/`; tablas con desplazamiento interno |
| Teclado y foco | PASS — orden de tabulación completo y foco visible de 2 px (`tab-order.json`); skip link oculto que aparece al enfocar y mueve el foco a `#contenido` (`skip-link.json`); contenedores `.table-scroll` enfocables con `role="region"` y desplazamiento con flechas |
| Etiquetas y errores | PASS — 0 controles sin etiqueta; `aria-invalid` + `aria-describedby` en correo duplicado y contraseña incorrecta; 403 de capacidad y de contexto validados, con botón de cierre de sesión estilizado en la variante de contexto |
| Tablas | PASS — `caption` y `scope="col"` en usuarios y auditoría; contenedores desplazables accesibles por teclado |
| Objetivos táctiles | PASS — 0 controles visibles menores a 24×24 px |
| Contraste | PASS — 13,58:1 texto, 6,40:1 texto suave, 6,89:1 botón, 6,69:1 borde de control y 9,44:1 error |
| Movimiento reducido | PASS — `scroll-behavior: auto` y transición de ~0 s con `prefers-reduced-motion` |
| Estados | PASS — vacío (auditoría), error (login, alta, contraseña, 403 de capacidad y de contexto, 404), carga (`aria-busy`), confirmación (rol y contraseña temporal) y éxito (empresa) |
| 404 con `DEBUG=False` | PASS — 404 uniforme con `Cache-Control: no-store` |
| Admin/panel | PASS — `/admin/` redirige a `/admin/login/`, sin sesión comercial ni `main.css` |
| Aislamiento | PASS — la empresa ajena no aparece en `/users/` |

### Hallazgos corregidos

- Desbordamiento horizontal de las tablas de `/users/` y `/audit/` a 320/375 px
  (431/376 px). Se añadió `.table-scroll` en `user_list.html` y `audit_list.html`,
  y estilos de panel, tablas, formularios y paginación en `static/css/main.css`.
- Borde de controles con contraste 1,98:1; se cambió a `--color-ink-soft`
  (6,69:1) para cumplir el mínimo de 3:1 en componentes.
- Los contenedores `.table-scroll` quedaron enfocables (`tabindex="0"`,
  `role="region"` y `aria-label`) para que el contenido desplazable sea
  alcanzable con teclado; las flechas desplazan la tabla.
- El botón «Cerrar sesión» del 403 de contexto recibió `class="button
  button--primary"`; antes se renderizaba como botón nativo sin estilo.

### Capturas y artefactos

30 capturas numeradas en `<TEMP>\opencode\t23\`
(de `01-login-1440.png` a `24-not-found-1440.png`, con variantes de 320 y 1440
px), más `20b-forbidden-context-1440.png`, `tab-order.json`, `skip-link.json`,
`fix-verification.json` y los scripts de validación, fuera del repositorio.

### Observaciones

- El pie de las páginas que usan `base.html` (login, 403 y 404) conservaba
  «Etapa 001 — Django Project Foundation»; el panel usaba «Etapa 003». **Corregido
  en T-24 (2026-11-12):** `templates/components/footer.html` es el pie único con
  «Etapa 003 — Cuentas y multiempresa», y `base.html` y `base_panel.html` lo
  incluyen. Evidencia: `tests/test_accounts_navigation.py` verifica la etiqueta en
  login, panel, home, 403 y 404, y que «Etapa 001 — Django Project Foundation» ya
  no aparece; el panel renderiza un solo `<footer>`.
- El 403 y el 404 no ofrecían una acción de recuperación («Volver al panel» o
  «Iniciar sesión») y, al extender `base.html`, mostraban la navegación pública
  («Inicio» y «Administración») a una cuenta comercial autenticada. **Corregido en
  T-24 (2026-11-12):** las páginas de error sobrescriben el bloque `site_header`
  con `templates/components/error_header.html`, sin navegación pública; el 403 de
  capacidad ofrece «Volver al panel», el 403 de contexto ofrece «Cerrar sesión»
  con CSRF, el 404 autenticado ofrece «Volver al panel» y el 404 anónimo ofrece
  «Iniciar sesión». Se conservan `Cache-Control: no-store`, la uniformidad del 404
  y el logout por POST. Evidencia: `tests/test_accounts_navigation.py` (403 de
  capacidad y de contexto, 404 autenticado y anónimo, ausencia de `href="/admin/"`
  y de «Administración» en los errores).
- La navegación del panel mantenía visibles «Usuarios», «Empresa» y
  «Auditoría» para roles sin la capacidad correspondiente; el servidor responde
  403. **Corregido en T-24 (2026-11-12):** el context processor
  `apps.accounts.context_processors.panel_navigation` deriva `panel_nav` del rol de
  `request.membership` y `base_panel.html` envuelve cada enlace en
  `{% if panel_nav.users %}`, `{% if panel_nav.company %}` y
  `{% if panel_nav.audit %}`; los `href` usan `{% url %}`. Evidencia:
  `tests/test_accounts_navigation.py` comprueba que el dueño ve los tres enlaces,
  que encargado y consulta no los ven y que el servidor sigue respondiendo 403 con
  `no-store` a `/users/`, `/company/` y `/audit/`.
- El Admin Unfold conserva textos en inglés y acento violeta (limitación de la
  Etapa 001).
- El estado vacío de `/users/` no es alcanzable porque toda empresa conserva su
  dueño; la rama vacía existe como defensa. La captura correspondiente se
  denomina `22-single-member-1440.png` para no confundirla con un estado vacío.
- Checklist visual aprobado explícitamente por el usuario el 2026-11-12.
  Dictamen del Reviewer: APROBADO (2026-11-12).

## Etapa 003 — Cuentas y multiempresa

Implementación por tarea de la especificación 003 v1.0, el plan v1.4 y las tareas
de la etapa. T-01 a T-26 están cerradas y la Etapa 003 quedó cerrada el
2026-11-12; la Etapa 004 quedó cerrada el 2026-11-13. Toda la persistencia
operativa vive en MySQL 8.x (`nexopyme_bootstrap_dev` para desarrollo y
`nexopyme_bootstrap_test` para pruebas, autorizada por `DA-07`).

### Roles y capacidades

Roles fijos de la V1 (`Role`): `dueno`, `encargado`, `operador` y `consulta`. Las
capacidades (`Capability`) usan el patrón `recurso.accion` y se evalúan en
`apps/accounts/capabilities.py`:

| Rol | Capacidades |
|---|---|
| Dueño | Todas |
| Encargado | `producto.consultar`, `historial.consultar`, `producto.crear`, `producto.editar`, `producto.desactivar`, `movimiento.entrada`, `movimiento.salida`, `movimiento.ajustar`, `existencia.inicializar` |
| Operador | `producto.consultar`, `historial.consultar`, `movimiento.entrada`, `movimiento.salida` |
| Consulta | `producto.consultar`, `historial.consultar` |

`has_capability` deniega por defecto ante roles o capacidades desconocidos. Las
vistas se protegen con `require_capability` y los servicios repiten la validación;
un enlace oculto nunca sustituye la autorización del servidor.

### Rutas

| Ruta | Acceso | Función |
|---|---|---|
| `/login/` | Anónimo | Acceso con correo y contraseña |
| `/logout/` | Autenticado (POST) | Cierre de sesión con CSRF |
| `/panel/` | Membresía activa | Panel comercial de la empresa activa |
| `/profile/`, `/profile/<id>/` | Membresía activa | Perfil propio |
| `/password/` | Autenticado | Cambio de contraseña; obligatorio tras una temporal |
| `/users/`, `/users/new/`, `/users/<id>/role/`, `/users/<id>/deactivate/`, `/users/<id>/reactivate/`, `/users/<id>/password/` | `usuarios.gestionar` | Gestión de usuarios de la empresa |
| `/company/` | `empresa.configurar` | Configuración de la empresa |
| `/audit/` | `auditoria.consultar` | Auditoría de negocio y eventos de seguridad |
| `/admin/` | Personal técnico | Django Admin con Unfold, separado del panel |

### Comandos

```powershell
python manage.py init_company --name "Mi Empresa" --email dueno@example.com
python manage.py reset_owner_password --email dueno@example.com
```

`init_company` pide la contraseña por `getpass` con confirmación, valida la
política vigente, crea la empresa y su dueño en un bloque atómico y audita
`company.initialized`; es idempotente cuando ya existe una empresa activa con un
único dueño y el correo coincide, y falla con `CommandError` ante estados
ambiguos. `reset_owner_password` localiza al dueño activo por correo normalizado,
genera una contraseña temporal que muestra una sola vez por `stdout`, activa
`must_change_password` y audita `membership.owner_password_reset` con actor nulo.
Ninguno acepta contraseñas como argumento ni las escribe en logs o auditoría.

### Middleware y aislamiento

`ActiveCompanyMiddleware` resuelve una vez por solicitud `request.membership`,
`request.company`, `request.account` y `request.must_change_password`:

- Sin membresía activa o con empresa inactiva → 403 de contexto
  (`MissingContextDenied`).
- `company_id` enviado por el cliente se ignora: ninguna vista lo lee; la empresa
  siempre proviene de la membresía (CA-08).
- `company` (GET o POST) distinto de la empresa activa → 404 uniforme y evento
  `company.scope.injected`, con `attempted_company_id` cuando es numérico.
- Acceso a un recurso de otra empresa → 404 uniforme y evento
  `company.scope.foreign`, sin revelar la existencia del recurso. El aislamiento
  se evalúa antes que la capacidad.
- Rutas excluidas: `/`, `/health/`, `/favicon.ico`, `/login/`, `/logout/`,
  `/static/` y `/admin/`.

Los 403 y 404 se renderizan con `Cache-Control: no-store`; el 404 es idéntico para
un recurso ajeno y uno inexistente en el mismo estado de autenticación.

### Admin técnico y panel comercial

`AUTHENTICATION_BACKENDS` separa `EmailBackend` (cuentas comerciales con membresía
activa) y `TechnicalAdminBackend` (personal `is_staff` sin cuenta comercial). Una
cuenta comercial no puede iniciar sesión en el Admin, el personal técnico no accede
al panel sin membresía y el Admin no registra cuentas, roles ni empresa.

### Sesión, cookies y logging técnico

- `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`,
  `CSRF_COOKIE_HTTPONLY=True` y `CSRF_COOKIE_SAMESITE="Lax"`.
- `DJANGO_SECURE_COOKIES` (por defecto `False`) controla `Secure` en sesión y CSRF.
- `DJANGO_SESSION_COOKIE_AGE` (por defecto `1209600`, entero positivo).
- `DJANGO_LOG_LEVEL` (por defecto `INFO`) define el nivel del logging técnico por
  consola, sin archivos, sin cuerpos de solicitud y sin datos personales. La
  auditoría de negocio es independiente.

### Frontend y recuperación de errores

- Pie único en `templates/components/footer.html` («Etapa 003 — Cuentas y
  multiempresa»), incluido por `base.html` y `base_panel.html`.
- Navegación por capacidad mediante el context processor `panel_navigation`; el
  panel solo muestra «Usuarios», «Empresa» y «Auditoría» con la capacidad
  correspondiente y usa `{% url %}` para los enlaces.
- `base.html` expone el bloque `site_header`; las páginas de error lo sobrescriben
  con `templates/components/error_header.html`, una cabecera mínima sin navegación
  pública.
- 403 de capacidad: «Volver al panel». 403 de contexto: «Cerrar sesión» por POST
  con CSRF. 404 autenticado: «Volver al panel». 404 anónimo: «Iniciar sesión».
  Un usuario autenticado nunca ve «Iniciar sesión» en el 404, para evitar el bucle
  de `redirect_authenticated_user`.

### Estrategia de pruebas

- **DB-free:** estructura, settings, home, URLs, Admin y catálogo de capacidades;
  no preparan base de datos.
- **Con base autorizada (`DA-07`):** `tests/conftest.py` aporta las fixtures
  `company`, `owner_account`, `owner_membership`, `foreign_company`,
  `foreign_account` y `foreign_membership`; cubren autenticación, autorización,
  aislamiento entre empresas, middleware, usuarios, empresa, auditoría, seguridad,
  comandos, formularios, navegación e integración de extremo a extremo.
- **Comandos:** se ejecutan con `call_command` y `getpass` simulado sobre la base
  de pruebas; nunca sobre `nexopyme_bootstrap_dev`.
- `tests/test_db_guards.py` impide que la configuración de pruebas apunte a la base
  de desarrollo.
- Limitación del proceso único: ejecutar toda la suite en una sola invocación hace
  fallar la guarda preexistente
  `test_settings_foundation.py::test_settings_test_guard_variables_are_present`,
  porque pytest-django cambia `DATABASES["default"]["NAME"]` al nombre de la base
  de pruebas cuando ya la preparó. No es una regresión de la etapa; la evidencia se
  obtiene en dos invocaciones (DB-free primero y con base después) sin modificar
  las guardas de la Etapa 001.

### Evidencias CA-42, CA-43 y CA-44

| CA | Estado | Evidencia |
|---|---|---|
| CA-42 | PASS | Validación visual T-23 con teclado, foco visible, etiquetas, errores asociados, contraste (13,58:1 texto; 6,69:1 borde; 9,44:1 error), objetivos ≥ 24×24 px, zoom 200 %, `lang="es"` y `prefers-reduced-motion`; aprobada por el usuario el 2026-11-12. |
| CA-43 | PASS | Estados vacío (auditoría), error (login, alta, contraseña, 403 de capacidad y de contexto, 404), carga (`aria-busy`), confirmación (rol y contraseña temporal) y éxito (empresa) validados en T-23; T-24 mejora la recuperación de 403/404 y el pie único. |
| CA-44 | PASS | `ruff check .` sin errores; **337 pruebas en verde** en la suite completa de T-25 (36 DB-free + 301 con base autorizada) y 278 en la ejecución objetivo de 12 archivos; `manage.py check` y `makemigrations --check --dry-run` sin cambios. |

### Evidencias T-24

- `apps/accounts/context_processors.py`: `panel_navigation` deriva `panel_nav` del
  rol de la membresía ya resuelta por el middleware, sin consultas adicionales.
- `templates/components/footer.html`: pie único con «Etapa 003 — Cuentas y
  multiempresa»; `base_panel.html` dejó de declarar un `<footer>` literal y ahora
  incluye el componente.
- `templates/base.html` expone `{% block site_header %}`;
  `templates/components/error_header.html` es la cabecera mínima de errores.
- `config/urls.py`: `handler403` y `handler404` reciben `signed_in` y
  `can_return_to_panel`; se conservan `no-store`, el registro de seguridad y el
  orden aislamiento → capacidad.
- `templates/errors/403.html` y `404.html`: acciones de recuperación y ausencia de
  navegación pública.
- `templates/home.html` y `templates/components/footer.html`: etapa 003 y
  descripción de cuentas, roles y aislamiento; se mantiene un solo `h1` y
  «Pendiente de especificación» en los módulos.
- `tests/test_accounts_navigation.py`: 18 pruebas nuevas en T-24, ampliadas a 19
  en T-25 con la regresión del POST real de logout desde el 403 de contexto.
- `.env.example`: el comentario de la base de pruebas ya no dice «prohibida en la
  Etapa 001» y la describe como «base fija de pruebas».
- Verificación de T-24 (histórico): `ruff check .` → All checks passed;
  `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes
  detected; **277 passed** en la ejecución objetivo de 12 archivos, incluidas las
  18 nuevas, y **336 passed** en la suite completa (36 DB-free + 300 con base
  autorizada). Tras las regresiones de T-25, la evidencia vigente es **278 / 337**.

### Validación visual T-24

Fecha: 2026-11-12. G-3 ampliado por el usuario para T-24. Dos servidores locales
(`127.0.0.1:8000` con `DJANGO_DEBUG=True` y `127.0.0.1:8001` con
`DJANGO_DEBUG=False --insecure`) sobre `nexopyme_bootstrap_dev`, sin modificar
esquema, datos, permisos MySQL ni migraciones. Batería automatizada con Brave
aislado y CDP; 13 capturas enmascaradas en `<TEMP>\opencode\t24\`.

| Punto | Resultado |
|---|---|
| Viewports | PASS — 0 px de desbordamiento en login, home, panel (dueño, encargado y consulta), 403 de capacidad y 404 anónimo/autenticado en 320/375/768/1440/1920 px |
| Pie único | PASS — un solo `<footer>` y «Etapa 003 — Cuentas y multiempresa» en las cinco superficies; «Etapa 001 — Django Project Foundation» ausente |
| Navegación por capacidad | PASS — el dueño ve Usuarios, Empresa y Auditoría; encargado y consulta solo Panel, Perfil y Cerrar sesión |
| Recuperación | PASS — 403 de capacidad con «Volver al panel»; 404 anónimo con «Iniciar sesión»; 404 autenticado con «Volver al panel»; el 403 de contexto conserva el logout por POST con CSRF |
| Navegación pública en errores | PASS — 403 y 404 no muestran «Inicio», «Administración» ni `href="/admin/"` |

Hallazgo corregido: el botón de recuperación quedaba pegado al párrafo en 403 y
404. Se añadió `.error-actions` (`margin-top: var(--space-4)`) en `main.css` y el
contenedor en ambas plantillas; la captura repetida confirma el espaciado.

Limitación: el 403 de contexto no se capturó porque la única cuenta sin membresía
(`inactivo@bodega.example`) no puede iniciar sesión y no se modificaron datos de
desarrollo; queda cubierto por `tests/test_accounts_navigation.py`.

### Evidencias T-25 — Revisión final

- Trazabilidad: los 116 identificadores RF/RNF/CA/RN de `spec.md` están cubiertos
  por la matriz §7 de `tasks.md`; los identificadores intermedios de los rangos
  «x a y» quedan incluidos por su rango.
- RNF-12: se mantiene en T-24 como soporte documental de la política de
  persistencia; su verificación es la revisión de configuración del plan (§14,
  con el estado de partida de §3): MySQL 8.x y SQLite solo para el checkpointer.
- Commits: T-01 `4344c31`; un commit por tarea hasta T-24 `6d70e7e`, incluidos
  T-20 `01e55c4`, T-21 `4542c33`, T-22 `56eab2d` y T-23 `1babad1`; commits
  documentales `d907766`, `a355248` y `e622137`; fix de inicializadores de
  migración `441c2a4`; corrección de aislamiento `540b0c3` (M-1/M-2 de RC-6).
- Correcciones: registro de T-24 publicado, nota de la incidencia del BOM del
  commit `6d70e7e`, G-5 sin anticipar el dictamen, copy de
  `templates/accounts/panel.html` con las secciones disponibles para el rol,
  árbol documental completado con `forms.py` y `emails.py`, checklist manual de
  T-16 alineado con la etapa 003 y regresiones del 404 anónimo y del POST real de
  logout desde el 403 con el token renderizado en el formulario.
- Verificación: 278 pruebas en la ejecución objetivo de 12 archivos y 337 en la
  suite completa (36 DB-free + 301 con base autorizada); `ruff check .` → All
  checks passed; `manage.py check` sin problemas; `makemigrations --check
  --dry-run` → No changes detected; enlaces internos válidos.
- Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes; B-1,
  B-2 y O-1 a O-9 cerrados.
- Incidencia aceptada: el asunto de `6d70e7e` contiene un BOM UTF-8 al inicio; no
  se reescribió el historial por decisión del usuario. Los commits de T-25 y T-26
  se crean con `git commit -F` desde un archivo UTF-8 sin BOM.

### Evidencias T-26 — Cierre de la etapa

- `MEMORY.md` actualizado a 40 líneas con el estado final de la Etapa 003, el
  stack, las decisiones vigentes, la documentación, las limitaciones y la Etapa
  004 no iniciada.
- Consistencia revisada: `plan.md` con `tasks.md` v1.7; `tasks.md` v1.7 con T-26
  `[x]`; `docs/README.md` y `README.md` con el estado final. `spec.md` §17 se
  conserva como instantánea no normativa de la aprobación; el estado operativo y
  el cierre se registran en `plan.md`, `tasks.md` y este documento.
- Verificación final de RC-7: 337 pruebas (36 DB-free + 301 con base autorizada);
  `ruff check .` → All checks passed; `manage.py check` sin problemas;
  `makemigrations --check --dry-run` → No changes detected; enlaces internos
  válidos.
- Git: T-24 `6d70e7e` y T-25 `3611f7c` publicados; T-26 en commit propio; Build
  ejecuta el push de cierre y verifica `HEAD` = `origin/main`, divergencia `0 0`
  y árbol limpio salvo los tres no rastreados preexistentes.
- Incidencia aceptada: el BOM de `6d70e7e` permanece documentado sin reescribir el
  historial; los commits de T-25 y T-26 se crean con `git commit -F` desde un
  archivo UTF-8 sin BOM.
- Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes; B-1
  cerrado.

### Limitaciones

- El Admin Unfold conserva textos en inglés y acento violeta (limitación de la
  Etapa 001).
- El estado vacío de `/users/` no es alcanzable porque toda empresa conserva su
  dueño; la rama vacía existe como defensa.
- El 403 de CSRF lo emite el middleware de CSRF y no pasa por `handler403`, por lo
  que conserva su cacheabilidad.
- El evento `membership.owner_password_reset` usa `actor=None` y, por RF-39/CA-39,
  no aparece en la consulta de auditoría del panel.
- `spec.md` §17 conserva la instantánea de la aprobación (plan y tareas v1.2,
  T-01); es no normativa y no se alteró. El estado operativo y el cierre se
  registran en `plan.md`, `tasks.md` y este documento.
- La suite completa en un solo proceso mantiene la limitación preexistente de
  `test_settings_test_guard_variables_are_present` descrita arriba.
- Windows 11 no se probó independientemente.

## Etapa 004 — Rediseño visual

Implementación de la especificación 004 v0.1, el plan v0.1 y las tareas v0.1.
T-01 a T-11 están cerradas y RC-10 quedó APROBADO el 2026-11-13. La etapa no
modifica `apps/**`, `config/**`, migraciones, Admin/Unfold, la Etapa 003 ni las
pruebas.

### Decisiones y alcance

- D-01 «Mostrador»: cal fría, verde profundo y ámbar de sello; Candara + Segoe UI
  con fallbacks del sistema.
- D-02 P0 sin JavaScript, login de una columna, acciones de usuarios visibles y
  tablas con scroll interno accesible.
- D-03 P1 posterior: menú móvil, `<details>` por fila y login de dos columnas.
- D-04 copy verificado conservado; D-05 etapa independiente; D-06 única barra
  superior verde y login sin columna verde profunda.
- Superficies P0: shell público y de panel, login, panel, usuarios, empresa,
  auditoría, perfil, contraseña, 403 y 404; home P2 intacta; Admin sin `main.css`.

### Criterios R

| Criterio | Estado | Evidencia |
|---|---|---|
| R-01 | PASS | 0 px de scroll horizontal de página en 320/375/768/1440/1920; 404 propia con `DEBUG=False`. |
| R-02 | PASS | Foco doble de 3 px (`--color-focus`) con halo de 2 px; `focus` sobre `canvas` 5,20:1. |
| R-03 | PASS | 23 pares medidos: texto ≥ 4,5:1 y componentes no textuales ≥ 3:1. |
| R-04 | PASS | `aria-invalid="true"` y `aria-describedby` en errores de campo; resumen `role="alert"`. |
| R-05 | P1 | Menú móvil diferido por D-03; no implementado. |
| R-06 | P1 | Gestión por fila con `<details>` diferida por D-03; no implementada. |
| R-07 | PASS | `caption`, `scope` y `.table-scroll` enfocable con `aria-label` en usuarios y auditoría. |
| R-08 | PASS | `prefers-reduced-motion`: transición de 1e-05s y `scroll-behavior: auto`. |
| R-09 | PASS | Recibo con un único `<code>`, `role="status"`, sin duplicación; sin registro en logs ni auditoría. |
| R-10 | PASS | Vacíos de auditoría con el copy verificado; el vacío de usuarios no es alcanzable y la acción «Crear usuario» está en la cabecera. |
| R-11 | PASS | Zoom 200 % en `/panel/`, `/users/` y `/audit/` sin scroll de página; tablas con scroll interno. |
| R-12 | PASS | 337 pruebas en verde (36 DB-free + 301 con base), sin cambios de copy ni de pruebas. |

### Validación T-10

Fecha: 2026-11-13. Servidor local `127.0.0.1:8000` con `DJANGO_DEBUG=True` sobre
`nexopyme_bootstrap_dev` y servidor auxiliar `127.0.0.1:8001` con
`DJANGO_DEBUG=False --insecure` para la 404 propia. Evidencias CDP en
`<TEMP>\opencode\t10\` (`results-t10.json`, `results-a11y.json`,
`results-receipt-403.json`, `results-empty.json`, `results-step9.json`,
`results-temp-password.json`, `results-fc-zoom.json`,
`results-404-debug-off.json`, `contrast.py` y capturas por ancho y estado).

| Punto | Resultado |
|---|---|
| Viewports 320/375/768/1440/1920 px | PASS — 0 px de desbordamiento en login, panel, usuarios, alta, empresa, auditoría, perfil, contraseña y 404 propia; home 1440/1920 sin regresión |
| Zoom 200 % | PASS — 0 px de página en `/panel/`, `/users/` y `/audit/`; scroll interno de tabla 596/960 |
| Contraste | PASS — 23 pares medidos, 21 de §5.2 más `ink`/`ink-soft` sobre `surface`; umbral 4,5:1/3:1 |
| Teclado y foco | PASS — skip link visible, orden lógico, anillo de 3 px `rgb(11,110,138)` con halo y `aria-current="page"` |
| Formularios | PASS — error de login con `role="alert"`, `aria-invalid`/`aria-describedby`; carga con `aria-busy` y botón deshabilitado |
| Tablas | PASS — operaciones de 6 columnas, seguridad de 4, `caption`/`scope`, borde `rgb(169,181,172)`, scroll interno en 375 y sin scroll de página en 1920 |
| Recibo | PASS — borde discontinuo, borde superior ámbar `rgb(178,106,31)`, un único `<code>`, `role="status"`, 0 px en 320/768/1440 |
| Estados | PASS — vacíos de auditoría, aviso de contraseña temporal, 403 de contexto y carga/error de login |
| Accesibilidad del sistema | PASS — `prefers-reduced-motion`, `forced-colors` con Tab real, `lang="es"` y un `h1` por superficie |
| 404 con `DEBUG=False` | PASS — «Recurso no encontrado», código 404, `main.css` cargada, 0 px en los cinco anchos |
| Nombre de 150 caracteres | PASS — truncado con elipsis y 0 px de desbordamiento en 320/1440/1920 |
| Admin/panel | PASS — el Admin no carga `main.css`; `test_project_structure` lo verifica |
| Home P2 | PASS — `.panel__stage` en `accent-ink` `rgb(138,78,18)`, 0 nodos en ámbar y 0 px de desbordamiento |

### Limitaciones

- P1 y P2 no se implementan; requieren especificación o ampliación aprobada.
- Sin cambios de backend, copy verificado, pruebas, migraciones ni Admin/Unfold.
- `tfoot` y `aria-disabled` se incorporaron por el catálogo y los estados de
  `spec.md` §5.5, pero no tienen consumidor P0.
- `.container--wide` (80 rem) está disponible sin uso; el contenido P0 usa
  `.container` (72 rem), compatible con `spec.md` §5.4.
- El vacío de usuarios no es alcanzable porque toda empresa conserva su dueño; la
  rama vacía existe como defensa.
- La base de desarrollo no permite `DELETE`; los registros temporales de la
  validación (`t10-receipt@example.com` y `t10_super`) quedaron desactivados.
- La suite completa se ejecuta en dos invocaciones por la guarda preexistente de
  `test_settings_test_guard_variables_are_present`.
- El borde verde del login queda junto al encabezado (observación N-10, aceptada
  desde T-07/RC-9).

### RC-10

Dictamen del Reviewer: APROBADO (2026-11-13), sin hallazgos bloqueantes; T-11
APROBADA y RC-10 cerrado.
