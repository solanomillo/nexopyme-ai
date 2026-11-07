# Plan técnico 000 — Bootstrap inicial del proyecto

## Estado y autoridad

**ESPECIFICACIÓN v1.4, PLAN Y TAREAS APROBADOS; AUTORIZACIÓN DE IMPLEMENTACIÓN CONCEDIDA.** La aprobación de la especificación, plan y tareas y la autorización de implementación constan en declaraciones explícitas del usuario; Reviewer emitió APROBADO para plan y tareas. La v1.4 enmienda exclusivamente el criterio de plataformas, autorizada explícitamente por el usuario el 2026-11-07. T-01–T-03 tienen evidencia histórica y dictamen Reviewer APROBADO. T-04 está COMPLETADA: la verificación en Windows 10 y la consolidación del manifiesto único se ejecutaron bajo autorización explícita; Reviewer emitió APROBADO. T-05 está COMPLETADA: el manifiesto completo se instaló en `.venv`, `pip check` pasó y Reviewer emitió APROBADO. T-06 está COMPLETADA: configuración Django y archivos de entorno creados; check por etiquetas ejecutado y Reviewer emitió APROBADO. T-07 está COMPLETADA: preflight read-only y check completo en verde tras la enmienda autorizada del manifiesto a Django 6.0.9 (MySQL 8.0.36); Reviewer emitió APROBADO. T-08 está COMPLETADA: `GRANT` aplicado por el usuario, 18 migraciones aplicadas con éxito y Reviewer emitió APROBADO; T-08 `[x]`. T-09 está COMPLETADA: `migrate --check` confirmó cero pendientes, sin cambios en tablas, datos ni privilegios, y Reviewer emitió APROBADO; T-09 `[x]`. T-10–T-13 no iniciadas.

## Objetivo, alcance y estrategia

Preparar entorno local reproducible con Python 3.14.10, `.venv`, Django y MySQL 8.x exclusivamente operativo, configuración segura por entorno, verificaciones, migraciones iniciales, pruebas/calidad, `GET /health/` y documentación de evidencia. No incluye negocio, llamadas IA, checkpointer, despliegue ni SQLite operativo. Se mantiene estrictamente el alcance de `spec.md` v1.4 y `AGENTS.md`.

La secuencia de 13 tareas y trazabilidad detallada está en `tasks.md`. La estrategia de manifiesto es un solo `requirements.txt` con dependencias directas base+IA: Django, mysqlclient, pytest, pytest-django, Ruff, Pydantic, LangChain, LangGraph y `langchain-deepseek`. No se mantiene `requirements-ai.txt`, grupos separados ni locks. No se fijan versiones por conjetura: las del manifiesto son las verificadas en el entorno temporal. T-04 documenta metadatos/restricciones directas y transitivas y la resolución conjunta para Python 3.14.10; no exige una matriz cerrada de sistemas operativos ni prueba independiente Windows 10/11. Se documenta el entorno funcional efectivamente probado y no se afirma compatibilidad universal.

## Decisiones técnicas concretadas

- **Plataforma e intérprete:** Python objetivo 3.14.10. No se define una lista cerrada de sistemas operativos soportados ni se exige probar Windows 10 y Windows 11 separadamente. Se identifican con precisión las plataformas efectivamente verificadas; en esta ejecución, instalación e integración funcional se probaron en Windows 10 x64 con CPython 3.14.10. No inferir soporte de Windows 11 ni compatibilidad universal.
- **Dependencias:** T-04 documenta fuentes, `Requires-Python`, `Requires-Dist`, marcadores relevantes, cierre transitivo seleccionado y resolución conjunta del conjunto directo para Python 3.14.10 en el entorno temporal descrito. La inclusión condicional de `langchain-deepseek` forma parte de la decisión aprobada en v1.4; no se sustituye por SDK/paquete alternativo unilateralmente. La compatibilidad declarada, resolución y ejecución funcional son tipos de evidencia distintos y se reportan por separado.
- **Instalación T-05:** tras gates de aprobación humana del plan/tareas y autorización explícita previa de implementación de `AGENTS.md` §5, ejecutar en `.venv` `python -m pip install -r requirements.txt` (una sola instalación del manifiesto; un reintento del mismo comando por timeout no es una instalación distinta ni altera el conjunto); al ser manifiesto único, el conjunto instalado es base+IA. Antes debe terminar satisfactoriamente T-04, con plugin incluido y compatibilidad demostrada. Si T-04 se bloquea, T-05 no empieza y no se instala un subconjunto mediante `-r` con exclusiones, ni se omite/reemplaza el plugin. Registrar versiones instaladas y ejecutar `python -m pip check`. La mera aprobación de este plan no habilita la instalación.
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

