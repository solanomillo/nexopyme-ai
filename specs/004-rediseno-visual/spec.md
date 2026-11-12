# Especificación funcional 004 — Rediseño visual — **v0.1 (aprobada)**

## 1. Identificación, estado y convenciones

| Campo | Valor |
|---|---|
| Funcionalidad | 004 — Rediseño visual |
| Artefacto | `specs/004-rediseno-visual/spec.md` |
| Versión | 0.1 (aprobada) |
| Fases SDD | 1 y 2: especificación y aclaración de ambigüedades |
| Autor | Planner |
| Estado | **APROBADO — G-0a por el usuario el 2026-11-12**; G-0b aprobado en `plan.md`/`tasks.md`; G-1 aprobado para T-04 a T-09 |
| Fecha | 2026-11-12 |
| Especificación fuente | Propuesta «Mostrador» aprobada el 2026-11-12, recuperada de la sesión de trabajo |
| Etapa previa | 003 cerrada y publicada en `6893e59`; 337 pruebas (36 DB-free + 301 con base autorizada) |
| Depende de | `CONSTITUTION.md`, `AGENTS.md`, `specs/003-cuentas-multiempresa/spec.md` v1.0 |
| Consumida por | `plan.md` v0.1 y `tasks.md` v0.1 de esta etapa |
| Artefactos activos | 14 RF · 10 RNF · 12 R · 6 D aprobadas · 18 riesgos (16 de la propuesta final + copy del pie + compatibilidad de la home) · 5 ambigüedades |

**Fuente y verificación.** La propuesta final corregida prevalece sobre la propuesta original del Planner. La aprobación humana alcanza a las seis decisiones de §4 y a la dirección «Mostrador»; no autoriza la implementación.

| Documento | SHA-256 |
|---|---|
| Propuesta final aprobada | `E349441BD1C7B06AD9F9F125C1C7C30EB019D04CA67AC451D0DED8D5151DBA9D` |
| Aprobación humana | `A78C68D96CFCD5AE0BF2BF00364479143EC3CF7E8F6BBB3BD6155675A6FCD017` |
| Propuesta original del Planner (referencia) | `7DB4D3CE61649C2B638E6E18411FED041449F54C81C8AFA9A3A78F66494CA585` |

La propuesta final incorpora el dictamen del Reviewer: bloqueantes A-1 a A-6, altos B-1 a B-6, medios C-1 a C-8 y bajos. Esta especificación los resuelve o los declara; no reabre las decisiones aprobadas.

**Convenciones de marcado**

- EARS para requisitos verificables: `CUANDO`, `SI … ENTONCES`, `MIENTRAS`, `DONDE`, `El sistema DEBE`.
- `[P0]`, `[P1]`, `[P2]`: prioridad. Solo P0 se implementa en esta etapa.
- `[D-xx]`: decisión aprobada en §4. `[R-xx]`: criterio de aceptación de §9. `[A-xx]`: ambigüedad de §13.
- Toda tabla de requisitos lleva columna **Estado**.
- No se asume aprobación tácita: este documento está aprobado en G-0a (2026-11-12); ninguna tarea de código puede iniciarse sin G-1.

---

## 2. Objetivo

Definir el sistema visual y el comportamiento de presentación verificable de NexoPyme AI bajo la dirección «Mostrador», para las superficies P0 de la Etapa 003, sin alterar comportamiento de negocio, backend, permisos ni datos. La etapa entrega un CSS propio, un vocabulario de componentes y quince plantillas actualizadas que conservan el copy verificado, la accesibilidad y la suite existente.

---

## 3. Alcance y exclusiones

### 3.1 Incluido en P0

Shell público y de panel · acceso de una columna · panel · listado, alta y confirmación de usuarios · datos de la empresa · auditoría y eventos de seguridad · perfil · cambio de contraseña · páginas 403 y 404.

### 3.2 P1 y P2: documentados y fuera de esta implementación

| Fase | Alcance | Estado |
|---|---|---|
| P1 | Menú móvil con JavaScript mínimo; gestión por fila con `<details>`; login de dos columnas opcional con panel de marca en verde suave | Aprobado como fase posterior (`D-03`); no se implementa en 004-P0 |
| P2 | Home pública de producto; parciales `_alert`/`_badge`/`_field`; favicon e iconografía mínima; ajustes de copy | Diferido; requiere especificación o ampliación aprobada |

### 3.3 Exclusiones de esta etapa

| Exclusión | Estado |
|---|---|
| Backend: `apps/**`, `config/**`, modelos, vistas, formularios, servicios, URLs, middleware, autenticación, permisos y settings | Firme |
| Migraciones y cambios de esquema | Firme; G-2 no aplica |
| Django Admin y Unfold: plantillas, estilos y configuración | Firme: `main.css` no se carga en Admin |
| Home pública (`templates/home.html`) | P2 |
| Modo oscuro, header sticky, ocultamiento de columnas con `display:none` | Firme |
| Toasts, modales, pestañas, menús desplegables de escritorio y cualquier patrón con JavaScript nuevo en P0 | Firme |
| Frameworks CSS, fuentes externas, `@import` remoto, iconografías o recursos remotos | Firme |
| Cambios de copy verificado por pruebas | Firme salvo lista explícita aprobada (`D-04`) |
| Cambios en `specs/003-cuentas-multiempresa/`, `CONSTITUTION.md` o `AGENTS.md` | Firme |
| Cambios en `tests/**` | Firme; no hay cambios de prueba previstos en P0 |

---

## 4. Decisiones aprobadas (no se reabren)

Aprobadas por el usuario el 2026-11-12. Su consecuencia es normativa para esta especificación.

