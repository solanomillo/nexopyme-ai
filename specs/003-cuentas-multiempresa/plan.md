# Plan técnico 003 — Cuentas y multiempresa

## 1. Identificación y estado

| Campo | Valor |
|---|---|
| Funcionalidad | 003 — Cuentas y multiempresa |
| Artefacto | `specs/003-cuentas-multiempresa/plan.md` |
| Versión | 1.3 |
| Estado | APROBADO — v1.2 aprobado por el usuario el 2026-11-10; v1.3 registra `/panel/` y `panel.html` de T-11 |
| Especificación de referencia | `specs/003-cuentas-multiempresa/spec.md` v1.0 aprobada el 2026-11-10 |
| Tareas | `specs/003-cuentas-multiempresa/tasks.md` v1.2 |
| Fecha | 2026-11-10 |
| Responsable | Planner |
| Fase SDD | 5 a 7: plan técnico y descomposición en tareas |
| Base de partida | `HEAD` = `origin/main` = `bef5c58`; Etapa 001 cerrada |

**Historial:** v1.0: plan inicial. v1.1: correcciones del primer dictamen (backends, catálogo primero, `Account`, regresión de pruebas, sesión y logging, concurrencia, Git). v1.2: correcciones del segundo dictamen — auditoría después de `Company`, renumeración secuencial de tareas, aprobaciones A-09/A-10/A-13 registradas, `username` opaco, aplicación única de `must_change_password`, dos variantes de 403, pruebas de `on_commit`, 404 con `DEBUG=False`, variables opcionales y trazabilidad completa de RN. v1.3: se registran `/panel/` y `templates/accounts/panel.html` como shell protegido y landing del panel de T-11.

---

## 2. Objetivo del plan

Definir cómo se implementará el comportamiento de la especificación 003 sin alterar sus decisiones: cuentas con correo único, empresa única activa, membresías con un rol, cuatro roles fijos, autorización en servidor por capacidades, auditoría compartida, panel comercial propio y Django Admin reservado a superusuarios técnicos.

---

## 3. Estado de partida

| Elemento | Estado real verificado |
|---|---|
| Repositorio | `main` sincronizada con `origin/main` en `bef5c58` |
| Aplicaciones | Solo `apps.core`, sin modelos ni migraciones |
| Modelo de usuario | `django.contrib.auth.models.User`, sin `AUTH_USER_MODEL` personalizado |
| Admin | Unfold con `User` y `Group` registrados en `apps/core/admin.py` |
| Autenticación | Backend estándar de Django; sin vistas propias |
| Base de datos | MySQL 8.0.36; `nexopyme_bootstrap_dev` |
| Pruebas | Guardas activas; 20 pruebas DB-free de la Etapa 001 en verde |
| Base de pruebas | `nexopyme_bootstrap_test`, autorizada solo para esta etapa (`DA-07`) |
| Plantillas | `base.html`, `home.html` y componentes; `base.html` no usa `request.user`, `perms` ni `messages` |
| Dependencias | Sin dependencias nuevas previstas |

### 3.1 Pruebas de la Etapa 001 afectadas

| Prueba | Efecto | Tratamiento |
|---|---|---|
| `tests/test_project_structure.py::test_no_business_apps_were_created` | Afirma que `apps/` contiene solo `__init__.py` y `core` | T-02 la actualiza para `accounts` y T-04 para `audit`; se informa al usuario (O-2) |
| `tests/test_settings_foundation.py::test_installed_apps_enable_unfold_before_admin` | Exige `INSTALLED_APPS[-1] == "apps.core"` | `accounts` y `audit` se insertan antes de `apps.core` |
| `tests/test_home_view.py::test_home_templates_do_not_touch_session_context` | Prohíbe `request.user`, `perms` y `messages` en `base.html` y navbar | El panel usa `base_panel.html`; `base.html` no se modifica |

---

## 4. Decisiones aplicadas

