# Tareas 004 — Rediseño visual — **v0.1 (aprobadas)**

## 1. Identificación

| Campo | Valor |
|---|---|
| Funcionalidad | 004 — Rediseño visual |
| Artefacto | `specs/004-rediseno-visual/tasks.md` |
| Versión | 0.1 (aprobada) |
| Estado | **APROBADO — G-0a y G-0b; G-1 aprobado para T-04 a T-09; T-04 a T-08 publicadas; RC-8 APROBADO; T-09 no iniciada; T-10/T-11 no autorizadas** |
| Especificación | `specs/004-rediseno-visual/spec.md` v0.1 (aprobada) |
| Plan | `specs/004-rediseno-visual/plan.md` v0.1 (aprobado) |
| Fecha | 2026-11-12 |
| Responsable | Planner |
| Tareas | 11 (T-01 a T-11) |

**Historial:** v0.1: descomposición inicial en once tareas documentales y de implementación, con checkpoints RC-8 a RC-10 y gates G-0a, G-0b, G-1, G-3, G-4 y G-5.

---

## 2. Convenciones

- `[ ]` no iniciada; `[~]` implementada y pendiente de aprobación o commit; `[x]` completada y aprobada; `[!]` bloqueada.
- Cada tarea es pequeña, ordenada y verificable; no se fragmenta en subtareas informales.
- Ninguna tarea de implementación comienza sin G-0a, G-0b y G-1. T-01 a T-03 son documentales y no autorizan código; T-02 produce G-0a (spec) y T-03 produce G-0b (plan/tareas). G-1 se requiere antes de T-04.
- Un commit por tarea con archivos versionables, incluido su registro de estado en este archivo.
- No se modifica `specs/003-cuentas-multiempresa/`, `CONSTITUTION.md` ni `AGENTS.md`.
- No se modifican pruebas en P0. Cualquier cambio futuro de copy requiere ampliación aprobada de G-1, actualización de la prueba en la misma tarea y registro aquí.
- Las evidencias no contienen contraseñas, tokens ni datos personales.
- No se afirma una prueba, medición o captura que no se haya ejecutado.

### 2.1 Flujo obligatorio de revisión y Git por tarea

Aplica a cada tarea de implementación (T-04 a T-11):

1. Implementer ejecuta una única tarea.
2. Ejecuta las pruebas pertinentes y Ruff.
3. Reviewer revisa la tarea y emite `APROBADO` o `CAMBIOS NECESARIOS`.
4. Build revisa el resultado.
5. Solo después de obtener `APROBADO`, Implementer realiza el commit de esa tarea.
6. Build verifica el commit, el contenido y el push.
7. Solo entonces se permite avanzar a la siguiente tarea.

Reglas adicionales:

- RC-8, RC-9 y RC-10 son checkpoints adicionales y no sustituyen la revisión individual de cada tarea.
- Si Reviewer emite `CAMBIOS NECESARIOS`, se corrige y se solicita una nueva revisión.
- Una aprobación anterior no puede reutilizarse para aprobar correcciones posteriores.
- No se usa `git commit --amend`, force push ni se agrupan archivos de otras tareas.
- Ante conflictos, fallos inesperados o cambios fuera de alcance, se detiene y se consulta.
- Una tarea no se marca `[x]` hasta que su revisión individual, commit y push estén completos.

---

## 3. Prerrequisitos

| Prerrequisito | Estado |
|---|---|
| Etapa 003 cerrada y publicada en `6893e59` | Cumplido |
| Suite de referencia: 337 pruebas (36 DB-free + 301 con base) | Cumplido en el cierre de 003 |
| Propuesta «Mostrador» aprobada el 2026-11-12 y recuperada de la sesión de trabajo | Cumplido: aprobación registrada; T-01 verifica la copia y sus hashes |
| Decisiones D-01 a D-06 aprobadas | Cumplido |
| `spec.md`, `plan.md` y `tasks.md` v0.1 | Aprobados en G-0a/G-0b el 2026-11-12 |
| G-0a: aprobación de la especificación | APROBADO el 2026-11-12 |
| G-0b: aprobación del plan y las tareas | APROBADO el 2026-11-12 |
| G-1: autorización de implementación | APROBADO el 2026-11-12 para T-04 a T-09; T-10 y T-11 no autorizadas |
| G-3 y G-4: servidor y base de pruebas | Pendientes de autorización por ejecución |
| Dependencias nuevas | Ninguna |

---

## 4. Resumen de tareas

| ID | Tarea | Fase | Depende de | Gate | Estado |
|---|---|---|---|---|---|
| T-01 | Recuperar y verificar decisiones existentes | F0 | — | — | `[x]` |
| T-02 | Formalizar especificación y criterios | F1 | T-01 | — (produce G-0a) | `[x]` |
| T-03 | Plan y tareas | F1 | T-02 | — (produce G-0b) | `[x]` |
| T-04 | Tokens, tipografía y CSS base | F2 | T-03 | G-1 | `[x]` |
| T-05 | Encabezado, navegación y pie | F2 | T-04 | G-1, G-3, G-4 | `[x]` |
| T-06 | Botones, campos, alertas y componentes | F2 | T-05 | G-1 | `[x]` |
| T-07 | Login y panel | F3 | T-06 | G-1, G-3, G-4 | `[x]` |
| T-08 | Usuarios, empresa y auditoría | F3 | T-07 | G-1, G-3, G-4 | `[x]` |
| T-09 | Perfil, contraseñas y errores | F3 | T-08 | G-1, G-3, G-4 | `[ ]` |
| T-10 | Responsive, accesibilidad y pruebas visuales | F4 | T-09 | G-1, G-3, G-4 | `[ ]` |
| T-11 | Revisión final y documentación | F4 | T-10 | G-1, G-5 | `[ ]` |

