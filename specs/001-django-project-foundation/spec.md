# Especificación 001 — Django Project Foundation

## 1. Identificación y estado

| Campo | Valor |
|---|---|
| Funcionalidad | 001 — Django Project Foundation (fundación del proyecto Django) |
| Identificador | `specs/001-django-project-foundation/` |
| Versión | 1.1 (aprobada) |
| Estado | **APROBADA** — decisiones D-01 a D-12 aprobadas por el usuario el 2026-11-09. La v1.1 incorpora `python-dotenv==1.2.4` como dependencia aprobada para la carga local de `.env`. G-0 y G-1 fueron concedidas; implementación en curso. |
| Responsable | Planner |
| Fase SDD | 8: implementación en curso conforme a G-0/G-1; RC-3 pendiente. |
| Fecha | 2026-11-09 |
| Trazabilidad | RF/RNF → CA → tarea/evidencia; D-01 a D-12 aprobadas en §17 |
| Relación con Bootstrap 000 | No modifica `specs/000-project-bootstrap/*` ni sus guardas. Extiende `config/settings.py`, `config/urls.py`, `config/views.py` y `README.md` conforme a D-01. |
| Numeración | `000-project-bootstrap`, `001-django-project-foundation`, `002-productos-inventario` (renumerada, contenido intacto; SHA-256 verificado) |
| Dependencias nuevas | `django-unfold==0.110.1` y `python-dotenv==1.2.4` (ambas aprobadas) |
| MySQL | Autorizado exclusivamente `nexopyme_bootstrap_dev` en `127.0.0.1:3306`; prohibido acceder a `nexopyme_bootstrap_test` |
| Skill opcional | `frontend-design` (aprobada su incorporación tras verificar la instalación y antes de diseñar el frontend; no es dependencia Python) |

**Convenciones**

- `[F]` requisito firme, verificable y aprobado.
- Los supuestos `S-xx` no son normativos.
- Las decisiones D-01 a D-12 están aprobadas y se registran en §17.
- La aprobación de esta especificación no autoriza implementación: se requieren además la aprobación del plan técnico y la autorización explícita de implementación (`AGENTS.md` §5).

## 2. Objetivo

Definir la estructura organizativa y la configuración mínima de Django que permita incorporar aplicaciones funcionales en etapas posteriores, con paquete `apps`, plantillas y estáticos globales, URLs globales, página de inicio informativa, Django Admin integrado con Django Unfold, superusuario local, servidor de desarrollo documentado, verificación HTTP real y pruebas básicas, sin implementar lógica de negocio, sin crear aplicaciones funcionales y sin alterar el Bootstrap 000.

## 3. Alcance y exclusiones

### 3.1 Incluido

- Crear la estructura `apps/`, `templates/`, `static/` y `docs/` con contenido mínimo versionable (`.gitkeep`/`__init__.py` según corresponda).
- Configurar `TEMPLATES["DIRS"]`, `STATICFILES_DIRS` y `STATIC_ROOT` en `config/settings.py`.
- Registrar `/admin/` en `config/urls.py` y conservar `/health/`.
- Añadir una vista `home` y la ruta `/` con una página informativa sin lógica de negocio.
- Integrar Django Unfold como interfaz exclusiva de Django Admin.
- Configurar y verificar `/admin/` con sesión autenticada de superusuario local.
- Crear un superusuario local mediante `createsuperuser` y documentar creación y recuperación segura.
- Documentar y verificar la ejecución local con `runserver` contra `nexopyme_bootstrap_dev`.
- Cargar `.env` localmente con `python-dotenv` y `override=False`, sin versionar el archivo ni sobrescribir variables ya definidas.
- Crear la fundación visual propia: `templates/base.html`, `templates/home.html`, componentes de navegación y pie, y `static/css/main.css`.
- Incorporar pruebas automatizadas sin acceso a base de datos y verificación manual documentada del administrador.
- Actualizar `README.md` y `docs/README.md` con estructura, comandos y evidencias.

### 3.2 Excluido

- Aplicaciones funcionales de negocio (productos, inventario, ventas, compras, clientes, finanzas, reportes).
- Modelos, migraciones propias, formularios o servicios de negocio.
- Dashboard con datos ficticios, métricas simuladas o módulos no implementados.
- Autenticación pública, registro de usuarios, recuperación de contraseña por correo o gestión de permisos más allá del Admin.
- Bootstrap 5, React, Vue, Node.js, bundlers o herramientas adicionales de frontend.
- Despliegue remoto, contenedores, CI/CD, Redis, microservicios, RAG o bases vectoriales.
- Uso de SQLite para datos operativos.
- Acceso a `nexopyme_bootstrap_test`, modificación de permisos MySQL, eliminación o recreación de bases.
- Cambios de esquema ajenos a esta etapa o alteración de migraciones existentes sin justificación y revisión.
- Instalación de Django Unfold o de la skill `frontend-design` durante esta ejecución de especificación.
- Renumeración de `specs/001-productos-inventario/`: ya ejecutada como prerrequisito documental (D-06), conservando íntegramente el contenido; no se aprueba ni implementa productos e inventario.
- Aprobación o implementación de productos e inventario.

## 4. Contexto, restricciones y supuestos

### 4.1 Normativa aplicable

- `CONSTITUTION.md` prevalece sobre `AGENTS.md`, esta especificación y el plan.
- `AGENTS.md` prevalece en lo no cubierto por la Constitución.
- Se respetan: simplicidad, fuente de verdad, desacoplamiento, calidad, seguridad y consistencia; MySQL 8.x como persistencia operativa; ORM y migraciones para acceso a datos; aislamiento entre empresas; seguridad de secretos; y el flujo SDD con sus tres aprobaciones.
- Esta especificación no concede por sí sola autorización de implementación, instalación de dependencias ni operaciones Git. La autorización de alcance para MySQL de desarrollo fue concedida por el usuario y solo se ejecuta tras la autorización de implementación (G-1) y la confirmación de identidad.

