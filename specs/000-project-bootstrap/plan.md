# Plan técnico 000 — Bootstrap inicial del proyecto

## Estado y autoridad

**ESPECIFICACIÓN v1.4, PLAN Y TAREAS APROBADOS; AUTORIZACIÓN DE IMPLEMENTACIÓN CONCEDIDA.** La aprobación de la especificación, plan y tareas y la autorización de implementación constan en declaraciones explícitas del usuario; Reviewer emitió APROBADO para plan y tareas. La v1.4 enmienda exclusivamente el criterio de plataformas, autorizada explícitamente por el usuario el 2026-11-07. T-01–T-03 tienen evidencia histórica y dictamen Reviewer APROBADO. T-04 está INICIADA: la verificación en Windows 10 y la consolidación del manifiesto único se ejecutaron bajo autorización explícita; Reviewer emitió APROBADO. T-05–T-13 no iniciadas.

## Objetivo, alcance y estrategia

Preparar entorno local reproducible con Python 3.14.10, `.venv`, Django y MySQL 8.x exclusivamente operativo, configuración segura por entorno, verificaciones, migraciones iniciales, pruebas/calidad, `GET /health/` y documentación de evidencia. No incluye negocio, llamadas IA, checkpointer, despliegue ni SQLite operativo. Se mantiene estrictamente el alcance de `spec.md` v1.4 y `AGENTS.md`.

La secuencia de 13 tareas y trazabilidad detallada está en `tasks.md`. La estrategia de manifiesto es un solo `requirements.txt` con dependencias directas base+IA: Django, mysqlclient, pytest, pytest-django, Ruff, Pydantic, LangChain, LangGraph y `langchain-deepseek`. No se mantiene `requirements-ai.txt`, grupos separados ni locks. No se fijan versiones por conjetura: las del manifiesto son las verificadas en el entorno temporal. T-04 documenta metadatos/restricciones directas y transitivas y la resolución conjunta para Python 3.14.10; no exige una matriz cerrada de sistemas operativos ni prueba independiente Windows 10/11. Se documenta el entorno funcional efectivamente probado y no se afirma compatibilidad universal.

## Decisiones técnicas concretadas

- **Plataforma e intérprete:** Python objetivo 3.14.10. No se define una lista cerrada de sistemas operativos soportados ni se exige probar Windows 10 y Windows 11 separadamente. Se identifican con precisión las plataformas efectivamente verificadas; en esta ejecución, instalación e integración funcional se probaron en Windows 10 x64 con CPython 3.14.10. No inferir soporte de Windows 11 ni compatibilidad universal.
- **Dependencias:** T-04 documenta fuentes, `Requires-Python`, `Requires-Dist`, marcadores relevantes, cierre transitivo seleccionado y resolución conjunta del conjunto directo para Python 3.14.10 en el entorno temporal descrito. La inclusión condicional de `langchain-deepseek` forma parte de la decisión aprobada en v1.4; no se sustituye por SDK/paquete alternativo unilateralmente. La compatibilidad declarada, resolución y ejecución funcional son tipos de evidencia distintos y se reportan por separado.
- **Instalación T-05:** tras gates de aprobación humana del plan/tareas y autorización explícita previa de implementación de `AGENTS.md` §5, ejecutar en `.venv` `python -m pip install -r requirements.txt` una sola vez; al ser manifiesto único, el conjunto instalado es base+IA. Antes debe terminar satisfactoriamente T-04, con plugin incluido y compatibilidad demostrada. Si T-04 se bloquea, T-05 no empieza y no se instala un subconjunto mediante `-r` con exclusiones, ni se omite/reemplaza el plugin. Registrar versiones instaladas y ejecutar `python -m pip check`. La mera aprobación de este plan no habilita la instalación.
- **Artefactos anteriores:** T-04 identificó `requirements-ai.txt`, `requirements-win-py314.lock.txt` y `requirements-ai-win-py314.lock.txt`. Con autorización explícita del usuario (2026-11-07), se verificó que sus versiones y metadata estaban documentadas en `tasks.md` y se retiraron; `requirements.txt` quedó como manifiesto único consolidado. Los hashes de los locks no se trasladaron porque la estrategia aprobada excluye locks. No hay estrategia de lock en el plan.
- **Entorno Django:** variables `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`. No se agrega cargador `.env` ni dependencia nueva sin necesidad aprobada: la aplicación consume variables del proceso. `.env.example` solo contiene nombres y placeholders no utilizables; `.env` será vacío/plantilla local sin credenciales inventadas y estará excluido de Git. Los valores reales solo se completan mediante provisión segura autorizada; no se escriben en documentación, salida o logs. `python manage.py check` se ejecuta separadamente de DB.
- **MySQL y control de acceso:** T-01 contiene autorización histórica de destino `127.0.0.1:3306/nexopyme_bootstrap_dev`; no implica autorización de conexión/escritura actual ni prueba de aprovisionamiento. Antes de toda conexión de escritura/migración y de toda prueba con acceso a DB, obtener autorización explícita separada para host, puerto, nombre exacto y aprovisionamiento, registrar la tupla no sensible, probar procedencia/reserva exclusiva y confirmar entorno controlado aprobado. La configuración efectiva debe coincidir exactamente. Preflight solo lectura confirma MySQL 8.x y destino antes de escribir. Si falta cualquier evidencia/gate, detenerse antes de conectar/modificar. No reutilizar base de procedencia desconocida. Prohibidas operaciones destructivas y cambios en bases ajenas; solo operaciones estrictamente necesarias y autorizadas sobre DB dedicada.
- **Verificaciones separadas:** `django check`; preflight DB read-only; `migrate`; posterior `migrate --check`; pytest; Ruff; servidor local y GET health. No declarar resultados no ejecutados como exitosos.
- **Documentación y privacidad:** actualización documental limitada a artefactos existentes en alcance, siguiendo CA-10. Checklist por rutas relativas, estado `[x]`/`[ ]` y evidencia. Eliminar nombres de cuentas personales y rutas absolutas de perfil/home de los documentos a actualizar; sustituir paths de evidencias históricas por rutas relativas del repo, `<ruta del entorno virtual>` o equivalente sin datos personales. Las ediciones de esta fase se limitaron a `spec.md` (enmienda v1.4 de plataformas), `plan.md`, `tasks.md` y `requirements.txt`, más el retiro autorizado de los tres artefactos legacy; no se editó código ni README. No reproducir secretos.