G-5 aplica a toda tarea que genere archivos: T-01 a T-11. No se repite en cada fila. G-2 no aplica: la etapa no genera migraciones.

---

## 5. Tareas detalladas

### T-01 — Recuperar y verificar decisiones existentes

- **Objetivo:** confirmar que la propuesta aprobada, su aprobación y el estado de partida coinciden antes de escribir cualquier artefacto o código.
- **Alcance:** lectura de fuentes, verificación de referencias y registro en este archivo. Sin cambios de código.
- **Dependencias:** ninguna.
- **Pasos:**
  1. Verificar los SHA-256 de la propuesta final y de la aprobación contra `spec.md` §1.
  2. Verificar que la Etapa 003 está cerrada en `6893e59` y que la suite de referencia es de 337 pruebas.
  3. Inventariar `static/css/main.css` (732 líneas), las 15 plantillas del alcance y los acoplamientos de §3.1 del plan.
  4. Confirmar que no existe `static/js/ui.js` y que los scripts de interfaz son los inline existentes de login, alta de usuario, empresa y contraseña.
  5. Registrar el resultado y las diferencias encontradas.
- **Verificación:** hashes coincidentes; referencia `6893e59`; inventario completo; sin diferencias sin explicar.
- **Evidencia:** salidas de verificación, `git status` y registro en este archivo.
- **Trazabilidad:** D-01 a D-06; R-12; RNF-06, RNF-10.
- **Prohibiciones:** modificar código, plantillas, pruebas o la Etapa 003; aprobar decisiones en nombre del usuario.

### T-02 — Formalizar especificación y criterios

- **Objetivo:** revisar la especificación y obtener su aprobación humana.
- **Alcance:** `spec.md`; registro de la revisión y de la aprobación.
- **Dependencias:** T-01.
- **Pasos:**
  1. Revisar RF-01 a RF-14, RNF-01 a RNF-10 y R-01 a R-12 contra `CONSTITUTION.md` y `AGENTS.md`.
  2. Incorporar las observaciones del Reviewer y del usuario que no reabran D-01 a D-06.
  3. Verificar que P1 y P2 permanecen fuera de la implementación y que las exclusiones son completas.
  4. Presentar el documento y registrar la aprobación de G-0a para la especificación.
- **Verificación:** aprobación humana registrada; sin contradicciones normativas; trazabilidad completa.
- **Evidencia:** versión revisada y registro de aprobación.
- **Trazabilidad:** D-01 a D-06; R-01 a R-12; RF-01 a RF-14; RNF-01 a RNF-10.
- **Prohibiciones:** declarar aprobado un documento sin aprobación explícita; modificar 003.

### T-03 — Plan y tareas

- **Objetivo:** revisar el plan técnico y la descomposición, y obtener la aprobación de G-0b.
- **Alcance:** `plan.md` y `tasks.md`; registro de la aprobación.
- **Dependencias:** T-02.
- **Pasos:**
  1. Verificar el mapa de archivos, las decisiones técnicas y las restricciones de pruebas.
  2. Verificar que las once tareas son secuenciales, verificables y sin fragmentación innecesaria.
  3. Confirmar gates, checkpoints y criterios de cierre.
  4. Presentar ambos documentos y registrar G-0b.
- **Verificación:** plan y tareas aprobados; dependencias y gates coherentes; ninguna tarea de código habilitada sin G-1.
- **Evidencia:** versión revisada y registro de aprobación.
- **Trazabilidad:** D-01 a D-06; R-01 a R-12; RF/RNF completos.
- **Prohibiciones:** iniciar T-04 sin G-0a, G-0b y G-1; ampliar el alcance sin aprobación.

### T-04 — Tokens, tipografía y CSS base

- **Objetivo:** establecer la fundación visual de «Mostrador» en `main.css`.
- **Alcance:** `static/css/main.css`, secciones 1 a 4, 13 y 14: tokens, reset, base tipográfica, layout, skip link, utilidades, foco, `::selection`, `prefers-reduced-motion`, `forced-colors` y bloque de compatibilidad de la home.
- **Dependencias:** T-03.
- **Pasos:**
  1. Reescribir los tokens con los 28 colores de `spec.md` §5.1 y la escala de espaciado; durante T-04, `--color-accent` conserva temporalmente el valor petróleo anterior y se documenta como alias de compatibilidad hasta T-06. Conservar todos los tokens heredados que aún usan las secciones no migradas y la home: `--color-paper`, `--color-paper-raised`, `--color-rule`, `--color-rule-strong`, `--color-accent-deep`, `--color-danger-bg`, `--color-danger-ink`, `--font-serif`, `--text-*`, `--line-*`, `--measure*`, `--gutter`, `--container-max`, `--rule-hairline`, `--rule-hairline-strong`, `--radius-sm`, `--focus-ring`, `--focus-offset` y `--transition-quick`.
  2. Definir familias, escala, pesos 700 en Candara, cifras tabulares y medidas; el login queda en 28rem como excepción.
  3. Implementar reset, layout, contenedor 72/80rem, gutter y skip link.
  4. Implementar foco doble, `::selection` con `primary`/`surface`, `prefers-reduced-motion`, `forced-colors` y utilidades.
  5. Crear el bloque de compatibilidad de la home con sus reglas actuales y `.panel__stage` en `accent-ink`; documentar que se conserva hasta P2 sin rediseñarla.
  6. Documentar los alias y el orden de retiro: tokens de color P0 en T-06, `.panel*`/selectores en T-09, home hasta P2.
  7. Verificar estáticamente (diff y búsqueda) que las reglas existentes y la home siguen renderizando sin roturas con los alias; sin captura ni G-3 en esta tarea.
