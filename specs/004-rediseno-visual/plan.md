# Plan técnico 004 — Rediseño visual — **v0.1 (aprobado)**

## 1. Identificación y estado

| Campo | Valor |
|---|---|
| Funcionalidad | 004 — Rediseño visual |
| Artefacto | `specs/004-rediseno-visual/plan.md` |
| Versión | 0.1 (aprobada) |
| Estado | **APROBADO — G-0b por el usuario el 2026-11-12**; G-1 aprobado para T-04 y el bloque T-05/T-06 |
| Especificación de referencia | `specs/004-rediseno-visual/spec.md` v0.1 (aprobada) |
| Tareas | `specs/004-rediseno-visual/tasks.md` v0.1 (aprobadas) |
| Fecha | 2026-11-12 |
| Responsable | Planner |
| Fase SDD | 5 a 7: plan técnico y descomposición en tareas |
| Base de partida | Etapa 003 cerrada y publicada en `6893e59`; 337 pruebas en verde |

**Historial:** v0.1: plan inicial derivado de la propuesta «Mostrador» aprobada el 2026-11-12, con las correcciones del dictamen del Reviewer (A-1 a A-6, B-1 a B-6, C-1 a C-8).

---

## 2. Objetivo del plan

Definir cómo se implementará el sistema visual de la especificación 004 sin alterar el comportamiento de negocio de la Etapa 003: una reescritura de `static/css/main.css` por secciones y en tres hitos, la migración de quince plantillas a un vocabulario de componentes y la validación funcional y visual de las superficies P0, conservando el copy y las pruebas existentes.

---

## 3. Estado de partida

| Elemento | Estado real verificado |
|---|---|
| Repositorio | Etapa 003 cerrada y publicada en `6893e59`; árbol limpio salvo no rastreados preexistentes |
| Pruebas | 337: 36 DB-free + 301 con base autorizada (`nexopyme_bootstrap_test`) |
| CSS | `static/css/main.css` con 732 líneas y paleta anterior (papel, tinta, petróleo) |
| Plantillas | 17 archivos en `templates/`; 15 en el alcance P0 |
| Shell | `base.html` público y `base_panel.html` independiente; `panel.html` extiende `base_panel.html` |
| Acceso | `login.html` con script inline que usa `.login form` y `aria-busy` |
| Contraseña temporal | Primer `<code>` del documento en `user_form.html` y `user_confirm.html` |
| Admin | Unfold sin `main.css`; `User` y `Group` en solo lectura |
| Dependencias | Ninguna nueva prevista |
| Migraciones | Ninguna; G-2 no aplica |
| Autorización | G-0a y G-0b aprobados; G-1 aprobado para T-04 y el bloque T-05/T-06 |

### 3.1 Restricciones de pruebas en el estado de partida