## Riesgos y paradas

Incompatibilidad/no disponibilidad del plugin o resolución conjunta, diferencias entre metadatos/resolución/ejecución funcional, alteración del conjunto de dependencias, exposición de secretos, `.env` versionado, intérprete equivocado, destino MySQL no autorizado/no aprovisionado/mismatch, efectos sobre bases ajenas, pruebas que creen o eliminen un destino no aprobado y evidencia incompleta. Documentar plataformas reales sin inferir soporte universal. En cualquiera, detener tarea dependiente e informar; no sustituir paquetes ni ampliar alcance. T-10 no corre pytest con DB sin autorización específica del destino de pruebas y sus operaciones de ciclo de vida. Se prohíben `flush`, `drop`, reset y acciones destructivas fuera de DB dedicada aprobada.

## Trazabilidad resumida

La matriz completa tarea→requisito→criterio→evidencia está en `tasks.md`.

| Requisitos | Criterios | Tareas principales |
|---|---|---|
| RB-01 | CA-01 | T-02, T-03, T-13 |
| RB-02 | CA-01, CA-02 | T-03, T-05, T-13 |
| RB-03 | CA-02, CA-03, CA-09 | T-04, T-05, T-13 |
| RB-04 | CA-04 | T-06, T-11, T-13 |
| RB-05 | CA-05, CA-06 | T-07, T-08, T-09, T-10, T-11, T-13 |
| RB-06 | CA-01, CA-05, CA-06 | T-02, T-07–T-11, T-13 |
| RB-07 | CA-07 | T-12, T-13 |
| RB-08 | CA-08 | T-13 |
| RB-09 | CA-03, CA-09 | T-04, T-13 |
| RB-10 | CA-10 | T-04, T-11, T-13 |

## Gate de fase

Este plan y `tasks.md` fueron aprobados por Reviewer y por el usuario; la autorización de implementación fue concedida. La especificación v1.4 fue enmendada y aprobada por el usuario exclusivamente en el criterio de plataformas. T-04 ejecutó la verificación temporal y la consolidación del manifiesto único bajo autorización explícita; Reviewer emitió APROBADO. No se instalaron dependencias en `.venv` del proyecto. No se conectó a MySQL ni hubo migraciones. T-05 no puede iniciar hasta que el usuario lo autorice.

## Registro de ejecución — T-04 (2026-11-07; consolidación ejecutada; Reviewer APROBADO)

