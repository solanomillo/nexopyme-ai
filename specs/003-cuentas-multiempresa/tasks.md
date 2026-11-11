# Tareas 003 — Cuentas y multiempresa

## 1. Identificación

| Campo | Valor |
|---|---|
| Funcionalidad | 003 — Cuentas y multiempresa |
| Artefacto | `specs/003-cuentas-multiempresa/tasks.md` |
| Versión | 1.4 |
| Estado | G-0 APROBADO — T-01 a T-15 publicadas; RC-5 APROBADO (2026-11-10); T-16 pendiente |
| Especificación | `spec.md` v1.0 aprobada el 2026-11-10 |
| Plan | `plan.md` v1.4 (v1.2 aprobado; v1.3 registra `/panel/`; v1.4 ajusta §7.6 al middleware de T-12) |
| Fecha | 2026-11-10 |
| Responsable | Planner |
| Tareas | 26 (T-01 a T-26) |

**Historial:** v1.0 inicial; v1.1 correcciones del primer dictamen; v1.2 correcciones del segundo dictamen y renumeración secuencial (capacidades → modelos → auditoría → servicios); v1.3 registro de la corrección documental de T-11 (`/panel/`, `panel.html`, validación visual y estilos diferidos a T-22/T-23); v1.4 sincroniza con `plan.md` v1.4 y registra las correcciones de T-12 (consulta de perfil filtrada por empresa, pruebas adicionales).

---

## 2. Convenciones

- `[ ]` no iniciada; `[x]` completada y aprobada; `[~]` implementada y pendiente de aprobación o commit; `[!]` bloqueada.
- Cada tarea es pequeña, ordenada y verificable.
- Ninguna tarea de implementación comienza sin `G-1`; ninguna migración se genera ni aplica sin `G-2` y `G-3`.
- Las pruebas con base usan exclusivamente `nexopyme_bootstrap_test` (`DA-07`) y las guardas existentes.
- `conftest.py` raíz, `config/settings_test.py`, `pytest.ini` y `tests/test_db_guards.py` no se modifican; `tests/conftest.py` es nuevo y solo contiene fixtures.
- Las evidencias no contienen contraseñas, tokens ni datos personales.
- Toda prueba que afirme registros de auditoría usa `django_capture_on_commit_callbacks(execute=True)`; `TransactionTestCase` se reserva para la reversión.
- **Git:** un commit por tarea con archivos versionables, incluido su registro de estado en este archivo. La revisión y el commit son incrementales: cada tarea se revisa y se commitea antes de que la siguiente modifique los mismos archivos. Toda tarea que modifique archivos genera commit, aunque el único archivo sea `tasks.md`.
- `MEMORY.md` se actualiza y se commitea solo en T-26.

---

## 3. Prerrequisitos ejecutados

| Prerrequisito | Estado |
|---|---|
| Etapa 001 cerrada y publicada | Cumplido: `bef5c58` |
| Especificación 003 aprobada | Cumplido: v1.0, 2026-11-10 |
| DA-01 a DA-08 | Aprobadas el 2026-11-10 |
| A-09, A-10 y A-13 | Aprobadas el 2026-11-10 al autorizar la planificación |
| Base de pruebas autorizada | `DA-07`, solo para esta etapa |
| Dependencias nuevas | Ninguna |

---

## 4. Resumen de tareas

| ID | Tarea | Fase | Depende de | Gate | Estado |
|---|---|---|---|---|---|
| T-01 | Verificar estado de partida y guardas | F0 | — | — | `[x]` |
| T-02 | Catálogo de roles y capacidades | F1 | T-01 | G-1 | `[x]` |
| T-03 | Modelos `Account`, `Company` y `Membership` | F1 | T-02 | G-1, G-2, G-3, G-4 | `[x]` |
| T-04 | Auditoría: modelos y migración | F1 | T-03 | G-1, G-2, G-3, G-4 | `[x]` |
| T-05 | Servicios de auditoría y eventos de seguridad | F1 | T-04 | G-1, G-4 | `[x]` |
| T-06 | Servicios de empresa y membresía | F2 | T-03, T-05 | G-1, G-4 | `[x]` |
| T-07 | Invariantes y concurrencia | F2 | T-06 | G-1, G-4 | `[x]` |
| T-08 | Middleware de contexto y punto de bloqueo | F3 | T-03, T-07 | G-1, G-4 | `[x]` |
| T-09 | Autorización en vistas y servicios | F3 | T-02, T-08 | G-1, G-4 | `[x]` |
| T-10 | Backends de autenticación | F4 | T-03, T-09 | G-1, G-4 | `[x]` |
| T-11 | Acceso, cierre de sesión y rutas protegidas | F4 | T-10 | G-1, G-4 | `[x]` |
| T-12 | Cambio obligatorio y autogestión de contraseña | F4 | T-11 | G-1, G-4 | `[x]` |
| T-13 | Comandos de inicialización y recuperación | F5 | T-07, T-12 | G-1, G-3, G-4 | `[x]` |
| T-14 | Listado de usuarios del panel | F5 | T-09, T-12 | G-1, G-4 | `[x]` |
| T-15 | Alta de empleado con contraseña temporal | F5 | T-14 | G-1, G-4 | `[x]` |
| T-16 | Rol, desactivación, reactivación y regeneración | F5 | T-15 | G-1, G-4 | `[ ]` |
| T-17 | Configuración de la empresa | F6 | T-06, T-16 | G-1, G-4 | `[ ]` |
| T-18 | Consulta de auditoría y eventos | F6 | T-05, T-09 | G-1, G-4 | `[ ]` |
| T-19 | Separación Django Admin / panel comercial | F7 | T-10 | G-1, G-4 | `[ ]` |
| T-20 | Seguridad de sesión y logging técnico | F7 | T-11, T-19 | G-1, G-4 | `[ ]` |
| T-21 | Pruebas de aislamiento entre empresas | F8 | T-02 a T-20 | G-4 | `[ ]` |
| T-22 | Integración, regresión y calidad | F8 | T-21 | G-4 | `[ ]` |
| T-23 | Validación funcional y visual | F9 | T-22 | G-3 | `[ ]` |
| T-24 | Documentación de la etapa | F9 | T-23 | — | `[ ]` |
| T-25 | Revisión final del Reviewer | F9 | T-24 | — | `[ ]` |
| T-26 | Cierre documental y verificación Git | F9 | T-25 | G-5 | `[ ]` |

La columna Gate lista G-1 a G-4. G-5 (commit y push por tarea) aplica a toda tarea que genere archivos: T-01 a T-24 y T-26; no se repite en cada fila.

---

## 5. Tareas detalladas

### T-01 — Verificar estado de partida y guardas

- **Objetivo:** confirmar repositorio, configuración y guardas antes de escribir código.
- **Alcance:** solo el registro de estado en `tasks.md`.
- **Dependencias:** ninguna.
- **Pasos:**
  1. Verificar `HEAD` = `origin/main` = `bef5c58`.
  2. Verificar que las guardas no tienen cambios.
  3. Ejecutar `python manage.py check`.
  4. Ejecutar las 20 pruebas DB-free de la Etapa 001.
  5. Ejecutar `python -m ruff check .`.
  6. Registrar el resultado.