### 4.2 Estado técnico de partida (Bootstrap 000 cerrado)

| Elemento | Estado observado |
|---|---|
| Python | 3.14.10 (entorno `.venv` del bootstrap) |
| Django | `Django==6.0.9` |
| MySQL | 8.0.36; base de desarrollo `nexopyme_bootstrap_dev` |
| Driver | `mysqlclient==2.3.0` |
| `INSTALLED_APPS` | `admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles` |
| `TEMPLATES["DIRS"]` | `[]` |
| Estáticos | Solo `STATIC_URL = "static/"`; sin `STATICFILES_DIRS` ni `STATIC_ROOT` |
| URLs | Solo `health/` |
| `DEBUG` | Default `False`, gobernado por `DJANGO_DEBUG` |
| `ALLOWED_HOSTS` | Vacío por defecto; gobernado por `DJANGO_ALLOWED_HOSTS` |
| Pruebas | `pytest.ini` fuerza `config.settings_test`, que exige `nexopyme_bootstrap_test` y `nexopyme_test_user`; `conftest.py` aborta ante configuración insegura |

### 4.3 Restricciones específicas

- **R-01.** No se modifica ningún archivo de `specs/000-project-bootstrap/`.
- **R-02.** No se modifican `config/settings_test.py`, `conftest.py`, `pytest.ini` ni `tests/test_db_guards.py`: son guardas de seguridad del Bootstrap 000.
- **R-03.** No se accede a `nexopyme_bootstrap_test` en ninguna fase de esta etapa.
- **R-04.** No se modifican permisos MySQL, no se eliminan ni recrean bases y no se ejecutan operaciones destructivas.
- **R-05.** No se alteran migraciones existentes sin justificación documentada y revisión.
- **R-06.** No se almacenan contraseñas, tokens ni secretos en código, documentación, archivos versionados, capturas ni evidencias.
- **R-07.** Django Admin y Unfold son infraestructura de administración; no son el frontend empresarial y no comparten estilos ni plantillas con él.
- **R-08.** La interfaz propia no presenta datos ficticios ni funcionalidades no implementadas.
- **R-09.** Toda modificación de interfaz requiere validación funcional y visual (`AGENTS.md` §8).
- **R-10.** La suite completa de pytest queda fuera del alcance de ejecución por depender de la base prohibida; se registra explícitamente como `NO EJECUTADO` (D-08 aprobada).
- **R-11.** Las guardas de pruebas no se modifican. Cualquier ejecución de `pytest` desde la raíz carga `conftest.py`, que exige `config.settings_test` y la identidad de `nexopyme_bootstrap_test`; por tanto, las pruebas DB-free deben ejecutarse sin abrir conexión MySQL y con una invocación compatible con esas guardas, definida en el plan (D-08).

### 4.4 Supuestos no normativos

- **S-01.** El entorno local dispone de navegador para la verificación visual del Admin y de la página principal.
- **S-02.** Las credenciales de `nexopyme_bootstrap_dev` existen en el entorno local del usuario y no se reproducen en esta especificación.
- **S-03.** El superusuario local se crea con un correo y contraseña elegidos por el usuario; no se versionan.
- **S-04.** Django Unfold 0.110.1 mantiene la compatibilidad declarada en PyPI durante la implementación; se reverifica en el plan.
- **S-05.** La skill `frontend-design` es orientativa y su ausencia no bloquea la aceptación técnica.

## 5. Requisitos verificables (EARS)

### 5.1 Requisitos funcionales