### 4.1 Decisiones aprobadas por el usuario

`DA-01` a `DA-08` fueron aprobadas el 2026-11-10. `A-09`, `A-10` y `A-13` fueron aprobadas explícitamente por el usuario el 2026-11-10 al autorizar esta planificación: solo nombre de empresa, validadores y sesión de Django documentados por entorno, y sin purga automática de auditoría.

| ID | Decisión | Efecto en el plan |
|---|---|---|
| DA-01 | Correo único como identificador | `Account.email` único y normalizado |
| DA-02 | Cuatro roles fijos | Catálogo en código; sin tablas de roles ni permisos individuales |
| DA-03 | Un dueño y una empresa activa | Invariantes en servicios con bloqueo y pruebas |
| DA-04 | Inicialización idempotente | `manage.py init_company` |
| DA-05 | Contraseña temporal con cambio obligatorio | Indicador en la membresía; bloqueo en middleware |
| DA-06 | Recuperación por el dueño y por comando técnico | Servicio del panel y `manage.py reset_owner_password` |
| DA-07 | Base de test autorizada para esta etapa | Pruebas con base acotadas a `nexopyme_bootstrap_test` |
| DA-08 | Módulo compartido `apps/audit` | Aplicación nueva con auditoría y eventos |
| A-09 | Solo nombre de empresa | `Company.name` obligatorio; sin campos adicionales |
| A-10 | Validadores y sesión de Django | Validadores sin cambios; duración de sesión por entorno |
| A-13 | Sin purga de auditoría | Sin tarea de limpieza ni retención programada |

### 4.2 Decisiones técnicas del plan (sujetas a la aprobación de este plan)

| ID | Decisión | Motivo | Alternativa descartada |
|---|---|---|---|
| D-01 | Se conserva `auth.User`; se añade `Account` con correo único normalizado y nombre visible | `User.username` limita a 150 caracteres y el correo admite 254; `Account` da unicidad real sin migrar el usuario ni imponer una limitación no aprobada | `username` = correo |
| D-02 | Roles y capacidades en `apps/accounts/capabilities.py` | Fuente única consumible por 002 y por módulos futuros | Tablas editables |
| D-03 | `Membership` referencia `Account` y `Company`, con unicidad `(account, company)`; una sola membresía por cuenta en V1 se impone en el servicio | MySQL 8 no admite índices únicos parciales | Índice único parcial |
| D-04 | La unicidad de empresa activa se impone en el servicio con bloqueo transaccional | Misma limitación del motor | Restricción parcial |
| D-05 | Middleware después de `AuthenticationMiddleware`, con exclusiones exactas | Resuelve contexto una vez por solicitud | Resolución por vista |
| D-06 | Auditoría de negocio con `transaction.on_commit`; eventos de seguridad en el límite de rechazo | Registro tras commit y supervivencia al rechazo | Escritura en la transacción de negocio |
| D-07 | `User` y `Group` en Admin en solo lectura; `accounts` y `audit` no se registran | Separa Admin y negocio sin retirar visibilidad técnica | Edición plena en Admin |
| D-08 | `must_change_password` en la membresía | No altera `auth.User` | Modelo de perfil adicional |
| D-09 | Backends disjuntos: correo solo cuentas comerciales; técnico solo personal | Impide el bypass por `ModelBackend` | Cadena que autentica ambos |
| D-10 | Solo la duración de sesión se configura por entorno; validadores existentes | Cumple A-10 sin ampliar superficie | Validadores configurables |
| D-11 | `accounts` y `audit` antes de `apps.core` en `INSTALLED_APPS` | Conserva la prueba existente | Añadirlas al final |
| D-12 | El panel usa `base_panel.html`; `base.html` no se modifica | Conserva pruebas de la home | Contexto de sesión en `base.html` |
| D-13 | `tests/conftest.py` para fixtures; `conftest.py` raíz intacto | Evita duplicación sin debilitar guardas | Fixtures duplicadas |
| D-14 | Logging técnico por consola, nivel por entorno, sin datos personales | Cumple RNF-05 y separa diagnóstico de auditoría | Logging implícito |
| D-15 | `auth.User.username` se genera como valor opaco único, nunca visible ni usado para autenticar | `username` es obligatorio y único; usarlo para el correo reintroduce el límite de 150 | `username` = correo truncado |