- **Verificación:** igualdad de referencias; 20 pruebas en verde; Ruff sin errores; guardas intactas.
- **Evidencia:** salidas de los comandos y `git status`.
- **Trazabilidad:** RNF-09, RNF-12.
- **Registro de ejecución (2026-11-10):** `HEAD` = `origin/main` = `bef5c58`, divergencia `0 0`. `python manage.py check` → sin problemas. 20 pruebas DB-free en verde (1,09 s). `ruff check .` → All checks passed (exit 0). `conftest.py`, `config/settings_test.py`, `pytest.ini` y `tests/test_db_guards.py` sin cambios. `config/settings.py` usa `django.db.backends.mysql`; sin SQLite operativo, sin migraciones, sin base de pruebas y sin dependencias nuevas. `git status`: sin cambios en archivos versionados; `specs/003-cuentas-multiempresa/` aún sin versionar (`spec.md`, `plan.md`, `tasks.md`); `.opencode/`, `opencode.jsonc` y `specs/002-productos-inventario/` permanecen fuera del control de versiones por decisión previa. Dictamen del Reviewer: APROBADO (2026-11-10). Cierre: commit `4344c31` publicado; `spec.md` y `plan.md` versionados en `d907766`; corrección de estado de §17 en `a355248`.

### T-02 — Catálogo de roles y capacidades

- **Objetivo:** definir la fuente única de roles, capacidades y asignación.
- **Alcance:** paquete `apps/accounts` (`__init__.py`, `apps.py`, `capabilities.py`), `config/settings.py`; `tests/test_accounts_capabilities.py`; `tests/test_project_structure.py`.
- **Dependencias:** T-01.
- **Pasos:**
  1. Crear el paquete `apps/accounts` con `AppConfig`.
  2. Definir `Role`, `Capability`, `ROLE_CAPABILITIES` y `has_capability`.
  3. Insertar `"apps.accounts"` antes de `"apps.core"` en `INSTALLED_APPS` (D-11).
  4. Actualizar la aserción de aplicaciones de `tests/test_project_structure.py` para incluir `accounts` (O-2).
  5. Escribir pruebas de matriz completa, rol sin capacidades y capacidad desconocida, y una guarda que recorra `apps/` y falle si aparece otra definición de `Role`, `Capability` o `ROLE_CAPABILITIES` fuera de `capabilities.py` (CA-20).
- **Verificación:** matriz idéntica a la especificación §4.3; `apps.core` al final; prueba de estructura en verde; guarda de que no existe otra definición de roles o capacidades fuera de `capabilities.py` (CA-20).
- **Evidencia:** pytest de capacidades y estructura.
- **Trazabilidad:** RF-14, RF-16, RF-20; CA-14, CA-16, CA-20; RN-05, RN-06.
- **Registro de ejecución (2026-11-10):** `apps/accounts` creada con `AccountsConfig`; `Role`, `Capability`, `ROLE_CAPABILITIES` y `has_capability` en `capabilities.py`; `"apps.accounts"` insertado antes de `"apps.core"`; prueba de estructura actualizada; **14 pruebas en verde** (9 del catálogo + 5 de estructura), incluida la guarda CA-20; `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-03 — Modelos `Account`, `Company` y `Membership`

- **Objetivo:** representar cuentas, empresa y membresía con las restricciones acordadas.
- **Alcance:** `apps/accounts/{models,emails}.py`, `migrations/0001_initial.py`, `tests/conftest.py`, `tests/test_accounts_company.py`.
- **Dependencias:** T-02.
- **Pasos:**
  1. Implementar `Account` con `user`, `email` único normalizado y `display_name`.
  2. Implementar `Company` y `Membership` con `unique(account, company)` e índices.
  3. Generar `auth.User.username` como valor opaco único (D-15).
  4. Centralizar `normalize_email()` en `emails.py`.
  5. Generar y aplicar la migración (G-2, G-3).
  6. Crear `tests/conftest.py` con fixtures de empresa, cuenta y membresía.
  7. Probar unicidad, normalización, correo de 254 caracteres y valores por defecto.
- **Verificación:** migración aplicada; correo único en base; `username` opaco; pruebas de modelo en verde.
- **Evidencia:** salidas de migración y pytest.
- **Trazabilidad:** RF-08, RF-21 a RF-28, RF-30, RF-32; RN-01, RN-02, RN-03, RN-04; RNF-01.
- **Registro de ejecución (2026-11-10):** migración `accounts.0001_initial` generada y aplicada en `nexopyme_bootstrap_dev` (`showmigrations` → `[X]`); `manage.py check` sin problemas; 8 pruebas de modelo en verde (incluye unicidad de correo, correo de 254 caracteres, unicidad de membresía y `username` opaco); `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10). Sin avance a servicios ni middleware.
- **Prohibido:** modelos de rol o permiso; registrar en Admin; alterar `auth`; modificar el `conftest.py` raíz.

### T-04 — Auditoría: modelos y migración

- **Objetivo:** disponer de la auditoría compartida con integridad referencial.
- **Alcance:** `apps/audit/{__init__,apps,models}.py`, `migrations/0001_initial.py`; `config/settings.py`; `tests/test_accounts_audit.py`; `tests/test_project_structure.py`.
- **Dependencias:** T-03.
- **Pasos:**
  1. Crear la aplicación `apps.audit`.
  2. Definir `AuditEvent` y `SecurityEvent` con FK a `Company` e índices por empresa y fecha.
  3. Implementar la inmutabilidad por instancia y por `QuerySet` en los modelos.
  4. Generar y aplicar la migración (G-2, G-3).
  5. Insertar `"apps.audit"` antes de `"apps.core"` (D-11).
  6. Actualizar la aserción de aplicaciones para incluir `audit` (O-2).
  7. Verificar `check`, `showmigrations` y las pruebas de estructura.
  8. Probar en `tests/test_accounts_audit.py` que `save()` posterior, `delete()`, `QuerySet.update()` y `QuerySet.delete()` quedan bloqueados.