| ID | Requisito | CA | Estado |
|---|---|---|---|
| RF-01 | CUANDO se implemente la etapa, el proyecto DEBE contener `apps/`, `templates/`, `static/` y `docs/` con los archivos mínimos versionables que permitan su uso, sin crear aplicaciones funcionales ni modelos de negocio. | CA-01 | [F] |
| RF-02 | CUANDO se configuren plantillas y estáticos, `config/settings.py` DEBE declarar `TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]`, `STATICFILES_DIRS = [BASE_DIR / "static"]` y `STATIC_ROOT = BASE_DIR / "staticfiles"`, manteniendo `STATIC_URL` y `STATICFILES_DIRS` compatibles con `django.contrib.staticfiles`. | CA-02 | [F] |
| RF-03 | CUANDO un visitante solicite `GET /`, la aplicación DEBE responder HTTP 200 con una página informativa renderizada desde `templates/home.html`, sin lógica de negocio, sin datos ficticios y sin consultas a la base de datos. | CA-03 | [F] |
| RF-04 | CUANDO se configuren las URLs, la ruta `health/` DEBE conservar su comportamiento actual de respuesta HTTP 200 en texto plano y su nombre `health`. | CA-04 | [F] |
| RF-05 | CUANDO se solicite `GET /admin/` sin sesión, la aplicación DEBE responder con la pantalla de inicio de sesión del administrador; tras autenticarse con el superusuario local, DEBE responder HTTP 200 con el panel de administración. | CA-05 | [F] |
| RF-06 | CUANDO se integre Unfold, el proyecto DEBE declarar `django-unfold==0.110.1` en `requirements.txt` e incluir `"unfold"` en `INSTALLED_APPS` antes de `"django.contrib.admin"`, conservando las aplicaciones de administración y autenticación existentes. | CA-06 | [F] |
| RF-07 | CUANDO se cargue el administrador, la configuración `UNFOLD` DEBE definir la identidad mínima de NexoPyme AI (título del sitio y encabezado) y el administrador DEBE renderizar con la interfaz de Unfold, no con la interfaz por defecto de Django. | CA-07 | [F] |
| RF-08 | CUANDO se acceda a los modelos `User` y `Group` en el administrador, sus pantallas DEBEN renderizarse con los estilos de Unfold, sin errores de plantilla ni de registro. | CA-08 | [F] |
| RF-09 | CUANDO se cree el superusuario local, DEBE utilizarse `python manage.py createsuperuser` de forma interactiva, sin contraseñas en argumentos, variables versionadas, fixtures ni scripts, y la contraseña NO DEBE registrarse en documentación ni evidencias. | CA-09, CA-10 | [F] |
| RF-10 | CUANDO el superusuario inicie sesión en `/admin/`, DEBE acceder al panel, visualizar los módulos de autenticación y poder cerrar sesión correctamente. | CA-05, CA-06 | [F] |
| RF-11 | CUANDO se ejecute el servidor local, DEBE arrancar con `python manage.py runserver 127.0.0.1:8000` contra `nexopyme_bootstrap_dev` en `127.0.0.1:3306`, y `GET /`, `GET /health/` y `GET /admin/` DEBEN responder según RF-03, RF-04 y RF-05. | CA-11 | [F] |
| RF-12 | CUANDO se implemente la fundación visual, DEBEN existir `templates/base.html`, `templates/home.html`, `templates/components/navbar.html`, `templates/components/footer.html` y `static/css/main.css`, con navegación responsive, jerarquía tipográfica, paleta consistente y estructura accesible. | CA-12, CA-13 | [F] |
| RF-13 | CUANDO se documente la etapa, `README.md` y `docs/README.md` DEBEN describir la estructura, la configuración de Admin y Unfold, el procedimiento de superusuario, la ejecución local, la estrategia de estáticos y las evidencias obtenidas, sin secretos. | CA-17 | [F] |
| RF-14 | CUANDO se ejecuten las pruebas automatizadas, DEBEN cubrir sin acceso a base de datos la estructura, la resolución de URLs, la vista `home`, la configuración de plantillas y estáticos y la configuración de Unfold; DEBEN ejecutarse sin abrir conexión MySQL y sin modificar las guardas existentes, y la suite completa de pytest NO DEBE ejecutarse contra `nexopyme_bootstrap_test`. | CA-15, CA-16 | [F] |
| RF-15 | CUANDO se renumere la especificación de productos, el contenido de `specs/001-productos-inventario/spec.md` DEBE conservarse íntegramente en `specs/002-productos-inventario/spec.md`, sin aprobarlo ni implementarlo. | CA-18 | [F] |

### 5.2 Requisitos no funcionales

| ID | Requisito | CA | Estado |
|---|---|---|---|
| RNF-01 | CUANDO se instale Unfold, la versión DEBE ser exactamente `0.110.1`, compatible con Django 6.0.9 y Python 3.14.10 según metadata verificable; la instalación DEBE ocurrir solo tras autorización de implementación y confirmarse con `pip check` y `manage.py check`. | CA-06 | [F] |
| RNF-02 | El repositorio, la documentación y las evidencias NO DEBEN contener contraseñas, tokens, `SECRET_KEY`, credenciales MySQL ni datos personales innecesarios. | CA-10 | [F] |
| RNF-03 | Django Admin y el frontend propio DEBEN permanecer separados: Unfold solo afecta a `/admin/`; las plantillas y estilos propios NO DEBEN depender de assets de Unfold ni viceversa. | CA-14 | [F] |
| RNF-04 | La interfaz propia DEBE cumplir accesibilidad básica: HTML semántico, `lang="es"`, un solo `h1` por página, contraste suficiente, foco visible, navegación por teclado y textos alternativos cuando correspondan imágenes. | CA-13 | [F] |
| RNF-05 | La interfaz propia DEBE ser responsive entre 320 px y 1920 px, sin desbordamiento horizontal ni contenido inaccesible. | CA-13 | [F] |
| RNF-06 | La fundación visual NO DEBE incorporar frameworks ni dependencias frontend adicionales; DEBE usar HTML5, CSS y JavaScript nativo mínimo, sin datos ficticios. | CA-12 | [F] |
| RNF-07 | El código Python DEBE cumplir PEP 8 y Ruff sin errores, con type hints donde aporten claridad, y mantener la separación de responsabilidades existente. | CA-15 | [F] |
| RNF-08 | Las versiones declaradas DEBEN ser exactas y reproducibles; no se aceptan rangos abiertos para las dependencias nuevas. | CA-06 | [F] |
| RNF-09 | Ninguna operación de la etapa DEBE acceder a `nexopyme_bootstrap_test`, modificar permisos MySQL, eliminar o recrear bases ni ejecutar operaciones destructivas. | CA-11 | [F] |
| RNF-10 | Cada criterio de aceptación DEBE aportar evidencia verificable (comando y resultado, captura sin secretos o prueba automatizada) y los elementos no ejecutados DEBEN registrarse como `NO EJECUTADO`. | CA-17 | [F] |

## 6. Criterios de aceptación