Las variables de entorno nuevas son opcionales con valor por defecto; no se añaden requisitos obligatorios a `_get_required_env`.

---

## 5. Estrategia general y fases

| Fase | Contenido | Tareas |
|---|---|---|
| F0 | Verificación del estado de partida | T-01 |
| F1 | Capacidades, modelos y auditoría base | T-02 a T-05 |
| F2 | Servicios, invariantes y concurrencia | T-06, T-07 |
| F3 | Contexto y autorización | T-08, T-09 |
| F4 | Acceso, sesión y contraseñas | T-10 a T-12 |
| F5 | Comandos y panel de usuarios | T-13 a T-16 |
| F6 | Empresa y consulta de auditoría | T-17, T-18 |
| F7 | Separación Admin/panel y seguridad de sesión | T-19, T-20 |
| F8 | Pruebas con base autorizada y calidad | T-21, T-22 |
| F9 | Validación, documentación y cierre | T-23 a T-26 |

---

## 6. Dependencias y orden de ejecución

```text
T-01 ── T-02 ── T-03 ── T-04 ── T-05
T-05, T-03 ── T-06 ── T-07
T-03, T-07 ── T-08; T-02, T-08 ── T-09
T-03, T-09 ── T-10 ── T-11 ── T-12
T-07, T-12 ── T-13
T-09, T-12 ── T-14 ── T-15 ── T-16
T-06, T-16 ── T-17
T-05, T-09 ── T-18
T-10 ── T-19
T-11, T-19 ── T-20
T-02..T-20 ── T-21 ── T-22 ── T-23 ── T-24
T-24 APROBADO y commiteado ── T-25 ── T-26
```

| Tarea | Depende de |
|---|---|
| T-01 | — |
| T-02 | T-01 |
| T-03 | T-02 |
| T-04 | T-03 |
| T-05 | T-04 |
| T-06 | T-03, T-05 |
| T-07 | T-06 |
| T-08 | T-03, T-07 |
| T-09 | T-02, T-08 |
| T-10 | T-03, T-09 |
| T-11 | T-10 |
| T-12 | T-11 |
| T-13 | T-07, T-12 |
| T-14 | T-09, T-12 |
| T-15 | T-14 |
| T-16 | T-15 |
| T-17 | T-06, T-16 |
| T-18 | T-05, T-09 |
| T-19 | T-10 |
| T-20 | T-11, T-19 |
| T-21 | T-02 a T-20 |
| T-22 | T-21 |
| T-23 | T-22 |
| T-24 | T-23 |
| T-25 | T-24 APROBADO y commiteado |
| T-26 | T-25 |

El orden de ejecución coincide con la numeración.

---

## 7. Detalle técnico

### 7.1 Estructura final

```text
apps/
├── accounts/
│   ├── __init__.py, apps.py, admin.py, backends.py, capabilities.py
│   ├── decorators.py, emails.py, forms.py, middleware.py, models.py
│   ├── services.py, urls.py, views.py
│   ├── management/commands/{init_company.py,reset_owner_password.py}
│   └── migrations/0001_initial.py
├── audit/
│   ├── __init__.py, apps.py, models.py, services.py
│   └── migrations/0001_initial.py
└── core/            # solo cambia admin.py en T-19
templates/
├── base_panel.html
├── accounts/{panel,login,profile,password_change,user_list,user_form,user_confirm,company_form,audit_list}.html
└── errors/403.html, errors/404.html
tests/
├── conftest.py
├── test_accounts_capabilities.py, test_accounts_forms.py
├── test_accounts_auth.py, test_accounts_authorization.py, test_accounts_middleware.py
├── test_accounts_users.py, test_accounts_company.py, test_accounts_audit.py
├── test_accounts_isolation.py, test_accounts_commands.py
├── test_accounts_admin_separation.py, test_accounts_security.py
```