| ID | Decisión aprobada | Consecuencia |
|---|---|---|
| D-01 | Dirección «Mostrador»: cal fría `#F1F3EC`, verde profundo `#14523F`, ámbar `#B26A1F`; Candara + Segoe UI con fallbacks del sistema | §5 fija paleta, tipografía y proporción 70/25/5; el ámbar no se usa como texto pequeño |
| D-02 | P0 sin JavaScript, login de una columna, acciones de usuarios visibles y tablas con scroll interno accesible | RF-03, RF-05, RF-14; prohibido ocultar columnas o introducir JS nuevo |
| D-03 | P1 posterior: menú móvil con JavaScript mínimo, `<details>` por fila y login de dos columnas opcional | RF-14; R-05 y R-06 se difieren a P1 |
| D-04 | Conservar los textos verificados por las pruebas en P0; cualquier cambio de copy requiere aprobación y trazabilidad | §10 regla 2; §12 riesgo de copy; A-05 |
| D-05 | Etapa independiente `specs/004-rediseno-visual/` | No se modifica la Etapa 003 |
| D-06 | La única gran superficie verde es la barra superior; el login P0 no tiene columna verde profunda | RF-02, RF-03; el panel de marca P1 usa `primary-soft`, no `primary` |

---

## 5. Sistema visual

### 5.1 Tokens de color

La propuesta aprobada enumera 28 tokens de color; se documentan todos con su rol.

| Token | HEX | Rol | Uso |
|---|---|---|---|
| `--color-canvas` | `#F1F3EC` | Base | Fondo de página, pared de cal fría |
| `--color-surface` | `#FBFCF7` | Superficie | Hojas, tablas, formularios |
| `--color-surface-sunken` | `#E7EBE2` | Superficie hundida | Estados vacíos, filas alternas, badges neutros |
| `--color-ink` | `#17251F` | Texto principal | Títulos, nombres, énfasis |
| `--color-ink-soft` | `#4A5A52` | Texto secundario | Párrafos, ayudas, metadatos |
| `--color-ink-muted` | `#5E6E65` | Texto terciario | Placeholders, notas, deshabilitado |
| `--color-primary` | `#14523F` | Acento primario | Barra superior, botón primario, enlaces, foco de marca |
| `--color-primary-deep` | `#0D3D2F` | Primario profundo | Hover/active del primario |
| `--color-primary-soft` | `#DDEAE3` | Primario suave | Badge de encargado, hover secundario, panel de marca P1 |
| `--color-accent` | `#B26A1F` | Acento cálido | Sello, muesca activa, borde de recibo; **no usar como texto** |
| `--color-accent-ink` | `#8A4E12` | Acento legible | Texto de badge de dueño, énfasis cálido |
| `--color-accent-soft` | `#F6E7D2` | Acento suave | Fondo de badge de dueño, aviso cálido |
| `--color-success` | `#1E6B45` | Éxito | Texto y borde de éxito |
| `--color-success-soft` | `#E3F1E8` | Éxito suave | Fondo de aviso o badge |
| `--color-warning` | `#7A4E00` | Advertencia | Texto y borde |
| `--color-warning-soft` | `#FBF0D9` | Advertencia suave | Fondo |
| `--color-danger` | `#9B2C2C` | Peligro | Errores y acciones destructivas |
| `--color-danger-soft` | `#FBEDEC` | Peligro suave | Fondo de error |
| `--color-info` | `#245A6B` | Información | Texto y borde |
| `--color-info-soft` | `#E6F1F4` | Información suave | Fondo |
| `--color-border` | `#C9D0C6` | Filete decorativo | Separadores y bordes de hoja |
| `--color-border-strong` | `#A9B5AC` | Filete fuerte | Cabecera y pie de tabla |
| `--color-control-border` | `#6F7F76` | Borde de control | Inputs, selects, botones secundarios |
| `--color-focus` | `#0B6E8A` | Foco | Anillo exterior |
| `--color-header` | `#14523F` | Barra superior | Fondo de la barra |
| `--color-header-ink` | `#FBFCF7` | Texto de barra | Marca y enlaces |
| `--color-header-muted` | `#CFDDD6` | Texto secundario de barra | Contexto de empresa y rol |
| `--color-header-accent` | `#E8B05C` | Acento de barra | Muesca activa y sello |

**Reglas de color.** Proporción 70/25/5; ámbar solo en bordes, muescas, sellos y componentes no textuales; verde no es fondo de contenido; sin gradientes, negro puro ni blanco puro; bordes antes que sombras; los estados semánticos se usan solo para estados.

### 5.2 Pares de contraste verificados

| Par | Ratio |
|---|---:|
| `ink` sobre `canvas` | **14,21:1** |
| `ink-soft` sobre `canvas` | **6,53:1** |
| `ink-muted` sobre `canvas` | **4,82:1** |
| `surface` sobre `primary` | **8,82:1** |
| `primary` sobre `canvas` | **8,13:1** |
| `accent-ink` sobre `canvas` | **5,90:1** |
| `accent` sobre `canvas` | **3,77:1** (solo componentes no textuales) |
| `success` sobre `canvas` | **5,79:1** |
| `warning` sobre `canvas` | **6,43:1** |
| `danger` sobre `canvas` | **6,73:1** |
| `info` sobre `canvas` | **6,83:1** |
| `danger` sobre `danger-soft` | **6,60:1** |
| `success` sobre `success-soft` | **5,55:1** |
| `warning` sobre `warning-soft` | **6,36:1** |
| `info` sobre `info-soft` | **6,64:1** |
| `accent-ink` sobre `accent-soft` | **5,44:1** |
| `control-border` sobre `canvas` | **3,77:1** |
| `control-border` sobre `surface` | **4,10:1** |
| `header-muted` sobre `primary` | **6,48:1** |
| `header-accent` sobre `primary` | **4,68:1** |
| `focus` sobre `canvas` | **5,20:1** |
| `focus` sobre `primary` | **1,56:1** → exige **anillo doble** |