- **Verificación:** tokens nuevos y tokens heredados documentados; pares de contraste que no dependen del ámbar verificados (los de acento se verifican en T-06); foco visible; `forced-colors`; sin recursos remotos; CSS válido; sin captura de pantalla en esta tarea.
- **Evidencia:** diff y búsqueda de tokens/alias.
- **Trazabilidad:** D-01, D-02; RF-01; RNF-01, RNF-02, RNF-03, RNF-04, RNF-05; R-01, R-02, R-03, R-08, R-11.
- **Prohibiciones:** modificar plantillas, pruebas o backend; introducir fuentes o frameworks; usar ámbar como texto; retirar tokens o `.panel*` antes de migrar sus usos; romper la compatibilidad de la home.
- **Registro de ejecución (2026-11-12):** T-04 implementada únicamente en `static/css/main.css` (897 líneas). Se incorporaron los 28 colores aprobados, la tipografía Candara/Segoe UI/Consolas, la escala y las medidas, el espaciado, los tokens de layout 72/80rem, las utilidades (`.num`, `.muted`, `.visually-hidden`, `.stack`, `.cluster`, `.grid`), el foco doble y `::selection`, `forced-colors` y el bloque de compatibilidad de la home (`.home-panels .panel__stage` en `accent-ink`). `--color-accent` conserva petróleo y el ámbar queda reservado sin uso como texto; se conservan los tokens y selectores heredados necesarios para T-05–T-09. **Verificación:** 36 pruebas DB-free en verde; `ruff check .` → All checks passed; `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes detected; todas las referencias `var()` resueltas (0 sin resolver); 36 tokens de color (28 aprobados + 7 heredados + ámbar reservado); tokens `--text-*`, `--line-*` y `--measure*` heredados idénticos a `6893e59`; `--container-max` 72rem y `--container-wide` 80rem sin overrides 76/82; sin `@import`, `@font-face`, `url(...)`, recursos remotos ni «unfold»; reglas de home presentes. Deuda transitoria registrada: `.panel__title` conserva peso 600 y las medidas H2/H3 se aplicarán al migrar los títulos en T-06/T-07. Sin captura ni G-3 en esta tarea. Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes.

### T-05 — Encabezado, navegación y pie

- **Objetivo:** aplicar la barra superior única y el pie compartido sin romper el shell.
- **Alcance:** `templates/base.html`, `templates/base_panel.html`, `templates/components/navbar.html`, `templates/components/footer.html` y estilos de cabecera y pie.
- **Dependencias:** T-04.
- **Pasos:**
  1. Migrar la barra a `.app-header` con marca, contexto y navegación; `aria-current="page"` en el enlace activo.
  2. Truncar el nombre de empresa con `max-width` y `text-overflow: ellipsis`.
  3. Conservar en `base.html` la ausencia de `request.*`, `perms` y `messages`, y el bloque `site_header`.
  4. Conservar `base_panel.html` independiente, sin extender `base.html`, con skip link, `main#contenido`, bloque `scripts` e inclusión del pie; migrar `.panel-context*` a las clases de contexto de la barra.
  5. Conservar en el pie «Etapa 003 — Cuentas y multiempresa» y el año.
  6. Mantener `href="/admin/"` con «Acceso técnico» discreto en la navegación pública.
  7. Conservar el estilo de `.site-header` que usan las páginas de error mediante `components/error_header.html`, sin modificar ese archivo.
  8. Verificar que las páginas de error no muestran «Administración» ni `/admin/`.