| Prueba | Acoplamiento | Tratamiento en este plan |
|---|---|---|
| `test_accounts_auth.py::test_login_template_implements_error_and_loading_states` | Lee `login.html` y exige `role="alert"` y `aria-busy` | Conservar el script inline y el atributo en P0 |
| `login.html` (script) | Depende de `.login form` | Conservar el contenedor `.login` y el `<form>` descendiente |
| `test_accounts_auth.py::test_panel_template_extends_independent_base_panel` | `base_panel.html` no extiende `base.html`; `panel.html` extiende `base_panel.html` | No crear shell compartido; mantener la jerarquía actual |
| `test_accounts_users.py` (alta y regeneración) | `re.search(r"<code>([^<]+)</code>")` y `count == 1` | El recibo envuelve el mismo `<code>`; sin duplicados |
| `test_accounts_users.py` (listado) | Exige `05/03/2026 12:00`, `Activa`, `Inactiva`, `Nunca` | Conservar `d/m/Y H:i` y los textos |
| `test_accounts_users.py` (paginación) | Exige 20 y 2 `scope="row"`, `Página X de Y`, `aria-label` | Mantener `th scope="row"` por fila y la paginación |
| `test_accounts_audit.py` | Exige «No hay operaciones auditadas.», «No hay eventos de seguridad.», «Personal técnico» y los parámetros de página | Conservar textos y enlaces de paginación |
| `test_accounts_company.py` | Exige «Nombre de la empresa actualizado.» | Conservar el mensaje |
| `test_accounts_navigation.py` | Exige «Etapa 003 — Cuentas y multiempresa» en login, panel, home, 403 y 404; un solo `<footer>`; ausencia de «Administración» y `/admin/` en errores | Conservar la etiqueta del pie y el bloque de cabecera de errores; sus pruebas requieren base (G-4) |
| `test_accounts_auth.py::test_base_template_stays_free_of_panel_context` | Prohíbe `request.*` en `base.html` | No introducir contexto de sesión en `base.html` |
| `test_home_view.py` | Prohíbe `request.user`, `perms` y `messages` en base, home, navbar y footer; exige `href="/admin/"` y «Pendiente de especificación» | No tocar la home en P0; conservar enlaces y textos |
| `test_project_structure.py` | Escanea cinco archivos: `base.html`, `home.html`, `navbar.html`, `footer.html`, `main.css` | La política cubre las plantillas nuevas aunque la prueba no las escanee; en P0 no se crean parciales |
| Pruebas de un `h1` | Login, panel, usuarios, empresa y auditoría | Un solo `h1` por página |

---

## 4. Arquitectura del cambio

### 4.1 Estrategia

1. **Reescritura por secciones en tres hitos sobre `static/css/main.css`.** T-04 define tokens y base con alias de compatibilidad; T-06 migra componentes y retira los tokens de color antiguos de las reglas P0; T-09 retira `.panel*` y los selectores de compatibilidad restantes, salvo el bloque de la home. Así ninguna regla antigua queda apuntando a tokens con semántica nueva.
2. **Sin shell nuevo.** Se conservan `base.html` y `base_panel.html` como estructuras independientes; el rediseño cambia clases y marcado, no la jerarquía de herencia.
3. **P0 sin JavaScript nuevo.** Se conservan los scripts inline existentes de `login.html`, `user_form.html`, `company_form.html` y `password_change.html`; no se crea `static/js/ui.js`.
4. **P1 futuro.** `static/js/ui.js` (~30–35 líneas) queda documentado para menú móvil y `<details>`, sin implementarse.
5. **Backend intacto.** No se tocan `apps/**`, `config/**`, migraciones, Admin/Unfold ni `specs/003-cuentas-multiempresa/**`.

### 4.2 Secciones de `main.css`

| # | Sección | Contenido |
|---|---|---|
| 1 | Tokens | Color, tipografía, espaciado, layout, radios, bordes, foco, movimiento |
| 2 | Reset y base | Box-sizing, `html`, `body`, títulos, párrafos, enlaces, medios, controles, `::selection` |
| 3 | Layout | `.site`, `.container`, `.site-main`, utilidades de pila y grilla |
| 4 | Salto de contenido | `.skip-link` con foco visible |
| 5 | Barra superior | `.app-header`, marca, contexto, navegación, enlace actual, truncado y estilo mínimo de `.site-header` para errores |
| 6 | Botones | Primario, secundario, ghost, peligro, peligro silencioso, tamaño, block, disabled |
| 7 | Campos | `.form-field`, label, control, ayuda, errores, acciones, `aria-invalid` |
| 8 | Avisos y badges | `.alert` por estado, `.badge` por rol y estado |
| 9 | Hojas y contexto | `.sheet`, `.sheet--accent`, `.context-strip` |
| 10 | Tablas y paginación | `.table-scroll`, `.table`, `.table--audit`, `.pagination` |
| 11 | Estados y recibo | `.empty-state`, `[aria-busy="true"]`, `.receipt`, `.error-page` |
| 12 | Responsive | Cortes en 48rem, 64rem, 90rem y 120rem con contenedor 72/80rem |
| 13 | Preferencias | `prefers-reduced-motion` y `forced-colors` |
| 14 | Compatibilidad home (P2) | Reglas acotadas de `.home-hero*`, `.home-panels`, `.next-steps*`, los `.panel*` usados por la home y sus reglas responsive; `.panel__stage` en `accent-ink`. No se rediseña la home |
| 15 | Pie | `.site-footer`, identidad, etapa y año; estructura de T-05 |