**Foco.** Anillo doble de 2 px `--color-surface` + 3 px `--color-focus`. Sobre fondos claros se ve el azul; sobre la barra verde se ve el halo claro. Nunca se elimina el outline.

### 5.3 Tipografía

| Rol | Familia |
|---|---|
| Títulos y marca | `"Candara", "Optima", "Segoe UI", system-ui, sans-serif` |
| Cuerpo y controles | `"Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif` |
| Datos y cifras | Sans del cuerpo con `font-variant-numeric: tabular-nums` |
| Código y secretos | `"Consolas", "Cascadia Mono", "Courier New", monospace` |

| Rol | Tamaño | Peso | Line-height | Tracking | Medida |
|---|---|---:|---:|---:|---:|
| Display | `clamp(2.5rem, 2rem + 2.2vw, 4rem)` · 40–64 px | 700 | 1,05 | `-0.02em` | 22ch |
| H1 | `clamp(1.75rem, 1.45rem + 1.2vw, 2.5rem)` · 28–40 px | 700 | 1,12 | `-0.015em` | 26ch |
| H2 | 20–24 px | 700 | 1,20 | `-0.01em` | 36ch |
| H3 | 18 px | 700 | 1,25 | `0` | 42ch |
| Lead | 18–20 px | 400 | 1,55 | `0` | 60ch |
| Body | 16 px | 400 | 1,55 | `0` | 66ch |
| Small | 14 px | 400 | 1,45 | `0` | 60ch |
| Label | 13 px | 600 | 1,30 | `0.01em` | 34ch |
| Tabla | 14 px | 400 | 1,35 | `0` | 40ch |
| Botón | 14 px | 600 | 1,20 | `0.01em` | — |
| Código | 13 px | 400 | 1,40 | `0` | — |

**Reglas tipográficas.** Títulos en oración, sin mayúsculas forzadas; sin tracking en etiquetas de tabla (el token Label conserva `0.01em` por legibilidad); cifras tabulares para datos; alineación numérica a la derecha en columnas comparables; monoespaciada solo para códigos; 66ch de medida de cuerpo y 36rem máximo en formularios, con el login P0 limitado a 28rem como excepción. La tabla fija Código en 13 px; el recibo de contraseña temporal usa 16 px como excepción declarada. En Candara se usa **700**, no 600, para evitar síntesis de peso; si aparece un número en un título se fuerza `lnum`/`tnum`.

**Limitación declarada.** Candara y Segoe UI no existen en Linux; allí títulos y cuerpo caen a `system-ui` y la jerarquía se sostiene por tamaño y peso. No se declara equivalencia tipográfica (A-03).

### 5.4 Espaciado, layout, radios, bordes y elevación

| Token | Valor | Uso |
|---|---:|---|
| `--space-1` | 4 px | Icono-texto, separación mínima |
| `--space-2` | 8 px | Badges, tabla compacta |
| `--space-3` | 12 px | Celda, gap de formulario |
| `--space-4` | 16 px | Control, separación de campos |
| `--space-5` | 24 px | Hoja, bloques |
| `--space-6` | 32 px | Secciones |
| `--space-7` | 48 px | Páginas |
| `--space-8` | 64 px | Aire de portada |
| `--space-9` | 96 px | Excepcional |

- **Contenedor:** 80rem máximo; lectura 72rem; formularios 36rem.
- **Gutter:** `clamp(1.25rem, 4vw, 2.5rem)`.
- **Radios:** 2 px hojas, 4 px controles, 999 px badges.
- **Bordes:** 1 px `--color-border` en hojas; 1 px `--color-border-strong` en cabecera y pie de tabla; 1 px `--color-control-border` en controles; 3 px `--color-primary` solo en la hoja principal; 3 px `--color-accent` en el recibo.
- **Elevación:** nivel 0 sin sombra; nivel 1 para menú móvil; nivel 2 para diálogos. Sin sombra en hojas, tablas ni formularios.
- **Contraste forzado:** con `forced-colors: active`, los bordes y el foco siguen siendo visibles sin depender del color.

### 5.5 Catálogo de componentes

| Componente | Clases | Estados |
|---|---|---|
| Botón | `.button`, `.button--primary`, `.button--secondary`, `.button--ghost`, `.button--danger`, `.button--danger-quiet`, `.button--sm`, `.button--block` | default, hover, active, focus-visible, disabled, loading |
| Campo | `.form-field`, `.form-field__label`, `.form-field__control`, `.form-field__help`, `.form-field__errors`, `.form-actions` | default, focus, error, read-only, disabled |
| Badge | `.badge`, `.badge--owner`, `.badge--manager`, `.badge--operator`, `.badge--viewer`, `.badge--active`, `.badge--inactive`, `.badge--success`, `.badge--warning`, `.badge--danger`, `.badge--info`, `.badge--neutral` | estático; siempre con texto |
| Aviso | `.alert`, `.alert--info`, `.alert--success`, `.alert--warning`, `.alert--error`, `.alert__title`, `.alert__body` | info, éxito, advertencia, error |
| Hoja | `.sheet`, `.sheet__header`, `.sheet__title`, `.sheet__body`, `.sheet__footer`, `.sheet--accent`, `.sheet--quiet` | normal, acentuada, silenciosa |
| Contexto | `.context-strip`, `.context-strip__item`, `.context-strip__label`, `.context-strip__value` | `dl` de empresa, rol y sesión; no es un KPI |
| Tabla | `.table-scroll`, `.table`, `.table--audit`, `.table__caption`, `.table__actions`, `.table__num`, `.table__code` | normal, hover, focus-within, vacía |
| Paginación | `.pagination`, `.pagination__list`, `.pagination__link`, `.pagination__current`, `.pagination__meta` | normal, actual, disabled |
| Navegación | `.app-header`, `.app-header__inner`, `.app-header__brand`, `.app-header__context`, `.app-header__nav`, `.app-header__link`, `.app-header__toggle` (P1) | normal, hover, actual, abierta/cerrada (P1) |
| Estado vacío | `.empty-state`, `.empty-state__title`, `.empty-state__text`, `.empty-state__action` | vacío |
| Carga | `[aria-busy="true"]`, `.is-loading` (reservado; sin activador en P0) | cargando |
| Recibo | `.receipt`, `.receipt__label`, `.receipt__code`, `.receipt__note` | secreto temporal, confirmación |
| Error de página | `.error-page`, `.error-page__code`, `.error-page__title`, `.error-page__actions` | 403, 404 |
| Utilidades | `.num`, `.muted`, `.visually-hidden`, `.stack`, `.cluster`, `.grid`, `.grid--2`, `.grid--3` | — |

