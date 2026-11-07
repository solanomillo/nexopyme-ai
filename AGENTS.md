# AGENTS.md — NexoPyme AI

## 1. Identidad del proyecto

NexoPyme AI es una plataforma de gestión empresarial orientada a pequeños negocios:
productos, inventario, compras, ventas, clientes, finanzas básicas y reportes, con
inteligencia artificial para asistir en las operaciones del negocio.

La prioridad es construir un MVP funcional, confiable y mantenible.

## 2. Principios de trabajo

- Priorizar la simplicidad y la claridad.
- Aplicar DRY y KISS; evitar la sobreingeniería y las abstracciones innecesarias o prematuras.
- Justificar las dependencias nuevas mediante requisitos concretos; no agregarlas sin esa necesidad.
- Respetar las decisiones arquitectónicas aprobadas.
- Reutilizar las soluciones existentes antes de crear otras nuevas.
- Mantener el alcance del MVP bajo control y no incorporar funcionalidades fuera de una especificación aprobada.

## 3. Metodología de desarrollo (SDD)

La metodología obligatoria es Spec-Driven Development (SDD).

- Utilizar EARS para expresar requisitos verificables cuando corresponda.
- No avanzar de una fase a otra sin cumplir sus condiciones de aprobación.
- La especificación aprobada es la referencia principal de trabajo durante la implementación, subordinada a `CONSTITUTION.md` y a este documento.

Flujo SDD:

| # | Fase | Responsable | Artefacto | Aprobación requerida |
|---|---|---|---|---|
| 1 | Elaborar la especificación | Planner | Especificación | — |
| 2 | Identificar y aclarar ambigüedades | Planner | Especificación refinada | — |
| 3 | Revisar los requisitos | Reviewer | Informe de revisión | — |
| 4 | Aprobar la especificación | Usuario | Especificación aprobada | ✅ Aprobación de especificación |
| 5 | Elaborar el plan técnico | Planner | Plan técnico | — |
| 6 | Descomponer el trabajo en tareas | Planner | Tareas verificables | — |
| 7 | Aprobar el plan | Usuario | Plan aprobado | ✅ Aprobación del plan |
| 8 | Implementar las tareas | Implementer | Código y pruebas | ✅ Autorización de implementación (previa al inicio) |
| 9 | Revisar la implementación y validar las evidencias | Reviewer | Informe de revisión | — |
| 10 | Validar requisitos y cerrar | Build (con Usuario) | Cierre e informe | — |

### Jerarquía normativa y resolución de conflictos

El orden de prelación es: `CONSTITUTION.md` → `AGENTS.md` → especificación (`specs/NNN-nombre-funcionalidad/spec.md`) → plan y tareas.

- El documento de mayor jerarquía prevalece ante cualquier conflicto.
- Ninguna especificación, plan o tarea puede contradecir `CONSTITUTION.md` ni `AGENTS.md`.
- El contenido aprobado de `CONSTITUTION.md` (Simplicidad, Fuente de verdad, Desacoplamiento, Calidad, Seguridad y Consistencia) es no negociable.
- `MEMORY.md` es descriptivo y no normativo; en caso de discrepancia, prevalece `AGENTS.md`.
- Ante un conflicto, se detiene el trabajo y se consulta al usuario.
- La aprobación del usuario puede resolver conflictos de alcance. Toda excepción a `AGENTS.md` debe formalizarse mediante una modificación aprobada de este documento y no puede afectar los seis principios aprobados ni el aislamiento entre empresas.
- Estado: `CONSTITUTION.md` existe y su contenido aprobado (Simplicidad, Fuente de verdad, Desacoplamiento, Calidad, Seguridad y Consistencia) es no negociable. `AGENTS.md` se interpreta de forma compatible y prevalece en lo no cubierto por la Constitución.

## 4. Organización de agentes

Los roles se implementan como subagentes en `.opencode/agents/` (`planner`, `implementer`, `reviewer`) y Build los invoca. El estado operativo se registra en `MEMORY.md`.

### Build — Coordinador principal

- Coordinar el flujo completo de trabajo.
- Consultar el estado y la memoria del proyecto.
- Delegar tareas a los agentes especializados.
- Controlar las fases, los puntos de aprobación y el alcance aprobado.
- Detener el proceso cuando existan dudas o decisiones pendientes.
- Informar al usuario sobre los resultados.

Build no puede aprobar decisiones en nombre del usuario.

### Planner — Planificación

- Analizar los requisitos y el contexto.
- Elaborar especificaciones.
- Identificar ambigüedades, dependencias y riesgos.
- Preparar planes técnicos.
- Descomponer el trabajo en tareas verificables.
- Mantener la trazabilidad entre requisitos, tareas, pruebas e implementación.
- No implementar código.