**Sin** `@import` remoto, fuentes externas, frameworks, gradientes, sombras en hojas ni la palabra «unfold».

---

## 5. Mapa de archivos

| Ruta | Cambio | Conservar |
|---|---|---|
| `static/css/main.css` | Reescritura completa por secciones | Sin recursos remotos |
| `templates/base.html` | Clase de página, `meta theme-color` opcional, skip link, `main` | Sin `request.*`, `perms` ni `messages`; bloque `site_header`; un solo `main#contenido` |
| `templates/base_panel.html` | `.app-header`, contexto, navegación con `aria-current`, pie | No extender `base.html`; `{% include "components/footer.html" %}`; skip link; bloque `scripts` |
| `templates/components/navbar.html` | Marca, «Acceso al panel», «Acceso técnico» discreto | `href="/admin/"` |
| `templates/components/footer.html` | Estructura y estilos del pie | «Etapa 003 — Cuentas y multiempresa» y el año |
| `templates/accounts/login.html` | Login de una columna P0 | `role="alert"`, `aria-busy`, `data-loading-label`, `name="username"`, `name="password"`, CSRF, `.login form` y script inline |
| `templates/accounts/panel.html` | `h1`, contexto `dl`, acción y lista de trabajo | Sin consultas nuevas; `request.company`, `request.account`, `request.membership` |
| `templates/accounts/user_list.html` | Tabla de 5 columnas, badges, acciones agrupadas | `caption`, `scope`, `.table-scroll`, textos, formularios POST, `th scope="row"` |
| `templates/accounts/user_form.html` | Hoja, ayuda, «Cancelar», recibo | Bucle de campos, `aria-invalid`/`aria-describedby`, `role="status"`, primer `<code>`, `aria-busy` |
| `templates/accounts/user_confirm.html` | Aviso y recibo | `title`, `message`, `temporary_password`, `role`, primer `<code>` |
| `templates/accounts/company_form.html` | Hoja, ayuda, aviso, «Cancelar» | `messages`, errores, CSRF y el mensaje de éxito |
| `templates/accounts/audit_list.html` | Cabecera, tablas, chips, estados vacíos | `caption`, `scope`, `audit_page`, `security_page`, `audit_rows`, `security_rows`, textos vacíos |
| `templates/accounts/profile.html` | Identidad, badge, hoja, acciones | `profile_account`, `profile_membership`, `messages`, «Contraseña actualizada.» |
| `templates/accounts/password_change.html` | Hoja, aviso temporal, ayuda, acciones | Bucle de campos, `field.help_text`, errores, CSRF, `aria-busy` |
| `templates/errors/403.html` | `.error-page`, código, explicación, acciones | `reason == "context"`, cierre de sesión, CSRF, «Volver al panel» |
| `templates/errors/404.html` | `.error-page`, código, explicación, acción | `h1`, «Recurso no encontrado», «Volver al panel», «Iniciar sesión» |
| `templates/home.html` | **Fuera de alcance (P2)** | `href="/admin/"`, «Pendiente de especificación», etiqueta de etapa |
| `templates/components/error_header.html` | Sin cambios en P0; conserva `.site-header` y `.brand` | Marca y ausencia de «Administración»; el CSS mantiene un estilo mínimo de `.site-header` para las páginas de error |