**Especificaciones clave**

- **Botones:** 44 px mínimo; primario verde; secundario con borde `--color-control-border`; ghost con texto `--color-primary`; peligro para confirmación destructiva; peligro silencioso para «Desactivar» dentro de la fila. Sin flechas decorativas.
- **Campos:** label visible de 13 px/600; control de 44 px; borde `--color-control-border`; foco de anillo doble; error con borde `--color-danger`, mensaje debajo y `aria-invalid`/`aria-describedby`; ayuda de 12 px.
- **Badges:** pill 999 px, 12 px/600, borde 1 px y texto. Dueño `accent-soft`/`accent-ink`; encargado `primary-soft`/`primary`; operador `info-soft`/`info`; consulta `surface-sunken`/`ink-soft`; activa `success-soft`/`success`; inactiva `surface-sunken`/`ink-soft`.
- **Avisos:** borde izquierdo de 3 px, fondo suave, padding 12/16 px, radio 2 px. Info y éxito con `role="status"`; error con `role="alert"`. Sin bloques rojos de fondo completo.
- **Hojas:** superficie, borde 1 px, radio 2 px, sin sombra; cabecera 16/24, cuerpo 24/32, pie 16/24 con borde superior. Hoja acentuada solo para la principal.
- **Contexto:** `dl` en tres columnas con filetes; no `.stat-grid` para datos no numéricos. Etiqueta «Sesión iniciada» en lugar de «Último acceso», porque `last_login` corresponde al acceso actual.
- **Tablas:** se conserva `.table-scroll` enfocable; `caption` y `scope`; `th` 13 px/600 en oración; `td` 14 px; padding 12/16; nombres en `ink`/600; correo y metadatos en `ink-soft`; acciones en una columna a la derecha. **No se ocultan columnas con `display:none`.** En móvil se mantiene el scroll interno.
- **Recibo:** hoja con reglas discontinuas, borde superior ámbar, código en Consolas 16 px, `user-select: all`. **La contraseña temporal debe seguir siendo el primer `<code>` del documento y no duplicarse.**
- **Estados:** vacío con explicación y acción si existe; carga con `aria-busy` y botón deshabilitado; error con resumen `role="alert"` y errores de campo; confirmación con `h1` y recibo; éxito con `role="status"` y texto exacto de la operación.

**Migración de tokens y selectores.** La migración se hace en tres hitos para no dejar reglas apuntando a tokens con semántica nueva:
1. **T-04:** define los tokens nuevos y conserva los alias de compatibilidad (`--color-paper*`, `--rule-hairline`, `--color-accent-deep` y el resto de tokens heredados enumerados en T-04); mantiene `--color-accent` con el valor petróleo anterior hasta que todas las reglas estén migradas.
2. **T-06:** migra las secciones de componentes P0, cambia `--color-accent` a ámbar y elimina los tokens de color retirados de las reglas P0. Al cierre de T-06 la búsqueda de `--color-paper`, `--color-accent-deep` y `--rule-hairline` debe devolver cero usos en reglas P0; el bloque de compatibilidad de la home puede conservar los tokens heredados.
3. **T-09:** elimina los selectores `.panel*` genéricos, los selectores desnudos (`table`, `th, td`, `thead th`, `code`, `caption`, `dl`), el selector CSS `[role="status"]` global y los alias restantes de las reglas P0, una vez migradas las 9 plantillas P0 que los usan (8 de contenido más `base_panel.html`); conserva las definiciones de token que usa el bloque de la home hasta P2. `.panel-context*` de `base_panel.html` pasa a las clases de contexto de la barra; el resto pasa a `.sheet`. Los scripts inline de `user_form.html`, `company_form.html` y `password_change.html` que hoy usan `.panel form` se actualizan a `.sheet form` en la misma tarea que migra cada plantilla; el script de acceso conserva `.login form`. Se excluye el bloque de compatibilidad de la home.

**Compatibilidad de la home (P2).** La home no se rediseña en esta etapa. T-04 crea un bloque acotado con sus reglas actuales, incluidas las responsive (`.home-hero*`, `.home-panels`, `.next-steps*`, los `.panel*` que usa y sus reglas de ancho), y lo conserva hasta P2; `.panel__stage` se fija a `--color-accent-ink` para que la etiqueta de etapa no quede en ámbar (3,77:1). T-09 no elimina ese bloque; T-10 verifica que la home no sufre regresión.

