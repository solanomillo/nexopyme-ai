# Tareas 003 — Cuentas y multiempresa

## 1. Identificación

| Campo | Valor |
|---|---|
| Funcionalidad | 003 — Cuentas y multiempresa |
| Artefacto | `specs/003-cuentas-multiempresa/tasks.md` |
| Versión | 1.2 |
| Estado | G-0 APROBADO (2026-11-10) — implementación en curso; T-01 publicada; T-02 en curso |
| Especificación | `spec.md` v1.0 aprobada el 2026-11-10 |
| Plan | `plan.md` v1.2 aprobado el 2026-11-10 |
| Fecha | 2026-11-10 |
| Responsable | Planner |
| Tareas | 26 (T-01 a T-26) |

**Historial:** v1.0 inicial; v1.1 correcciones del primer dictamen; v1.2 correcciones del segundo dictamen y renumeración secuencial (capacidades → modelos → auditoría → servicios).

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
| T-03 | Modelos `Account`, `Company` y `Membership` | F1 | T-02 | G-1, G-2, G-3, G-4 | `[ ]` |
| T-04 | Auditoría: modelos y migración | F1 | T-03 | G-1, G-2, G-3, G-4 | `[ ]` |
| T-05 | Servicios de auditoría y eventos de seguridad | F1 | T-04 | G-1, G-4 | `[ ]` |
| T-06 | Servicios de empresa y membresía | F2 | T-03, T-05 | G-1, G-4 | `[ ]` |
| T-07 | Invariantes y concurrencia | F2 | T-06 | G-1, G-4 | `[ ]` |
| T-08 | Middleware de contexto y punto de bloqueo | F3 | T-03, T-07 | G-1, G-4 | `[ ]` |
| T-09 | Autorización en vistas y servicios | F3 | T-02, T-08 | G-1, G-4 | `[ ]` |
| T-10 | Backends de autenticación | F4 | T-03, T-09 | G-1, G-4 | `[ ]` |
| T-11 | Acceso, cierre de sesión y rutas protegidas | F4 | T-10 | G-1, G-4 | `[ ]` |
| T-12 | Cambio obligatorio y autogestión de contraseña | F4 | T-11 | G-1, G-4 | `[ ]` |
| T-13 | Comandos de inicialización y recuperación | F5 | T-07, T-12 | G-1, G-3, G-4 | `[ ]` |
| T-14 | Listado de usuarios del panel | F5 | T-09, T-12 | G-1, G-4 | `[ ]` |
| T-15 | Alta de empleado con contraseña temporal | F5 | T-14 | G-1, G-4 | `[ ]` |
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
- **Evidencia:** pytest y validación visual del formulario.
- **Trazabilidad:** RF-03, RF-04; CA-03, CA-04; RNF-03.

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
| G-1 | Autorización de implementación | Autorizado para T-01 y T-02 el 2026-11-10; el resto requiere autorización del usuario |
| G-2 | Generación y aplicación de migraciones | Pendiente |
| G-3 | Comandos y servidor sobre desarrollo | Pendiente |
| G-4 | Pruebas con `nexopyme_bootstrap_test` (`DA-07`) | Autorizado para esta etapa; se confirma por ejecución |
| G-5 | Commit y push por tarea | Operativo; T-01 publicado |

---

## 10. Estado de las tareas

- `[x]` T-01: verificaciones de partida aprobadas por el Reviewer (2026-11-10) y commiteadas.
- `[x]` T-02: catálogo de roles y capacidades aprobado por el Reviewer (2026-11-10) y commiteado.
- `[ ]` T-03 a T-26: no iniciadas.
- O-2 aplicada en T-02; O-1, O-3 y O-4 pendientes de confirmación del usuario.
- A-09, A-10 y A-13 aprobadas el 2026-11-10; no requieren nueva confirmación.
- G-0 aprobado y G-1 autorizado para T-01 y T-02; sin migraciones, comandos ni commits de implementación fuera de las tareas autorizadas.
- `specs/003-cuentas-multiempresa/` versionado: `spec.md` y `plan.md` en `d907766`; `tasks.md` en `4344c31`.

---

**Fin de las tareas v1.2.** La especificación 003 v1.0 y la planificación v1.2 están aprobadas (G-0). La implementación avanza por tarea con autorización explícita.