Planner confirmó en fuentes públicas que `langchain-deepseek` existe en PyPI, versión observada 1.1.1, con `Requires-Python >=3.10.0,<4.0.0`, y dependencias declaradas `langchain-core >=1.4.7,<2.0.0` y `langchain-openai >=1.3.1,<2.0.0`. El wheel publicado es `py3-none-any`; esto solo acredita que el artefacto del plugin es Python puro y no demuestra compatibilidad de sus dependencias con Windows ni funcionamiento. Fuentes: <https://pypi.org/pypi/langchain-deepseek/json>, <https://pypi.org/project/langchain-deepseek/1.1.1/>, <https://docs.langchain.com/oss/python/integrations/chat/deepseek>, <https://docs.langchain.com/oss/python/langchain/install>.

En la revisión preliminar original no se obtuvo metadata actual suficiente de LangChain/LangGraph ni se resolvió el grafo completo. En esa primera evaluación no se ejecutó resolución `pip` ni había ejecución funcional del plugin en Windows 10/11. Reviewer dictaminó **NO APROBADO** para T-04 con la evidencia disponible entonces; a continuación se registra la evidencia complementaria posterior, incluida la prueba temporal en Windows 10.

**Investigación complementaria autorizada:** en un entorno temporal aislado `$TEMP/opencode/t04-validation/venv`, sin usar `.venv` del proyecto, se ejecutó Windows 10 x64 build `10.0.19045`, CPython 3.14.10 64-bit, pip 26.2.2. El comando `pip install` con los nueve directos candidatos terminó con código 0: Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. `pip check` terminó con código 0 (“No broken requirements found”). La resolución incluyó LangChain Core 1.7.6, LangChain OpenAI 1.7.4, LangGraph Checkpoint 4.3.1, LangGraph Prebuilt 1.1.1, LangGraph SDK 0.4.14, Pydantic Core 2.50.4, uuid-utils 0.19.0, orjson 3.13.0, ormsgpack 1.13.0, websockets 17.4 y openai 3.46.0 como transitiva. La lista completa del freeze se registra en `tasks.md` T-04.

Todos los imports solicitados (`langchain_deepseek`, `langchain`, `langchain_core`, `langchain_openai`, `langgraph`, `langgraph.graph`, `pydantic`, `django`, `MySQLdb`, `pytest`, `ruff`) pasaron. La instancia `ChatDeepSeek` se creó usando una clave ficticia solo en memoria; se construyó y compiló un `StateGraph` sin ejecutar el nodo ni hacer solicitudes de red. El smoke test inicial tuvo código 1 por una construcción incorrecta del `TypedDict` en el comando; se corrigió el comando sin cambiar paquetes y la repetición terminó con código 0. No se llamó a la API ni a MySQL.

**Criterio de plataforma de spec v1.4:** no se exige una prueba independiente de Windows 11 ni se define una lista cerrada de sistemas soportados. La resolución y las restricciones se atribuyen a Python 3.14.10 en el entorno temporal Windows 10 x64 y la prueba funcional solo a ese entorno. No afirmar cobertura universal ni Windows 11 probado.

**Consolidación del manifiesto único (2026-11-07):** `requirements.txt` contiene las nueve dependencias directas verificadas: Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. Se retiraron `requirements-ai.txt`, `requirements-win-py314.lock.txt` y `requirements-ai-win-py314.lock.txt` tras verificar que todas sus versiones estaban documentadas en el cierre transitivo de `tasks.md`; los hashes no se conservaron porque la estrategia aprobada excluye locks. El checklist CA-10 quedó actualizado. No se inició T-05 ni se accedió a MySQL.

**Enmienda v1.4 y conflicto resuelto:** `spec.md` v1.4 sustituye la matriz obligatoria Windows 10/11 por evidencia de resolución en el entorno realmente verificado (Windows 10 x64, CPython 3.14.10), sin lista cerrada de sistemas y sin afirmar compatibilidad universal. Windows 11 no probado no bloquea por sí solo. La enmienda fue autorizada explícitamente por el usuario y no altera alcance funcional, arquitectura, Python 3.14.10 ni la elección de `langchain-deepseek`.

**Dictamen Reviewer (2026-11-07): APROBADO.** T-04 satisface RB-03, RB-09, RB-10 y CA-03, CA-09, CA-10. El veredicto es técnico y no autoriza T-05. Quedan observaciones no bloqueantes para una edición documental posterior: etiquetas `BORRADOR` en las filas de spec v1.4, omisión de CA-10 en la trazabilidad inversa de RB-03, evidencia funcional no nombrada en RB-09/CA-09, frase histórica en §4 y `MEMORY.md` desactualizado.