Este plan y `tasks.md` fueron aprobados por Reviewer y por el usuario; la autorización de implementación fue concedida. La especificación v1.4 fue enmendada y aprobada por el usuario exclusivamente en el criterio de plataformas. T-04 ejecutó la verificación temporal y la consolidación del manifiesto único bajo autorización explícita; Reviewer emitió APROBADO. T-05 fue autorizada por el usuario e instaló el manifiesto completo en `.venv` del proyecto; Reviewer emitió APROBADO. T-06 fue autorizada por el usuario y configuró Django con variables de entorno; Reviewer emitió APROBADO. No se conectó a MySQL ni hubo migraciones en T-06. T-07 está COMPLETADA con Reviewer APROBADO. T-08 está COMPLETADA con Reviewer APROBADO: el usuario autorizó completarla, el `GRANT` fue aplicado y las 18 migraciones se aplicaron con éxito. T-09 está COMPLETADA con Reviewer APROBADO: `migrate --check` confirmó cero pendientes. T-10 no puede iniciar sin la autorización explícita del usuario.

## Registro de ejecución — T-04 (2026-11-07; consolidación ejecutada; Reviewer APROBADO)

Planner confirmó en fuentes públicas que `langchain-deepseek` existe en PyPI, versión observada 1.1.1, con `Requires-Python >=3.10.0,<4.0.0`, y dependencias declaradas `langchain-core >=1.4.7,<2.0.0` y `langchain-openai >=1.3.1,<2.0.0`. El wheel publicado es `py3-none-any`; esto solo acredita que el artefacto del plugin es Python puro y no demuestra compatibilidad de sus dependencias con Windows ni funcionamiento. Fuentes: <https://pypi.org/pypi/langchain-deepseek/json>, <https://pypi.org/project/langchain-deepseek/1.1.1/>, <https://docs.langchain.com/oss/python/integrations/chat/deepseek>, <https://docs.langchain.com/oss/python/langchain/install>.

En la revisión preliminar original no se obtuvo metadata actual suficiente de LangChain/LangGraph ni se resolvió el grafo completo. En esa primera evaluación no se ejecutó resolución `pip` ni había ejecución funcional del plugin en Windows 10/11. Reviewer dictaminó **NO APROBADO** para T-04 con la evidencia disponible entonces; a continuación se registra la evidencia complementaria posterior, incluida la prueba temporal en Windows 10.

**Investigación complementaria autorizada:** en un entorno temporal aislado `$TEMP/opencode/t04-validation/venv`, sin usar `.venv` del proyecto, se ejecutó Windows 10 x64 build `10.0.19045`, CPython 3.14.10 64-bit, pip 26.2.2. El comando `pip install` con los nueve directos candidatos terminó con código 0: Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. `pip check` terminó con código 0 (“No broken requirements found”). La resolución incluyó LangChain Core 1.7.6, LangChain OpenAI 1.7.4, LangGraph Checkpoint 4.3.1, LangGraph Prebuilt 1.1.1, LangGraph SDK 0.4.14, Pydantic Core 2.50.4, uuid-utils 0.19.0, orjson 3.13.0, ormsgpack 1.13.0, websockets 17.4 y openai 3.46.0 como transitiva. La lista completa del freeze se registra en `tasks.md` T-04. **Nota de vigencia (2026-11-07):** esta evidencia histórica corresponde a Django 6.1.3; la enmienda autorizada en T-07 fijó la resolución vigente en Django 6.0.9. El resto del conjunto directo y transitivo no cambió.