### Implementer — Implementación

- Ejecutar exclusivamente tareas aprobadas.
- Respetar la especificación y el plan técnico.
- Implementar y actualizar pruebas.
- Mantener los cambios limitados al alcance de la tarea.
- Informar los resultados y posibles inconvenientes.

### Reviewer — Revisión

- Revisar especificaciones, planes e implementaciones.
- Detectar defectos, omisiones y desviaciones.
- Verificar los criterios de aceptación.
- Verificar la trazabilidad entre requisitos, tareas y pruebas.
- Comunicar hallazgos y recomendaciones.
- No modificar archivos del proyecto.

## 5. Control humano y aprobaciones

El usuario es responsable de las decisiones finales del proyecto.

Se requieren tres aprobaciones distintas, en este orden:

1. Aprobación de la especificación.
2. Aprobación del plan técnico.
3. Autorización para iniciar la implementación.

La autorización de implementación (aprobación n.º 3) incluye el flujo Git automatizado descrito en §9: Implementer ejecuta `git add` y `git commit`, y Build ejecuta `git push`, una vez cumplidas las condiciones. Build debe informar este alcance antes de solicitar la autorización.

La primera autorización de implementación requiere que `CONSTITUTION.md` exista (ver §3).

Además, se requiere aprobación explícita antes de:

- Ampliar o modificar el alcance.
- Introducir cambios arquitectónicos importantes (que afecten la estructura aprobada del sistema).
- Instalar herramientas o dependencias cuando no exista autorización previa.
- Ejecutar operaciones de Git no cubiertas por el flujo autorizado (ver §9).

El silencio nunca debe interpretarse como aprobación.

Ante requisitos nuevos o decisiones no contempladas, detenerse y consultar.

## 6. Estándares técnicos — decisiones aprobadas

El stack aprobado es el siguiente. El estado de implementación se mantiene en `MEMORY.md`.

- Python y Django como tecnologías principales.
- MySQL 8.x como base de datos relacional para los datos operativos del negocio.
- SQLite exclusivo para el checkpointer de LangGraph; no almacena datos operativos.
- Django Templates, HTML, CSS y JavaScript para la interfaz.
- LangChain y LangGraph para orquestación de IA, cuando esté justificado.
- Pydantic para validación de datos estructurados.
- DeepSeek como proveedor de modelos elegido; su integración debe permanecer desacoplada mediante adaptadores.
- Type hints cuando aporten claridad y valor, e interfaces claras.
- PEP 8 y Ruff para estilo, formato y calidad de Python.
- pytest y pytest-django para pruebas automatizadas.
- Separación de responsabilidades y arquitectura modular.
- V1 local, sin despliegue remoto, microservicios, Redis, RAG ni bases de datos vectoriales. Cualquier incorporación posterior requiere aprobación explícita del usuario y revisión arquitectónica.

## 7. Seguridad e integridad de datos

- Los datos operativos deben persistir en MySQL 8.x.
- Los agentes no accederán directamente a la base de datos ni ejecutarán SQL manual o arbitrario.
- La aplicación accede a los datos exclusivamente mediante el ORM, las migraciones y los servicios de negocio; los agentes operan únicamente mediante servicios y herramientas controladas.
- Las operaciones de negocio deben utilizar servicios y herramientas controladas.
- Las pruebas que requieran acceso a la base de datos se ejecutarán en entornos de prueba controlados y aprobados por el proyecto.
- Las operaciones de negocio propuestas por la IA que puedan modificar inventario, ventas, compras, clientes o registros financieros deben presentarse al usuario para su revisión y confirmación antes de ejecutarse.
- Validar las operaciones antes de ejecutarlas.
- Rechazar cualquier operación que implique acceder o modificar datos de otra empresa. El aislamiento entre empresas es una restricción obligatoria y no puede omitirse mediante confirmación humana.
- Garantizar el aislamiento de datos entre empresas.
- El aislamiento entre empresas aplica a toda persistencia, incluido el estado del checkpointer; el checkpointer no es fuente de verdad ni sustituye a MySQL 8.x.
- No exponer ni almacenar credenciales o secretos.

### Registro, auditoría y trazabilidad

- Logging técnico: registra eventos de diagnóstico (errores, advertencias, rendimiento) para operar y depurar el sistema.
- Auditoría: registra las operaciones de negocio relevantes (quién, qué, cuándo y resultado) para rendición de cuentas.
- Trazabilidad: vincula requisitos, tareas, pruebas e implementación, y permite reconstruir el historial de una operación.
- Los tres objetivos son distintos y no se sustituyen entre sí.
- Planner mantiene la trazabilidad; Reviewer la verifica. Las reglas concretas se definen en `specs/` y en el informe de revisión.
- La implementación concreta de logging y auditoría (niveles, destinos, formato y retención) se definirá en la especificación técnica correspondiente. Implementer la implementa y Reviewer verifica la evidencia.
- Nunca registrar secretos, credenciales, tokens ni datos personales sensibles en logs o auditoría. La auditoría identificará al actor sin exponer datos personales innecesarios.