Sin dependencias nuevas.

### 7.2 Capacidades (T-02)

`Role`, `Capability`, `ROLE_CAPABILITIES` y `has_capability`, con la matriz de la especificación §4.3 y sin caché en sesión. Se implementa antes de los modelos porque `Membership.role` y los servicios lo necesitan.

### 7.3 Modelos (T-03)

| Modelo | Campos | Restricciones |
|---|---|---|
| `Account` | `user` (OneToOne con `auth.User`), `email` único normalizado, `display_name`, fechas | Fuente única del identificador |
| `Company` | `name`, `is_active`, fechas | `name` obligatorio |
| `Membership` | `account`, `company`, `role`, `is_active`, `must_change_password`, fechas | `unique(account, company)` |

`auth.User.username` recibe un valor opaco generado y único, nunca mostrado ni usado para autenticar (D-15). `apps/accounts/emails.py` centraliza la normalización y la validación; se prueba con un correo de 254 caracteres.

### 7.4 Auditoría (T-04, T-05)

`AuditEvent` y `SecurityEvent` con empresa obligatoria u opcional según el caso, índices por empresa y fecha, sin datos sensibles. `AuditEvent.company` se crea después de `Company`, por eso la auditoría depende de los modelos.

- `record_audit` se invoca con `transaction.on_commit`.
- `record_security` se invoca en el límite de rechazo, fuera de la transacción de negocio.
- Inmutabilidad por instancia y por `QuerySet` (`update()` y `delete()` bloqueados).
- Pruebas de auditoría con `django_capture_on_commit_callbacks(execute=True)`; `TransactionTestCase` solo para la reversión.

### 7.5 Servicios e invariantes (T-06, T-07)

`create_company_with_owner`, `create_employee`, `change_role`, `deactivate_membership`, `reactivate_membership`, `regenerate_temporary_password`, `update_company_name`.

Invariantes: una empresa activa, una sola membresía por cuenta, un dueño activo, ausencia de segundo dueño. Operaciones sensibles con `transaction.atomic()` y `select_for_update()` sobre la empresa. Toda mutación audita con valores anterior y nuevo.

**Riesgo residual aceptado:** si no existe ninguna fila de empresa, `select_for_update()` no bloquea; dos ejecuciones simultáneas de `init_company` podrían crear dos empresas. La instalación es local y el comando es manual; la comprobación de existencia previa y la restricción de servicio cubren el caso normal. Se documenta como limitación.

### 7.6 Middleware y bloqueo de contraseña temporal (T-08)

- `ActiveCompanyMiddleware` después de `AuthenticationMiddleware`.
- Resuelve `request.membership` y `request.company` en una consulta.
- Exclusiones exactas: `/`, `/health/`, `/favicon.ico`, `/static/`, `/admin/`, `/login/`, `/logout/`, `/password/`.
- Deniega si la membresía o la empresa están inactivas, mediante `PermissionDenied` para usar el handler 403.
- Un visitante no autenticado no recibe contexto ni denegación: la protección la aporta `login_required`.
- Si la solicitud trae un identificador de empresa distinto de `request.company.pk`, responde 404 uniforme y registra el evento de seguridad; si coincide o falta, el alcance sigue siendo el de la sesión.
- **Único punto de aplicación de `must_change_password`:** el middleware redirige a `/password/` cualquier ruta del panel con el indicador activo, salvo `/logout/`, `/password/` y `/static/`. Una ruta nueva queda cubierta automáticamente.

### 7.7 Autorización (T-09)