Se eliminan además los selectores desnudos y el selector CSS `[role="status"]` global (el atributo ARIA se conserva). `::selection` usa `primary` con `surface`, no ámbar.

---

## 6. Superficies y comportamiento por pantalla

| Pantalla | Objetivo | Jerarquía y componentes | Copy conservado |
|---|---|---|---|
| Login | Dar contexto y reducir el vacío | Regla verde de 3 px, wordmark, promesa, `h1` «Acceso al panel», formulario de 28rem, error genérico; botón block en móvil | `role="alert"`, `aria-busy`, nombres de campo y CSRF |
| Panel | Mostrar qué se puede hacer hoy | `h1`, `dl` de contexto (empresa, rol, sesión), acción «Gestionar usuarios» si hay capacidad, lista de trabajo con verbos completos, módulos en preparación | Textos actuales del panel y rol visible |
| Usuarios — lista | Leer personas y estados | 5 columnas (Persona, Rol, Estado, Último acceso, Acciones); correo dentro de Persona; badges; acciones agrupadas visibles; `caption`, `scope`, `.table-scroll` | `Activa`, `Inactiva`, `Nunca`, `Página X de Y`, `No hay usuarios registrados en la empresa.` |
| Usuarios — alta | Explicar el resultado y entregar el secreto | Hoja de formulario, ayuda, «Cancelar», recibo de contraseña temporal | `role="status"`, primer `<code>`, `aria-busy`, nombres de campo |
| Usuarios — confirmación | Distinguir éxito de error | `h1` dinámico, aviso de éxito o error, recibo si hay contraseña, «Volver al listado» | `title`, `message`, `temporary_password`, `role` |
| Empresa | Dar importancia al nombre del negocio | Hoja de un campo, ayuda, «Guardar cambios» y «Cancelar» | «Nombre de la empresa actualizado.» y errores |
| Auditoría | Leer como libro de operaciones | Dos secciones, `.table--audit`, fecha `.num`, acción en `code`, valores en chips, paginación | `No hay operaciones auditadas.`, `No hay eventos de seguridad.`, `Personal técnico`, `audit_page`/`security_page` |
| Perfil | Dar identidad a la cuenta | Bloque de identidad con nombre, correo, badge de rol y empresa; «Cambiar contraseña» | `Contraseña actualizada.`, `profile_account`, `profile_membership` |
| Contraseña | Hacer visible el estado temporal | Aviso `.alert--warning` si `must_change_password`, campos, ayuda y acciones | Validadores, `aria-invalid`/`aria-describedby`, `aria-busy` |
| 403/404 | Explicar y ofrecer salida | `.error-page` con código grande, `h1`, explicación y acción; shell actual en P0 | `reason == "context"`, cierre de sesión con CSRF, «Volver al panel», «Iniciar sesión» |
| Admin | Convivencia discreta | Sin `main.css` ni cambios en Unfold; «Acceso técnico» discreto en el shell público | `href="/admin/"` |
| Home pública | P2 | Copy de producto y acceso al panel | `href="/admin/"`, «Pendiente de especificación» y «Etapa 003 — Cuentas y multiempresa» hasta aprobación |

**Copy verificado que se conserva en P0:** «No hay operaciones auditadas.», «No hay eventos de seguridad.», «Nombre de la empresa actualizado.», «Personal técnico», «No hay usuarios registrados en la empresa.», «El correo ya está registrado.», «Rol actualizado», «No se pudo cambiar el rol», «dueño activo», «ya está activa», «ya está inactiva», «comando técnico», «Contraseña actualizada.», «Cerrar sesión», «Volver al panel», «Iniciar sesión», «Nunca», «Activa», «Inactiva», «Página X de Y», «Pendiente de especificación», «Etapa 003 — Cuentas y multiempresa», el formato de fecha `dd/mm/yyyy hh:mm`, `href="/admin/"`, el `aria-label` de la paginación de usuarios y la ausencia del bloque de paginación en el estado vacío. Se conserva además el copy existente de las plantillas aunque no esté verificado por pruebas (por ejemplo, «Cuenta del dueño»).

---

## 7. Requisitos funcionales (EARS)