- **Verificación:** migración aplicada; FKs correctas; `apps.core` al final; estructura en verde; inmutabilidad probada.
- **Evidencia:** salidas de migración y pytest.
- **Trazabilidad:** RF-37, RF-38, RF-40; RN-14; RNF-04; DA-08.
- **Registro de ejecución (2026-11-10):** migración `audit.0001_initial` generada y aplicada en `nexopyme_bootstrap_dev` (`showmigrations` → `[X]`); `manage.py check` sin problemas; 12 pruebas en verde (7 de auditoría + 5 de estructura), incluidas inmutabilidad por instancia y por `QuerySet` en ambos modelos, eventos sin actor ni empresa y ausencia de campos sensibles; `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10).
- **Prohibido:** registrar en Admin; migraciones de datos; alterar guardas.

### T-05 — Servicios de auditoría y eventos de seguridad

- **Objetivo:** centralizar el registro con las garantías de la especificación.
- **Alcance:** `apps/audit/services.py`; `tests/test_accounts_audit.py`.
- **Dependencias:** T-04.
- **Pasos:**
  1. Implementar `record_audit` y `record_security`.
  2. Registrar la auditoría de negocio con `transaction.on_commit`.
  3. Registrar el evento de seguridad en el límite de rechazo, fuera del bloque atómico.
  4. Sanear los datos: sin contraseñas, tokens ni correo tentativo.
  5. Escribir pruebas con `django_capture_on_commit_callbacks(execute=True)` y `TransactionTestCase` para la reversión.
- **Verificación:** la auditoría se registra solo tras el commit; el evento sobrevive al rechazo; no hay datos sensibles.
- **Evidencia:** pytest del archivo.
- **Trazabilidad:** RF-38, RF-40; RN-14; RNF-04, RNF-05.
- **Registro de ejecución (2026-11-10):** implementados `record_audit` (con `transaction.on_commit`) y `record_security` (inmediato, fuera del bloque de negocio), con saneamiento recursivo de claves sensibles y sin mutar los datos originales; 14 pruebas del archivo de auditoría en verde, incluidas captura de `on_commit`, diferimiento hasta el commit, saneamiento y supervivencia al rechazo con `TransactionTestCase`; `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-06 — Servicios de empresa y membresía

- **Objetivo:** concentrar las mutaciones de cuentas en servicios auditados.
- **Alcance:** `apps/accounts/services.py`; `tests/test_accounts_company.py`.
- **Dependencias:** T-03, T-05.
- **Pasos:**
  1. Implementar `create_company_with_owner`, `create_employee`, `change_role`, `deactivate_membership`, `reactivate_membership`, `regenerate_temporary_password` y `update_company_name`.
  2. Revalidar capacidad y empresa en cada servicio.
  3. Auditar cada mutación con valores anterior y nuevo y sin secretos.
  4. Rechazar rol `dueno` en alta y cambio, y cualquier operación que deje la empresa sin dueño.
  5. Probar alta, cambio de rol, desactivación, reactivación, regeneración, rechazos y auditoría.