- `require_capability` delega en `has_capability`; los servicios usan la misma función.
- **404 uniforme** para recurso ajeno, inexistente o identificador de empresa ajeno al contexto.
- **403 con dos variantes:** un único `handler403` con mensaje de acceso denegado y una acción para cerrar sesión cuando falta contexto (sin forzar el cierre); mensaje de permiso insuficiente cuando falta capacidad.
- **404 uniforme** también para el identificador de empresa ajeno, con evento de seguridad.
- Orden: aislamiento, capacidad, estado del recurso, validación, reglas, persistencia, auditoría (RN-09).

### 7.8 Autenticación (T-10)

- `EmailBackend`: solo cuentas comerciales con membresía y empresa activas; rechaza personal y superusuarios.
- `TechnicalAdminBackend`: solo `is_staff`.
- Backends disjuntos; ningún camino permite saltarse la membresía.
- Normalización única y mensaje genérico.
- Pruebas: cuenta válida, membresía inactiva, cuenta inactiva, personal sin membresía y cuenta comercial contra Admin.

### 7.9 Sesión, contraseñas e interfaz (T-11 a T-17, T-20, T-23)

- Vistas propias de acceso, salida, perfil y cambio de contraseña.
- El cambio exige la contraseña actual, aplica los validadores y audita sin valores.
- `base_panel.html` aporta navegación y contexto sin tocar `base.html`.
- URLs: `/login/`, `/logout/`, `/panel/`, `/profile/`, `/profile/<int:pk>/`, `/password/`, `/users/`, `/company/`, `/audit/`.
- `/profile/<int:pk>/`: propio → 200; otra cuenta de la misma empresa → 403; otra empresa → 404 uniforme.
- Respuestas autenticadas con `Cache-Control: no-store` para que el botón atrás no recupere datos.
- Estados vacío, error, carga, confirmación y éxito; accesibilidad RNF-07.

### 7.10 Gestión de usuarios y empresa (T-14 a T-17)

Listado paginado por empresa; alta con rol distinto de `dueno`; cambio de rol, desactivación, reactivación y regeneración con auditoría; rechazo de segundo dueño y de empresa sin dueño; nombre de empresa con `empresa.configurar`.

### 7.11 Consulta de auditoría (T-18)

Listado paginado de auditoría y eventos de la empresa; requiere `auditoria.consultar`; no muestra eventos sin actor ni de otra empresa ni el identificador de empresa intentada; sin filtros adicionales en V1.

### 7.12 Separación Admin/panel (T-19)

`User` y `Group` en solo lectura; `Account`, `Company`, `Membership`, `AuditEvent` y `SecurityEvent` no se registran. Cuenta comercial en `/admin/`: redirección al login o denegación, nunca acceso. Superusuario técnico sin membresía.

### 7.13 Seguridad de sesión y logging (T-20)

Cookies `HttpOnly`, `SameSite=Lax`, `Secure` por entorno; `SESSION_COOKIE_AGE` por entorno con valor por defecto; validadores de contraseña sin cambios. `LOGGING` por consola, nivel por entorno, sin cuerpos de solicitud ni datos personales y sin retención en archivo. Variables opcionales, nunca obligatorias.

### 7.14 Pruebas y documentación (T-21 a T-24)

- DB-free: capacidades y formularios (salvo correo duplicado).
- Con base: modelos, servicios, middleware, autorización, autenticación, vistas, auditoría, comandos, aislamiento y seguridad de sesión.
- `tests/test_db_guards.py` se ejecuta en T-22.
- Fixtures compartidas en `tests/conftest.py`.
- Cada tarea de vista o servicio incluye su caso de acceso cruzado.
- Documentación en `README.md`, `docs/README.md`, `.env.example` y `tasks.md`.

---

## 8. Migraciones y operaciones que requieren MySQL