| ID | Enunciado | R | Estado |
|---|---|---|---|
| RF-01 | El sistema DEBE aplicar el sistema visual de §5 —tokens, tipografía, espaciado y componentes— a las plantillas P0, sin frameworks, fuentes externas ni recursos remotos. | R-01, R-02, R-03, R-08, R-11 | [P0] |
| RF-02 | CUANDO se renderiza cualquier pantalla del panel, el sistema DEBE mostrar el shell con una única barra superior verde, contexto de empresa y rol, navegación filtrada por capacidad y `aria-current` en el enlace activo. | R-01, R-02, R-07 | [P0] |
| RF-03 | El acceso P0 DEBE presentarse en una columna dentro del shell actual, con regla verde de 3 px, wordmark, promesa breve, un único `h1` y un único formulario; y DEBE conservar `role="alert"`, `aria-busy`, CSRF y los nombres `username` y `password`. | R-04, R-12 | [P0] |
| RF-04 | CUANDO el usuario abre el panel, el sistema DEBE mostrar un `h1`, un `dl` con empresa, rol y sesión iniciada, una acción primaria solo si tiene capacidad y una lista de trabajo con verbos completos, sin consultas nuevas. | R-10 | [P0] |
| RF-05 | CUANDO el dueño lista usuarios, el sistema DEBE mostrar las columnas Persona, Rol, Estado, Último acceso y Acciones, con nombre y correo en Persona, badges de rol y estado, `caption`, `scope` y scroll interno accesible. | R-07, R-12 | [P0] |
| RF-06 | CUANDO se crea un usuario, el sistema DEBE mostrar la contraseña temporal una sola vez dentro de un recibo identificado, que DEBE ser el primer `<code>` del documento y no duplicar el valor. | R-09, R-12 | [P0] |
| RF-07 | CUANDO se confirma una operación de usuario, el sistema DEBE distinguir éxito y error con un aviso y, si corresponde, un recibo, conservando `title`, `message`, `temporary_password` y `role`. | R-09 | [P0] |
| RF-08 | CUANDO el dueño edita la empresa, el sistema DEBE mostrar una hoja de un campo con ayuda, «Guardar cambios» y «Cancelar», y conservar el mensaje «Nombre de la empresa actualizado.» y los errores de validación. | R-12 | [P0] |
| RF-09 | CUANDO se consulta auditoría, el sistema DEBE mostrar dos secciones con tablas `.table--audit`, fechas con cifras tabulares, acciones en `code`, valores en chips y paginación, conservando los estados vacíos y los parámetros `audit_page` y `security_page`. | R-07 | [P0] |
| RF-10 | CUANDO se consulta el perfil, el sistema DEBE mostrar identidad con nombre, correo, badge de rol y empresa, y la acción «Cambiar contraseña», conservando «Contraseña actualizada.». | R-12 | [P0] |
| RF-11 | CUANDO se cambia la contraseña, el sistema DEBE mostrar un aviso de advertencia si la contraseña es temporal, campos con ayuda y errores asociados, y `aria-busy` al enviar. | R-04, R-12 | [P0] |
| RF-12 | CUANDO se produce un 403 o un 404, el sistema DEBE mostrar `.error-page` con código, `h1`, explicación y acción de recuperación, conservando la variante de contexto con cierre de sesión y CSRF y el shell actual. | R-12 | [P0] |
| RF-13 | El sistema DEBE ofrecer estados donde correspondan: error y carga en login; vacío, error, éxito y confirmación en usuarios, empresa y auditoría; error en 403/404. Cada estado incluye explicación y acción cuando exista. | R-04, R-07, R-10 | [P0] |
| RF-14 | El sistema NO DEBE implementar en esta etapa el menú móvil con JavaScript, la gestión por fila con `<details>`, el login de dos columnas ni la home pública; esos alcances quedan en P1/P2 y requieren autorización propia. | R-05, R-06 | [P1/P2] |

---

## 8. Requisitos no funcionales

| ID | Requisito | Verificación | Estado |
|---|---|---|---|
| RNF-01 | Accesibilidad verificable: teclado completo y foco lógico; foco visible; etiquetas programáticas; errores asociados; contraste de texto ≥ 4,5:1 y de componentes ≥ 3:1; color no exclusivo; estados anunciados; objetivos táctiles ≥ 44 px en acciones principales y ≥ 40 px en filas; tablas con `caption` y `scope`; zoom 200 %; `lang="es"`; un `h1` por página; `forced-colors` con bordes y foco visibles. | R-02, R-03, R-04, R-07, R-11 | [P0] |
| RNF-02 | Responsive sin scroll horizontal de página en 320, 375, 768, 1440 y 1920 px; el único scroll horizontal permitido es el interno de `.table-scroll`, con contenedor enfocable. | R-01, R-11 | [P0] |
| RNF-03 | Con `prefers-reduced-motion`, no hay animaciones ni transiciones no esenciales. | R-08 | [P0] |
| RNF-04 | Sin dependencias nuevas, fuentes externas, `@import` remoto ni recursos de red; el CSS y los activos son locales. | R-03, R-12 | [P0] |
| RNF-05 | Mantenibilidad: CSS organizado por secciones, tokens con rol, sin selectores desnudos que afecten componentes no previstos, sin duplicación innecesaria y sin lógica de presentación en Python. | R-12 | [P0] |
| RNF-06 | Compatibilidad: `base.html` sin `request.*`, `perms` ni `messages`; `base_panel.html` no extiende `base.html`; Django Admin no carga `main.css`; la suite existente sigue en verde. | R-12 | [P0] |
| RNF-07 | Rendimiento: sin JavaScript nuevo en P0, sin consultas adicionales y sin recursos de red, fuentes externas ni JS externo. | R-01 | [P0] |
| RNF-08 | Seguridad: la contraseña temporal se muestra una sola vez y no se registra en logs ni auditoría; no se introducen secretos en plantillas, CSS o comentarios. | R-09 | [P0] |
| RNF-09 | Terminología uniforme en español y mensajes accionables; no se introduce nuevo lenguaje interno de proyecto ni se modifica el copy verificado en P0. | R-10, R-12 | [P0] |
| RNF-10 | Evidencia y trazabilidad: cada tarea registra verificación funcional y visual; los criterios R se mapean a RF, RNF y a la Etapa 003. | R-12 | [P0] |

---

## 9. Criterios de aceptación

Se conservan literalmente los criterios aprobados. R-05 y R-06 corresponden a P1 y no se implementan en esta etapa.

| ID | Criterio | Estado |
|---|---|---|
| R-01 | En 320/375/768/1440/1920 px, el documento no presenta scroll horizontal de página. | [P0] |
| R-02 | Todo control interactivo muestra foco visible con contraste ≥3:1 respecto del fondo adyacente. | [P0] |
| R-03 | Todo texto tiene contraste ≥4,5:1; los componentes no textuales, ≥3:1. | [P0] |
| R-04 | Todo error de validación asocia `aria-invalid="true"` y `aria-describedby` al mensaje, con resumen `role="alert"`. | [P0] |
| R-05 | El menú móvil expone `aria-expanded`/`aria-controls`; Escape cierra y devuelve el foco. | [P1] |
| R-06 | La gestión de fila se anuncia, se cierra con Escape y devuelve el foco al botón que la abrió. | [P1] |
| R-07 | Las tablas conservan `caption`, `scope` y contenedor enfocable con `aria-label` si hay desplazamiento. | [P0] |
| R-08 | Con `prefers-reduced-motion`, no hay animaciones ni transiciones no esenciales. | [P0] |
| R-09 | La contraseña temporal se muestra una sola vez, en un bloque identificado, y no se registra en logs ni auditoría. | [P0] |
| R-10 | Todo estado vacío incluye explicación y acción cuando existe. | [P0] |
| R-11 | Con zoom 200 %, el contenido sigue legible y no se superpone ni requiere scroll horizontal de página. | [P0] |
| R-12 | La suite existente pasa; si se cambia copy verificado, se actualiza la prueba en la misma tarea con aprobación y trazabilidad. | [P0] |