| ID | Escenario verificable | Requisitos | Estado |
|---|---|---|---|
| CA-01 | Existen `apps/__init__.py`, `templates/`, `static/`, `docs/` y sus archivos mínimos; una comprobación automatizada verifica las rutas y confirma que no se creó ninguna aplicación funcional ni modelo de negocio. | RF-01 | [F] |
| CA-02 | Una prueba automatizada sin base de datos verifica `TEMPLATES[0]["DIRS"]`, `STATICFILES_DIRS` y `STATIC_ROOT`, y `python manage.py check` finaliza sin errores. | RF-02 | [F] |
| CA-03 | `GET /` responde HTTP 200, usa `templates/home.html`, no accede a la base de datos y muestra información institucional de NexoPyme AI sin datos ficticios ni módulos no implementados. | RF-03 | [F] |
| CA-04 | `GET /health/` responde HTTP 200 con `Content-Type: text/plain` y cuerpo `ok`, y la ruta conserva el nombre `health`. | RF-04 | [F] |
| CA-05 | `GET /admin/` sin sesión presenta el formulario de acceso; tras autenticarse con el superusuario, responde HTTP 200 y muestra el panel; el cierre de sesión funciona. | RF-05, RF-10 | [F] |
| CA-06 | `requirements.txt` declara `django-unfold==0.110.1`; `INSTALLED_APPS` contiene `"unfold"` antes de `"django.contrib.admin"`; `pip check` no reporta conflictos; `manage.py check` no reporta errores; la respuesta de `/admin/` referencia assets o clases de Unfold. | RF-06, RNF-01, RNF-08 | [F] |
| CA-07 | La respuesta del administrador contiene el título y encabezado definidos en `UNFOLD` para NexoPyme AI y no corresponde a la apariencia por defecto de Django. | RF-07 | [F] |
| CA-08 | `GET /admin/auth/user/` y `GET /admin/auth/group/` responden HTTP 200 con la sesión del superusuario y renderizan con estilos de Unfold, sin errores de plantilla. | RF-08 | [F] |
| CA-09 | El superusuario existe en `nexopyme_bootstrap_dev`, tiene `is_staff=True` e `is_superuser=True`, inicia sesión correctamente y el procedimiento documentado permite recrearlo o cambiar su contraseña sin exponerla. | RF-09 | [F] |
| CA-10 | Una revisión de archivos versionados y evidencias no encuentra contraseñas, tokens, `SECRET_KEY`, credenciales MySQL ni datos personales innecesarios; `.env` no está versionado y `.env.example` carece de valores reales. | RF-09, RNF-02 | [F] |
| CA-11 | `python manage.py runserver 127.0.0.1:8000` arranca contra `nexopyme_bootstrap_dev`; `migrate --check` no reporta migraciones pendientes; `GET /`, `GET /health/` y `GET /admin/` responden; los registros confirman el destino `127.0.0.1:3306` y en ningún momento se accede a `nexopyme_bootstrap_test`. | RF-11, RNF-09 | [F] |
| CA-12 | Existen `templates/base.html`, `templates/home.html`, `templates/components/navbar.html`, `templates/components/footer.html` y `static/css/main.css`; `home.html` extiende `base.html`; no se incorporan frameworks ni dependencias frontend adicionales. | RF-12, RNF-06 | [F] |
| CA-13 | La validación visual documentada cubre 320 px, 768 px, 1440 px y 1920 px sin desbordamiento horizontal, navegación por teclado con foco visible, jerarquía de encabezados correcta, `lang="es"` y contraste suficiente. | RF-12, RNF-04, RNF-05 | [F] |
| CA-14 | Las plantillas y estilos propios no extienden ni importan assets de Unfold; las plantillas de Admin no dependen de `static/css/main.css`; una revisión de archivos confirma la separación. | RNF-03 | [F] |
| CA-15 | Las pruebas automatizadas sin base de datos pasan con una invocación que no abre conexión MySQL y que no modifica `conftest.py`, `pytest.ini` ni las guardas, y Ruff finaliza sin errores sobre el código modificado. | RF-14, RNF-07 | [F] |
| CA-16 | El informe registra la suite completa de pytest como `NO EJECUTADO`, con la causa (base de pruebas prohibida) y la estrategia alternativa aplicada. | RF-14 | [F] |
| CA-17 | `README.md` y `docs/README.md` documentan estructura, Admin, Unfold, superusuario, ejecución local, estáticos y evidencias; cada CA indica comando/resultado o `NO EJECUTADO`. | RF-13, RNF-10 | [F] |
| CA-18 | `specs/002-productos-inventario/spec.md` existe y su contenido coincide íntegramente con el original; `specs/001-productos-inventario/` ya no existe; la especificación permanece sin aprobar ni implementar. | RF-15 | [F] |

## 7. Estructura definitiva propuesta

```text
nexopyme-ai/
├── apps/
│   ├── __init__.py
│   └── core/                      # App de infraestructura (D-02)
│       ├── __init__.py
│       ├── apps.py                # AppConfig sin modelos
│       └── admin.py               # Re-registro Unfold de User/Group
├── config/
│   ├── settings.py                # TEMPLATES, STATIC*, INSTALLED_APPS, UNFOLD
│   ├── urls.py                    # admin/, home, health/
│   └── views.py                   # home; health conservada
├── docs/
│   └── README.md                  # Índice y guías de la etapa
├── specs/
│   ├── 000-project-bootstrap/     # Cerrado; no modificar
│   ├── 001-django-project-foundation/
│   │   └── spec.md                # Este documento
│   └── 002-productos-inventario/  # Renumerada; contenido intacto
├── static/
│   └── css/
│       └── main.css               # Fundación visual propia
├── templates/
│   ├── base.html                  # Layout global propio
│   ├── home.html                  # Página informativa
│   └── components/
│       ├── navbar.html
│       └── footer.html
├── tests/
│   ├── test_db_guards.py          # Guarda existente; no modificar
│   ├── test_project_structure.py  # Sin base de datos
│   ├── test_settings_foundation.py
│   ├── test_home_view.py          # Sin base de datos
│   ├── test_urls.py               # Sin base de datos
│   └── test_admin_unfold.py       # Sin base de datos
└── README.md
```

**Notas de estructura**

- `apps/` es un paquete contenedor; no se crean aplicaciones funcionales.
- `apps/core` (D-02 aprobada) es una aplicación de infraestructura sin modelos ni migraciones, destinada únicamente al re-registro de `User`/`Group` con Unfold.
- `templates/` y `static/` son globales; no se crean directorios por aplicación funcional.
- `tests/` aloja las pruebas nuevas DB-free de la etapa. `tests/test_db_guards.py` es una guarda existente que no se modifica; su prueba con `@pytest.mark.django_db` queda excluida del subconjunto DB-free y se registra como `NO EJECUTADA`.
- `staticfiles/` (salida de `collectstatic`) no se versiona y se añade a `.gitignore` si no está ya cubierto.