- **Verificación:** pruebas DB-free de home y estructura en verde; pruebas con base (G-4) de auth y navegación en verde; sin desborde con nombre de 150 caracteres; un solo `<footer>`; capturas en 320/768/1440 (G-3).
- **Evidencia:** pytest objetivo, capturas y búsqueda de tokens prohibidos.
- **Trazabilidad:** D-01, D-06; RF-01, RF-02; RNF-01, RNF-02, RNF-06; R-02, R-07, R-11, R-12.
- **Prohibiciones:** cambiar el copy del pie; introducir contexto de sesión en `base.html`; crear un shell compartido; tocar pruebas.
- **Registro de ejecución (2026-11-12):** T-05 implementada en `templates/base_panel.html`, `templates/components/navbar.html` y `static/css/main.css`; `base.html`, `components/footer.html` y `components/error_header.html` se conservan. La barra usa `.app-header` con marca, contexto de empresa/rol, navegación visible sin JavaScript y `aria-current="page"` en Panel, Perfil, Usuarios, Empresa y Auditoría según la ruta. La navegación pública queda con «Acceso al panel» y «Acceso técnico» discreto (`href="/admin/"`), y el pie compartido conserva «Etapa 003 — Cuentas y multiempresa», el año y un solo `<footer>`. El nombre de empresa se trunca con `max-width`/`text-overflow`; la simulación de 150 caracteres devolvió `truncated: true` (scrollWidth 1300, clientWidth 352). **Verificación:** 119 pruebas en verde (DB-free de home/estructura y con base de auth, navegación, autorización y aislamiento); `ruff check .` → All checks passed; `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes detected; 12 capturas en 320/768/1440 con 0 px de desbordamiento, un solo pie, etapa correcta, enlaces del dueño visibles y ausencia de `/admin/` en el panel; la visibilidad por capacidad se cubre además en `tests/test_accounts_navigation.py`. Hallazgo corregido: un `*/` dentro de un comentario CSS anulaba `--color-paper`; se reemplazó por texto sin cierre de comentario y se repitieron las capturas (botones con texto legible). Observaciones no bloqueantes: retirar `.site-nav*` huérfano en T-06/T-09; tokenizar el `rgba` del hover en T-06; confirmar el borde ámbar de la barra en T-10/RC-8; evaluar `aria-current` de «Perfil» en `/password/` en T-09; pulir alineación del nav público en 320 y el login en T-07/T-10; actualizar `MEMORY.md` y los estados de G-3/G-4 al cierre. Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes.

### T-06 — Botones, campos, alertas y componentes

- **Objetivo:** completar el vocabulario de componentes reutilizables.
- **Alcance:** `static/css/main.css`, secciones 5 a 11: botones, campos, badges, avisos, hojas, contexto, tablas, paginación, estados, recibo y error de página.
- **Dependencias:** T-05.
- **Pasos:**
  1. Implementar botones con sus variantes y estados, mínimo 44 px.
  2. Implementar campos, ayuda, errores, `aria-invalid` y acciones.
  3. Implementar badges por rol y estado, avisos por estado y hojas.
  4. Implementar `.context-strip` como `dl`, sin `.stat-grid`.
  5. Implementar tablas, `.table--audit`, paginación, estado vacío, carga, recibo y `.error-page`.
  6. Cambiar `--color-accent` a ámbar, migrar las reglas de componentes P0, eliminar `--color-paper*`, `--rule-hairline` y `--color-accent-deep` de las reglas P0 y verificar que no quedan usos en ellas; el bloque de compatibilidad de la home puede conservarlos.
  7. Conservar los selectores desnudos y el `[role="status"]` global como compatibilidad hasta T-09, porque las plantillas de T-07 a T-09 aún los usan.
  8. Conservar `.panel*` hasta T-09, porque las plantillas de T-07 a T-09 aún no están migradas.
  9. Verificar estáticamente que `.alert`, `.receipt` y `.empty-state` no heredan bordes ni fondos ajenos; sin capturas en esta tarea.
- **Verificación:** componentes definidos y consistentes en el diff; sin colisiones de especificidad; sin sombras en hojas; búsqueda de tokens retirados con cero usos en reglas P0; selectores de compatibilidad documentados.
- **Evidencia:** diff, búsqueda de tokens y lista de selectores de compatibilidad.
- **Trazabilidad:** D-01, D-02; RF-01, RF-13; RNF-01, RNF-05; R-02, R-03, R-04, R-10.
- **Prohibiciones:** crear plantillas de demostración o parciales; cambiar copy; usar `display:none` en columnas; retirar selectores o `.panel*` antes de T-09; tocar las reglas de la home fuera de su bloque de compatibilidad; tocar pruebas.
- **Registro de ejecución (2026-11-12):** T-06 implementada únicamente en `static/css/main.css`. Se añadieron los componentes aprobados: botones primario/secundario/ghost/peligro/peligro silencioso/tamaño/block, campos con label/control/ayuda/errores/acciones y `aria-invalid`, badges por rol y estado, avisos info/éxito/advertencia/error, hojas, `.context-strip` como `dl`, tablas `.table`/`.table--audit`/caption/actions/num/code, paginación, estados vacío/carga, recibo y `.error-page`. `--color-accent` pasó a ámbar y se migraron las reglas P0 para que no usen `--color-paper*`, `--rule-hairline`, `--color-rule`, `--color-accent-deep`, `--color-danger-bg` ni `--color-danger-ink`; el ámbar solo aparece en bordes decorativos y nunca como texto. Se conservaron `.panel*`, los selectores desnudos y `[role="status"]` como compatibilidad hasta T-09, y las reglas/responsive de la home. **Verificación estática:** 194 llaves balanceadas, 0 `var()` sin resolver, todos los componentes presentes, sin recursos remotos, sin `display:none` en tablas y sin acento ámbar como texto. **Pruebas:** 36 DB-free en verde; `ruff check .` → All checks passed; `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes detected. Sin capturas ni G-3 en esta tarea. Observaciones no bloqueantes: H-1 `.context-strip` debe validarse en 320/T-07 y T-10; H-2 completar estados `:active`, disabled, hover/focus de filas y paginación en T-08/T-09; H-3 se acepta `--text-label` de 13 px para ayuda/badge en lugar de 12 px; H-4 cuerpo de hoja con 24 px uniformes; H-5 recibo con borde sólido en lugar de discontinuo; H-6 `.table--audit` a 14 px y diferenciación pendiente en T-08; H-7 renumerar comentarios de secciones en T-09; H-8 retirar `.site-nav*` huérfano y tokenizar el `rgba` del hover en T-08/T-09; H-9 `.button--sm` de 40 px como excepción para filas; H-10 `filter: brightness` informativo. Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes.

### T-07 — Login y panel