---

## 10. Reglas de implementación

1. **P0 sin JavaScript nuevo.** No se agrega JavaScript. Se conservan los scripts inline existentes de `login.html`, `user_form.html`, `company_form.html` y `password_change.html` para cumplir `aria-busy`; no se extraen a `static/js/`.
2. **Copy verificado.** Se conserva la lista de §6. Cualquier cambio requiere aprobación explícita, actualización de la prueba afectada en la misma tarea y registro en `tasks.md`.
3. **Backend intacto.** No se modifican `apps/**`, `config/**`, migraciones, vistas, formularios, servicios, URLs, middleware, autenticación, permisos ni settings.
4. **Pruebas.** No se modifican pruebas en P0. La única lista admisible de cambios futuros es la aprobada en G-1 y debe constar en la tarea.
5. **`base_panel.html` no extiende `base.html`.** `panel.html` extiende `base_panel.html`; no se crea un shell compartido que rompa la prueba.
6. **Primer `<code>`.** El recibo envuelve el mismo `<code>` de la contraseña temporal, sin duplicarlo en `aria-label`, `title`, badges ni un segundo `<code>`.
7. **Formato de fecha.** Se conserva `d/m/Y H:i` (`dd/mm/yyyy hh:mm`) en usuarios y auditoría.
8. **`aria-busy` inline.** Se mantiene el atributo y el selector `.login form` en el script de acceso; los scripts de alta, empresa y contraseña se actualizan a `.sheet form` al migrar su plantilla.
9. **Columnas.** No se usa `display:none` para ocultar columnas; la tabla conserva 5–6 columnas con scroll interno.
10. **Foco doble.** Todo control enfocable usa anillo de 2 px `surface` + 3 px `focus`; el outline nunca se elimina.
11. **Nombre de empresa.** Se trunca con `max-width` + `text-overflow: ellipsis` en barra, `h1` y contexto, y se valida con un nombre de 150 caracteres.
12. **Pruebas.** R-12 no habilita por sí solo cambios de prueba: cualquier actualización requiere ampliación aprobada de G-1 y registro en la tarea.
13. **Home P2.** No se rediseña; se conserva su bloque de compatibilidad y se verifica que no sufre regresión. Cualquier cambio visual de la home requiere ampliación aprobada.

---

## 11. Trazabilidad

### 11.1 Decisiones → requisitos

| Decisión | RF | RNF | R |
|---|---|---|---|
| D-01 | RF-01, RF-03 | RNF-01, RNF-04 | R-02, R-03 |
| D-02 | RF-03, RF-05, RF-14 | RNF-01, RNF-07 | R-01, R-04, R-07 |
| D-03 | RF-14 | RNF-01 | R-05, R-06 |
| D-04 | RF-03 a RF-12 | RNF-06, RNF-09 | R-12 |
| D-05 | — | RNF-10 | — |
| D-06 | RF-02, RF-03 | RNF-04 | R-03 |

### 11.2 Criterios → requisitos → Etapa 003

| R | RF | RNF | Referencia 003 |
|---|---|---|---|
| R-01 | RF-01, RF-02 | RNF-02, RNF-07 | 003-RNF-07, 003-CA-42 |
| R-02 | RF-01, RF-02 | RNF-01 | 003-RNF-07, 003-CA-42 |
| R-03 | RF-01 | RNF-01 | 003-RNF-07, 003-CA-42 |
| R-04 | RF-03, RF-11, RF-13 | RNF-01 | 003-RNF-07, 003-CA-42 |
| R-05 | RF-14 | RNF-01 | 003-RNF-07, 003-CA-42 (P1) |
| R-06 | RF-14 | RNF-01 | 003-RNF-07, 003-CA-42 (P1) |
| R-07 | RF-02, RF-05, RF-09 | RNF-01 | 003-RNF-07, 003-CA-42; 003-RF-23 y 003-CA-23 |
| R-08 | RF-01 | RNF-03 | 003-RNF-07, 003-CA-42 |
| R-09 | RF-06, RF-07 | RNF-08 | 003-RF-21, 003-RF-27, 003-CA-21, 003-CA-27; 003-RNF-03 |
| R-10 | RF-04, RF-13 | RNF-09 | 003-RNF-08, 003-CA-43; 003-RNF-10 |
| R-11 | RF-01 | RNF-02, RNF-01 | 003-RNF-07, 003-CA-42 |
| R-12 | RF-03 a RF-12 | RNF-06, RNF-09 | 003-RNF-09, 003-CA-44 |

Los identificadores con prefijo `003-` pertenecen a `specs/003-cuentas-multiempresa/spec.md`; los de esta especificación no llevan prefijo.

**RF-23 de la Etapa 003.** El listado de usuarios debe mostrar correo, nombre, rol, estado y último acceso. La columna «Persona» conserva nombre y correo; las columnas Rol, Estado y Último acceso se mantienen. La agrupación no elimina ningún dato exigido por RF-23 ni por CA-23.