Todos los imports solicitados (`langchain_deepseek`, `langchain`, `langchain_core`, `langchain_openai`, `langgraph`, `langgraph.graph`, `pydantic`, `django`, `MySQLdb`, `pytest`, `ruff`) pasaron. La instancia `ChatDeepSeek` se creó usando una clave ficticia solo en memoria; se construyó y compiló un `StateGraph` sin ejecutar el nodo ni hacer solicitudes de red. El smoke test inicial tuvo código 1 por una construcción incorrecta del `TypedDict` en el comando; se corrigió el comando sin cambiar paquetes y la repetición terminó con código 0. No se llamó a la API ni a MySQL.

**Criterio de plataforma de spec v1.4:** no se exige una prueba independiente de Windows 11 ni se define una lista cerrada de sistemas soportados. La resolución y las restricciones se atribuyen a Python 3.14.10 en el entorno temporal Windows 10 x64 y la prueba funcional solo a ese entorno. No afirmar cobertura universal ni Windows 11 probado.

**Consolidación del manifiesto único (2026-11-07):** `requirements.txt` contiene las nueve dependencias directas verificadas: Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. Se retiraron `requirements-ai.txt`, `requirements-win-py314.lock.txt` y `requirements-ai-win-py314.lock.txt` tras verificar que todas sus versiones estaban documentadas en el cierre transitivo de `tasks.md`; los hashes no se conservaron porque la estrategia aprobada excluye locks. El checklist CA-10 quedó actualizado. En ese momento no se había iniciado T-05 ni se accedió a MySQL. **Nota de vigencia (2026-11-07):** el pin de Django cambió a 6.0.9 en T-07 por compatibilidad con MySQL 8.0.36; las otras ocho dependencias directas conservan las versiones indicadas.

**Enmienda v1.4 y conflicto resuelto:** `spec.md` v1.4 sustituye la matriz obligatoria Windows 10/11 por evidencia de resolución en el entorno realmente verificado (Windows 10 x64, CPython 3.14.10), sin lista cerrada de sistemas y sin afirmar compatibilidad universal. Windows 11 no probado no bloquea por sí solo. La enmienda fue autorizada explícitamente por el usuario y no altera alcance funcional, arquitectura, Python 3.14.10 ni la elección de `langchain-deepseek`.

**Dictamen Reviewer (2026-11-07): APROBADO.** T-04 satisface RB-03, RB-09, RB-10 y CA-03, CA-09, CA-10. El veredicto es técnico y no autoriza T-05. Quedan observaciones no bloqueantes para una edición documental posterior: etiquetas `BORRADOR` en las filas de spec v1.4, omisión de CA-10 en la trazabilidad inversa de RB-03, evidencia funcional no nombrada en RB-09/CA-09, frase histórica en §4 y `MEMORY.md` desactualizado.

## Registro de ejecución — T-05 (2026-11-07; instalación completa; Reviewer APROBADO)

**Precondiciones verificadas:** rama `main` con `origin/main...HEAD` = `0 0` (sincronizada); intérprete `.venv\Scripts\python.exe` con Python 3.14.10, `sys.prefix` distinto de `sys.base_prefix`; pip 26.2.2; `requirements.txt` con las nueve dependencias directas aprobadas. No se modificó el manifiesto.

**Comando y resultado:** se ejecutó `.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt`. El primer intento superó el timeout de la herramienta (600 s) durante la fase de instalación: quedaron instaladas las dependencias base y sus transitivas, pero faltaban las de IA. No hubo error de pip ni conflicto reportado. Se reejecutó el mismo comando autorizado: `Successfully installed langchain-1.4.9 langchain-core-1.7.6 langchain-deepseek-1.1.1 langchain-openai-1.7.4 langgraph-1.2.20 langgraph-checkpoint-4.3.1 langgraph-prebuilt-1.1.1 langgraph-sdk-0.4.14 langsmith-0.14.17 openai-3.46.0`, código de salida 0. No se instaló ningún paquete fuera del manifiesto ni se sustituyó dependencia alguna.