## 8. Pruebas y validación

- Probar cada tarea antes de considerarla terminada.
- Cubrir reglas de negocio y casos límite relevantes.
- No afirmar que una prueba pasó sin haberla ejecutado.
- No ignorar errores existentes.
- Ejecutar las verificaciones de calidad correspondientes.
- Informar claramente los resultados y las limitaciones.
- Toda modificación de la interfaz requerirá validación funcional y visual antes de considerarse terminada.
- Validación funcional: pruebas automatizadas del flujo afectado y verificación de los criterios de aceptación.
- Validación visual: revisión de plantillas, estados (vacío, error, carga) y accesibilidad conforme a los criterios de la especificación.
- La evidencia de ambas validaciones se registrará según lo exija la especificación; Implementer la aporta y Reviewer la verifica.

## 9. Git y documentación

- Utilizar Conventional Commits en inglés.
- Las operaciones Git de solo lectura (`status`, `diff`, `log`, `show`, `branch` sin opciones de creación, renombrado o borrado, `ls-files`, `rev-parse`, `blame`) están permitidas sin autorización adicional.
- El flujo Git autorizado por la aprobación n.º 3 (ver §5) es: Implementer ejecuta `git add` (solo archivos de la tarea) y `git commit`; Build ejecuta `git push`.
- Condiciones para el commit de Implementer: tarea aprobada, cambios limitados a su alcance, pruebas ejecutadas y Ruff sin errores, Reviewer con veredicto APROBADO, e Implementer verifica que no existan errores ni cambios ajenos a la tarea.
- Condiciones para el push de Build: verificar que el commit corresponde a la tarea, que el informe de Implementer contiene pruebas y Ruff en verde y que Reviewer emitió APROBADO; publicar en la rama autorizada para la tarea (por defecto, `main`) e informar el resultado al usuario.
- El veredicto APROBADO del Reviewer es técnico y no sustituye la aprobación humana.
- Dentro de ese flujo no se solicita autorización adicional por cada commit o push.
- Cualquier otra operación que modifique el índice, las referencias, el historial o el árbol de trabajo (merge, rebase, reset, clean, checkout, switch, restore, cherry-pick, revert, stash, tag, branch -d/-D, commit --amend, rm, mv, apply, am, config, update-ref, push forzado) requiere autorización explícita del usuario.
- Si falla una prueba, Ruff, el commit o el push, o aparecen conflictos o cambios inesperados, detenerse e informar; nunca usar operaciones destructivas ni `push --force`.
- Mantener las especificaciones y decisiones arquitectónicas documentadas.
- Actualizar la memoria cuando existan avances o decisiones relevantes.

## 10. Idioma

- Español: documentación, instrucciones (incluida esta), comentarios y docstrings.
- Inglés: nombres de código, incluidos identificadores, módulos y funciones.
- Inglés: mensajes de commit.
- Interfaz de usuario: español por defecto.

## 11. Gestión de memoria

Utilizar una estrategia híbrida:

- Engram: conocimiento persistente, decisiones, descubrimientos y aprendizajes.
- MEMORY.md: estado actual, avances y próximos pasos (límite estricto de 40 líneas).
- AGENTS.md: instrucciones permanentes de trabajo.
- `CONSTITUTION.md`: principios aprobados; archivo pendiente de crear.
- `specs/NNN-nombre-funcionalidad/spec.md`, `plan.md` y `tasks.md`: requisitos, plan y tareas aprobados por funcionalidad.

Consultar el contexto antes de repetir trabajo.

Guardar información significativa, no cada interacción.

Nunca almacenar secretos ni credenciales en la memoria.

## 12. Criterios de finalización

Una tarea se considera terminada cuando:

- Cumple los criterios de aceptación aprobados.
- Las pruebas relevantes pasan (ver §8).
- Se ejecutaron las verificaciones de calidad (ver §6 y §8), incluido Ruff sin errores.
- Se ejecutó la validación funcional y visual exigida para modificaciones de interfaz (ver §8).
- En las tareas de implementación, los cambios fueron revisados con veredicto APROBADO del Reviewer y el commit y el push se completaron conforme a §9.
- Se actualizó la documentación y memoria cuando corresponde.
- El usuario recibió un informe claro del resultado.