## 8. Dependencias nuevas, justificación y versiones candidatas

| Dependencia | Versión candidata | Tipo | Justificación | Estado |
|---|---|---|---|---|
| Django | `6.0.9` | Python (existente) | Framework base; sin cambios | Confirmada |
| Python | `3.14.10` | Intérprete (existente) | Entorno del Bootstrap 000; sin cambios | Confirmada |
| mysqlclient | `2.3.0` | Python (existente) | Driver MySQL; sin cambios | Confirmada |
| django-unfold | `0.110.1` | Python (nueva) | Interfaz moderna del administrador solicitada; reemplaza la apariencia por defecto de Django Admin | Aprobada |
| python-dotenv | `1.2.4` | Python (nueva) | Carga local de `.env` sin sobrescribir variables ya definidas; facilita la ejecución local y no se versiona el archivo | Aprobada por el usuario el 2026-11-09 |

**Evidencia de compatibilidad de `django-unfold==0.110.1`**

- PyPI declara `requires_python: <4.0,>=3.12` y `requires_dist: django>=5.2`.
- Clasificadores: Django 5.2, 6.0 y 6.1; Python 3.12, 3.13, 3.14 y 3.15.
- Publicación observada: 2026-11-01.
- El paquete no incluye migraciones propias; las migraciones halladas en el repositorio corresponden solo a la aplicación de ejemplo de pruebas.
- La verificación efectiva (`pip check`, `manage.py check` y smoke test del Admin) se realizará en la implementación; la metadata por sí sola no se considera prueba de funcionamiento.

**Restricciones de dependencias**

- No se añaden dependencias Python distintas de `django-unfold==0.110.1` y `python-dotenv==1.2.4`.
- `python-dotenv` se usa solo para cargar `.env` localmente con `override=False`; no sobrescribe variables de entorno ya definidas y `.env` no se versiona.
- `frontend-design` no es una dependencia Python y no se declara en `requirements.txt`.
- Bootstrap 5 permanece diferido; incorporarlo requiere decisión formal posterior.
- No se aceptan rangos abiertos ni instalaciones implícitas: la instalación de Unfold requiere autorización de implementación (D-07).

## 9. Plan de configuración Django Admin + Unfold

### 9.1 Principios

- Unfold se usa **exclusivamente** para el administrador.
- La configuración parte de la existente y se limita a lo necesario; no se reescribe el proyecto.
- Los módulos opcionales de Unfold (`unfold.contrib.filters`, `forms`, `inlines`, etc.) no se incorporan inicialmente (D-09).
- No se personalizan plantillas de Unfold ni se crean overrides en esta etapa.

### 9.2 Cambios previstos en `config/settings.py`

1. Añadir `"unfold"` al inicio de `INSTALLED_APPS`, antes de `"django.contrib.admin"`.
2. Mantener el resto de aplicaciones en su orden actual.
3. Declarar la identidad mínima:

```python
UNFOLD = {
    "SITE_TITLE": "NexoPyme AI",
    "SITE_HEADER": "NexoPyme AI",
    "SITE_SUBHEADER": "Administración",
    "SITE_URL": "/",
}
```

4. No se define `DASHBOARD_CALLBACK`, `SITE_DROPDOWN`, `SITE_ICON`, `SITE_LOGO` ni widgets personalizados en esta etapa.

### 9.3 Cambios previstos en `config/urls.py`

```python
from django.contrib import admin
from django.urls import path

from .views import health, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("health/", health, name="health"),
]
```

### 9.4 Re-registro de `User` y `Group`

Unfold documenta que `User` y `Group` aparecen sin estilos si no se re-registran con `unfold.admin.ModelAdmin` y los formularios de `unfold.forms`. El re-registro se ubicará en `apps/core/admin.py` (D-02 aprobada):