**Verificaciones:** `python -m pip check` → `No broken requirements found.`, código 0. Las nueve dependencias directas coinciden exactamente con el manifiesto (9/9): Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. Los imports de los nueve paquetes directos y de `langchain_deepseek`/`langgraph` cargaron correctamente, código 0. El freeze completo del entorno (58 distribuciones, incluido `pip`) se registra en `tasks.md` T-05. Ruff (`ruff check .`) → `All checks passed!`, código 0, sin archivos Python todavía. No hay pruebas de negocio aplicables en esta tarea. No se conectó a MySQL, no se ejecutaron migraciones y no se inició T-06. No se revelaron secretos ni rutas absolutas de perfil. **Nota de vigencia (2026-11-07):** la versión vigente de Django es 6.0.9 desde la enmienda autorizada en T-07; las otras ocho dependencias directas mantienen la correspondencia 9/9 documentada.

## Registro de ejecución — T-06 (2026-11-07; configuración creada; Reviewer APROBADO)

**Precondiciones verificadas:** rama `main` con `origin/main...HEAD` = `0 0` (sincronizada); intérprete `.venv\Scripts\python.exe` con Python 3.14.10; `pip check` sin problemas; Django 6.1.3 disponible. No se modificó `spec.md` ni `requirements.txt`.