**Total P0:** `main.css` y 15 plantillas. Doce plantillas concentran el shell y el contenido principal; `password_change.html`, `403.html` y `404.html` completan las superficies P0. La home queda para P2.

**No tocar:** `apps/**`, `config/**`, `tests/**`, migraciones, Admin/Unfold, `CONSTITUTION.md`, `AGENTS.md` y `specs/003-cuentas-multiempresa/**`.

---

## 6. Decisiones técnicas

| ID | Decisión | Motivo | Alternativa descartada |
|---|---|---|---|
| P-01 | Migrar tokens por hitos: T-04 con alias, T-06 cambia `--color-accent` a ámbar y retira tokens de color, T-09 retira `.panel*` | Evita reglas antiguas usando ámbar como texto y pantallas sin superficie | Cambiar toda la semántica en T-04 sin compatibilidad |
| P-02 | Mantener los selectores desnudos y el `[role="status"]` global como compatibilidad hasta T-09; retirarlos al migrar la última plantilla P0 | Evita romper tablas y avisos de pantallas aún no migradas | Retirarlos en T-06 |
| P-03 | Foco doble con 2 px `surface` + 3 px `focus` | El azul sobre verde solo alcanza 1,56:1 | Outline simple |
| P-04 | Truncar el nombre de empresa con `max-width` + `text-overflow: ellipsis` | Admite nombres de 150 caracteres sin desbordar | Alturas fijas |
| P-05 | Tabla con scroll interno y contenedor enfocable | Conserva la asociación de encabezados y evita scroll de página | Ocultar columnas |
| P-06 | Contexto como `dl`, sin `.stat-grid` | Empresa, rol y sesión no son cifras | Tarjetas de KPI |
| P-07 | `aria-current="page"` en el enlace activo | Ubicación explícita y accesible | Solo color |
| P-08 | Conservar `href="/admin/"` con «Acceso técnico» discreto | Mantiene la prueba de la home y separa negocios de técnica | Retirar el enlace |
| P-09 | Errores con el shell actual en P0 | No rompe `base_panel` ni duplica shell | `base_minimal` nuevo |
| P-10 | Reemplazar `.panel*` por `.sheet`/`.sheet__title` en las 9 plantillas P0 que las usan (8 de contenido más `base_panel.html`), migrar `.panel-context*` de la barra a `.app-header__context` y actualizar los scripts `.panel form` a `.sheet form` | Un solo vocabulario visual y `aria-busy` operativo | Conservar dos sistemas |
| P-11 | Mantener `.panel*`, los selectores desnudos y los tokens heredados no reemplazados hasta que cada consumidor migre: color P0 en T-06, `.panel*`/selectores en T-09, home hasta P2 | Las plantillas y la home siguen funcionando durante la transición | Retirarlos antes de migrar sus consumidores |

**Migración de clases.** `.panel`, `.panel--stage`, `.panel__title`, `.panel__text`, `.panel__subtitle`, `.panel__stage` y `.panel-context*` se reemplazan por `.sheet`, `.sheet__header`, `.sheet__title`, `.sheet__body`, `.app-header__context` y utilidades. La migración se reparte: `base_panel.html` en T-05; `panel.html` en T-07; usuarios, empresa y auditoría en T-08; perfil, contraseña y errores en T-09. La home conserva sus clases hasta P2. Los scripts inline de alta, empresa y contraseña pasan de `.panel form` a `.sheet form` en la misma tarea que migra su plantilla. La búsqueda de tokens retirados (`--color-paper`, `--color-accent-deep`, `--rule-hairline`) debe devolver cero usos en reglas P0 al cerrar T-06; el bloque de compatibilidad de la home puede conservarlos hasta P2. `.panel*` debe devolver cero usos en plantillas P0 al cerrar T-09, salvo el bloque acotado de la home. Los selectores desnudos y `[role="status"]` se retiran en T-09, cuando ya no quedan consumidores P0.