```python
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

**Nota técnica:** `django.contrib.admin.autodiscover()` importa el módulo `admin` de cada app de `INSTALLED_APPS`. `config/` no es una app instalada, por lo que `config/admin.py` no se autodescubre; requeriría una importación explícita. Por eso se usa `apps/core` (D-02 aprobada); `"apps.core"` debe añadirse a `INSTALLED_APPS` para que su `admin.py` se autodescubra.

### 9.5 Secuencia de implementación prevista

1. Añadir `django-unfold==0.110.1` y `python-dotenv==1.2.4` a `requirements.txt` e instalar solo tras autorización (G-2/D-07).
2. Aplicar los cambios de `settings.py` (incluida la carga de `.env` con `override=False`), `urls.py` y el re-registro de auth.
3. Ejecutar `python -m pip check` y `python manage.py check`.
4. Ejecutar `python manage.py migrate --check` contra `nexopyme_bootstrap_dev`; si hay pendientes, documentar y aplicar solo lo justificado (D-11).
5. Crear el superusuario (D-12).
6. Ejecutar `runserver` y validar `/`, `/health/` y `/admin/` en navegador.
7. Documentar evidencias y registrar lo no ejecutado.

### 9.6 Verificación de que Unfold está activo

- La respuesta de `/admin/` debe referenciar assets de Unfold (por ejemplo, rutas bajo `unfold/` o clases propias) y no el CSS por defecto de Django.
- `User` y `Group` deben renderizar con la interfaz de Unfold.
- El título del documento y el encabezado deben corresponder a `UNFOLD`.
- No se considera suficiente que el paquete esté instalado: la verificación es visual y HTTP.

## 10. Procedimiento seguro para el superusuario local

### 10.1 Creación

1. Verificar que `DJANGO_SETTINGS_MODULE` apunta a `config.settings` y que las variables MySQL apuntan a `nexopyme_bootstrap_dev` en `127.0.0.1:3306`.
2. Ejecutar `python manage.py createsuperuser`.
3. Introducir nombre de usuario, correo y contraseña **de forma interactiva**, sin argumentos ni variables de entorno versionadas.
4. Verificar en el Admin que la cuenta tiene `is_staff=True` e `is_superuser=True`.
5. No registrar la contraseña en terminales compartidas, documentos, capturas ni memoria.

### 10.2 Recuperación

- Cambio de contraseña: `python manage.py changepassword <usuario>`, interactivo.
- Si se perdió el acceso: crear otro superusuario con `createsuperuser` o usar `python manage.py shell` únicamente para marcar `is_staff`/`is_superuser` y `set_password()` de forma interactiva, sin escribir la contraseña en el comando.
- No se documenta ni se ejecuta `DJANGO_SUPERUSER_PASSWORD` en archivos versionados.
- No se elimina ni recrea la base para recuperar acceso.

### 10.3 Datos que no deben exponerse

- Contraseña, hash de contraseña, `SECRET_KEY`, credenciales MySQL.
- Correo personal y nombre de usuario en capturas o evidencias; si se muestran, se enmascaran.
- El nombre del superusuario puede documentarse solo si el usuario lo autoriza; por defecto se usa un marcador genérico.

### 10.4 Evidencia esperada

- Comando ejecutado (sin contraseña) y resultado exitoso.
- Verificación de `is_staff`/`is_superuser` sin exponer el hash.
- Captura del Admin autenticado con datos personales enmascarados.
- Confirmación de que la contraseña no aparece en archivos versionados ni evidencias.

## 11. Estrategia de ejecución de `runserver` con MySQL de desarrollo

### 11.1 Condiciones previas

- Autorización de implementación vigente y plan/tareas aprobados.
- Variables de entorno cargadas: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`, `MYSQL_DATABASE=nexopyme_bootstrap_dev`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST=127.0.0.1`, `MYSQL_PORT=3306`.
- Verificación de que `MYSQL_DATABASE` es exactamente `nexopyme_bootstrap_dev`.
- Prohibido establecer `MYSQL_DATABASE=nexopyme_bootstrap_test` o reutilizar la configuración de pruebas.

### 11.2 Comandos previstos

```text
python manage.py check
python manage.py migrate --check
python manage.py runserver 127.0.0.1:8000
```

- `manage.py check` no requiere conexión a base por defecto.
- `migrate --check` y `runserver` sí abren conexión MySQL; se ejecutan solo contra la base de desarrollo autorizada.
- Si `migrate --check` reporta pendientes, se documenta el motivo y se decide si corresponde aplicar `migrate` (D-11). No se aplican migraciones ajenas a la etapa.
- `runserver` ejecuta `check_migrations()` al arrancar; un fallo de conexión o de migraciones debe detener el proceso y reportarse, sin cambiar de base.

### 11.3 Estáticos en local

Con `DEBUG=False`, `runserver` no sirve archivos estáticos. **Decisión D-03 aprobada:** definir `DJANGO_DEBUG=True` únicamente en el entorno local documentado, manteniendo el default `False` en el código. No se usa `runserver --insecure` ni `collectstatic` como estrategia principal. La configuración local debe documentarse y no puede cambiar el default de `DEBUG` en el repositorio.

### 11.4 Verificación HTTP y visual

- `GET http://127.0.0.1:8000/` → 200 y página informativa.
- `GET http://127.0.0.1:8000/health/` → 200 `ok`.
- `GET http://127.0.0.1:8000/admin/` → login; tras autenticación, panel Unfold.
- Verificación en navegador de estilos, navegación y responsive.
- Registro del resultado y de cualquier limitación.

### 11.5 Prohibiciones durante la ejecución

- No conectar a `nexopyme_bootstrap_test`.
- No ejecutar `flush`, `reset`, `drop`, `sqlmigrate` con efectos destructivos ni scripts SQL manuales.
- No modificar permisos MySQL.
- No eliminar ni recrear bases.
- No exponer credenciales en la salida de comandos o capturas.

## 12. Alcance visual inicial

### 12.1 Archivos y responsabilidades

| Archivo | Responsabilidad |
|---|---|
| `templates/base.html` | Documento HTML5, `lang="es"`, metadatos, carga de `main.css`, landmarks, bloques de contenido y scripts |
| `templates/components/navbar.html` | Marca, navegación principal y enlace al administrador |
| `templates/components/footer.html` | Identidad del proyecto, etapa actual y año |
| `templates/home.html` | Contenido informativo de la etapa, sin lógica de negocio |
| `static/css/main.css` | Variables de diseño, reset mínimo, layout, componentes, responsive y accesibilidad |

### 12.2 Dirección visual propuesta

- Estilo profesional, limpio y sobrio, orientado a pequeñas empresas.
- Paleta mediante variables CSS: color base neutro, color de texto con contraste suficiente y un acento institucional.
- Tipografía con pila de fuentes del sistema; sin fuentes externas ni peticiones de red.
- Espaciado consistente basado en una escala simple.
- Componentes reutilizables mínimos: contenedor, encabezado, tarjeta informativa, botón/enlace y pie.
- Sin imágenes decorativas obligatorias; si se usan, con texto alternativo y sin datos ficticios.
- Sin animaciones esenciales; si existen, respetar `prefers-reduced-motion`.

### 12.3 Contenido de la página principal

- `h1` con el nombre del proyecto y una descripción breve.
- Mensaje de etapa actual: fundación técnica del proyecto.
- Enlace a Administración. No se enlaza documentación si no existe una ruta que la sirva.
- Sección de próximos pasos que identifique módulos como **pendientes de especificación**, sin presentarlos como disponibles.
- Sin métricas, gráficos, tablas de negocio ni datos de ejemplo.