**Estructura creada:** `manage.py` y paquete `config/` (`__init__.py`, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`). `DJANGO_SETTINGS_MODULE=config.settings`. La configuración sensible se lee exclusivamente de variables de entorno del proceso: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER` y `MYSQL_PASSWORD`. `DATABASES["default"]["ENGINE"]` es `django.db.backends.mysql`; no hay SQLite operativo. No se añadió cargador `.env` ni dependencia alguna.

**Archivos de entorno:** `.env.example` contiene solo nombres y valores vacíos/placeholders no utilizables, sin credenciales; su comentario aclara que no hay cargador automático de `.env` y que las variables se exportan en el entorno del proceso. `.env` local es una plantilla vacía no versionada; `.gitignore` lo excluye mediante `.env` y permite `.env.example` con `!.env.example`. `.gitignore` se versiona en esta tarea para que la exclusión quede garantizada por el repositorio. `git check-ignore` confirmó la exclusión de `.env`; `.env` no está rastreado y no aparece en `git status`. No se inventaron ni escribieron credenciales reales.

**Comportamiento de Django 6.1 y decisión:** el `manage.py check` completo ejecuta comprobaciones de modelos contra todas las bases y, con MySQL, abre conexión para introspección (`has_native_uuid_field` → `mysql_server_info`). Se reprodujo con marcadores y falló con `Access denied`, confirmando el intento de conexión no autenticado, sin acceso a datos ni uso de credenciales reales. Es un cambio de comportamiento documentado de Django 6.1. El intento se reportó al usuario como desviación y el usuario autorizó el check por etiquetas, excluyendo `models` y `database`:

`python manage.py check --tag admin --tag caches --tag commands --tag compatibility --tag files --tag mail --tag security --tag staticfiles --tag templates --tag translation --tag urls` → `System check identified no issues (0 silenced).`, código 0, sin conexión a MySQL.

Las comprobaciones de modelos y de base quedan diferidas a T-07/T-08, cuando exista autorización de acceso de solo lectura. La inspección de settings confirmó `ENGINE=django.db.backends.mysql`, `NAME`/`USER`/`PASSWORD` presentes desde entorno, `HOST=127.0.0.1`, `PORT=3306` y ausencia de SQLite. Ruff (`ruff check .`) → `All checks passed!`, código 0. **Desviación detectada y resuelta:** el `check` completo intentó una conexión no autenticada que falló con `Access denied`, sin acceso a datos ni uso de credenciales reales; se reportó al usuario y este autorizó el check por etiquetas sin conexión. No se accedió a datos, no se ejecutaron migraciones y no se inició T-07. `.gitignore` se versiona en esta tarea para que la exclusión de `.env` quede garantizada por el repositorio. No se revelaron secretos ni rutas absolutas de perfil. **Nota para T-10/T-11:** las ocho variables son obligatorias al importar settings; las pruebas deberán proveer el entorno completo o definir una estrategia explícita.

## Registro de ejecución — T-07 (2026-11-07; preflight read-only exitoso; bloqueo de compatibilidad detectado)

**Precondiciones verificadas:** rama `main` con `origin/main...HEAD` = `0 0` (sincronizada); intérprete `.venv` Python 3.14.10; `pip check` sin problemas. Autorización explícita del usuario registrada para MySQL 8.x, versión confirmada 8.0.36, host `127.0.0.1`, puerto `3306`, base `nexopyme_bootstrap_dev`, usuario `nexopyme_user`, base creada exclusivamente para NexoPyme AI.

**Configuración efectiva:** comparación exacta con la tupla autorizada. `ENGINE=django.db.backends.mysql`, `HOST=127.0.0.1`, `PORT=3306`, `NAME=nexopyme_bootstrap_dev`, `USER=nexopyme_user`, contraseña presente y no expuesta. `CONFIG_MATCH=True`.

**Preflight read-only (MySQLdb directo, sin el gate de versión de Django):** se abrió `START TRANSACTION READ ONLY` y se ejecutaron únicamente consultas de lectura. Resultado: `VERSION=8.0.36`; `DATABASE=nexopyme_bootstrap_dev`; `CURRENT_USER=nexopyme_user@localhost`; `SERVER_PORT=3306`; `HOSTNAME=DESKTOP-UDA02EM`; `SERVER_UUID=9ba1dc5a-6bb1-11ef-b5db-48ba4eb0477b`; `READ_ONLY_TRANSACTION_COMPLETED=True`. `SHOW GRANTS`: `GRANT USAGE ON *.* TO 'nexopyme_user'@'localhost'` y `GRANT SELECT ON 'nexopyme_bootstrap_dev'.* TO 'nexopyme_user'@'localhost'`. `SHOW DATABASES`: `information_schema`, `nexopyme_bootstrap_dev`, `performance_schema`; no se ven otras bases de negocio. `INFORMATION_SCHEMA.TABLES` sobre la base autorizada: `TABLE_COUNT=0`, `TABLES=[]`. No se ejecutaron escrituras, migraciones ni cambios de permisos. Sin secretos ni contraseñas en la evidencia.

**Bloqueo de compatibilidad detectado:** Django 6.1.3 define `minimum_database_version` de MySQL como `(8, 4)` en `django/db/backends/mysql/features.py`; el servidor autorizado es 8.0.36. Por eso el `manage.py check` completo y cualquier conexión ORM fallaban con `django.db.utils.NotSupportedError: MySQL 8.4 or later is required (found 8.0.36)`. Django 6.0.x y 5.2.x soportan MySQL 8.0.11 o superior; Django 6.1 y posteriores exigen MySQL 8.4 o superior. Se detuvo T-07 antes de escribir o migrar y se consultó al usuario con tres opciones: (a) actualizar MySQL a 8.4 LTS manteniendo Django 6.1.3; (b) cambiar Django a 6.0.x o 5.2.x modificando el manifiesto aprobado; (c) pausar. El usuario autorizó la opción (b) con Django 6.0.9.

**Enmienda autorizada del manifiesto y revalidación:** se cambió `Django==6.1.3` por `Django==6.0.9` en `requirements.txt` y se reinstaló con `pip install -r requirements.txt` → `Successfully installed Django-6.0.9`, código 0. `pip check` → `No broken requirements found.`, código 0. Metadata de Django 6.0.9: `Requires-Python >=3.12` (Python 3.14.10 cumple), `Requires-Dist: asgiref>=3.9.1`, `sqlparse>=0.5.0`, `tzdata; sys_platform == "win32"`; el resto del manifiesto quedó sin cambios. El backend MySQL de Django 6.0.9 define `minimum_database_version=(8, 0, 11)`, compatible con el servidor 8.0.36. La evidencia histórica de T-04 para Django 6.1.3 se conserva como registro; la resolución vigente del manifiesto es Django 6.0.9.

**Verificación final de T-07 con Django 6.0.9:** `python manage.py check` completo → `System check identified no issues (0 silenced).`, código 0. Verificación read-only vía Django con `START TRANSACTION READ ONLY`: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `AUTHORIZED_SCHEMA_EXISTS=True`, `TABLE_COUNT=0`, `TABLES=[]`, `GRANT USAGE ON *.*` y `GRANT SELECT ON nexopyme_bootstrap_dev.*`, bases visibles `information_schema`/`nexopyme_bootstrap_dev`/`performance_schema`, `VERSION_MATCH_8_0_36=True`, `DATABASE_MATCH=True`, `USER_MATCH=True`, `READ_ONLY_TRANSACTION_COMPLETED=True`, código 0. Sin escrituras, migraciones ni cambios de permisos; sin secretos. T-07 queda COMPLETADA; Reviewer emitió APROBADO. T-08 no iniciada.

## Registro de preparación — T-08 (2026-11-07; permisos propuestos; pendiente de dictamen y autorización)

**Precondiciones revalidadas:** rama `main` con `origin/main...HEAD` = `0 0`; intérprete `.venv` Python 3.14.10; `pip check` sin problemas; Django 6.0.9. Entorno controlado aprobado: base dedicada y exclusiva del proyecto, tupla autorizada y servidor MySQL 8.0.36, sin indicios de otras bases de negocio. Preflight read-only repetido antes y después de la inspección de migraciones: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `HOST=127.0.0.1`, `PORT=3306`, `CONFIG_MATCH=True`; grants vigentes `USAGE ON *.*` y `SELECT ON nexopyme_bootstrap_dev.*`; bases visibles `information_schema`, `nexopyme_bootstrap_dev`, `performance_schema`; `TABLE_COUNT=0`, `TABLES=[]`; `READ_ONLY_TRANSACTION_COMPLETED=True`. No se modificaron permisos, tablas ni datos.

**Plan real de migraciones (18):** `contenttypes.0001_initial`, `auth.0001_initial`, `admin.0001_initial`, `admin.0002_logentry_remove_auto_add`, `admin.0003_logentry_add_action_flag_choices`, `contenttypes.0002_remove_content_type_name`, `auth.0002`–`auth.0012`, `sessions.0001_initial`.

**SQL representativo verificado con `sqlmigrate` (recolección de SQL, sin ejecutar DDL):** `CREATE TABLE` para `django_content_type`, `auth_permission`, `auth_group`, `auth_group_permissions`, `auth_user`, `auth_user_groups`, `auth_user_user_permissions`, `django_admin_log` y `django_session`, más `django_migrations` creada por el registrador; `ALTER TABLE ... ADD CONSTRAINT ... UNIQUE`, `ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY`, `ALTER TABLE ... MODIFY` y `ALTER TABLE ... DROP COLUMN`; `CREATE INDEX django_session_expire_date_a5c62663 ON django_session (expire_date)`; `UPDATE` de `auth_permission` en `auth.0011`; `INSERT` en `django_migrations` y en la creación de content types/permisos de `post_migrate`. No hay `AddIndex`, `AddConstraint`, `DeleteModel`, `RunSQL`, `DROP TABLE` ni `DELETE` en las 18 migraciones. `contenttypes.0002` usa `RunPython` solo en reversa (`noop` al avanzar) y `auth.0006_require_contenttypes_0002` no tiene operaciones.

**Privilegios propuestos (mínimos para el avance):** `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `INDEX`, `REFERENCES` sobre `nexopyme_bootstrap_dev.*`.

- `SELECT`: lectura de `django_migrations`, content types, permisos e introspección del esquema.
- `INSERT`: registro de migraciones aplicadas y creación de content types/permisos en `post_migrate`.
- `UPDATE`: migración de datos `auth.0011_update_proxy_permissions`; `create_contenttypes` solo inserta, no actualiza.
- `CREATE`: creación de las tablas de las 18 migraciones y de `django_migrations`.
- `ALTER`: `MODIFY`, `DROP COLUMN`, `ADD CONSTRAINT UNIQUE` y `ADD CONSTRAINT FOREIGN KEY`.
- `INDEX`: `CREATE INDEX` de `sessions.0001`; las restricciones únicas creadas vía `ALTER TABLE` se cubren con `ALTER` + `CREATE` + `INSERT`.
- `REFERENCES`: creación de claves foráneas de `auth`, `admin` y sus tablas intermedias.

MySQL 8.0 exige `ALTER` + `CREATE` + `INSERT` para `ALTER TABLE`, `REFERENCES` sobre la tabla padre para claves foráneas e `INDEX` para `CREATE INDEX`; todo queda cubierto por el grant a nivel de base. No hay vistas, rutinas, triggers ni tablas temporales en el camino.

**Excluidos deliberadamente:** `DELETE`, `DROP`, `CREATE TEMPORARY TABLES`, `LOCK TABLES`, `TRIGGER`, `EVENT`, `CREATE ROUTINE`, `EXECUTE` y `GRANT OPTION`. No son necesarios para el avance; `DELETE` y `DROP` habilitarían operaciones destructivas no autorizadas. La reversión/desaplicación de migraciones requeriría `DELETE`/`DROP` y una autorización separada.

**Sentencias propuestas (no ejecutadas):**

```sql
GRANT SELECT, INSERT, UPDATE, CREATE, ALTER, INDEX, REFERENCES
ON `nexopyme_bootstrap_dev`.*
TO 'nexopyme_user'@'localhost';
```

No se incluye `FLUSH PRIVILEGES`: `GRANT` actualiza las tablas de privilegios sin requerirlo. El `GRANT` se limita exclusivamente a `nexopyme_bootstrap_dev.*`; no se otorga nada sobre `*.*` ni sobre otras bases.

**Ejecución del `GRANT` (solo tras autorización explícita):** lo ejecuta una cuenta administrativa (root/DBA) fuera de la conexión de la aplicación, porque `nexopyme_user` no tiene `GRANT OPTION`. Registrar fecha, aprobador y resultado redactado. La aplicación nunca recibe privilegios globales ni `GRANT OPTION`. Esta autorización de escritura es distinta e independiente de la autorización read-only de T-07, con aprobador y fecha propios.

**Verificación posterior al `GRANT` y previa a `migrate`:** `SHOW GRANTS FOR 'nexopyme_user'@'localhost'` (o `SHOW GRANTS` desde la propia cuenta) debe mostrar exactamente `USAGE ON *.*` y los siete privilegios sobre `nexopyme_bootstrap_dev.*`, sin otros privilegios globales ni sobre otras bases. Repetir la comparación exacta de tupla y el preflight read-only inmediatamente antes de migrar.

**Resultado esperado de `migrate`:** `python manage.py migrate` ejecutado con el intérprete de `.venv` y sin banderas; 18 migraciones aplicadas, 10 tablas (9 + `django_migrations`) y 18 filas en `django_migrations`. Prohibidos `--fake`, `--fake-initial`, `--run-syncdb`, `--database` distinto de `default` y SQL manual.

**Contingencia:** MySQL no revierte DDL; con `DROP` excluido, un fallo parcial deja el esquema a medias y la recuperación requiere intervención del DBA con autorización separada. Detenerse e informar.

**Consideraciones posteriores:** tras T-08, evaluar si se revocan `CREATE`/`ALTER`/`INDEX`/`REFERENCES`; T-09 solo necesita `SELECT`. T-10 requerirá autorización separada y este grant no cubre la base de pruebas (`test_nexopyme_bootstrap_dev`).

**Estado de la preparación:** T-08 quedó preparada y aprobada técnicamente por el Reviewer (revisión inicial: CAMBIOS NECESARIOS B1–B3, incorporados; re-revisión: APROBADO). El usuario autorizó formalmente completar T-08 y el `GRANT` fue aplicado desde MySQL Workbench. La ejecución se registra a continuación.

## Registro de ejecución — T-08 (2026-11-07; migraciones aplicadas; Reviewer APROBADO)

**Autorización y `GRANT`:** el usuario del proyecto (vía Build) autorizó formalmente completar T-08 el 2026-11-07. El `GRANT` fue aplicado desde una sesión administrativa en MySQL Workbench y `SHOW GRANTS` confirmó los siete privilegios (`SELECT`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `INDEX`, `REFERENCES`) limitados a `nexopyme_bootstrap_dev.*` para `'nexopyme_user'@'localhost'`, además de `USAGE ON *.*`. Sin `GRANT OPTION` y sin privilegios sobre otras bases.

**Preflight read-only previo:** `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `HOST=127.0.0.1`, `PORT=3306`, `CONFIG_MATCH=True`; grants exactos (siete privilegios + `USAGE ON *.*`); bases visibles `information_schema`, `nexopyme_bootstrap_dev`, `performance_schema`; `TABLE_COUNT=0`, `TABLES=[]`; `PREFLIGHT_EXIT=0`.

**Ejecución:** `.\.venv\Scripts\python.exe manage.py migrate` (intérprete `.venv`, sin banderas). Salida: `Operations to perform: Apply all migrations: admin, auth, contenttypes, sessions`; 18 migraciones `OK` (`contenttypes.0001`, `auth.0001`, `admin.0001`–`0003`, `contenttypes.0002`, `auth.0002`–`0012`, `sessions.0001`); `MIGRATE_EXIT=0`. No se usaron `--fake`, `--fake-initial`, `--run-syncdb`, `--database` ni SQL manual.

**Verificación posterior read-only:** preflight: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `CONFIG_MATCH=True`, grants sin cambios (siete privilegios + `USAGE ON *.*`), `TABLE_COUNT=10`, `PREFLIGHT_EXIT=0`. Consulta read-only: `django_migrations` con 18 filas, conjunto esperado presente, sin migraciones inesperadas ni faltantes; 10 tablas, conjunto esperado presente, sin tablas inesperadas ni faltantes; `django_content_type`=6, `auth_permission`=24; `READ_ONLY_TRANSACTION_COMPLETED=True`; `VERIFY_EXIT=0`.

**Verificaciones adicionales:** `showmigrations` → las 18 en `[X]`, `SHOWMIGRATIONS_EXIT=0`; `manage.py check` → `System check identified no issues (0 silenced).`, `CHECK_EXIT=0`; `ruff check .` → `All checks passed!`, `RUFF_EXIT=0`.

**Límites respetados:** no `flush`, `drop`, reset ni migraciones inversas; no se tocaron otras bases; no se ampliaron privilegios; no se inició T-09; sin secretos ni credenciales en la evidencia. No se ejecutó `migrate --check` porque corresponde a T-09.

**Estado:** T-08 COMPLETADA; Reviewer emitió APROBADO y T-08 quedó `[x]`. El dictamen técnico no sustituye la autorización humana. No se inició T-09.

## Registro de ejecución — T-09 (2026-11-07; sin migraciones pendientes; Reviewer APROBADO)

**Autorización:** el usuario del proyecto (vía Build) autorizó formalmente iniciar T-09 el 2026-11-07.

**Precondiciones:** rama `main` con `origin/main...HEAD` = `0 0`; `.venv` Python 3.14.10; Django 6.0.9; `pip check` sin problemas. Preflight read-only: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `HOST=127.0.0.1`, `PORT=3306`, `CONFIG_MATCH=True`; grants exactos (siete privilegios + `USAGE ON *.*`); bases visibles `information_schema`, `nexopyme_bootstrap_dev`, `performance_schema`; `TABLE_COUNT=10`; `PREFLIGHT_EXIT=0`.

**Verificación:** `python manage.py migrate --check` con el intérprete `.venv` → sin salida y `MIGRATE_CHECK_EXIT=0`, lo que indica cero migraciones pendientes. Se confirmó en el código de Django 6.0.9 (`migrate.py` L240, L258-261; `recorder.py` L84-97) que el flujo `--check` no ejecuta ninguna escritura.

**Estado posterior:** preflight: grants sin cambios, `TABLE_COUNT=10`, `PREFLIGHT_EXIT=0`. Consulta read-only: 18 filas en `django_migrations`, conjunto esperado presente, sin migraciones ni tablas inesperadas o faltantes; `django_content_type`=6, `auth_permission`=24; `READ_ONLY_TRANSACTION_COMPLETED=True`; `VERIFY_EXIT=0`. `showmigrations` → 18 en `[X]`, `SHOWMIGRATIONS_EXIT=0`; `manage.py check` → `System check identified no issues (0 silenced).`, `CHECK_EXIT=0`; `ruff check .` → `All checks passed!`, `RUFF_EXIT=0`.

**Límites respetados:** solo verificaciones de lectura; no se ejecutó `migrate` sin `--check`; sin escrituras, migraciones, `flush`, `drop`, reset ni cambios de permisos; sin tocar otras bases; T-10 no iniciada; sin secretos. No se modificaron tablas ni datos.

**Estado:** T-09 COMPLETADA; Reviewer emitió APROBADO y T-09 quedó `[x]`. El dictamen técnico no sustituye la autorización humana. No se inició T-10.