---

## 7. Restricciones de pruebas y mitigaciones

| ID | Hallazgo del Reviewer | Mitigación en este plan |
|---|---|---|
| A-3 | Copy nuevo rompe pruebas: estados vacíos de auditoría, formato de fecha y mensaje de empresa | Conservar los textos de §3.1 y el formato `d/m/Y H:i`; no hay cambios de copy en P0 |
| A-4 | `aria-busy` literal y selector `.login form` | Mantener el script inline y la clase `.login` en P0 |
| A-5 | Primer `<code>` es la contraseña temporal y se verifica una sola vez | El recibo envuelve el `<code>` existente; prohibido duplicarlo |
| A-6 | `base_panel.html` no puede extender `base.html` | Sin shell compartido; `panel.html` sigue extendiendo `base_panel.html` |
| C-5 | `test_project_structure` solo escanea cinco archivos | No se crean parciales en P0; si se crearan, la política las cubriría y se revisaría la prueba con aprobación |
| — | El pie debe contener «Etapa 003 — Cuentas y multiempresa» en login, panel, home, 403 y 404 | Conservar la etiqueta; el copy de producto queda para P2 con prueba actualizada |
| — | `scope="row"` se cuenta por página (20 y 2) | Una fila de encabezado por membresía; sin filas adicionales que lo dupliquen |
| — | Un solo `h1` por página | El código de error y los títulos de sección usan `p`/`h2` |

---

## 8. Accesibilidad y responsive

| Ancho | Barra superior | Contenido | Tablas | Formularios |
|---|---|---|---|---|
| 320 px | Dos filas: marca y contexto; menú P1 | Una columna; H1 28 px | 5–6 columnas con scroll interno | Ancho completo; botones block |
| 375 px | Igual, con más aire | Una columna | Igual | Igual |
| 768 px | Dos filas | Contexto en 2 columnas | Scroll si hace falta | Máximo 36rem |
| 1024 px | Una franja; navegación visible | 72rem | Tabla completa | 36rem |
| 1440 px | Una franja; 64 px | 72rem centrado | Tabla completa | 36rem |
| 1920 px | Igual | 80rem máximo; no se estira el texto | Tabla completa | Igual |

**Regla transversal:** sin scroll horizontal de página en 320, 375, 768, 1440 y 1920 px. El único scroll horizontal permitido es el interno de `.table-scroll`, con contenedor enfocable y `aria-label`.

**Verificaciones obligatorias**

- Contraste ≥ 4,5:1 en texto y ≥ 3:1 en componentes y foco.
- Orden de tabulación: skip link → marca → contexto → navegación → contenido.
- Objetivos táctiles ≥ 44 px en acciones principales y ≥ 40 px en filas.
- Zoom 200 % sin superposición ni scroll horizontal de página.
- `prefers-reduced-motion` sin transiciones no esenciales; `forced-colors` con bordes visibles.
- `lang="es"`, un `h1`, `caption` y `scope` en tablas, `aria-invalid`/`aria-describedby` en errores.
- Estados vacío, carga, error, éxito y confirmación anunciados y visibles.
- `hidden` no se usa en HTML inicial; el menú móvil es P1.
- Admin sin `main.css`; cuenta comercial fuera de `/admin/`.

---