| Operación | Tarea | Autorización |
|---|---|---|
| `makemigrations accounts` y `migrate` | T-03 | G-2, G-3 |
| `makemigrations audit` y `migrate` | T-04 | G-2, G-3 |
| `init_company` y `reset_owner_password` | T-13 | G-3 |
| Base de pruebas por pytest | T-03 a T-23 | G-4 (`DA-07`) |

Sin migraciones de datos ni cambios en tablas de `auth`.

---

## 9. Estrategia de pruebas y guardas

- `conftest.py` raíz y `config/settings_test.py` no se modifican; `tests/conftest.py` es nuevo y solo contiene fixtures.
- Guardas: `config.settings_test`, `nexopyme_test_user`, `127.0.0.1:3306`, `nexopyme_bootstrap_test`; prohibidos `--reuse-db`, `--create-db`, paralelo y `--nomigrations`.
- Segunda empresa de prueba por ORM, fuera de los servicios e inactiva.
- Auditoría: `django_capture_on_commit_callbacks(execute=True)`; `TransactionTestCase` para la reversión.
- 404 uniforme validado con `DEBUG=False`; 403 con sus dos variantes también con `DEBUG=False`, porque los handlers personalizados solo se aplican en ese modo.
- Cada vista y servicio tiene prueba de acceso cruzado en su tarea; T-21 consolida.

---

## 10. Validación funcional y visual

Flujo completo de inicialización, acceso, alta, primer acceso, operaciones permitidas y denegadas, desactivación, reactivación, recuperación y auditoría; estados de interfaz; 320, 375, 768, 1440 y 1920 px; teclado, foco, etiquetas, errores asociados, contraste, objetivos táctiles ≥ 24×24 px, tablas con encabezados y `scope`, zoom 200 %, `lang="es"`, color no exclusivo, estados anunciados y movimiento reducido; cuenta comercial fuera de `/admin/`.

---

## 11. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Bypass de membresía | Acceso indebido | Backends disjuntos y pruebas de los cinco casos |
| Consultas sin filtro de empresa | Fuga de datos | Servicios como única puerta; acceso cruzado por tarea |
| Autorización solo en plantillas | Escalada por URL | Doble verificación con la misma función |
| Carrera al crear dueño o empresa | Dos dueños o dos empresas | `select_for_update()`; riesgo residual documentado para el primer arranque |
| Auditoría revertida | Pérdida de evidencia | `on_commit` y `TransactionTestCase` |
| Inmutabilidad incompleta | Alteración de auditoría | Instancia y `QuerySet` restringidos |
| Regresión de pruebas de 001 | Bloqueo | Solo cambia la lista de apps; `base.html` intacto |
| `must_change_password` mal aplicado | Rutas sin bloqueo o usuario atrapado | Punto único en middleware y excepciones explícitas |
| Middleware afecta Admin o home | Bloqueo indebido | Exclusiones exactas y pruebas |
| 403 único | Incumple CA-09 o RF-14 | Dos variantes de 403 |
| Correas de auditoría en tests | Falsos negativos | `django_capture_on_commit_callbacks` |
| Variables obligatorias nuevas | Rompen pruebas DB-free | Variables opcionales con valor por defecto |
| Deriva de identidad | Identificador ambiguo | `Account.email` única; `username` opaco |
| Fuga en eventos o logs | Datos personales | Sin correo tentativo, contraseña ni cuerpos |
| Complejidad de permisos | Sobringenie | Cuatro roles fijos |

---

## 12. Puntos de autorización y control

| Gate | Cuándo | Quién | Alcance |
|---|---|---|---|
| G-0 | Antes de implementar | Usuario | Aprobación de `plan.md` y `tasks.md` |
| G-1 | Antes de la primera tarea de código | Usuario | Autorización de implementación |
| G-2 | Antes de generar y aplicar migraciones | Usuario | `makemigrations` y `migrate` |
| G-3 | Antes de comandos o servidor sobre desarrollo | Usuario | Comandos y validación manual |
| G-4 | Antes de la suite con base | Usuario | `nexopyme_bootstrap_test` según `DA-07` |
| G-5 | Por cada tarea con archivos | Implementer y Build | `git add` y commit de Implementer; push de Build |