- **Verificación:** cada mutación queda auditada (con `django_capture_on_commit_callbacks(execute=True)`); los rechazos no persisten cambios; el correo duplicado no crea registros parciales.
- **Evidencia:** pytest del archivo.
- **Trazabilidad:** RF-21, RF-24 a RF-28, RF-30; CA-21, CA-24 a CA-28, CA-30, CA-37; RN-14; RNF-14.
- **Registro de ejecución (2026-11-10):** implementados `create_company_with_owner`, `create_employee`, `change_role`, `deactivate_membership`, `reactivate_membership`, `regenerate_temporary_password` y `update_company_name`; revalidación de aislamiento y capacidad, rechazo de segundo dueño, de la degradación del último dueño y de la regeneración del dueño por panel, contraseñas temporales y auditoría con valores anterior y nuevo; **25 pruebas en verde** (8 de modelo + 17 de servicios) y `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-07 — Invariantes y concurrencia

- **Objetivo:** garantizar dueño único, empresa activa única y una sola membresía por cuenta, incluso con solicitudes concurrentes.
- **Alcance:** `apps/accounts/services.py`; `tests/test_accounts_company.py`.
- **Dependencias:** T-06.
- **Pasos:**
  1. Implementar `ensure_single_owner`, la unicidad de empresa activa y la de membresía por cuenta.
  2. Usar `transaction.atomic()` y `select_for_update()` en las operaciones sensibles.
  3. Verificar que la desactivación impide nuevas autenticaciones y retira el acceso.
  4. Probar invariantes y carrera con transacciones.
- **Verificación:** no se puede crear un segundo dueño ni una segunda empresa activa; una cuenta no obtiene dos membresías.
- **Evidencia:** pytest del archivo.
- **Trazabilidad:** RF-28, RF-32; CA-28, CA-32; RN-02, RN-04, RN-11; RNF-01.
- **Registro de ejecución (2026-11-10):** implementados `ensure_single_owner` y bloqueo `select_for_update()` sobre la empresa en inicialización, cambio de rol y desactivación; rechazo de empresa duplicada, de degradación del último dueño y de empresa con cero o dos dueños; **30 pruebas en verde** (8 de modelo + 22 de servicios) y `ruff check .` → All checks passed. No se añade prueba de carrera por limitación del entorno: el bloqueo se verifica por código y el riesgo residual de tabla vacía queda documentado. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-08 — Middleware de contexto y punto de bloqueo

- **Objetivo:** resolver empresa y membresía una vez por solicitud y definir el único punto de bloqueo por contraseña temporal.
- **Alcance:** `apps/accounts/middleware.py`, `config/settings.py`, `tests/test_accounts_middleware.py`.
- **Dependencias:** T-03, T-07.
- **Pasos:**
  1. Implementar `ActiveCompanyMiddleware` después de `AuthenticationMiddleware`.
  2. Resolver membresía y empresa con una consulta y `select_related`.
  3. Excluir `/`, `/health/`, `/favicon.ico`, `/static/`, `/admin/`, `/login/`, `/logout/` y `/password/`.
  4. Denegar con `PermissionDenied` si la membresía o la empresa están inactivas; un visitante no autenticado no recibe contexto y delega en `login_required`.
  5. Definir el punto único de evaluación de `must_change_password` (la rama de redirección se completa en T-12).
  6. Detectar un identificador de empresa en la solicitud distinto de `request.company.pk` y responder 404 uniforme con evento de seguridad; si coincide o falta, el alcance sigue siendo el de la sesión.
  7. Probar `assertNumQueries`, rutas excluidas, visitante anónimo, empresa inactiva, `company_id` coincidente (200 con datos de la sesión y una sola resolución) y `company_id` distinto (404 uniforme con evento).
- **Verificación:** una consulta de contexto por solicitud; Admin y home sin cambios; denegación correcta; anónimo redirigido; identificador coincidente aceptado; inyección rechazada con evento.
- **Evidencia:** pytest del archivo.
- **Trazabilidad:** RF-08, RF-09, RF-10; CA-08, CA-09, CA-10; RN-07, RN-10, RN-17; RNF-06.
- **Registro de ejecución (2026-11-10):** `ActiveCompanyMiddleware` insertado tras `AuthenticationMiddleware`; resuelve membresía y empresa con una consulta `select_related`; expone `request.must_change_password` como punto único de evaluación para T-12; excluye `/`, `/health/`, `/favicon.ico`, `/static/`, `/admin/`, `/login/`, `/logout/` y `/password/`; deniega con 403 sin membresía o con empresa inactiva; detecta `company` inyectado distinto en GET o POST y responde 404 con evento de seguridad. **9 pruebas en verde** (contexto, anónimo, membresía inactiva, empresa inactiva, exclusiones, helper de exclusiones, inyección GET, inyección POST y coincidencia) y `ruff check .` → All checks passed. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-09 — Autorización en vistas y servicios

- **Objetivo:** imponer capacidades en servidor con códigos y mensajes correctos.
- **Alcance:** `apps/accounts/{decorators,services,views}.py`, `templates/errors/{403,404}.html`, `config/urls.py`; `tests/test_accounts_authorization.py`.
- **Dependencias:** T-02, T-08.
- **Pasos:**
  1. Implementar `require_capability` delegando en `has_capability`.
  2. Usar la misma función en los servicios.
  3. Implementar 404 uniforme para recurso ajeno, inexistente o identificador de empresa ajeno.
  4. Implementar un único `handler403` con dos mensajes según el motivo: acceso denegado sin contexto (con cierre de sesión) y permiso insuficiente; `handler404` uniforme. Usar vistas mínimas de prueba en el módulo de pruebas hasta que existan las vistas reales.
  5. Probar 403 en sus dos variantes, 404 uniforme, orden de comprobaciones, evento de seguridad y ausencia de verificaciones ad hoc.
- **Verificación:** códigos y mensajes correctos; el orden se respeta; no se filtra información; las dos variantes de 403 se prueban con `DEBUG=False`.
- **Evidencia:** pytest del archivo y revisión de templates.
- **Trazabilidad:** RF-11 a RF-19, RF-29; CA-11 a CA-19, CA-29, CA-38; RN-08, RN-09, RN-15.
- **Nota:** CA-14, CA-18 y CA-19 se verifican con evidencia equivalente en el panel; la literal corresponde a 002 (O-1).
- **Registro de ejecución (2026-11-10):** `require_capability` delega en `has_capability`; los servicios ya delegaban desde T-06 y no requirieron cambios; `handler403` distingue acceso sin contexto (con opción de cerrar sesión) de permiso insuficiente y registra `permission.denied`; `handler404` uniforme para recurso ajeno, inexistente o empresa inyectada; orden aislamiento → capacidad verificado; **15 pruebas en verde** (6 de autorización + 9 de middleware, sin regresión) y `ruff check .` → All checks passed. El enlace de cierre de sesión apunta a `/logout/`, que implementa T-11; la validación con `DEBUG=False` queda para T-22/T-23. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-10 — Backends de autenticación

- **Objetivo:** autenticar cuentas comerciales por correo sin bypass y mantener el acceso técnico.
- **Alcance:** `apps/accounts/backends.py`, `config/settings.py`; `tests/test_accounts_auth.py`.
- **Dependencias:** T-03, T-09.
- **Pasos:**
  1. Implementar `EmailBackend` para cuentas comerciales: membresía y empresa activas; rechaza personal y superusuarios.
  2. Implementar `TechnicalAdminBackend` restringido a `is_staff`.
  3. Configurar `AUTHENTICATION_BACKENDS`, `LOGIN_URL`, `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL`.
  4. Probar cuenta válida, membresía inactiva, cuenta inactiva, personal sin membresía y cuenta comercial contra Admin.
- **Verificación:** ninguna cuenta comercial se autentica sin membresía activa; el personal entra solo por Admin.
- **Evidencia:** pytest del archivo.
- **Trazabilidad:** RF-01, RF-02; CA-01, CA-02, CA-38; RN-13, RN-16; RNF-03.
- **Registro de ejecución (2026-11-10):** `EmailBackend` autentica solo cuentas comerciales con cuenta, membresía y empresa activas, normaliza el correo y rechaza personal y superusuarios; `TechnicalAdminBackend` autentica solo `is_staff` sin cuenta comercial; ambos caminos registran el fallo sin correo ni contraseña y ambos `get_user` descartan usuarios inactivos. Configurados `AUTHENTICATION_BACKENDS`, `LOGIN_URL`, `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL`. **18 pruebas en verde** (1 DB-free de configuración + 17 con base) y `ruff check .` → All checks passed; `manage.py check` sin problemas. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-11 — Acceso, cierre de sesión y rutas protegidas

- **Objetivo:** ofrecer la puerta de entrada del panel y proteger las rutas.
- **Alcance:** `apps/accounts/views.py`, `urls.py`, `templates/accounts/login.html`, `templates/base_panel.html`, `config/urls.py`; `tests/test_accounts_auth.py`.
- **Dependencias:** T-10.
- **Pasos:**
  1. Implementar acceso y cierre de sesión con destino seguro.
  2. Crear `base_panel.html` sin modificar `base.html` (D-12).
  3. Proteger las rutas del panel y añadir cabeceras de no almacenamiento (`no-store`) a las respuestas autenticadas.
  4. Implementar estados de error y carga.
  5. Probar redirección, cierre, destino seguro, ausencia de cambios en `base.html` y cabeceras de no almacenamiento.
- **Verificación:** sin sesión se redirige; el cierre invalida la sesión; la prueba de la home sigue en verde.
- **Evidencia:** pytest y verificación estructural de estados; la validación visual formal y los ajustes de estilo se abordan en T-22/T-23 (plan §10).
- **Trazabilidad:** RF-03, RF-04; CA-03, CA-04; RNF-03.
- **Registro de ejecución (2026-11-10):** `PanelLoginView` usa `EmailAuthenticationForm` con mensaje genérico y `redirect_authenticated_user`; los errores de campo se asocian con `aria-invalid` y `aria-describedby`; `PanelLogoutView` exige POST y vuelve a `/login/`; `panel_home` en `/panel/` está protegido por `login_required` y decorado con `no_store` (`Cache-Control: no-store`). `base_panel.html` es una plantilla independiente con navegación, contexto de empresa/membresía y cierre de sesión por POST, sin modificar `base.html` (D-12); `accounts/panel.html` la extiende como landing del panel. `login.html` extiende `base.html` e incluye estados de error (`role="alert"`) y carga (`aria-busy` + botón deshabilitado). Rutas incluidas en `config/urls.py` con namespace `accounts`; `/panel/` y `panel.html` quedan registrados en `plan.md` v1.3. **44 pruebas en `test_accounts_auth.py`** (18 de T-10 + 26 de T-11; 5 DB-free y 39 con base) y **51 en verde** junto con `test_home_view.py` y `test_urls.py`; `ruff check .` → All checks passed; `manage.py check` sin problemas. Limitaciones registradas: la validación visual formal y los estilos del formulario se abordan en T-22/T-23, fuera del alcance de T-11; los enlaces a `/profile/`, `/users/`, `/company/` y `/audit/` quedan transitoriamente en 404 hasta T-12/T-14/T-17/T-18; el 403 del middleware no lleva `no-store` y se evaluará en T-20; `base_panel.html` accede a `request.user.account.display_name` y añade una consulta por render, que se revisará en T-21 (RNF-06) sin modificar el middleware de T-08. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-12 — Cambio obligatorio y autogestión de contraseña

- **Objetivo:** garantizar el cambio de la contraseña temporal y permitir la autogestión.
- **Alcance:** vistas y plantillas `password_change.html` y `profile.html`; `middleware.py`, `views.py`, `urls.py`; `tests/test_accounts_auth.py`.
- **Dependencias:** T-11.
- **Pasos:**
  1. Completar en el middleware la redirección a `/password/` cuando `must_change_password` esté activo, con excepciones para `/logout/`, `/password/` y `/static/`.
  2. Implementar el cambio con contraseña actual y validadores.
  3. Limpiar el indicador y auditar el cambio sin valores (RF-06), comprobando la auditoría con `django_capture_on_commit_callbacks(execute=True)`.
  4. Implementar el perfil propio y exponer `/profile/<int:pk>/`: propio → 200; otra cuenta de la misma empresa → 403 sin datos; otra empresa → 404 uniforme.
  5. Probar el bloqueo de todas las rutas del panel, las excepciones, el cambio correcto, la contraseña actual errónea y los tres casos de perfil.
- **Verificación:** ninguna ruta del panel queda sin bloqueo ni atrapada; el cambio exige la actual; la auditoría no registra valores.
- **Evidencia:** pytest y capturas de estados.
- **Trazabilidad:** RF-05, RF-06, RF-07; CA-05, CA-06, CA-07; RN-12; RNF-03.
- **Registro de ejecución (2026-11-10):** el middleware ya no excluye `/password/`; resuelve `request.account` con `select_related("account", "company")` y redirige cualquier ruta del panel a `/password/` cuando `must_change_password` está activo, salvo `/logout/`, `/password/` y `/static/`. `PanelPasswordChangeForm` exige la contraseña actual, aplica los validadores, asocia errores con `aria-invalid`/`aria-describedby`, limpia el indicador, actualiza el hash de sesión y audita `password.changed` sin valores (`before`/`after` nulos). `/profile/` redirige al perfil propio; `/profile/<int:pk>/` consulta la membresía filtrando por `company=request.company` y `account_id=pk`, responde 200 para la cuenta propia, 403 sin datos para otra cuenta de la misma empresa y 404 uniforme para otra empresa o cuenta inexistente. Plantillas `password_change.html` y `profile.html` con estados de error, carga y éxito; el enlace de perfil de `base_panel.html` usa `{% url %}`. **61 pruebas en `test_accounts_auth.py`** (18 de T-10 + 26 de T-11 + 17 de T-12; 5 DB-free y 56 con base), **9 en `test_accounts_middleware.py`** y **77 en verde** junto con `test_home_view.py` y `test_urls.py`; `ruff check .` → All checks passed; `manage.py check` sin problemas. Se actualizó la prueba de exclusiones de T-08 para reflejar que `/password/` ya no está excluida. La validación visual formal y los estilos se abordan en T-22/T-23. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-13 — Comandos de inicialización y recuperación

- **Objetivo:** crear la empresa y el dueño de forma idempotente y permitir la recuperación técnica.
- **Alcance:** `apps/accounts/management/commands/{init_company,reset_owner_password}.py`; `tests/test_accounts_commands.py`.
- **Dependencias:** T-07, T-12.
- **Pasos:**
  1. Implementar `init_company` con nombre y correo, contraseña interactiva y transacción.
  2. Definir idempotencia: con la empresa existente no se modifica nada y termina con éxito; con datos inconsistentes termina con error explícito.
  3. Implementar `reset_owner_password` con contraseña temporal mostrada una vez, cambio obligatorio y auditoría.
  4. Impedir que la contraseña aparezca en argumentos, logs o auditoría.
  5. Probar primera ejecución, segunda ejecución, datos inconsistentes y recuperación.
- **Verificación:** dos ejecuciones dejan una empresa y un dueño; la contraseña no se registra; el cambio obligatorio queda activo; la auditoría se comprueba con `django_capture_on_commit_callbacks(execute=True)`.
- **Evidencia:** pytest y salida de comandos sin secretos.
- **Trazabilidad:** RF-30, RF-41; CA-30, CA-41; RN-14; DA-04, DA-06.
- **Registro de ejecución (2026-11-10):** `init_company` recibe `--name`, `--email` y `--display-name` opcional, solicita la contraseña por `getpass` con confirmación y la valida con los validadores vigentes; no acepta `--password`. Es idempotente: si existe una empresa activa con un único dueño y el correo coincide, informa y no modifica nada; con más de una empresa activa, sin dueño único o con otro correo termina con `CommandError` explícito. La creación delega en `create_company_with_owner`, que audita `company.initialized` sin valores. `reset_owner_password` localiza al dueño activo por correo normalizado, genera una contraseña temporal con `generate_temporary_password`, la muestra una sola vez por `stdout`, activa `must_change_password` y audita `membership.owner_password_reset` con actor nulo y sin valores. Ninguna contraseña se acepta como argumento ni se escribe en logs o auditoría. **12 pruebas en `test_accounts_commands.py`** (creación, idempotencia, empresa sin dueño, dueño distinto, varias empresas activas, contraseña como argumento, política, confirmación, recuperación, correo inexistente, no dueño y ausencia de contraseña en logs) y **89 en verde** junto con auth, middleware, home y urls; `ruff check .` → All checks passed; `manage.py check` sin problemas. Los comandos no se ejecutaron sobre la base de desarrollo; la verificación se realizó con pytest sobre la base de pruebas autorizada. Limitaciones registradas: el evento `membership.owner_password_reset` usa `actor=None` y, por RF-39/CA-39, no se mostrará en la consulta de T-18 (se revisará en T-18/T-24); el endurecimiento de `--display-name` vacío o excesivo, la traducción de `IntegrityError` por correo existente y las pruebas adicionales (correo inválido, `--display-name`, dueño o empresa inactivos, contraseña ausente en logs de `init_company`) quedan para T-22. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-14 — Listado de usuarios del panel

- **Objetivo:** que el dueño consulte las cuentas de su empresa.
- **Alcance:** vista y `user_list.html`; `tests/test_accounts_users.py`.
- **Dependencias:** T-09, T-12.
- **Pasos:**
  1. Implementar listado paginado con correo, nombre, rol, estado y último acceso.
  2. Filtrar por la empresa de la sesión.
  3. Exigir `usuarios.gestionar`.
  4. Implementar estado vacío y navegación accesible.
  5. Incluir un caso de acceso cruzado.
- **Verificación:** solo se ven membresías de la empresa; sin capacidad se responde 403.
- **Evidencia:** pytest y validación visual.
- **Trazabilidad:** RF-23; CA-23; RN-07; RNF-01.
- **Registro de ejecución (2026-11-10):** `user_list` en `/users/` exige sesión y `usuarios.gestionar`, filtra `Membership.objects.select_related("account__user").filter(company=request.company)` y pagina 20 membresías por página con `Paginator.get_page`, tolerando páginas inválidas. `user_list.html` extiende `base_panel.html`, muestra correo, nombre, rol, estado y último acceso (o «Nunca»), un solo `h1`, tabla con `caption` y `scope`, estado vacío y navegación de paginación con `aria-label` y `rel`. No muestra credenciales ni datos de otra empresa. **8 pruebas en `test_accounts_users.py`** (ruta, login, capacidad, aislamiento entre empresas, estado y último acceso, estado vacío, paginación de 21 empleados y página inválida) y **97 en verde** junto con auth, middleware, comandos, home y urls; `ruff check .` → All checks passed; `manage.py check` sin problemas. La validación visual formal y los estilos se abordan en T-22/T-23. Limitaciones registradas: el enlace «Usuarios» de `base_panel.html` sigue siendo literal y visible para roles sin capacidad (se corrige en T-22/T-23); los docstrings de `views.py`/`urls.py` se actualizarán en la próxima tarea que los modifique; las pruebas de `page=0`, `page=999` y del parámetro `company` ajeno sobre `/users/` se consolidan en T-21. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-15 — Alta de empleado con contraseña temporal

- **Objetivo:** incorporar empleados con su rol.
- **Alcance:** vista y `user_form.html`; `tests/test_accounts_users.py` (alta y duplicado) y `tests/test_accounts_forms.py` (validación DB-free).
- **Dependencias:** T-14.
- **Pasos:**
  1. Implementar el formulario con correo, nombre y rol.
  2. Excluir `dueno` de las opciones.
  3. Generar la contraseña temporal y mostrarla una sola vez.
  4. Auditar el alta sin registrar la contraseña.
  5. Probar alta válida, correo duplicado, rol inválido, normalización y un intento con identificador de empresa ajeno.
- **Verificación:** cuenta y membresía se crean juntas; el duplicado devuelve 400 sin registros parciales; el alta queda auditada con `django_capture_on_commit_callbacks(execute=True)`.
- **Evidencia:** pytest y captura con contraseña enmascarada.
- **Trazabilidad:** RF-21, RF-22; CA-21, CA-22, CA-37; RN-13.
- **Registro de ejecución (2026-11-10):** `EmployeeCreateForm` en `apps/accounts/forms.py` con correo, nombre y rol; las opciones excluyen `dueno`; el correo se normaliza con `clean_email`; los campos inválidos reciben `aria-invalid` y `aria-describedby`. `user_create` en `/users/new/` exige sesión y `usuarios.gestionar`, delega en `create_employee` (servicio de T-07) y reutiliza su auditoría `membership.created` sin valores. En el POST exitoso devuelve 200 con la contraseña temporal en un bloque `role="status"` y no la repite en la siguiente petición; el duplicado responde 400 con error en el campo y sin registros parciales; el rol inválido responde 400; un `company` ajeno responde 404 uniforme y registra `company.scope.injected`. `user_list.html` incorpora el enlace «Crear usuario»; `user_form.html` incluye estados de error, envío con `aria-busy` y confirmación. Los errores agregados por el servicio (`DuplicateEmailError`) reaplican `aria-invalid`/`aria-describedby` mediante `EmployeeCreateForm.apply_error_attributes`. **7 pruebas DB-free en `test_accounts_forms.py`** y **8 pruebas de alta en `test_accounts_users.py`** (login, capacidad, formulario sin `dueno`, alta con contraseña mostrada una vez, duplicado con asociación accesible y sin usuario huérfano, rol inválido parametrizado, normalización y empresa inyectada); **113 en verde** junto con auth, middleware, comandos, home y urls; `ruff check .` → All checks passed; `manage.py check` sin problemas. La validación visual formal y los estilos se abordan en T-22/T-23. Limitaciones registradas: recargar el POST exitoso reenvía el formulario y responde 400 por duplicado (la contraseña solo se recupera con la regeneración de T-16), sin patrón PRG para no guardar el secreto en sesión; la verificación de extremo a extremo de CA-21 (acceso con la contraseña temporal y cambio obligatorio) se consolida en T-21; la captura con contraseña enmascarada queda diferida a T-22/T-23. Dictamen del Reviewer: APROBADO (2026-11-10).

### T-16 — Rol, desactivación, reactivación y regeneración

- **Objetivo:** completar la gestión de empleados sin romper invariantes.
- **Alcance:** vistas y `user_confirm.html`; servicios; `tests/test_accounts_users.py`.
- **Dependencias:** T-15.
- **Pasos:**
  1. Implementar cambio de rol con auditoría anterior y nuevo.
  2. Implementar desactivación y reactivación con contraseña temporal nueva.
  3. Implementar regeneración de contraseña temporal.
  4. Rechazar segundo dueño y empresa sin dueño.
  5. Probar cada operación, cada rechazo, el acceso cruzado y la efectividad en la siguiente solicitud.
- **Verificación:** el rol rige en la siguiente solicitud; la desactivación bloquea; el último dueño queda protegido; los cambios quedan auditados con `django_capture_on_commit_callbacks(execute=True)`.
- **Evidencia:** pytest y capturas de confirmación.
- **Trazabilidad:** RF-24 a RF-28; CA-24 a CA-28, CA-37; RN-04, RN-11; RNF-03.

### T-17 — Configuración de la empresa

- **Objetivo:** mantener el nombre del negocio.
- **Alcance:** vista y `company_form.html`; `tests/test_accounts_company.py`.
- **Dependencias:** T-06, T-16.
- **Pasos:**
  1. Implementar el formulario con `empresa.configurar`.
  2. Auditar valor anterior y nuevo.
  3. Probar actualización, permiso, validación y acceso cruzado.
- **Verificación:** solo el dueño actualiza; el cambio queda auditado con `django_capture_on_commit_callbacks(execute=True)`; sin campos adicionales.
- **Evidencia:** pytest y validación visual.
- **Trazabilidad:** RF-31; CA-31, CA-37; RN-14; RNF-14.

### T-18 — Consulta de auditoría y eventos

- **Objetivo:** consultar auditoría y eventos de la empresa.
- **Alcance:** vista y `audit_list.html`; `tests/test_accounts_audit.py`.
- **Dependencias:** T-05, T-09.
- **Pasos:**
  1. Implementar listado paginado de auditoría y eventos.
  2. Exigir `auditoria.consultar`.
  3. Filtrar por empresa y excluir eventos sin actor o de otra empresa.
  4. No mostrar el identificador de empresa intentada.
  5. Probar visibilidad, permiso y acceso cruzado.
- **Verificación:** solo el dueño consulta; no se filtran datos ajenos ni secretos.
- **Evidencia:** pytest y validación visual.
- **Trazabilidad:** RF-37 a RF-40; CA-37 a CA-40; RN-14.

### T-19 — Separación Django Admin / panel comercial

- **Objetivo:** reservar el Admin a superusuarios técnicos sin flujos de negocio.
- **Alcance:** `apps/core/admin.py`, `apps/accounts/admin.py`; `tests/test_accounts_admin_separation.py`.
- **Dependencias:** T-10.
- **Pasos:**
  1. Ajustar `UserAdmin` y `GroupAdmin` a solo lectura.
  2. No registrar `Account`, `Company`, `Membership`, `AuditEvent` ni `SecurityEvent`.
  3. Verificar redirección al login o denegación para cuentas comerciales.
  4. Verificar el acceso del superusuario técnico sin membresía.
  5. Mantener en verde `tests/test_admin_unfold.py`.
- **Verificación:** cuenta comercial sin acceso; superusuario con acceso; modelos de negocio no editables.
- **Evidencia:** pytest de separación y Unfold en verde.
- **Trazabilidad:** RF-33 a RF-36; CA-33 a CA-36; RN-16; RNF-02, RNF-13, RNF-14.

### T-20 — Seguridad de sesión y logging técnico

- **Objetivo:** cumplir RNF-03 y RNF-05 con configuración explícita y verificable.
- **Alcance:** `config/settings.py`, `.env.example`; `tests/test_accounts_security.py`.
- **Dependencias:** T-11, T-19.
- **Pasos:**
  1. Configurar cookies de sesión y CSRF (`HttpOnly`, `SameSite=Lax`, `Secure` por entorno).
  2. Configurar `SESSION_COOKIE_AGE` por entorno, con valor por defecto y sin hacerla obligatoria.
  3. Configurar `LOGGING` por consola, nivel por entorno, sin cuerpos de solicitud ni datos personales.
  4. Probar CSRF en POST, atributos de cookies, ausencia de secretos en logs y separación entre logging y auditoría.
  5. Documentar las variables nuevas en `.env.example` con valores por defecto.
- **Verificación:** CSRF activo; cookies con atributos; logs sin secretos; configuración no rompe las pruebas DB-free.
- **Evidencia:** pytest del archivo y revisión de configuración.
- **Trazabilidad:** RNF-03, RNF-05; CA-40.

### T-21 — Pruebas de aislamiento entre empresas

- **Objetivo:** demostrar que ninguna vista ni servicio alcanza datos de otra empresa.
- **Alcance:** `tests/test_accounts_isolation.py`; fixtures en `tests/conftest.py`.
- **Dependencias:** T-02 a T-20.
- **Pasos:**
  1. Crear la segunda empresa inactiva por ORM, con su cuenta y membresía.
  2. Cubrir cada vista y servicio con un caso de acceso cruzado.
  3. Verificar 404 uniforme, ausencia de cambios y evento de seguridad.
  4. Verificar que listas y agregados no incluyen datos ajenos.
  5. Ejecutar con la base autorizada (G-4).
- **Verificación:** todas las pruebas pasan; no se filtra ningún dato entre empresas.
- **Evidencia:** pytest y conteo de casos por vista y servicio.
- **Trazabilidad:** RF-08 a RF-13; CA-08 a CA-13, CA-38; RN-14; RNF-01.

### T-22 — Integración, regresión y calidad

- **Objetivo:** validar flujos completos, evitar regresiones y dejar la calidad en verde.
- **Alcance:** pruebas de integración; ejecución completa; correcciones acotadas de estilo.
- **Dependencias:** T-21.
- **Pasos:**
  1. Cubrir inicialización, acceso, alta, primer acceso, cambio de rol, desactivación, reactivación y recuperación.
  2. Verificar la auditoría de cada flujo.
  3. Ejecutar las 20 pruebas DB-free de 001, `test_admin_unfold.py` y `tests/test_db_guards.py`.
  4. Ejecutar la suite completa con la base autorizada.
  5. Validar 404 uniforme con `DEBUG=False`.
  6. Ejecutar `python -m ruff check .` y corregir solo hallazgos de la etapa.
- **Verificación:** suite en verde; Ruff sin errores; sin regresiones; guardas intactas; 404 uniforme verificado.
- **Evidencia:** salidas de pytest y Ruff.
- **Trazabilidad:** CA-01 a CA-41, CA-44; RN-14; RNF-03, RNF-09, RNF-11.

### T-23 — Validación funcional y visual

- **Objetivo:** verificar la interfaz propia en estados, acceso y responsive.
- **Alcance:** servidor local y navegador; capturas fuera del repositorio.
- **Dependencias:** T-22.
- **Pasos:**
  1. Servir la aplicación en `127.0.0.1:8000` con `DJANGO_DEBUG=True` (G-3).
  2. Recorrer los flujos y los cinco estados de interfaz.
  3. Verificar 320, 375, 768, 1440 y 1920 px sin desbordamiento.
  4. Verificar teclado, foco, etiquetas, errores asociados, contraste, objetivos táctiles ≥ 24×24 px, tablas con encabezados y `scope`, zoom 200 %, `lang="es"`, color no exclusivo, estados anunciados y `prefers-reduced-motion`.
  5. Verificar la pantalla 404 con `DEBUG=False` y que una cuenta comercial no accede a `/admin/`.
- **Verificación:** checklist cerrado y aprobación explícita del usuario.
- **Evidencia:** capturas enmascaradas y registro en `docs/README.md`.
- **Trazabilidad:** RNF-07, RNF-08, RNF-10; CA-42, CA-43.

### T-24 — Documentación de la etapa

- **Objetivo:** dejar la etapa reproducible y comprensible.
- **Alcance:** `README.md`, `docs/README.md`, `.env.example`, `tasks.md`.
- **Dependencias:** T-23.
- **Pasos:**
  1. Documentar estructura, roles, capacidades y comandos.
  2. Documentar variables de entorno, política de sesión y logging.
  3. Documentar la separación Admin/panel y la estrategia de pruebas.
  4. Registrar resultados, evidencias y limitaciones.
  5. Verificar enlaces y ausencia de secretos.
- **Verificación:** checklist de documentación completo; enlaces válidos; sin secretos.
- **Evidencia:** diff de documentación y verificación de enlaces.
- **Trazabilidad:** RNF-12; criterios de cierre.

### T-25 — Revisión final del Reviewer

- **Objetivo:** obtener el veredicto técnico final.
- **Alcance:** implementación, pruebas, Ruff, documentación, evidencias y trazabilidad Git.
- **Dependencias:** T-24 APROBADO y commiteado.
- **Pasos:**
  1. Entregar informe, evidencias y commits por tarea.
  2. Verificar trazabilidad RF/RNF → CA → tareas.
  3. Verificar commits y alcance por tarea.
  4. Corregir hallazgos bajo la tarea afectada y obtener nuevo APROBADO.
- **Verificación:** veredicto APROBADO y commits completos.
- **Evidencia:** informe del Reviewer y hashes.
- **Trazabilidad:** todos los requisitos.

### T-26 — Cierre documental y verificación Git

- **Objetivo:** cerrar la etapa y sincronizar el repositorio.
- **Alcance:** `MEMORY.md` (commit propio) y verificación de Git.
- **Dependencias:** T-25 APROBADO.
- **Pasos:**
  1. Actualizar `MEMORY.md` con el estado final (máximo 40 líneas).
  2. Verificar que refleja la etapa cerrada y las limitaciones.
  3. Implementer ejecuta `git add MEMORY.md` y el commit en inglés.
  4. Build verifica los commits de las tareas y ejecuta el push a `main`.
  5. Verificar `git status`, `git log` y `origin/main...HEAD`.
- **Verificación:** `MEMORY.md` actualizado; árbol limpio; rama sincronizada.
- **Evidencia:** hash del commit y estado de la rama.
- **Trazabilidad:** criterios de cierre.
- **Prohibido:** `amend`, `force push`, agrupar archivos de otras tareas.

---

## 6. Puntos de revisión del Reviewer

| Checkpoint | Momento | Tareas | Veredicto |
|---|---|---|---|
| RC-1 | Antes de implementar | `plan.md` y `tasks.md` | APROBADO / CAMBIOS NECESARIOS |
| RC-5 | Tras T-01–T-09 | T-01 a T-09 | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-6 | Tras T-10–T-19 | T-10 a T-19 | APROBADO / CAMBIOS NECESARIOS por tarea |
| RC-7 | Tras T-20–T-24 | T-20 a T-24 | APROBADO / CAMBIOS NECESARIOS por tarea |
| T-25 | Tras T-24 commiteado | Etapa completa | APROBADO / CAMBIOS NECESARIOS |

---

## 7. Matriz de trazabilidad por tarea

| Tarea | Requisitos | CA |
|---|---|---|
| T-01 | RNF-09, RNF-12 | — |
| T-02 | RF-14, RF-16, RF-20; RN-05, RN-06 | CA-14, CA-16, CA-20 |
| T-03 | RF-08, RF-21 a RF-28, RF-30, RF-32; RN-01, RN-02, RN-03, RN-04; RNF-01 | CA-08, CA-21, CA-24 a CA-28, CA-30, CA-32 |
| T-04 | RF-37, RF-38, RF-40; RN-14; RNF-04 | CA-37, CA-38, CA-40 |
| T-05 | RF-38, RF-40; RN-14; RNF-04, RNF-05 | CA-38, CA-40 |
| T-06 | RF-21, RF-24 a RF-28, RF-30; RN-14; RNF-14 | CA-21, CA-24 a CA-28, CA-30, CA-37 |
| T-07 | RF-28, RF-32; RN-02, RN-04, RN-11; RNF-01 | CA-28, CA-32 |
| T-08 | RF-08 a RF-10; RN-07, RN-10, RN-17; RNF-06 | CA-08, CA-09, CA-10 |
| T-09 | RF-11 a RF-19, RF-29; RN-08, RN-09, RN-15; RNF-02 | CA-11 a CA-19, CA-29, CA-38 |
| T-10 | RF-01, RF-02; RN-13, RN-16; RNF-03 | CA-01, CA-02, CA-38 |
| T-11 | RF-03, RF-04; RNF-03 | CA-03, CA-04 |
| T-12 | RF-05, RF-06, RF-07; RN-12; RNF-03 | CA-05, CA-06, CA-07 |
| T-13 | RF-30, RF-41; RN-14 | CA-30, CA-41 |
| T-14 | RF-23; RN-07; RNF-01 | CA-23 |
| T-15 | RF-21, RF-22; RN-13 | CA-21, CA-22, CA-37 |
| T-16 | RF-24 a RF-28; RN-04, RN-11; RNF-03 | CA-24 a CA-28, CA-37 |
| T-17 | RF-31; RN-14; RNF-14 | CA-31, CA-37 |
| T-18 | RF-37 a RF-40; RN-14 | CA-37 a CA-40 |
| T-19 | RF-33 a RF-36; RN-16; RNF-02, RNF-13, RNF-14 | CA-33 a CA-36 |
| T-20 | RNF-03, RNF-05 | CA-40 |
| T-21 | RF-08 a RF-13; RN-14, RN-17; RNF-01 | CA-08 a CA-13, CA-38 |
| T-22 | Todos; RN-14; RNF-03, RNF-09, RNF-11 | CA-01 a CA-41, CA-44 |
| T-23 | RNF-07, RNF-08, RNF-10 | CA-42, CA-43 |
| T-24 | RNF-12 | — |
| T-25 | Todos | Todos |
| T-26 | Criterios de cierre | — |

---

## 8. Orden de ejecución

T-01 → T-02 → T-03 → T-04 → T-05 → T-06 → T-07 → T-08 → T-09 → T-10 → T-11 → T-12 → T-13 → T-14 → T-15 → T-16 → T-17 → T-18 → T-19 → T-20 → T-21 → T-22 → T-23 → T-24 → T-25 → T-26.

Cada tarea se revisa y se commitea al terminar, antes de que la siguiente modifique los mismos archivos. Los checkpoints cierran cuando todas sus tareas están aprobadas.

---

## 9. Autorizaciones requeridas

| Gate | Alcance | Estado |
|---|---|---|
| G-0 | Aprobación de `plan.md` y `tasks.md` | APROBADO por el usuario el 2026-11-10 |
| G-1 | Autorización de implementación | T-01 publicada; T-02 a T-19 autorizadas el 2026-11-10 |
| G-2 | Generación y aplicación de migraciones | Autorizado el 2026-11-10 para `accounts` y `audit` en `nexopyme_bootstrap_dev` |
| G-3 | Comandos y servidor sobre desarrollo | Autorizado el 2026-11-10 dentro del alcance de T-02 a T-19 |
| G-4 | Pruebas con `nexopyme_bootstrap_test` (`DA-07`) | Autorizado para esta etapa; se confirma por ejecución |
| G-5 | Commit y push por tarea | Operativo; T-01 a T-15 publicadas |

---

## 10. Estado de las tareas

- `[x]` T-01: verificaciones de partida aprobadas por el Reviewer (2026-11-10) y commiteadas.
- `[x]` T-02: catálogo de roles y capacidades aprobado por el Reviewer (2026-11-10) y commiteado.
- `[x]` T-03: modelos y migración aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-04: auditoría y eventos aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-05: servicios de auditoría aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-06: servicios de empresa y membresía aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-07: invariantes y concurrencia aprobadas por el Reviewer (2026-11-10) y commiteadas.
- `[x]` T-08: middleware de contexto aprobado por el Reviewer (2026-11-10) y commiteado.
- `[x]` T-09: autorización y handlers aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-10: backends de autenticación aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-11: acceso, cierre de sesión y rutas protegidas aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-12: cambio obligatorio, autogestión de contraseña y perfil aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-13: comandos de inicialización y recuperación aprobados por el Reviewer (2026-11-10) y commiteados.
- `[x]` T-14: listado de usuarios aprobado por el Reviewer (2026-11-10) y commiteado.
- `[x]` T-15: alta de empleado con contraseña temporal aprobada por el Reviewer (2026-11-10) y commiteada.
- `[ ]` T-16 a T-26: no iniciadas.
- **RC-5 APROBADO (2026-11-10):** 29 pruebas DB-free + 61 con base autorizada, Ruff y `manage.py check` en verde. Limitaciones asignadas: evidencia de suite y `DEBUG=False` → T-22/T-26; `company_id` inyectado → T-11/T-21; segunda empresa de prueba inactiva → T-21; evento de seguridad en rechazos de servicio → T-14 a T-18; reactivación de dueño → T-16; registros documentales → T-24.
- O-2 aplicada en T-02 y T-04; O-1, O-3 y O-4 pendientes de confirmación del usuario.
- A-09, A-10 y A-13 aprobadas el 2026-11-10; no requieren nueva confirmación.
- G-0 aprobado y G-1 autorizado para T-02 a T-19; G-2 y G-3 autorizados para las migraciones de `accounts` y `audit`; G-4 autorizado para las pruebas de la etapa.
- `specs/003-cuentas-multiempresa/` versionado: `spec.md` y `plan.md` en `d907766`; `tasks.md` versionado desde `4344c31` y actualizado en cada commit de tarea.

---

**Fin de las tareas v1.3.** La especificación 003 v1.0 y la planificación v1.3 están aprobadas (G-0). La implementación avanza por tarea con autorización explícita.