## 9. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Reglas antiguas con tokens retirados | Colores y contrastes degradados en silencio | Migrar por hitos con alias y buscar tokens retirados en reglas P0 antes de cerrar T-06 |
| Colisión de `[role="status"]` | Recibo y avisos con borde y fondo incorrectos | Eliminar el selector global; estilar por clase |
| Pérdida de copy verificado | Suite en rojo | Lista de §3.1 y revisión de copy en cada tarea |
| Duplicación del secreto | Falla la extracción del primer `<code>` | Un solo `<code>` dentro del recibo |
| Shell compartido | Rompe `base_panel` | Sin `base_shell` ni `base_minimal` en P0 |
| Tabla con columnas ocultas | Rompe la asociación de encabezados | Scroll interno; sin `display:none` |
| Nombre de empresa largo | Desbordes en barra y títulos | Truncado y prueba con 150 caracteres |
| Zoom 200 % | Solapamientos y scroll de página | `rem`, `min-height`, wrap; sin sticky |
| Foco sobre verde | 1,56:1 | Anillo doble |
| Admin afectado | Regresión visual técnica | `main.css` no se carga en Admin; no tocar Unfold |
| Dependencia de fuentes | Caída distinta en Linux | Fallbacks del sistema y limitación declarada |
| Evidencia de T-23 obsoleta | Validación visual no comparable | Re-medir y re-capturar en T-10 |
| CSS global afecta la home P2 | Pérdida de estilos o ámbar como texto | Bloque de compatibilidad explícito, `.panel__stage` en `accent-ink` y verificación de no regresión en T-10 |

---

## 10. Puntos de autorización y control

| Gate | Cuándo | Quién | Alcance |
|---|---|---|---|
| G-0a | Tras T-02 | Usuario | Aprobación de `spec.md` |
| G-0b | Tras T-03 | Usuario | Aprobación de `plan.md` y `tasks.md` |
| G-1 | Antes de T-04 | Usuario | Autorización de implementación de T-04 a T-11; aprobada para T-04 y el bloque T-05/T-06 |
| G-2 | No aplica | — | Sin migraciones ni cambios de esquema |
| G-3 | Antes de la primera captura o servidor local | Usuario | Servidor y datos ficticios solo en `nexopyme_bootstrap_dev` |
| G-4 | Antes de la primera prueba con base | Usuario | `nexopyme_bootstrap_test` autorizada para la etapa |
| G-5 | Por tarea con archivos | Implementer y Build | Flujo operativo de `git add`, commit y push; no requiere autorización adicional |

Sin G-1 no se ejecuta ninguna tarea de T-04 a T-11. G-0a y G-0b quedaron aprobados por el usuario el 2026-11-12; G-1 fue aprobado para T-04. G-3 y G-4 se confirman por ejecución antes de la primera captura y la primera prueba con base. El silencio no es aprobación.

**Registro de aprobación (2026-11-12):** G-0a APROBADO para `spec.md`; G-0b APROBADO para `plan.md` y `tasks.md`; G-1 APROBADO para T-04 y el bloque T-05/T-06. T-07 a T-11 permanecen no autorizadas.

### 10.1 Flujo obligatorio de revisión y Git por tarea

Cada tarea de implementación (T-04 a T-11) sigue este orden, sin excepciones:

1. Implementer ejecuta una única tarea.
2. Ejecuta las pruebas pertinentes y Ruff.
3. Reviewer revisa la tarea y emite `APROBADO` o `CAMBIOS NECESARIOS`.
4. Build revisa el resultado.
5. Solo después de obtener `APROBADO`, Implementer realiza el commit de esa tarea.
6. Build verifica el commit, el contenido y el push.
7. Solo entonces se permite avanzar a la siguiente tarea.

RC-8, RC-9 y RC-10 son checkpoints adicionales y no sustituyen la revisión individual. Si Reviewer emite `CAMBIOS NECESARIOS`, se corrige y se solicita una nueva revisión; una aprobación anterior no se reutiliza para correcciones posteriores. No se usa `git commit --amend`, force push ni se agrupan archivos de otras tareas. Ante conflictos, fallos inesperados o cambios fuera de alcance, se detiene y se consulta.

---

## 11. Verificación