### 12.1 Política de Git por tarea

- Un commit por tarea con archivos versionables, incluido su registro en `tasks.md`.
- Implementer ejecuta `git add` de los archivos de la tarea y `git commit` en inglés tras el APROBADO; Build verifica y hace `push`.
- Revisión y commit incrementales; el checkpoint cierra cuando todas sus tareas están aprobadas.
- Toda tarea que modifique archivos genera commit, aunque el único archivo sea `tasks.md`.
- `MEMORY.md` se actualiza y se commitea solo en T-26.

---

## 13. Revisión del Reviewer

| Checkpoint | Momento | Alcance | Veredicto |
|---|---|---|---|
| RC-1 | Antes de implementar | `plan.md` y `tasks.md` | APROBADO / CAMBIOS NECESARIOS |
| RC-5 | Tras T-01–T-09 | Capacidades, modelos, auditoría, servicios, middleware y autorización | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-6 | Tras T-10–T-19 | Acceso, panel, empresa, auditoría y Admin | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-7 | Tras T-20–T-24 | Seguridad, pruebas, calidad, validación y documentación | APROBADO / CAMBIOS NECESARIOS por tarea |
| T-25 | Tras T-24 commiteado | Etapa completa | APROBADO / CAMBIOS NECESARIOS |

---

## 14. Matriz de trazabilidad resumida

| Requisitos | CA | RN | Tareas |
|---|---|---|---|
| RF-01, RF-02, RF-22 | CA-01, CA-02, CA-22 | RN-13 | T-10, T-15 |
| RF-03, RF-04, RF-17 | CA-03, CA-04, CA-17 | — | T-11, T-09 |
| RF-05, RF-06, RF-07 | CA-05, CA-06, CA-07 | RN-12 | T-12 |
| RF-08, RF-09, RF-10 | CA-08, CA-09, CA-10 | RN-07, RN-10, RN-17 | T-08, T-21 |
| RF-11, RF-12, RF-13 | CA-11, CA-12, CA-13 | RN-08, RN-09, RN-17 | T-09, T-21 |
| RF-14 a RF-20 | CA-14 a CA-20 | RN-05, RN-06, RN-15 | T-02, T-09 |
| RF-21, RF-22 | CA-21, CA-22 | RN-03, RN-12, RN-13 | T-06, T-15 |
| RF-23 | CA-23 | RN-07 | T-14 |
| RF-24 a RF-28 | CA-24 a CA-28 | RN-02, RN-03, RN-04, RN-05, RN-11 | T-06, T-07, T-16 |
| RF-29 | CA-29 | RN-06 | T-09 |
| RF-30, RF-32 | CA-30, CA-32 | RN-01 | T-03, T-07, T-13 |
| RF-31 | CA-31 | RN-14; RNF-14 | T-17 |
| RF-33 a RF-36 | CA-33 a CA-36 | RN-16 | T-19 |
| RF-37 a RF-40 | CA-37 a CA-40 | RN-14 | T-04, T-05, T-18, T-21 |
| RF-41 | CA-41 | RN-12, RN-14 | T-13 |
| RNF-01 | CA-08 a CA-13, CA-39 | — | T-21 |
| RNF-02 | CA-14 a CA-19, CA-29, CA-33 a CA-36 | RN-16 | T-09, T-19 |
| RNF-03 | CA-01 a CA-06, CA-25, CA-27, CA-40 | — | T-10 a T-12, T-16, T-20 |
| RNF-04, RNF-05 | CA-37 a CA-40 | RN-14 | T-04, T-05, T-20 |
| RNF-06 | CA-08, CA-10, CA-23 | RN-10 | T-08 |
| RNF-07, RNF-08 | CA-42, CA-43 | — | T-23 |
| RNF-09, RNF-11 | CA-44 | — | T-22 |
| RNF-10 | CA-42, CA-43 | — | T-23 |
| RNF-12 | Verificación de configuración | — | T-01, T-24 |
| RNF-13 | CA-34, CA-36 | RN-16 | T-19 |
| RNF-14 | CA-21, CA-24, CA-31, CA-36 | — | T-06, T-17, T-19 |