- **Objetivo:** rediseñar el acceso de una columna y el panel de inicio.
- **Alcance:** `templates/accounts/login.html`, `templates/accounts/panel.html` y estilos asociados.
- **Dependencias:** T-06.
- **Pasos:**
  1. Login de una columna dentro del shell actual, con regla verde de 3 px, wordmark, promesa breve, un `h1` y un formulario de 28rem.
  2. Conservar `role="alert"`, `aria-busy`, `data-loading-label`, CSRF, `name="username"`, `name="password"`, la clase `.login`, el selector `.login form` y el script inline.
  3. Panel con `h1`, `dl` de contexto (empresa, rol, «Sesión iniciada»), acción «Gestionar usuarios» solo con capacidad y lista de trabajo con verbos completos; migrar `.panel*` de `panel.html` a `.sheet` y `.context-strip`.
  4. Conservar los textos actuales del panel y los datos ya disponibles; sin consultas nuevas.
- **Verificación:** login y panel renderizan sin error; prueba de `aria-busy` en verde; pruebas de auth y navegación con base (G-4); un `h1`; sin columna verde de contenido; capturas en 320/768/1440 (G-3).
- **Evidencia:** pytest de auth y navegación, diff y capturas.
- **Trazabilidad:** D-02, D-06; RF-03, RF-04; RNF-01, RNF-06, RNF-07; R-04, R-10, R-12.
- **Prohibiciones:** extraer el script a `static/js/`; cambiar nombres de campo o copy; añadir consultas; ocultar el header del login.
- **Registro de ejecución (2026-11-12):** T-07 implementada en `templates/accounts/login.html`, `templates/accounts/panel.html` y `static/css/main.css`. Login de una columna con wordmark, promesa y formulario de 28rem; se conservaron `role="alert"`, `aria-busy`, `data-loading-label`, CSRF, nombres de campo, `.login form` y el script inline. Panel con `.sheet`, `h1`, `.context-strip` (empresa, rol, sesión), acción «Gestionar usuarios» solo con capacidad y lista de trabajo con verbos completos; sin consultas nuevas. **Verificación:** 89 pruebas en verde (home, estructura, auth y navegación); `ruff check .` → All checks passed; `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes detected; 6 capturas regeneradas en 320/768/1440 con 0 px de desbordamiento, un solo `h1`, formulario 448/280 px, tres ítems de contexto, cuatro de trabajo con verbos completos («Gestionar usuarios», «Editar datos del negocio», «Revisar auditoría», «Ver mi perfil»), acción principal `.button--primary`, copy existente del panel restaurado y acción de usuarios solo para el dueño. Se citan `tests/test_accounts_navigation.py` para la visibilidad por capacidad y `tests/test_accounts_isolation.py` para las tres consultas. Observaciones menores: «Tu negocio, en orden.» proviene de la propuesta aprobada; el párrafo restaurado duplica contexto a evaluar en T-10; `.login`/`.sheet__header` duplican reglas de T-06 y se consolidarán en T-09. Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes.

### T-08 — Usuarios, empresa y auditoría

- **Objetivo:** rediseñar las superficies de gestión conservando datos, copy y formularios.
- **Alcance:** `user_list.html`, `user_form.html`, `user_confirm.html`, `company_form.html`, `audit_list.html` y estilos asociados.
- **Dependencias:** T-07.
- **Pasos:**
  1. Listado con 5 columnas: Persona (nombre y correo), Rol, Estado, Último acceso y Acciones; badges; acciones agrupadas visibles; aplicar `.table` y `.table__caption` (`.table--audit` es modificador de `.table`) y migrar `.panel*` a `.sheet`; conservar el `aria-label` de paginación y la ausencia de paginación en el estado vacío.
  2. Conservar `caption`, `scope`, `th scope="row"` por fila, `.table-scroll` enfocable y `aria-label`.
  3. Alta con hoja, ayuda, «Cancelar» y recibo; conservar el primer `<code>` único, `role="status"`, `aria-busy` y `data-loading-label`; actualizar el script de `.panel form` a `.sheet form`.
  4. Confirmación con `h1` dinámico, aviso de éxito o error y recibo; conservar `title`, `message`, `temporary_password` y `role`.
  5. Empresa con hoja de un campo, ayuda y acciones; conservar «Nombre de la empresa actualizado.» y los errores; actualizar el script de `.panel form` a `.sheet form`.
  6. Auditoría con dos secciones, `.table--audit`, fecha `.num`, acción en `code`, valores en chips y paginación; migrar `.panel*` a `.sheet` y conservar textos vacíos y parámetros.
- **Verificación:** pruebas de usuarios, empresa y auditoría con base (G-4) en verde; fecha `05/03/2026 12:00`; 20 `scope="row"` por página; contraseña extraíble por el primer `<code>` una sola vez; capturas (G-3).
- **Evidencia:** pytest objetivo, capturas y búsqueda de copy conservado.
- **Trazabilidad:** D-02, D-04; RF-05, RF-06, RF-07, RF-08, RF-09; RNF-06, RNF-08, RNF-09; R-07, R-09, R-10, R-12.
- **Prohibiciones:** duplicar el secreto; cambiar copy o formato de fecha; ocultar columnas; modificar formularios, vistas o pruebas.
- **Registro de ejecución (2026-11-12):** T-08 implementada en `templates/accounts/user_list.html`, `user_form.html`, `user_confirm.html`, `company_form.html`, `audit_list.html` y `static/css/main.css`. Listado de cinco columnas con Persona (nombre y correo), Rol/Estado con badges, Último acceso y Acciones agrupadas; se conservaron `caption`, `scope`, `th scope="row"`, `.table-scroll` enfocable, el `aria-label` de paginación y la ausencia de paginación en vacío. Alta, confirmación y empresa usan `.sheet`, ayuda, acciones secundarias y recibo; se conservaron el primer `<code>` único, `role="status"`, `aria-busy`, CSRF y el copy verificado; scripts de alta y empresa migrados a `.sheet form`. Auditoría con dos secciones, `.table--audit`, fechas `.num`, acciones `code`, estados vacíos y paginación. **Verificación:** 151 pruebas en verde; `ruff check .` → All checks passed; `manage.py check` sin problemas; `makemigrations --check --dry-run` → No changes detected; 12 capturas en 320/768/1440 con 0 px de desbordamiento, cinco cabeceras de usuarios, cinco filas, 14 filas de auditoría y dos secciones. Hallazgo corregido: `document.scrollWidth` incluía el ancho de la tabla aunque `.table-scroll` tuviera scroll interno; se añadió `overflow:auto` + `contain:paint`, y `.table--users` con anchos fijos y acciones que envuelven. Correcciones posteriores: valores de auditoría en chips `.table__chip` con anchos de columna legibles; acciones de usuarios alineadas a la derecha con `.table .table__actions`; `table__person` con `overflow-wrap`. Observaciones no bloqueantes: consolidar `.table__actions`/`.pagination__list` duplicados y renumerar comentarios en T-09; estados vacíos sin acción y `messages` siempre como éxito a T-10; conservar `[role="status"]` global hasta T-09; envolver los chips en un `div` y revisar la flecha `aria-hidden` y la tabla de seguridad de 4 columnas en T-10. Dictamen del Reviewer: APROBADO (2026-11-12), sin hallazgos bloqueantes.

### T-09 — Perfil, contraseñas y errores

- **Objetivo:** completar las superficies P0 de identidad, contraseña y recuperación.
- **Alcance:** `profile.html`, `password_change.html`, `errors/403.html`, `errors/404.html` y estilos asociados.
- **Dependencias:** T-08.
- **Pasos:**
  1. Perfil con identidad, badge de rol, empresa y acción «Cambiar contraseña»; conservar «Contraseña actualizada.» y migrar `.panel*` a `.sheet`.
  2. Contraseña con aviso de advertencia si `must_change_password`, campos, ayuda y errores asociados; conservar `aria-busy` y el script inline, y actualizar el selector `.panel form` a `.sheet form`.
  3. Errores con `.error-page`, código, `h1`, explicación y acción; conservar la variante `reason == "context"`, el cierre de sesión con CSRF y las acciones existentes.
  4. Mantener el shell actual en P0 y la ausencia de «Administración» y `/admin/` en errores.
  5. Eliminar los selectores `.panel*` genéricos, los selectores desnudos (`table`, `th, td`, `thead th`, `code`, `caption`, `dl`), el selector CSS `[role="status"]` global y los alias restantes de las reglas P0; conservar las definiciones de token que usa el bloque de la home hasta P2 y el atributo `role="status"` en las plantillas que lo usan. Verificar por búsqueda que no quedan usos en `main.css` ni en las plantillas P0, salvo el bloque acotado de compatibilidad de la home.
- **Verificación:** pruebas de auth, autorización y navegación con base (G-4) en verde; 403 de contexto y de capacidad distinguibles; 404 idénticos; un `h1`; capturas (G-3); búsqueda de `.panel*` y selectores desnudos con cero usos en P0; home sin regresión.
- **Evidencia:** pytest objetivo, capturas de 403/404 y diff.
- **Trazabilidad:** D-04, D-06; RF-10, RF-11, RF-12; RNF-01, RNF-06, RNF-09; R-04, R-10, R-12.
- **Prohibiciones:** crear shell nuevo; cambiar mensajes o acciones; extraer el script inline; tocar pruebas.

### T-10 — Responsive, accesibilidad y pruebas visuales

- **Objetivo:** validar el sistema en los cinco anchos y con las condiciones de accesibilidad exigidas; T-10 es principalmente una tarea de validación responsive, accesibilidad y pruebas visuales.
- **Alcance:** validación y correcciones puntuales de CSS o plantillas P0 justificadas por defectos detectados en las verificaciones; sin cambios de copy, comportamiento ni decisiones visuales.
- **Delimitación:** se permiten exclusivamente correcciones puntuales de CSS o plantillas P0 necesarias para cumplir los criterios aprobados, correcciones justificadas por defectos detectados durante las verificaciones y pruebas o evidencias que demuestren que la corrección resuelve el problema. No se permite rediseñar pantallas, cambiar decisiones visuales aprobadas, ampliar P0/P1/P2, cambiar copy o comportamiento ni modificar backend, modelos, migraciones o pruebas sin autorización expresa. Cada corrección se documenta, se prueba y pasa por revisión individual del Reviewer. Si una corrección supera el alcance aprobado, se detiene y se solicita autorización humana antes de modificar archivos.
- **Dependencias:** T-09.
- **Pasos:**
  1. Validar 320, 375, 768, 1440 y 1920 px sin scroll horizontal de página.
  2. Validar zoom 200 % sin superposición ni scroll de página.
  3. Verificar contraste de texto y componentes con los pares de `spec.md` §5.2.
  4. Recorrer con teclado: skip link, marca, contexto, navegación, contenido; foco visible en todos los controles.
  5. Verificar tablas con `caption`, `scope` y scroll interno; formularios con `aria-invalid`/`aria-describedby`.
  6. Verificar `prefers-reduced-motion`, `forced-colors`, `lang="es"`, un `h1` y objetivos táctiles.
  7. Verificar los estados según RF-13 (vacío, carga, error, éxito y confirmación donde correspondan) en las superficies P0.
  8. Ejecutar Ruff, `manage.py check`, `makemigrations --check --dry-run` y la suite completa en dos invocaciones (G-4).
  9. Verificar que Admin no carga `main.css`, que el nombre de empresa de 150 caracteres no desborda y que la home pública (P2) no sufre regresión visual ni de contraste.
  10. Documentar cada corrección aplicada, la prueba o evidencia que demuestra que resuelve el defecto, y someterla a revisión individual del Reviewer.
- **Verificación:** R-01 a R-04 y R-07 a R-12 cumplidos; R-05 y R-06 declarados P1; suite en verde; sin errores de Ruff; home P2 sin regresión visual ni de contraste; correcciones puntuales revisadas individualmente.
- **Evidencia:** capturas por ancho y estado, mediciones de contraste, orden de tabulación, salidas de comandos y registro de cada corrección.
- **Trazabilidad:** D-02, D-03; RF-01, RF-13, RF-14; RNF-01, RNF-02, RNF-03, RNF-07, RNF-10; R-01 a R-04, R-07, R-08, R-11, R-12.
- **Prohibiciones:** rediseñar pantallas; cambiar decisiones visuales, copy o comportamiento; ampliar P0/P1/P2; modificar backend, modelos, migraciones o pruebas sin autorización expresa; corregir accesibilidad cambiando copy o pruebas; introducir JS; ocultar columnas; rediseñar la home fuera de su bloque de compatibilidad.

### T-11 — Revisión final y documentación

- **Objetivo:** revisar la etapa completa, actualizar la documentación y cerrar con evidencia.
- **Alcance:** `README.md`, `docs/README.md`, registro de cierre en este archivo y `MEMORY.md` solo al cierre y con aprobación.
- **Dependencias:** T-10.
- **Pasos:**
  1. Revisar la trazabilidad D-01 a D-06, R-01 a R-12, RF/RNF y tareas.
  2. Confirmar que no se modificaron `apps/**`, `config/**`, migraciones, Admin/Unfold ni la Etapa 003.
  3. Actualizar `README.md` y `docs/README.md` con el estado de la Etapa 004 y sus límites.
  4. Registrar las evidencias finales, las limitaciones y los criterios R verificados.
  5. Presentar RC-10 al Reviewer y corregir los hallazgos.
  6. Verificar commits por tarea, `HEAD` publicado y árbol limpio; actualizar `MEMORY.md` con aprobación.
- **Verificación:** RC-10 con APROBADO; documentación coherente; suite y Ruff en verde; sin cambios fuera de alcance.
- **Evidencia:** informe de revisión, salidas de comandos, estado de Git y documentos actualizados.
- **Trazabilidad:** todos los RF, RNF y R; criterios de cierre del plan.
- **Prohibiciones:** cerrar sin APROBADO; reescribir historial; agrupar archivos de otras tareas.

---

## 6. Puntos de revisión del Reviewer

| Checkpoint | Momento | Tareas | Alcance | Veredicto |
|---|---|---|---|---|
| RC-8 | Tras T-06 | T-01 a T-06 | Sistema visual, shell y fundación de componentes | APROBADO (2026-11-12) |
| RC-9 | Tras T-09 | T-07 a T-09 | Login, panel, usuarios, empresa, auditoría, perfil, contraseña y errores | APROBADO / CAMBIOS NECESARIOS |
| RC-10 | Tras T-11 | T-10 y T-11 | Validación responsive y accesible, suite, documentación y cierre | APROBADO / CAMBIOS NECESARIOS |

Cada checkpoint cierra cuando todas sus tareas están aprobadas y commiteadas. RC-8, RC-9 y RC-10 son checkpoints adicionales y no sustituyen la revisión individual de cada tarea. Un veredicto CAMBIOS NECESARIOS reabre la tarea afectada sin avanzar a la siguiente.

- **RC-8 APROBADO (2026-11-12):** T-01 a T-06 revisadas; `HEAD` = `b6c3610`; suite completa **337 passed** (36 DB-free + 301 con base autorizada); Ruff, `manage.py check` y `makemigrations --check` en verde. Sin bloqueantes. Observaciones asignadas: O-1 delta visual de la home a validar en T-10 (aceptado provisionalmente); O-2 bordes de tabla y `tfoot` a T-08/T-10; O-3 hoja/H1 a T-07/T-10; O-4 recibo discontinuo a T-08/T-10; O-5 estados a T-08/T-09/T-10; O-6 `[role="status"]` a T-08/T-09; O-7 `.site-nav*`/`rgba` a T-08/T-09; O-8 context strip responsive a T-07/T-10; O-9 `aria-current`/nav/login a T-07/T-09/T-10; O-10 brand de error a T-09/T-10; O-11 comentarios a T-09; O-12 documentación/commits de T-01–T-03 a T-11; O-13 `.container--wide` a T-10; O-14 cierra el borde ámbar y las excepciones H-3/H-9/H-10. T-07 no iniciada y sin autorización.

---

## 7. Matriz de trazabilidad

### 7.1 Decisiones y criterios → tareas

| Elemento | Tareas |
|---|---|
| D-01 | T-01, T-04, T-05, T-06 |
| D-02 | T-04, T-06, T-07, T-08, T-10 |
| D-03 | T-10 (solo declaración P1) |
| D-04 | T-08, T-09, T-10 |
| D-05 | T-01, T-02, T-03, T-11 |
| D-06 | T-05, T-07, T-09 |
| R-01 | T-04, T-10 |
| R-02 | T-04, T-05, T-06, T-10 |
| R-03 | T-04, T-06, T-10 |
| R-04 | T-06, T-07, T-09, T-10 |
| R-05 | T-10 (declarado P1; no se implementa) |
| R-06 | T-10 (declarado P1; no se implementa) |
| R-07 | T-05, T-08, T-10 |
| R-08 | T-04, T-10 |
| R-09 | T-08, T-10 |
| R-10 | T-06, T-07, T-08, T-09, T-10 |
| R-11 | T-04, T-05, T-10 |
| R-12 | T-01 a T-11 |

### 7.2 Requisitos → tareas

| Requisitos | Tareas |
|---|---|
| RF-01 | T-04, T-05, T-06, T-10 |
| RF-02 | T-05, T-10 |
| RF-03 | T-07, T-10 |
| RF-04 | T-07, T-10 |
| RF-05, RF-06, RF-07 | T-08, T-10 |
| RF-08, RF-09 | T-08, T-10 |
| RF-10, RF-11, RF-12 | T-09, T-10 |
| RF-13 | T-06, T-09, T-10 |
| RF-14 | T-10 |
| RNF-01 | T-04 a T-10 |
| RNF-02 | T-04, T-05, T-10 |
| RNF-03 | T-04, T-10 |
| RNF-04 | T-04, T-06 |
| RNF-05 | T-04, T-06 |
| RNF-06 | T-05, T-07, T-08, T-09, T-10, T-11 |
| RNF-07 | T-07, T-10 |
| RNF-08 | T-08, T-10 |
| RNF-09 | T-08, T-09, T-10, T-11 |
| RNF-10 | T-01, T-10, T-11 |

---

## 8. Orden de ejecución

T-01 → T-02 → T-03 → T-04 → T-05 → T-06 → T-07 → T-08 → T-09 → T-10 → T-11.

T-01 a T-03 son documentales: no autorizan código. T-04 a T-11 requieren G-1. Cada tarea se revisa y se commitea antes de que la siguiente modifique los mismos archivos.

---

## 9. Autorizaciones requeridas

| Gate | Alcance | Estado |
|---|---|---|
| G-0a | Aprobación de `spec.md` | APROBADO el 2026-11-12 |
| G-0b | Aprobación de `plan.md` y `tasks.md` | APROBADO el 2026-11-12 |
| G-1 | Autorización de implementación de T-04 a T-11 | APROBADO el 2026-11-12 para T-04 a T-09; T-10 y T-11 no autorizadas |
| G-2 | Migraciones | No aplica |
| G-3 | Servidor local y datos ficticios en `nexopyme_bootstrap_dev` | Confirmado por ejecución en T-05; se reconfirma por tarea |
| G-4 | Pruebas con `nexopyme_bootstrap_test` | Confirmado por ejecución en T-05; se reconfirma por tarea |
| G-5 | Commit y push por tarea | Operativo dentro del flujo autorizado; no requiere autorización adicional |

El silencio no constituye aprobación. Ninguna aprobación de este documento autoriza por sí sola la implementación.

---

## 10. Estado de las tareas

- `[x]` T-01: recuperación y verificación de la propuesta completadas (2026-11-12).
- `[x]` T-02: `spec.md` v0.1 aprobada en G-0a (2026-11-12).
- `[x]` T-03: `plan.md` y `tasks.md` v0.1 aprobados en G-0b (2026-11-12).
- `[x]` T-04: tokens, tipografía y CSS base aprobados por el Reviewer (2026-11-12) y commiteados.
- `[x]` T-05: barra de aplicación, navegación con `aria-current` y pie compartido aprobados por el Reviewer (2026-11-12) y commiteados.
- `[x]` T-06: componentes de botones, campos, alertas, badges, hojas, contexto, tablas, paginación, estados, recibo y error aprobados por el Reviewer (2026-11-12) y commiteados.
- `[x]` T-07: login de una columna y panel con hoja, contexto y lista de trabajo aprobados por el Reviewer (2026-11-12) y commiteados.
- `[x]` T-08: usuarios, empresa y auditoría migrados a hojas, badges, tablas y recibos; aprobados por el Reviewer (2026-11-12) y commiteados.
- `[ ]` T-09: no iniciada; requiere G-1, G-3 y G-4.
- `[ ]` T-10: no iniciada; requiere G-1, G-3 y G-4.
- `[ ]` T-11: no iniciada; requiere G-1 y G-5.
- **Registro de aprobación (2026-11-12):** G-0a APROBADO para `spec.md`; G-0b APROBADO para `plan.md` y `tasks.md`; G-1 APROBADO para T-04 a T-09. T-10 y T-11 permanecen no autorizadas.

---

**Fin de las tareas v0.1.** Los tres documentos de la Etapa 004 están aprobados en G-0a/G-0b. G-1 está aprobado para T-04 a T-09. T-04 a T-08 están publicadas; RC-8 está APROBADO; T-09 autorizada y no iniciada; T-10 y T-11 no están autorizadas y la Etapa 003 no se modifica.