```text
# Calidad estática
python -m ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run

# Suite objetivo por tarea
python -m pytest tests/test_home_view.py tests/test_project_structure.py \
  tests/test_accounts_auth.py tests/test_accounts_navigation.py \
  tests/test_accounts_users.py tests/test_accounts_company.py \
  tests/test_accounts_audit.py tests/test_accounts_integration.py -q

# Suite DB-free
python -m pytest tests/test_project_structure.py tests/test_settings_foundation.py \
  tests/test_home_view.py tests/test_urls.py tests/test_admin_unfold.py \
  tests/test_accounts_capabilities.py tests/test_accounts_forms.py -q

# Suite con base autorizada (G-4)
python -m pytest tests/test_accounts_auth.py tests/test_accounts_authorization.py \
  tests/test_accounts_middleware.py tests/test_accounts_users.py \
  tests/test_accounts_company.py tests/test_accounts_audit.py \
  tests/test_accounts_navigation.py tests/test_accounts_isolation.py \
  tests/test_accounts_commands.py tests/test_accounts_admin_separation.py \
  tests/test_accounts_security.py tests/test_accounts_integration.py \
  tests/test_db_guards.py -q
```

**Validación visual.** Navegador local con CDP o herramienta equivalente: capturas en 320, 375, 768, 1440 y 1920 px; zoom 200 %; recorrido de teclado; foco visible; contraste medido; estados vacío, carga, error, éxito y confirmación; `prefers-reduced-motion`; tablas con scroll interno; nombre de empresa de 150 caracteres; verificación de no regresión de la home (P2); verificación de que Admin no carga `main.css`.

**Registro de evidencia.** Cada tarea guarda comandos, resultados y rutas de capturas en `tasks.md`, sin secretos ni datos personales. No se afirma una prueba no ejecutada.

---

## 12. Orden, checkpoints y criterios de cierre

- Orden: T-01 → T-02 → T-03 → T-04 → T-05 → T-06 → T-07 → T-08 → T-09 → T-10 → T-11.
- Checkpoints: **RC-8** tras T-06 (sistema visual y fundación), **RC-9** tras T-09 (pantallas rediseñadas), **RC-10** tras T-11 (validación y cierre).
- Veredicto de cada checkpoint: APROBADO o CAMBIOS NECESARIOS.

**T-10 — delimitación.** T-10 es principalmente una tarea de validación responsive, accesibilidad y pruebas visuales. Solo se permiten correcciones puntuales de CSS o plantillas P0 necesarias para cumplir los criterios aprobados, correcciones justificadas por defectos detectados en las verificaciones y pruebas o evidencias que demuestren que la corrección resuelve el problema. No se permite rediseñar pantallas, cambiar decisiones visuales aprobadas, ampliar P0/P1/P2, cambiar copy o comportamiento ni modificar backend, modelos, migraciones o pruebas sin autorización expresa. Cada corrección se documenta, se prueba y pasa por revisión individual; si supera el alcance, se detiene y se consulta.

**Criterios de cierre**

1. T-04 a T-09 implementadas sin cambios de backend, copy verificado ni pruebas.
2. R-01 a R-04 y R-07 a R-12 verificados; R-05 y R-06 declarados P1.
3. Los 14 RF y los 10 RNF cubiertos con evidencia.
4. `ruff check .`, `manage.py check` y `makemigrations --check --dry-run` sin errores.
5. Suite completa en verde en dos invocaciones (DB-free y con base autorizada).
6. Validación visual registrada en los cinco anchos y con zoom 200 %.
7. Reviewer con APROBADO individual en cada tarea y en RC-8, RC-9 y RC-10; los checkpoints no sustituyen la revisión por tarea.
8. Commits por tarea publicados, documentación actualizada y `MEMORY.md` revisado al cierre con aprobación.

---

## 13. Fuera de alcance

P1 (menú móvil con JS, `<details>` por fila, login de dos columnas) y P2 (home pública, parciales, favicon, iconografía, copy de producto); backend, migraciones, Admin/Unfold, modo oscuro, header sticky, ocultamiento de columnas, toasts, modales, pestañas, frameworks, fuentes externas y cambios en la Etapa 003.