**Evidencia de CA-14, CA-18 y CA-19:** la literal pertenece a `specs/002`; en esta etapa se verifica el comportamiento equivalente en el panel y se difiere la literal a 002 (O-1).

---

## 15. Criterios de cierre

1. Las 26 tareas completadas con evidencia.
2. CA-01 a CA-44 verificados o diferidos con evidencia declarada.
3. Los 41 RF, 17 RN y 14 RNF cubiertos.
4. `ruff check .` sin errores y suite en verde, incluida `tests/test_db_guards.py`.
5. Validación funcional y visual aprobada por el usuario.
6. Commits por tarea publicados y árbol limpio.
7. `MEMORY.md` actualizado y commiteado.
8. Revisión final del Reviewer con APROBADO.
9. Informe final al usuario.

---

## 16. Fuera de alcance

Varias empresas activas, selector de empresa, recuperación automática por correo, SSO, MFA, registro público, roles personalizados, permisos por objeto, transferencia de propiedad, módulos de negocio, exportación o purga de auditoría, cambios en `specs/002`, en las guardas o en el modelo de usuario.

---

## 17. Anexo: comandos previstos (no ejecutados)

```text
# Migraciones (G-2 y G-3)
python manage.py makemigrations accounts
python manage.py migrate
python manage.py makemigrations audit
python manage.py migrate

# Inicialización y recuperación (G-3)
python manage.py init_company --name "Nombre del negocio" --email "dueno@ejemplo.com"
python manage.py reset_owner_password --email "dueno@ejemplo.com"

# Pruebas DB-free
python -m pytest tests/test_project_structure.py tests/test_settings_foundation.py \
  tests/test_home_view.py tests/test_urls.py tests/test_admin_unfold.py \
  tests/test_accounts_capabilities.py tests/test_accounts_forms.py -q

# Pruebas con base autorizada (G-4)
python -m pytest tests/test_accounts_auth.py tests/test_accounts_authorization.py \
  tests/test_accounts_middleware.py tests/test_accounts_users.py \
  tests/test_accounts_company.py tests/test_accounts_audit.py \
  tests/test_accounts_isolation.py tests/test_accounts_commands.py \
  tests/test_accounts_admin_separation.py tests/test_accounts_security.py \
  tests/test_db_guards.py -q

# Calidad
python -m ruff check .
```

Ninguno se ejecutó durante la planificación.

---

## 18. Observaciones que requieren confirmación del usuario

| ID | Observación | Efecto si se confirma |
|---|---|---|
| O-1 | CA-14, CA-18 y CA-19 describen 403 en superficies de productos e historial de `specs/002`, aún no implementados | Se verifica el comportamiento equivalente en el panel y se difiere la literal a 002; no se modifica la especificación 003 |
| O-2 | La creación de `apps.accounts` y `apps.audit` obliga a actualizar `tests/test_project_structure.py` | Único cambio previsto a una prueba de 001; el resto queda intacto |
| O-3 | El correo vive en `Account.email` (254) y `username` es un valor opaco | Evita una limitación no prevista y no cambia el comportamiento observable |
| O-4 | La home pública conserva el enlace a `/admin/`; el acceso se deniega, pero el enlace revela la existencia del Admin | Se mantiene sin cambios; se registra como limitación conocida y se evaluará en la etapa de interfaz pública |

Las decisiones A-09, A-10 y A-13 ya fueron aprobadas por el usuario el 2026-11-10 y no requieren nueva confirmación.