### 12.4 Responsive y accesibilidad

- Navegación que se adapta sin JavaScript obligatorio (envoltura o apilado).
- Sin desbordamiento horizontal entre 320 px y 1920 px.
- Foco visible y orden de tabulación lógico.
- Enlace para saltar al contenido principal.
- Contraste mínimo 4.5:1 para texto normal.
- Un solo `h1` por página y jerarquía de encabezados coherente.
- `aria-current` o equivalente en el enlace activo si se implementa.

### 12.5 Validación visual

- Capturas o revisión documentada en 320 px, 768 px, 1440 px y 1920 px.
- Recorrido por teclado de navegación y enlaces.
- Verificación de estados vacío/error cuando correspondan; la home no depende de datos.
- Registro de hallazgos y correcciones.

## 13. Skill `frontend-design`

### 13.1 Disponibilidad observada

| Aspecto | Resultado |
|---|---|
| Existencia | Sí: `anthropics/skills/frontend-design` en el ecosistema agent skills |
| Instalación local | No instalada; solo `find-skills` está disponible en `C:\Users\julio\.agents\skills` |
| Directorios OpenCode | `~/.config/opencode/skills` y `~/.opencode/skills` no existen |
| Comando de instalación | `npx skills add https://github.com/anthropics/skills --skill frontend-design` |
| Dependencia Python | No; no se declara en `requirements.txt` |
| Node/npx | Disponibles en el entorno local |

### 13.2 Uso previsto

La skill orientaría dirección estética, jerarquía tipográfica, paleta, espaciado, componentes, responsive y accesibilidad. Su uso es **opcional** y no condiciona la aceptación técnica.

### 13.3 Límites

- No se instala durante esta ejecución de especificación.
- No sustituye las decisiones de diseño de esta especificación ni el stack aprobado.
- No autoriza Bootstrap 5, React, Vue, Node.js ni herramientas de frontend.
- Si se instala, debe ser compatible con OpenCode y no modificar configuraciones del proyecto sin aprobación.
- La instalación y su alcance se resuelven en D-05.

## 14. Trazabilidad

### 14.1 Requisitos → criterios de aceptación

| Requisito | Criterios |
|---|---|
| RF-01 | CA-01 |
| RF-02 | CA-02 |
| RF-03 | CA-03 |
| RF-04 | CA-04 |
| RF-05, RF-10 | CA-05 |
| RF-06 | CA-06 |
| RF-07 | CA-07 |
| RF-08 | CA-08 |
| RF-09 | CA-09, CA-10 |
| RF-11 | CA-11 |
| RF-12 | CA-12, CA-13 |
| RF-13 | CA-17 |
| RF-14 | CA-15, CA-16 |
| RF-15 | CA-18 |
| RNF-01, RNF-08 | CA-06 |
| RNF-02 | CA-10 |
| RNF-03 | CA-14 |
| RNF-04, RNF-05 | CA-13 |
| RNF-06 | CA-12 |
| RNF-07 | CA-15 |
| RNF-09 | CA-11 |
| RNF-10 | CA-17 |

**Nota:** `python-dotenv` es una dependencia de soporte para la ejecución local (RF-11/CA-11) y la reproducibilidad de versiones (RNF-08); no introduce comportamiento de negocio ni un criterio de aceptación nuevo.

### 14.2 Decisiones → requisitos afectados

| Decisión | Requisitos afectados |
|---|---|
| D-01 | RF-01, RF-02, RF-04 |
| D-02 | RF-08, CA-08 |
| D-03 | RF-11, CA-11, CA-13 |
| D-04 | RF-09, CA-09, CA-10 |
| D-05 | RF-12 (orientación), CA-13 |
| D-06 | RF-15, CA-18 |
| D-07 | RF-06, RNF-01 |
| D-08 | RF-14, CA-15, CA-16 |
| D-09 | RF-06, RF-07 |
| D-10 | RF-03, RF-12, CA-03, CA-12 |
| D-11 | RF-11, CA-11 |
| D-12 | RF-09, CA-09 |

### 14.3 Criterios → evidencia

| Criterio | Evidencia prevista |
|---|---|
| CA-01, CA-02, CA-12, CA-14 | Pruebas automatizadas DB-free y listado de archivos |
| CA-03, CA-04, CA-05, CA-06, CA-07, CA-08 | Pruebas HTTP y verificación manual en navegador |
| CA-09, CA-10 | Procedimiento documentado, verificación de cuenta y revisión de secretos |
| CA-11 | Salida de comandos, logs y comprobaciones HTTP |
| CA-13 | Checklist visual y capturas sin datos personales |
| CA-15, CA-16 | Salida de pytest selectivo y Ruff; registro `NO EJECUTADO` |
| CA-17 | Documentación actualizada |
| CA-18 | Comparación de contenido y estado de rutas |