---

## 12. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Ámbar como texto | 3,77:1; no cumple texto normal | Usar `accent-ink` (5,90:1); ámbar solo en bordes, muescas y sellos |
| Foco sobre verde | 1,56:1 | Anillo doble: 2 px `surface` + 3 px `focus` |
| Bordes de control | Un borde claro no alcanza 3:1 | `control-border` 3,77:1 sobre cal y 4,10:1 sobre hoja |
| Tablas responsivas | Ocultar celdas rompe la asociación de encabezados | No usar `display:none`; conservar 5–6 columnas y `.table-scroll` enfocable |
| `hidden` del menú (P1) | `[hidden]` pierde frente a `display:flex` | `[hidden] { display:none !important }` o `.is-hidden`; aplicarlo con JS |
| `[role="status"]` global | Colisiona con `.alert` y `.receipt` | Eliminar el selector global y usar clases de aviso |
| Migración de tokens | `--color-accent` cambia de semántica | Reescribir por hitos con alias; buscar tokens retirados y revisar `::selection`, `.skip-link` y filetes |
| Copy acoplado | Cambiar textos rompe la suite | Conservar la lista de §6; cambios solo con aprobación y actualización de pruebas |
| Copy del pie de página | La prueba exige «Etapa 003 — Cuentas y multiempresa» en login, panel, home, 403 y 404 | Conservarlo en P0; el copy de producto es P2 y requiere prueba actualizada |
| `aria-busy` literal | `test_accounts_auth` lee `login.html` | Mantener el JS inline en P0 o actualizar la prueba con aprobación |
| Primer `<code>` | Es la contraseña temporal y se verifica una sola vez | El recibo envuelve el mismo `<code>`, sin duplicarlo |
| `base_panel` | La prueba prohíbe que extienda `base.html` | No crear un shell compartido; errores con el shell actual en P0 |
| Nombre de empresa de 150 caracteres | Barra, `h1` y contexto pueden desbordar | `max-width` + `text-overflow: ellipsis`; prueba con nombre largo |
| Zoom 200 % | Header rígido y alturas fijas | `rem`, `min-height`, wrap controlado; sin header sticky en P0 |
| Admin/Unfold | Cambios globales pueden afectarlo | `main.css` no se carga en Admin; no tocar plantillas de Unfold |
| Tipografía en Linux | Candara y Segoe UI no existen | Declarar la limitación; la jerarquía se sostiene por tamaño y peso |
| Evidencia visual de T-23 | Ratios, capturas y orden de tabulación cambian | Re-medir y re-capturar en T-10; la evidencia anterior queda reemplazada |
| CSS global afecta la home P2 | La home usa `.home-*` y `.panel*`; una reescritura global puede dejarla sin estilos o con ámbar como texto | Bloque de compatibilidad explícito hasta P2, `.panel__stage` en `accent-ink` y verificación de no regresión en T-10 |

---

## 13. Ambigüedades y decisiones pendientes

| ID | Ambigüedad | Estado | Impacto |
|---|---|---|---|
| A-01 | Alcance exacto de P1 y su autorización | Aprobado como fase posterior (`D-03`); requiere especificación o ampliación y G-1 propios | RF-14, R-05, R-06 |
| A-02 | Copy de producto de la home pública | Diferido a P2; se conserva `href="/admin/"`, «Pendiente de especificación» y la etiqueta de etapa | RF-14, R-12 |
| A-03 | Tipografía en Linux sin Candara ni Segoe UI | Limitación declarada y aceptada; no se declara equivalencia | RNF-01, R-03 |
| A-04 | Autorización de implementación | G-1 aprobado el 2026-11-12 para T-04 a T-09; T-10 y T-11 no autorizadas | T-04 a T-09 |
| A-05 | Copy del pie de página | Resuelto para P0 por `D-04`: se conserva la etiqueta de etapa; el copy de producto requiere aprobación y actualización de prueba | R-12, RNF-09 |

**Bloqueantes para aprobar la especificación:** ninguno. **Bloqueantes para T-04 a T-09:** ninguno (G-1 aprobado). **T-10 y T-11:** requieren autorización de implementación.

---

## 14. Registro de cambios

| Versión | Cambio |
|---|---|
| v0.1 (2026-11-12) | Creación del borrador a partir de la propuesta «Mostrador» aprobada el 2026-11-12 y de su propuesta final corregida. Se incorporan las seis decisiones aprobadas, el sistema visual completo, las superficies P0, 14 RF, 10 RNF, los 12 criterios aprobados, las reglas de implementación, la trazabilidad con la Etapa 003, los 18 riesgos —los 16 de la propuesta final más el copy del pie y la compatibilidad de la home— y cinco ambigüedades. No se implementó CSS ni se modificó ninguna plantilla, prueba o documento existente. |

---

## 15. Estado de la especificación

- **Estado:** APROBADO v0.1 en G-0a por el usuario el 2026-11-12. La existencia de este documento no sustituye la aprobación de implementación.
- **G-0a:** APROBADO por el usuario el 2026-11-12 para `spec.md`. **G-0b:** APROBADO por el usuario el 2026-11-12 para `plan.md` y `tasks.md`.
- **G-1:** APROBADO por el usuario el 2026-11-12 para T-04 a T-09; T-10 y T-11 no autorizadas.
- **Etapa 003:** cerrada y publicada en `6893e59`; no se modifica.
- **Implementación:** T-04 a T-07 publicadas; RC-8 APROBADO; T-08 y T-09 autorizadas y no iniciadas; T-10 y T-11 no autorizadas; la validación visual completa queda para T-10 (T-05 y T-07 aportaron capturas parciales).