## 15. Riesgos y mitigaciones

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| RI-01 | Unfold 0.110.1 falla en tiempo de ejecución pese a la metadata | Alto | Verificar `pip check`, `manage.py check` y smoke test al inicio; si falla, detener y consultar sin sustituir la versión unilateralmente |
| RI-02 | Los estáticos no se sirven con `DEBUG=False` | Medio | Resolver D-03 y documentar la opción local sin cambiar el default |
| RI-03 | `User`/`Group` aparecen sin estilos | Medio | Re-registro con `unfold.admin.ModelAdmin` y `unfold.forms`; verificar CA-08 |
| RI-04 | Exposición de contraseñas o credenciales en evidencias | Alto | Enmascarar datos, revisar archivos versionados, no usar variables de contraseña |
| RI-05 | Acceso accidental a `nexopyme_bootstrap_test` | Alto | No ejecutar la suite completa; validar `MYSQL_DATABASE`; no modificar guardas |
| RI-06 | Migraciones pendientes o inesperadas | Medio | `migrate --check`; documentar; aplicar solo lo justificado y revisado |
| RI-07 | Pérdida de contenido al renumerar productos | Alto | Renombrar solo con autorización; comparar contenido/hash antes y después |
| RI-08 | Ampliación de alcance hacia dashboard o módulos de negocio | Medio | Exclusión explícita en §3.2 y revisión del Reviewer |
| RI-09 | Mezcla de estilos de Admin y frontend | Medio | Verificación de separación CA-14; plantillas independientes |
| RI-10 | Pérdida de acceso al superusuario | Medio | Procedimiento de recuperación documentado; sin borrar la base |
| RI-11 | `ALLOWED_HOSTS` vacío rompe pruebas con `DEBUG=False` | Bajo | Configurar `testserver` en la prueba sin relajar el default |
| RI-12 | Deriva de versión de Unfold | Bajo | Pin exacto `0.110.1` y revisión en el plan |

## 16. Evidencias esperadas

- Esta especificación v1.1 aprobada por el usuario.
- Plan técnico y tareas aprobados antes de implementar.
- Salida de `python -m pip check` y `python manage.py check`.
- Salida de `python manage.py migrate --check` contra `nexopyme_bootstrap_dev`.
- Salida de `python manage.py runserver 127.0.0.1:8000` y comprobaciones HTTP de `/`, `/health/` y `/admin/`.
- Capturas del Admin con Unfold y de `User`/`Group`, sin datos personales.
- Capturas o checklist visual de la home en 320 px, 768 px, 1440 px y 1920 px.
- Salida de pruebas DB-free y de Ruff.
- Registro explícito de la suite completa de pytest como `NO EJECUTADO`.
- `README.md` y `docs/README.md` actualizados.
- Verificación de ausencia de secretos en archivos versionados y evidencias.
- Comparación de contenido de la especificación de productos tras el renombrado, si se autoriza.

## 17. Decisiones aprobadas

Las decisiones D-01 a D-12 fueron aprobadas por el usuario el 2026-11-09. Su resolución es vinculante para el plan y las tareas.

| ID | Decisión | Resolución aprobada | Estado |
|---|---|---|---|
| D-01 | Alcance sobre Bootstrap 000 | Cambios mínimos en `config/` y `README.md`; no se modifica `specs/000-project-bootstrap/` ni sus guardas | Aprobada |
| D-02 | Ubicación del re-registro de `User`/`Group` | Crear `apps/core` como aplicación de infraestructura, sin modelos de negocio | Aprobada |
| D-03 | Estáticos en local | `DJANGO_DEBUG=True` únicamente en el entorno local documentado; el default general permanece `False` | Aprobada |
| D-04 | Privacidad del superusuario | No exponer identidad ni datos personales en documentación o evidencias | Aprobada |
| D-05 | Skill `frontend-design` | Incorporarla después de verificar su instalación y antes de diseñar el frontend | Aprobada |
| D-06 | Renumeración de productos | Renombrar `specs/001-productos-inventario/` a `specs/002-productos-inventario/` preservando íntegramente el contenido | Aprobada y ejecutada |
| D-07 | Instalación de Unfold | Solicitar la instalación de `django-unfold` al comenzar la implementación aprobada | Aprobada |
| D-08 | Pruebas con base prohibida | Mantener `config.settings_test` y las guardas; ejecutar solo pruebas sin DB y registrar la suite completa como `NO EJECUTADA` | Aprobada |
| D-09 | Módulos de Unfold | Utilizar únicamente Django Unfold, sin módulos `contrib` adicionales innecesarios | Aprobada |
| D-10 | Contenido de la home | Home informativa con próximos pasos, sin datos ficticios ni indicadores inventados | Aprobada |
| D-11 | Migraciones | `migrate --check` como comprobación inicial; las migraciones reales requieren justificación y autorización dentro del alcance | Aprobada |
| D-12 | Datos del superusuario | Datos elegidos por el usuario durante la creación interactiva | Aprobada |

### 17.1 Registro de aprobación

- Fecha: 2026-11-09.
- Aprobador: usuario del proyecto.
- Alcance aprobado: especificación v1.0 (decisiones D-01 a D-12) y enmienda v1.1 (dependencia `python-dotenv==1.2.4` para carga local de `.env`, aprobada el 2026-11-09).
- Condición: la implementación requiere aprobación del plan, aprobación de las tareas y autorización explícita de implementación (`AGENTS.md` §5).
- G-0 y G-1 fueron concedidas por el usuario. G-2 (django-unfold y python-dotenv), G-4 (frontend-design) y la regularización de G-5 (migrate accidental no-op) fueron aprobados el 2026-11-09. La autorización de alcance MySQL dev se mantiene, con `nexopyme_bootstrap_dev` en `127.0.0.1:3306`.
- La renumeración D-06 se ejecutó como prerrequisito documental; el hash SHA-256 del contenido se conservó (`DBDFB6A1FF5342F54F42BC1D6B73F3D3E89216504750F290B9238D2CB0AE923E`).

### 17.2 Siguiente fase

1. G-0 y G-1 concedidas; implementación en curso.
2. Tareas T-01 a T-11 ejecutadas; T-12 pendiente.
3. RC-3 pendiente de revisión del Reviewer.
4. El alcance regularizado (python-dotenv y `migrate` accidental no-op) requiere APROBADO del Reviewer antes de los commits `fix:`.
5. Cierre con T-17 y T-18.

---

**Fin de la especificación v1.1 aprobada.** La implementación de la Etapa 001 está en curso conforme a G-0/G-1; el estado operativo se registra en `MEMORY.md` y en `tasks.md`.
