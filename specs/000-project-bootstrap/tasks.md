# Tareas 000 — Bootstrap inicial del proyecto

**ESPECIFICACIÓN v1.4, PLAN Y TAREAS APROBADOS; AUTORIZACIÓN DE IMPLEMENTACIÓN CONCEDIDA.** La aprobación humana de estos artefactos y la autorización de implementación constan en declaraciones explícitas del usuario; Reviewer emitió APROBADO para plan y tareas. La v1.4 enmienda exclusivamente el criterio de plataformas, autorizada por el usuario el 2026-11-07. `[x]` en T-01–T-03 refleja evidencia histórica y dictamen independiente APROBADO. T-04 fue iniciada: la resolución, la prueba funcional temporal en Windows 10 y la consolidación del manifiesto único se ejecutaron bajo autorización explícita. No se afirma haber probado Windows 11 ni compatibilidad universal. Reviewer emitió APROBADO para T-04; T-04 `[x]`. T-05 está completada: el manifiesto completo se instaló en `.venv`, `pip check` pasó y Reviewer emitió APROBADO; T-05 `[x]`. T-06 está completada: configuración Django y archivos de entorno creados, check por etiquetas ejecutado y Reviewer APROBADO; T-06 `[x]`. T-07 ejecutada y aprobada por Reviewer; T-07 `[x]`. T-08 ejecutada, verificada y aprobada por Reviewer; T-08 `[x]`. T-09–T-13 `[ ]` y no iniciadas.

## Orden y trazabilidad

| Orden | ID/estado | Dependencias | Requisitos | Criterios |
|---:|---|---|---|---|
| 1 | T-01 [x] histórica | — | RB-03, RB-05, RB-06 | CA-03, CA-05, CA-06 |
| 2 | T-02 [x] histórica | T-01 | RB-01, RB-06 | CA-01 |
| 3 | T-03 [x] histórica | T-02 | RB-02 | CA-02 |
| 4 | T-04 [x] | T-01, T-03; gates humanos cumplidos | RB-03, RB-09, RB-10 | CA-03, CA-09, CA-10 |
| 5 | T-05 [x] | T-02–T-04, gates AGENTS §5 | RB-02, RB-03 | CA-02, CA-03 |
| 6 | T-06 [x] | T-05 | RB-04 | CA-04 |
| 7 | T-07 [x] | T-06; autorización DB explícita | RB-05, RB-06 | CA-05, CA-06 |
| 8 | T-08 [x] | T-07 satisfactorio, revalidación DB | RB-05, RB-06 | CA-05, CA-06 |
| 9 | T-09 [ ] | T-08 satisfactorio, revalidación DB | RB-06 | CA-06 |
| 10 | T-10 [ ] | T-09, guardas específicas de pytest/DB | RB-06 | CA-06 |
| 11 | T-11 [ ] | T-02–T-10 | RB-04–RB-06 | CA-04–CA-06 |
| 12 | T-12 [ ] | T-06, T-10 | RB-07 | CA-07 |
| 13 | T-13 [ ] | T-02–T-12 y resultados disponibles | RB-01–RB-10 | CA-01–CA-10 |

## Tareas verificables

### T-01 — Evidencia histórica de compatibilidad/plataformas y decisiones iniciales [x]
- **Estado/evidencia:** el registro histórico de `plan.md` indica ejecución 2026-11-06 y Reviewer APROBADO. La evidencia descrita allí corresponde a resolución sin instalación en Windows 10 x64 para dependencias entonces investigadas; Windows 11 no se probó independientemente. El registro enumera Python 3.14.10, Django, mysqlclient, pytest, pytest-django, Ruff, Pydantic, LangChain y LangGraph, pero no satisface RB-09 de la versión entonces vigente (v1.3): no verificó `langchain-deepseek`. No contarla como T-04.
- **Precondición:** no aplica (histórica).
- **Alcance realizado:** información de plataformas y resolución de candidatos; selector Python y tupla destino registrados. No se instaló nada, no se creó `.venv`, no se conectó a DB ni se demostró aprovisionamiento.
- **Comandos/patrón histórico:** consultas de metadatos y `pip install --dry-run --ignore-installed --no-cache-dir` con selector de Python 3.14. No repetir como sustituto de T-04.
- **Evidencia/aceptación:** consta en el registro histórico de `plan.md`; destino autorizado históricamente `127.0.0.1:3306/nexopyme_bootstrap_dev`, sin credenciales. Esa autorización no basta para conexión o escritura; T-07 exige autorización/procedencia verificables conforme v1.4.
- **Parada:** no inferir instalación, plugin compatible, Windows 11 probado, conexión ni aprovisionamiento.

### T-02 — Seleccionar y verificar Python 3.14.10 [x]
- **Estado/evidencia:** el registro histórico de tareas indica ejecución y Reviewer APROBADO; allí se consigna que en Windows 10 x64 el selector `py -3.14` informó 3.14.10 y la aserción pasó, mientras el intérprete bare 3.13.0 falló la aserción como se esperaba. Sin instalación.
- **Precondición:** T-01; no habilita tareas posteriores.
- **Comandos/patrón histórico:** `py -3.14 --version`; `py -3.14 -c "import sys; assert sys.version_info[:3] == (3, 14, 10)"`; prueba negativa con intérprete distinto.
- **Evidencia/aceptación:** transcripción histórica en este registro, Windows 10 solamente; selector a validar para el entorno de ejecución de tareas pendientes. CA-01 requiere éxito con versión exacta y fallo ante otra.
- **Parada:** si selector/version no coinciden, no sustituir por Python bare.

### T-03 — Crear y verificar `.venv` [x]
- **Estado/evidencia:** el registro histórico de tareas indica ejecución y Reviewer APROBADO; allí se consigna Windows 10 x64, `py -3.14 -m venv .venv`, activación PowerShell y aserciones de versión exacta, ejecutable bajo `.venv` y prefijos distintos, código 0. Sin pip/install. La evidencia previa a limpieza contenía rutas absolutas personales; aquí se sustituyen por `<ruta del entorno virtual>` y se preservan los hechos técnicos consignados.
- **Precondición:** T-02.
- **Comandos/patrón histórico:** `py -3.14 -m venv .venv`; ` .\.venv\Scripts\Activate.ps1`; comprobación asertiva con `pathlib`, `sys.version_info`, `sys.executable`, `sys.prefix` y `sys.base_prefix`.
- **Evidencia/aceptación:** `sys.version=3.14.10`, ejecutable `<ruta del entorno virtual>\Scripts\python.exe`, prefijos distintos, aserciones código 0. Windows 11 no probado independientemente. Evidencia histórica en registro anterior de `plan.md`; no repetir salidas personales.
- **Parada:** discrepancia de versión/ruta/prefijos. No inferir que el entorno sigue presente ahora.

### T-04 — Unificar manifiesto, verificar plugin y revisar artefactos antiguos [x]
- **Estado (2026-11-07): COMPLETADA; Reviewer APROBADO.** La resolución e integración funcional temporal en Windows 10 pasó. El usuario autorizó la opción 1: enmendar `spec.md` a v1.4, consolidar el manifiesto único y retirar los tres artefactos legacy. Todo ello se ejecutó y Reviewer emitió APROBADO; T-04 queda `[x]`. **Nota de vigencia:** la versión de Django del manifiesto cambió a `6.0.9` por enmienda autorizada en T-07 (2026-11-07); esta evidencia histórica corresponde a la resolución inicial con `6.1.3` y se conserva como registro.
- **Precondición:** el usuario aprobó spec v1.4 (enmienda de plataformas), plan/tareas y autorización de implementación; Reviewer aprobó plan/tareas. La consolidación y el retiro de artefactos se ejecutaron bajo autorización explícita del usuario (2026-11-07), tras verificar que las versiones y metadata estaban documentadas. No se instaló nada ni se inició T-05.
- **Alcance/resultado:** investigar existencia del paquete `langchain-deepseek`, metadatos/restricciones y resolución conjunta del conjunto directo completo para Python 3.14.10 en el entorno temporal de Windows 10 x64/CPython estándar. No exige prueba independiente Windows 10 y Windows 11 ni establece una lista cerrada de sistemas operativos. Documentar las plataformas efectivamente verificadas; la evidencia funcional disponible es Windows 10. No afirmar compatibilidad universal. El manifiesto único `requirements.txt` quedó consolidado con las nueve dependencias directas y sin locks. Checklist CA-10 con rutas relativas y evidencia.
- **Comandos/patrones:** se documentaron `Requires-Python`, `Requires-Dist`, marcadores activos, restricciones directas/transitivas y cierre completo seleccionado (57 distribuciones); se registraron `pip install` temporal, `pip check`, `pip freeze` y metadata del entorno. Plataforma real: Windows 10 x64, CPython 3.14.10. No se infiere Windows 11 ni otros OS. La instalación en `.venv` de proyecto sigue sujeta a T-05.
- **Evidencia/aceptación:** existencia del plugin; lista directa y cierre transitivo completo con versiones; metadata `Requires-Python`/`Requires-Dist` y edges/markers relevantes; resolución conjunta y `pip check` exitosos para Python 3.14.10 en entorno Windows 10 x64 documentado; prueba funcional/imports/grafo reportada separadamente y sin llamada API. Windows 11 figura como no probado, sin que eso bloquee por sí solo; no declarar universalidad. El manifiesto único y el checklist CA-10 están completos; Reviewer emitió APROBADO.
- **Parada:** si falla resolución o se observa incompatibilidad, consultar sin sustituir. Si no puede documentarse el cierre/metadata transitiva, registrar bloqueo. No instalar en `.venv`, no iniciar T-05, no conectar DB. No reintroducir locks ni grupos separados.

**Registro de investigación y prueba (2026-11-06):** Planner consultó fuentes públicas y encontró `langchain-deepseek` 1.1.1 publicado en PyPI, `Requires-Python >=3.10.0,<4.0.0`, dependencias `langchain-core >=1.4.7,<2.0.0` y `langchain-openai >=1.3.1,<2.0.0`, y wheel `py3-none-any`. Fuentes: <https://pypi.org/pypi/langchain-deepseek/json>, <https://pypi.org/project/langchain-deepseek/1.1.1/>, <https://docs.langchain.com/oss/python/integrations/chat/deepseek>, <https://docs.langchain.com/oss/python/langchain/install>. La etiqueta universal y el rango de Python no demuestran compatibilidad transitiva o funcionamiento en Windows.

Implementer probó sin modificar `.venv` del proyecto en un entorno temporal aislado `$TEMP/opencode/t04-validation/venv`. Plataforma: Windows 10 x64 build 10.0.19045, CPython 3.14.10 64 bits, pip 26.2.2. Comando ejecutado (código 0):

```powershell
& $python -m pip install 'Django==6.1.3' 'mysqlclient==2.3.0' 'pytest==9.2.0' 'pytest-django==4.14.0' 'ruff==0.17.4' 'pydantic==2.14.3' 'langchain==1.4.9' 'langgraph==1.2.20' 'langchain-deepseek==1.1.1'
& $python -m pip check
& $python -m pip freeze
```

`pip check` → `No broken requirements found` (código 0); freeze (código 0). **Nota de vigencia (2026-11-07):** este freeze histórico corresponde a Django 6.1.3; la resolución vigente es Django 6.0.9 (T-07), con el resto de versiones sin cambios:

```text
annotated-types==0.8.0
anyio==4.16.0
asgiref==3.13.0
certifi==2026.10.23
charset-normalizer==3.5.2
colorama==0.4.6
distro==1.9.0
Django==6.1.3
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.0
httpx==0.28.1
httpx2==2.16.0
idna==3.20
iniconfig==2.3.1
jiter==0.19.0
jsonpatch==1.44
jsonpointer==3.10
langchain==1.4.9
langchain-core==1.7.6
langchain-deepseek==1.1.1
langchain-openai==1.7.4
langchain-protocol==0.0.21
langgraph==1.2.20
langgraph-checkpoint==4.3.1
langgraph-prebuilt==1.1.1
langgraph-sdk==0.4.14
langsmith==0.14.17
mysqlclient==2.3.0
openai==3.46.0
orjson==3.13.0
ormsgpack==1.13.0
packaging==26.3
pluggy==1.7.0
pydantic==2.14.3
pydantic_core==2.50.4
Pygments==2.21.0
pytest==9.2.0
pytest-django==4.14.0
PyYAML==6.0.3
regex==2026.11.7
requests==2.34.2
requests-toolbelt==1.0.0
ruff==0.17.4
sniffio==1.3.1
sqlparse==0.6.1
tenacity==9.2.1
tiktoken==0.14.0
truststore==0.10.5
typing-inspection==0.4.5
typing_extensions==4.16.0
tzdata==2026.6
urllib3==2.8.0
uuid_utils==0.19.0
websockets==17.4
xxhash==4.0.2
zstandard==0.25.0
```

**Cierre transitivo y restricciones de metadata (entorno real Windows 10 x64, CPython 3.14.10):** se consultó `importlib.metadata` en el entorno temporal instalado y se evaluaron los marcadores de entorno para CPython 3.14 sobre Windows. La siguiente lista cubre las distribuciones del `pip freeze` (57 paquetes) y sus `Requires-Python` y `Requires-Dist` activos; las dependencias condicionadas por extras no solicitados se excluyen de las aristas activas, pero sus marcadores están en la metadata publicada. `pip check` confirmó que no hay requisitos rotos. Los nombres/constraints se preservan como publicados.

```text
annotated-types==0.8.0 | Python >=3.10 | —
anyio==4.16.0 | Python >=3.10 | idna>=2.8; typing_extensions>=4.16.0; python_version<3.15
asgiref==3.13.0 | Python >=3.11 | —
certifi==2026.10.23 | Python >=3.7 | —
charset-normalizer==3.5.2 | Python >=3.7 | —
colorama==0.4.6 | Python >=2.7 (except 3.0–3.6) | —
distro==1.9.0 | Python >=3.6 | —
Django==6.1.3 | Python >=3.12 | asgiref>=3.9.1; sqlparse>=0.5.0; tzdata; sys_platform==win32
h11==0.16.0 | Python >=3.8 | —
httpcore==1.0.9 | Python >=3.8 | certifi; h11>=0.16
httpcore2==2.16.0 | Python >=3.11 | h11>=0.16; truststore>=0.10
httpx==0.28.1 | Python >=3.8 | anyio; certifi; httpcore==1.*; idna
httpx2==2.16.0 | Python >=3.11 | anyio>=4.10; httpcore2==2.16.0; idna>=3.18; truststore>=0.10 (not emscripten)
idna==3.20 | Python >=3.9 | —
iniconfig==2.3.1 | Python >=3.10 | —
jiter==0.19.0 | Python >=3.11 | —
jsonpatch==1.44 | Python >=3.10 | jsonpointer>=3.8
jsonpointer==3.10 | Python >=3.10 | —
langchain==1.4.9 | Python >=3.10,<4 | langchain-core>=1.7.5,<2; langgraph>=1.2.12,<1.3; pydantic>=2.7.4
langchain-core==1.7.6 | Python >=3.10,<4 | certifi>=2026.10.19; httpx>=0.23; jsonpatch>=1.33; langchain-protocol>=0.0.20; langsmith>=0.14.9,<1; packaging>=23.2; pydantic>=2.7.4,<3; pyyaml>=5.3; tenacity>=8.1,!=8.4.0; typing-extensions>=4.7; uuid-utils>=0.12
langchain-deepseek==1.1.1 | Python >=3.10,<4 | langchain-core>=1.4.7,<2; langchain-openai>=1.3.1,<2
langchain-openai==1.7.4 | Python >=3.10,<4 | certifi>=2024.6.2; langchain-core>=1.7.5,<2; openai>=2.45; tiktoken>=0.7
langchain-protocol==0.0.21 | Python >=3.10,<4 | typing-extensions>=4.13,<5
langgraph==1.2.20 | Python >=3.10 | langchain-core>=1.4.7,<2; langgraph-checkpoint>=4.3,<5; langgraph-prebuilt>=1.1,<1.2; langgraph-sdk>=0.4.6,<0.5; pydantic>=2.7.4; xxhash>=3.5
langgraph-checkpoint==4.3.1 | Python >=3.10 | langchain-core>=0.2.38; ormsgpack>=1.12
langgraph-prebuilt==1.1.1 | Python >=3.10 | langchain-core>=1.3.1; langgraph-checkpoint>=2.1,<5
langgraph-sdk==0.4.14 | Python >=3.10 | httpx>=0.25.2; langchain-core>=1.4,<2; langchain-protocol>=0.0.15; orjson>=3.11.5; websockets>=14
langsmith==0.14.17 | Python >=3.10 | anyio>=3.5,<5; distro>=1.7,<2; httpx2>=2,<3; orjson>=3.9.14 (not PyPy); packaging>=23.2; pydantic>=2,<3; requests-toolbelt>=1; requests>=2; sniffio; typing-extensions>=4.14,<5; uuid-utils>=0.12,<1; websockets>=15; xxhash>=3; zstandard>=0.23
mysqlclient==2.3.0 | Python >=3.10 | —
openai==3.46.0 (transitiva) | Python >=3.10 | anyio>=4.10,<5; httpx2>=2.12,<3; jiter>=0.16,<1; pydantic>=1.10.13,<3 (except 2.0–2.3); sniffio; typing-extensions>=4.14,<5
orjson==3.13.0 | Python >=3.10 | —
ormsgpack==1.13.0 | Python >=3.11 | —
packaging==26.3 | Python >=3.9 | —
pluggy==1.7.0 | Python >=3.10 | —
pydantic==2.14.3 | Python >=3.10 | annotated-types>=0.6; pydantic-core==2.50.4; typing-extensions>=4.16; typing-inspection>=0.4.4
pydantic_core==2.50.4 | Python >=3.10 | typing-extensions>=4.16
Pygments==2.21.0 | Python >=3.9 | —
pytest==9.2.0 | Python >=3.10 | colorama>=0.4 (win32); iniconfig>=2; packaging>=24; pluggy>=1.6,<2; pygments>=2.15
pytest-django==4.14.0 | Python >=3.10 | pytest>=7
PyYAML==6.0.3 | Python >=3.8 | —
regex==2026.11.7 | Python >=3.11 | —
requests==2.34.2 | Python >=3.10 | charset_normalizer>=2,<4; idna>=2.5,<4; urllib3>=1.26,<3; certifi>=2023.5.7
requests-toolbelt==1.0.0 | Python >=2.7 (except 3.0–3.3) | requests>=2.0.1,<3
ruff==0.17.4 | Python >=3.7 | —
sniffio==1.3.1 | Python >=3.7 | —
sqlparse==0.6.1 | Python >=3.10 | —
tenacity==9.2.1 | Python >=3.10 | —
tiktoken==0.14.0 | Python >=3.9 | regex; requests
truststore==0.10.5 | Python >=3.10 | —
typing-inspection==0.4.5 | Python >=3.10 | typing-extensions>=4.15
typing_extensions==4.16.0 | Python >=3.9 | —
tzdata==2026.6 | Python >=2 | —
urllib3==2.8.0 | Python >=3.10 | —
uuid_utils==0.19.0 | Python >=3.10 | —
websockets==17.4 | Python >=3.11 | —
xxhash==4.0.2 | Python >=3.9 | —
zstandard==0.25.0 | Python >=3.9 | —
```

Esto documenta las restricciones activas de la resolución observada en el intérprete/plataforma probados; no es un lock, no fija futuras resoluciones y no demuestra soporte en otros sistemas. **Nota de vigencia (2026-11-07):** la fila de Django corresponde a 6.1.3; la resolución vigente usa 6.0.9, con `Requires-Python >=3.12` y las mismas restricciones `asgiref>=3.9.1`, `sqlparse>=0.5.0` y `tzdata` (win32).

Imports correctos (código 0): `langchain_deepseek`, `langchain`, `langchain_core`, `langchain_openai`, `langgraph`, `langgraph.graph`, `pydantic`, `django`, `MySQLdb`, `pytest` y `ruff`. Smoke test: `ChatDeepSeek(model='deepseek-chat', api_key='<clave-ficticia-en-memoria>')` solo en memoria; StateGraph con nodo diferido compiló como `CompiledStateGraph`, código 0. El nodo no se ejecutó y no hubo llamadas a API ni conexiones MySQL. El primer intento del smoke test dio código 1 por error de construcción del `TypedDict` (`type() doesn't support MRO entry resolution`); se corrigió únicamente el comando y la repetición pasó con código 0. La consulta de metadata confirmó extensiones CPython 3.14 de mysqlclient y pydantic-core.

El dictamen Reviewer **NO APROBADO** previo respondía al criterio anterior que exigía Windows 11. El usuario autorizó la opción 1: enmienda de `spec.md` a v1.4, consolidación del manifiesto único y retiro de los artefactos legacy. La consolidación se ejecutó y Reviewer emitió APROBADO. No se afirma que Windows 11 haya sido probado ni se inició T-05.

**Checklist CA-10 — inventario por rutas relativas (2026-11-07):**

| Artefacto | Estado | Evidencia |
|---|---|---|
| `specs/000-project-bootstrap/spec.md` | [x] enmendado a v1.4 | Solo criterio de plataformas; alcance funcional sin cambios; sin rutas absolutas de perfil |
| `specs/000-project-bootstrap/plan.md` | [x] sincronizado con v1.4 | Criterio de plataforma, consolidación y límites de atribución |
| `specs/000-project-bootstrap/tasks.md` | [x] sincronizado con v1.4 | T-04, cierre transitivo de 57 paquetes y este checklist |
| `specs/000-project-bootstrap/platform-criteria-proposal.md` | [x] eliminado (2026-11-07) | Orden explícita del usuario; contenido útil incorporado en plan/tareas |
| `requirements.txt` | [x] consolidado | Nueve dependencias directas verificadas; sin grupos separados ni locks |
| `requirements-ai.txt` | [x] retirado (2026-11-07) | Versiones y metadata cubiertas por el freeze documentado y el manifiesto único |
| `requirements-win-py314.lock.txt` | [x] retirado (2026-11-07) | Versiones cubiertas por el freeze; hashes no requeridos por la estrategia sin locks |
| `requirements-ai-win-py314.lock.txt` | [x] retirado (2026-11-07) | Versiones cubiertas por el freeze; hashes no requeridos por la estrategia sin locks |
| `README.md` | [x] revisado, no modificado | Sin rutas absolutas de perfil ni datos personales detectados |
| `MEMORY.md` | [ ] pendiente | Contiene estado desactualizado (CONSTITUTION.md y specs ya existen); no se modifica en esta corrección |

Los `[x]` documentan la consolidación y limpieza ejecutadas. T-04 aprobada por Reviewer; no se inició T-05.

**Consolidación y retiro verificados (2026-11-07):** `requirements.txt` contiene las nueve dependencias directas verificadas. Antes de retirar `requirements-ai.txt` y los dos locks se comprobó que las 57 versiones del freeze documentado cubren todas las versiones de esos artefactos; los 71 hashes SHA-256 de los locks no se trasladaron porque la estrategia aprobada excluye locks. El manifiesto no autoriza instalación.

### T-05 — Instalar dependencias del manifiesto único [x]
- **Estado (2026-11-07): COMPLETADA; Reviewer APROBADO.** El usuario autorizó T-05. La instalación del manifiesto completo en `.venv` terminó con código 0, `pip check` pasó, las nueve dependencias directas coinciden exactamente y Reviewer emitió APROBADO; T-05 `[x]`.
- **Precondición:** plan y tareas aprobados por usuario y autorización explícita previa de implementación según AGENTS §5; T-02–T-04 satisfactorias, plugin incluido y compatibilidad demostrada; `.venv` verificado. Aprobación de la especificación/plan por sí sola no autoriza instalar.
- **Alcance/resultado:** instalar el conjunto completo de dependencias directas base+IA del único `requirements.txt` dentro de `.venv`; no instalar subconjunto excluyendo IA y no usar otro manifiesto. Pydantic queda instalado, sin validación funcional de negocio ni llamadas IA.
- **Comando exacto:** con el intérprete del entorno (`.\\.venv\\Scripts\\python.exe`), ejecutar `python -m pip install -r requirements.txt`; después, por separado y con el mismo intérprete, `python -m pip check` y registrar versiones resueltas (`python -m pip list --format=freeze`).
- **Evidencia/aceptación:** intérprete dentro de `.venv`, versión 3.14.10; comando, salida/código, versiones reales, `pip check` satisfactorio y correspondencia con manifiesto. No revelar secretos.
- **Parada:** falta cualquier gate, T-04 sin demostrar, resolución incompatible, intérprete externo, fallo instalación/check o cambio no autorizado del manifiesto; detener y reportar.
- **Registro de ejecución (2026-11-07):** prechecks en `main` sincronizada (`origin/main...HEAD` = `0 0`), intérprete `.venv\Scripts\python.exe` 3.14.10 (`sys.prefix` ≠ `sys.base_prefix`), pip 26.2.2 y manifiesto de nueve directas sin cambios. El primer `pip install -r requirements.txt` superó el timeout de 600 s de la herramienta tras instalar las dependencias base; no hubo error de pip ni conflicto. Se reejecutó el mismo comando autorizado y terminó con código 0: `Successfully installed langchain-1.4.9 langchain-core-1.7.6 langchain-deepseek-1.1.1 langchain-openai-1.7.4 langgraph-1.2.20 langgraph-checkpoint-4.3.1 langgraph-prebuilt-1.1.1 langgraph-sdk-0.4.14 langsmith-0.14.17 openai-3.46.0`. No se instaló nada fuera del manifiesto ni se sustituyó dependencia. `pip check` → `No broken requirements found.`, código 0. Correspondencia directa 9/9 exacta: Django 6.1.3, mysqlclient 2.3.0, pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.4, Pydantic 2.14.3, LangChain 1.4.9, LangGraph 1.2.20 y langchain-deepseek 1.1.1. Imports de los nueve directos y de `langchain_deepseek`/`langgraph` correctos, código 0. Ruff → `All checks passed!`, código 0 (sin archivos Python todavía); sin pruebas de negocio aplicables. Freeze completo: 58 distribuciones, incluido `pip`, listadas abajo. No se conectó a MySQL, no hubo migraciones y no se inició T-06. **Nota de vigencia (2026-11-07):** la versión vigente de Django es 6.0.9 desde la enmienda autorizada en T-07; el resto del freeze se mantiene.
- **Freeze del entorno (58 distribuciones):** `annotated-types==0.8.0`, `anyio==4.16.0`, `asgiref==3.13.0`, `certifi==2026.10.23`, `charset-normalizer==3.5.2`, `colorama==0.4.6`, `distro==1.9.0`, `Django==6.1.3`, `h11==0.16.0`, `httpcore==1.0.9`, `httpcore2==2.16.0`, `httpx==0.28.1`, `httpx2==2.16.0`, `idna==3.20`, `iniconfig==2.3.1`, `jiter==0.19.0`, `jsonpatch==1.44`, `jsonpointer==3.10`, `langchain==1.4.9`, `langchain-core==1.7.6`, `langchain-deepseek==1.1.1`, `langchain-openai==1.7.4`, `langchain-protocol==0.0.21`, `langgraph==1.2.20`, `langgraph-checkpoint==4.3.1`, `langgraph-prebuilt==1.1.1`, `langgraph-sdk==0.4.14`, `langsmith==0.14.17`, `mysqlclient==2.3.0`, `openai==3.46.0`, `orjson==3.13.0`, `ormsgpack==1.13.0`, `packaging==26.3`, `pip==26.2.2`, `pluggy==1.7.0`, `pydantic==2.14.3`, `pydantic_core==2.50.4`, `Pygments==2.21.0`, `pytest==9.2.0`, `pytest-django==4.14.0`, `PyYAML==6.0.3`, `regex==2026.11.7`, `requests==2.34.2`, `requests-toolbelt==1.0.0`, `ruff==0.17.4`, `sniffio==1.3.1`, `sqlparse==0.6.1`, `tenacity==9.2.1`, `tiktoken==0.14.0`, `truststore==0.10.5`, `typing_extensions==4.16.0`, `typing-inspection==0.4.5`, `tzdata==2026.6`, `urllib3==2.8.0`, `uuid_utils==0.19.0`, `websockets==17.4`, `xxhash==4.0.2`, `zstandard==0.25.0`. **Nota de vigencia (2026-11-07):** este freeze histórico lista Django 6.1.3; la resolución vigente es Django 6.0.9 (T-07).

### T-06 — Configurar Django y archivos de entorno/secretos [x]
- **Estado (2026-11-07): COMPLETADA; Reviewer APROBADO.** Se creó `manage.py` y el paquete `config/` con settings por variables de entorno, `.env.example` con valores vacíos/no utilizables y `.env` local excluido. El check por etiquetas (sin `models`/`database`) pasó sin conectar a MySQL. Reviewer emitió APROBADO; T-06 `[x]`.
- **Precondición:** T-05 satisfactoria; autorización de implementación vigente.
- **Alcance/resultado:** configuración Django mínima; backend operativo exclusivamente MySQL 8.x. Definir variables `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`. Crear `.env.example` sin secretos ni credenciales utilizables, solo nombres y placeholders seguros; crear `.env` local vacío/plantilla no commiteada y excluida de Git. No inventar/completar credenciales: valores solo mediante provisión segura autorizada. No añadir cargador `.env` salvo necesidad aprobada; configurar Django desde entorno del proceso. Ejecutar `django check` sin conexión DB.
- **Comandos/patrones:** en Django 6.1 el `check` completo ejecuta comprobaciones de modelos contra todas las bases y accede a MySQL; por eso T-06 usa `python manage.py check` con etiquetas que excluyen `models` y `database`, sin conexión. El check completo se difiere a T-07/T-08 con acceso de solo lectura autorizado. Inspección de configuración, archivos y regla de exclusión sin imprimir valores sensibles; confirmar que `.env` no está versionado y `.env.example` no tiene secretos.
- **Evidencia/aceptación:** check y código; backend Django configurado MySQL; nombres de variables y placeholders documentados; `.env` local vacío/plantilla y exclusión efectiva, sin valores expuestos; sin SQLite operativo.
- **Parada:** check falla, secreto expuesto, `.env` versionable, credencial inventada o backend SQLite; corregir dentro del alcance aprobado y revisar exposición antes de avanzar. No conectarse a DB en T-06; la excepción documentada del check por etiquetas está en `Comandos/patrones` y el check completo se difiere a T-07/T-08.
- **Registro de ejecución (2026-11-07):** prechecks en `main` sincronizada (`origin/main...HEAD` = `0 0`), intérprete `.venv` 3.14.10, `pip check` sin problemas y Django 6.1.3. Se crearon `manage.py` y `config/` (`__init__.py`, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`); `DJANGO_SETTINGS_MODULE=config.settings`. Settings lee las ocho variables de entorno del proceso y no contiene credenciales. `DATABASES["default"]["ENGINE"]` = `django.db.backends.mysql`, sin SQLite. `.env.example` contiene solo nombres y valores vacíos/placeholders no utilizables; `.env` local es plantilla vacía, excluida por `.gitignore` (`.env`) y no rastreada; `!.env.example` la hace versionable. No se añadió cargador `.env` ni dependencia. El `check` completo de Django 6.1 ejecuta comprobaciones de modelos contra todas las bases y abre conexión MySQL para introspección (`has_native_uuid_field` → `mysql_server_info`); se reprodujo el intento con marcadores (`Access denied`), confirmando el comportamiento documentado de 6.1. Con autorización del usuario se ejecutó el check por etiquetas excluyendo `models` y `database`: `python manage.py check --tag admin --tag caches --tag commands --tag compatibility --tag files --tag mail --tag security --tag staticfiles --tag templates --tag translation --tag urls` → `System check identified no issues (0 silenced).`, código 0, sin conexión. Las comprobaciones de modelos/DB quedan diferidas a T-07/T-08 con acceso de solo lectura autorizado. Inspección de settings: `ENGINE=django.db.backends.mysql`, `NAME`/`USER`/`PASSWORD` presentes desde entorno, `HOST=127.0.0.1`, `PORT=3306`, sin SQLite. Ruff → `All checks passed!`, código 0. **Desviación detectada y resuelta:** el `check` completo intentó una conexión no autenticada que falló con `Access denied`, sin acceso a datos ni uso de credenciales reales; se reportó al usuario y este autorizó el check por etiquetas sin conexión. `.gitignore` se versiona en esta tarea para que la exclusión de `.env` quede garantizada por el repositorio. No se accedió a datos, no hubo migraciones y no se inició T-07. Sin secretos ni rutas personales.

### T-07 — Autorizar, aprovisionar y verificar MySQL (solo lectura) [x]
- **Estado (2026-11-07): COMPLETADA; Reviewer APROBADO.** La tupla autorizada coincide exactamente, el preflight read-only y el check completo pasaron con Django 6.0.9 (enmienda autorizada) y MySQL 8.0.36. Reviewer emitió APROBADO; T-07 `[x]`.
- **Precondición:** T-06; autorización explícita separada del usuario/proyecto para host, puerto, nombre exacto y aprovisionamiento, previa a toda conexión de escritura/migración o prueba con DB. La tupla histórica `127.0.0.1:3306/nexopyme_bootstrap_dev` no reemplaza aprobación/procedencia actual.
- **Alcance/resultado:** base MySQL 8.x local y exclusiva de desarrollo/pruebas creada/aprovisionada para el bootstrap, con procedencia comprobable. Registrar autorización (fecha/aprobador/tupla), evidencia de aprovisionamiento y entorno controlado aprobado conforme AGENTS §7. Comparar configuración Django efectiva con tupla autorizada; no registrar credenciales.
- **Comandos/patrones:** mostrar solo host, puerto y nombre efectivos y comparar igualdad exacta; comando de preflight de conexión estrictamente solo lectura que confirme servidor MySQL 8.x y base seleccionada. No ejecutar migraciones ni pruebas DB. Registrar comando/salida redactada.
- **Evidencia/aceptación:** aprobación explícita, tupla exacta autorizada y efectiva coincidente, evidencia verificable de creación/procedencia y exclusividad, entorno controlado aprobado, preflight read-only exitoso y MySQL 8.x. Sin secretos.
- **Parada:** no hay aprobación para cada componente de la tupla/aprovisionamiento, destino incierto/preexistente sin procedencia, mismatch, preflight fallido, versión distinta, entorno no aprobado. Detener antes de escribir o migrar; no reutilizar automáticamente DB desconocida.
- **Registro de ejecución (2026-11-07):** prechecks en `main` sincronizada (`origin/main...HEAD` = `0 0`), `.venv` Python 3.14.10 y `pip check` sin problemas. Autorización explícita del usuario registrada: MySQL 8.x, versión confirmada 8.0.36, `127.0.0.1:3306/nexopyme_bootstrap_dev`, usuario `nexopyme_user`, base exclusiva de NexoPyme AI. Configuración efectiva comparada con igualdad exacta: `ENGINE=django.db.backends.mysql`, `HOST=127.0.0.1`, `PORT=3306`, `NAME=nexopyme_bootstrap_dev`, `USER=nexopyme_user`, contraseña presente sin exponer; `CONFIG_MATCH=True`. Preflight read-only con MySQLdb directo y `START TRANSACTION READ ONLY`: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `SERVER_PORT=3306`, `SERVER_UUID=9ba1dc5a-6bb1-11ef-b5db-48ba4eb0477b`; `SHOW GRANTS` → `GRANT USAGE ON *.*` y `GRANT SELECT ON nexopyme_bootstrap_dev.*` para `nexopyme_user@localhost`; `SHOW DATABASES` → `information_schema`, `nexopyme_bootstrap_dev`, `performance_schema`; `TABLE_COUNT=0`, `TABLES=[]`; transacción cerrada con `ROLLBACK`; sin escrituras, migraciones ni cambios de permisos; sin secretos. **Bloqueo:** Django 6.1.3 exige MySQL 8.4+ (`minimum_database_version=(8,4)`) y el servidor es 8.0.36; `manage.py check` completo y cualquier conexión ORM fallaban con `NotSupportedError: MySQL 8.4 or later is required (found 8.0.36)`. Django 6.0.x/5.2.x soportan MySQL 8.0.11+. Se detuvo y se consultó al usuario, que autorizó Django 6.0.9. **Enmienda autorizada:** `requirements.txt` cambió de `Django==6.1.3` a `Django==6.0.9`; `pip install -r requirements.txt` → `Successfully installed Django-6.0.9`; `pip check` → `No broken requirements found.`; metadata `Requires-Python >=3.12`, `Requires-Dist: asgiref>=3.9.1`, `sqlparse>=0.5.0`, `tzdata` (win32); backend MySQL con `minimum_database_version=(8,0,11)`, compatible con 8.0.36. La evidencia histórica de T-04 para 6.1.3 se conserva; la resolución vigente es 6.0.9. **Verificación final con Django 6.0.9:** `python manage.py check` completo → `System check identified no issues (0 silenced).`, código 0; verificación read-only vía Django con `START TRANSACTION READ ONLY`: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `AUTHORIZED_SCHEMA_EXISTS=True`, `TABLE_COUNT=0`, `TABLES=[]`, `GRANT USAGE ON *.*` + `GRANT SELECT ON nexopyme_bootstrap_dev.*`, bases visibles `information_schema`/`nexopyme_bootstrap_dev`/`performance_schema`, `VERSION_MATCH_8_0_36=True`, `DATABASE_MATCH=True`, `USER_MATCH=True`, `READ_ONLY_TRANSACTION_COMPLETED=True`, código 0. Sin escrituras, migraciones ni cambios de permisos; sin secretos. **Cierre transitivo de 6.0.9:** idéntico al freeze de T-05; solo cambia Django 6.1.3 → 6.0.9 y `pip check` pasó. **Entorno controlado aprobado:** el usuario autorizó explícitamente la tupla y la base exclusiva de desarrollo/pruebas para el bootstrap; la procedencia de la base se sustenta en esa declaración del usuario, no en evidencia independiente obtenible con permisos `SELECT`. T-07 COMPLETADA; Reviewer emitió APROBADO. T-08 no iniciada.

### T-08 — Aplicar migraciones iniciales autorizadas [x]
- **Precondición:** T-07 completo; inmediatamente antes revalidar autorización, destino efectivo, procedencia y entorno aprobado; autorización de implementación vigente.
- **Alcance/resultado:** aplicar solo migraciones iniciales propias del bootstrap a la base dedicada autorizada mediante Django ORM/migraciones.
- **Comandos/patrones:** repetir comparación exacta de tuple no sensible y preflight MySQL 8.x read-only; solo con éxito `python manage.py migrate` con el intérprete `.venv` y sin banderas. Prohibidos `--fake`, `--fake-initial`, `--run-syncdb`, `--database` distinto de `default` y SQL manual/arbitrario en el camino de la aplicación; la única excepción es la sentencia `GRANT` exacta ejecutada por el DBA según el bullet siguiente.
- **Paso previo de permisos (solo tras autorización explícita):** ejecutar el `GRANT` exacto desde una cuenta administrativa (root/DBA) fuera de la conexión de la aplicación, porque `nexopyme_user` no tiene `GRANT OPTION`: `GRANT SELECT, INSERT, UPDATE, CREATE, ALTER, INDEX, REFERENCES ON nexopyme_bootstrap_dev.* TO 'nexopyme_user'@'localhost';`. Registrar fecha, aprobador y resultado redactado. La aplicación nunca recibe privilegios globales ni `GRANT OPTION`. Esta autorización de escritura es distinta e independiente de la autorización read-only de T-07, con aprobador y fecha propios.
- **Verificación posterior al `GRANT` y previa a `migrate`:** `SHOW GRANTS FOR 'nexopyme_user'@'localhost'` (o `SHOW GRANTS` desde la propia cuenta) debe mostrar exactamente `USAGE ON *.*` y los siete privilegios sobre `nexopyme_bootstrap_dev.*`, sin otros privilegios globales ni sobre otras bases; repetir la comparación exacta de tupla y el preflight read-only inmediatamente antes de migrar.
- **Evidencia/aceptación:** comando/salida/código de preflight y de `migrate` registrados separadamente; destino coincide, operación autorizada y sin errores. Resultado esperado verificable: 18 migraciones aplicadas, 10 tablas (9 + `django_migrations`) y 18 filas en `django_migrations`.
- **Parada:** cualquier gate ausente/mismatch/error/migración inesperada. Prohibidos `flush`, `drop`, reset u operaciones destructivas; no tocar otras bases. MySQL no revierte DDL; con `DROP` excluido, un fallo parcial deja el esquema a medias y la recuperación requiere intervención del DBA con autorización separada; detenerse e informar.
- **Registro de preparación (2026-11-07):** `main` sincronizada (`origin/main...HEAD` = `0 0`), `.venv` Python 3.14.10, `pip check` sin problemas y Django 6.0.9. Entorno controlado aprobado: base dedicada y exclusiva del proyecto, tupla autorizada y servidor MySQL 8.0.36, sin indicios de otras bases de negocio. Preflight read-only repetido antes y después de inspeccionar las migraciones: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `HOST=127.0.0.1`, `PORT=3306`, `CONFIG_MATCH=True`, grants `USAGE ON *.*` + `SELECT ON nexopyme_bootstrap_dev.*`, bases visibles `information_schema`/`nexopyme_bootstrap_dev`/`performance_schema`, `TABLE_COUNT=0`, `TABLES=[]`. Plan real: 18 migraciones (`contenttypes`, `auth`, `admin`, `sessions`). SQL representativo verificado con `sqlmigrate` (sin ejecutar DDL): `CREATE TABLE` (incluida `django_migrations`), `ALTER TABLE ... MODIFY/DROP COLUMN/ADD CONSTRAINT UNIQUE/ADD CONSTRAINT FOREIGN KEY`, `CREATE INDEX` en `sessions.0001`, `UPDATE` en `auth.0011`, `INSERT` en `django_migrations` y `post_migrate`; sin `AddIndex`, `AddConstraint`, `DeleteModel`, `RunSQL`, `DROP TABLE` ni `DELETE`. **Privilegios propuestos:** `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `INDEX`, `REFERENCES` sobre `nexopyme_bootstrap_dev.*`; excluidos `DELETE`, `DROP` y privilegios administrativos por no ser necesarios para el avance y por su carácter destructivo. **Sentencia propuesta, no ejecutada:** `GRANT SELECT, INSERT, UPDATE, CREATE, ALTER, INDEX, REFERENCES ON nexopyme_bootstrap_dev.* TO 'nexopyme_user'@'localhost';`. No se ejecutó `GRANT` ni `migrate` durante la preparación; no se crearon, alteraron ni eliminaron tablas. Revisión inicial del Reviewer: CAMBIOS NECESARIOS (B1–B3); incorporados. Re-revisión del Reviewer: APROBADO (técnico, no sustituye la autorización humana). La ejecución autorizada se registra en el bullet siguiente.
- **Registro de ejecución (2026-11-07):** el usuario del proyecto (vía Build) autorizó formalmente completar T-08 el 2026-11-07; el `GRANT` fue aplicado desde una sesión administrativa en MySQL Workbench y `SHOW GRANTS` confirmó los siete privilegios (`SELECT`, `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `INDEX`, `REFERENCES`) limitados a `nexopyme_bootstrap_dev.*` para `'nexopyme_user'@'localhost'`, más `USAGE ON *.*`, sin `GRANT OPTION` ni privilegios sobre otras bases. Preflight read-only previo: `VERSION=8.0.36`, `DATABASE=nexopyme_bootstrap_dev`, `CURRENT_USER=nexopyme_user@localhost`, `HOST=127.0.0.1`, `PORT=3306`, `CONFIG_MATCH=True`, grants exactos, bases visibles `information_schema`/`nexopyme_bootstrap_dev`/`performance_schema`, `TABLE_COUNT=0`, `TABLES=[]`, `PREFLIGHT_EXIT=0`. Ejecución: `.\.venv\Scripts\python.exe manage.py migrate` (intérprete `.venv`, sin banderas) → 18 migraciones aplicadas (`contenttypes` 2, `auth` 12, `admin` 3, `sessions` 1), `MIGRATE_EXIT=0`; sin `--fake`, `--fake-initial`, `--run-syncdb`, `--database` ni SQL manual. Verificación posterior read-only: preflight con grants sin cambios y `TABLE_COUNT=10`; `django_migrations` con 18 filas, conjunto esperado presente, sin migraciones ni tablas inesperadas o faltantes; `django_content_type`=6, `auth_permission`=24; `READ_ONLY_TRANSACTION_COMPLETED=True`; `VERIFY_EXIT=0`. `showmigrations` → 18 en `[X]`, `SHOWMIGRATIONS_EXIT=0`; `manage.py check` → `System check identified no issues (0 silenced).`, `CHECK_EXIT=0`; `ruff check .` → `All checks passed!`, `RUFF_EXIT=0`. Sin `flush`, `drop`, reset ni migraciones inversas; sin otras bases; sin ampliar privilegios; sin secretos; T-09 no iniciada. No se ejecutó `migrate --check` (corresponde a T-09). T-08 ejecutada, verificada y aprobada por el Reviewer; T-08 `[x]`.

### T-09 — Verificar ausencia de migraciones pendientes [ ]
- **Precondición:** T-08 satisfactorio; revalidar autorización, tuple, procedencia y entorno controlado antes de conexión.
- **Alcance/resultado:** confirmar estado posterior de migraciones sin pendientes, diferenciando esta verificación de `migrate`.
- **Comandos/patrones:** comparación exacta de configuración efectiva; preflight read-only MySQL 8.x; luego `python manage.py migrate --check`.
- **Evidencia/aceptación:** salida/código propio de preflight y `migrate --check`, registrado aparte de T-08; cero pendientes.
- **Parada:** gate DB ausente, mismatch, preflight/check fallido o pendientes. No reset/flush/drop.

### T-10 — Pytest y Ruff con guardas de DB [ ]
- **Precondición:** T-09 satisfactorio; entorno/dependencias autorizados. Si pytest accede a DB, autorización explícita separada de base de pruebas y de sus operaciones de ciclo de vida, con host/puerto/nombre exacto, aprovisionamiento y procedencia demostrables, entorno de pruebas aprobado.
- **Alcance/resultado:** ejecutar pytest y Ruff separadamente. Cualquier base que pytest-django cree/use/modifique/elimine debe ser exclusiva de pruebas y cubierta expresamente por autorización; comprobar nombre efectivo incluyendo `TEST.NAME` y que creación/teardown se limita exactamente al destino autorizado. Nunca inferir autorización por nombre.
- **Comandos/patrones:** `python -m pytest` solo después de obtener configuración DB efectiva, comparar tupla exacta, comprobar entorno/procedencia y ejecutar preflight read-only MySQL 8.x; pytest no se inicia si puede acceder a DB sin todos los controles. Ejecutar aparte `python -m ruff check .`. Confirmar intérprete `.venv`. Si suite no accede a DB, documentar base de esa determinación; aun así no cambiar configuración operativa a SQLite.
- **Evidencia/aceptación:** resultados y códigos separados de pytest y Ruff; resumen, cero fallos y Ruff sin errores. Para DB: autorización, aprobador/fecha, tupla, procedencia, operaciones de ciclo de vida autorizadas, configuración efectiva, preflight y entorno aprobado, sin secretos. Identificar explícitamente si pytest accedió a DB.
- **Parada:** falla prueba/Ruff; destino/servidor no coincide/no es MySQL 8.x; falta gate/procedencia/aprobación de ciclo de vida; posibilidad de afectar otra DB; creación/eliminación no autorizada; uso de SQLite operativo. No ejecutar acción destructiva fuera de DB dedicada aprobada.

### T-11 — Revisar evidencia técnica y trazabilidad [ ]
- **Precondición:** T-02–T-10; resultados efectivamente disponibles.
- **Alcance/resultado:** revisión independiente de evidencia de versión/venv, manifiesto/plugin, Django check, `.env`/ejemplo y exclusión, preflight, `migrate`, `migrate --check`, pytest y Ruff. Verificar secreto ausente, tuplas consistentes y límites de DB.
- **Comandos/patrones:** inspección documental de comando, fecha, código/salida y artefacto por resultado; repetir solo checks no destructivos si autorizado y con gates aplicables.
- **Evidencia/aceptación:** checklist de cada CA/RB con evidencia relativa y estado real; resultados DB separados; discrepancias resueltas o explícitamente pendientes, sin declarar éxito por ausencia de dato.
- **Parada:** evidencia ausente presentada como éxito, secreto expuesto, identidad/procedencia incongruente o incumplimiento; detener y elevar.

### T-12 — Servidor local y `GET /health/` [ ]
- **Precondición:** T-06 y T-10 satisfactorias; implementación incluye endpoint dentro del alcance; servidor exclusivamente local.
- **Alcance/resultado:** respuesta HTTP 200 a `GET /health/`, disponibilidad básica Django, sin negocio ni llamadas IA.
- **Comandos/patrones:** `python manage.py runserver <dirección>:<puerto>`; cliente HTTP `GET http://127.0.0.1:<puerto>/health/` (por ejemplo `curl -i`). No usar hosting remoto.
- **Evidencia/aceptación:** comando, dirección/puerto, método/ruta, estado HTTP 200 y salida no sensible; revisión de que endpoint solo comprueba disponibilidad básica.
- **Parada:** respuesta distinta, lógica fuera de alcance, exposición de secretos o servidor remoto.

### T-13 — Documentar versiones, resultados y checklist [ ]
- **Precondición:** T-02–T-12; documentación de destino dentro del alcance aprobada; evidencias reales disponibles. Para limpieza documental y eliminación de artefactos, aplicar gates específicos de CA-10/T-04 antes de cualquier cambio.
- **Alcance/resultado:** actualizar solo documentación existente contemplada en la especificación y autorizada; registrar Python 3.14.10, dependencias realmente resueltas, comandos/resultados/limitaciones, evidencia por CA y MySQL (fecha, aprobación, tupla y procedencia, sin secretos). Checklist CA-10 por rutas relativas, `[x]`/`[ ]` y evidencia para archivos objetivo y artefactos antiguos. Eliminar solo identificadores personales y rutas absolutas del perfil/home, reemplazando evidencias por rutas relativas o `<ruta del entorno virtual>`. No cambiar nombres del proyecto ni datos técnicos no personales. No editar otros archivos fuera del alcance aprobado.
- **Comandos/patrones:** inspección de documentación y versiones con intérprete `.venv`; comprobar que URLs externas se conservan y referencias locales son relativas; no Git. No reproducir rutas absolutas personales ni secretos.
- **Evidencia/aceptación:** documentación auditable y consistente con ejecución; resultados no ejecutados indicados pendientes; checklist revisado; ningún secreto o dato de cuenta/home. `[x]` solo para limpieza/verificación realmente completada y aprobada como tarea independiente.
- **Parada:** ubicación documental no aprobada, evidencia ausente o riesgo de secreto/expansión; consultar antes de modificar alcance adicional.

## Cobertura de criterios y evidencias

| CA | Tarea(s) responsable(s) | Evidencia de aceptación |
|---|---|---|
| CA-01 | T-02, T-03, T-13 | Versión exacta y prueba negativa; evidencia real y documentación |
| CA-02 | T-03, T-05, T-13 | venv aislado, instalación autorizada desde manifiesto único, versiones |
| CA-03 | T-04, T-05, T-13 | Manifiesto único consolidado; resolución conjunta y cierre transitivo documentados |
| CA-04 | T-06, T-11, T-13 | `.env.example`, `.env` excluido, check separado y no exposición |
| CA-05 | T-07, T-08, T-10 | MySQL 8.x, destino autorizado/procedencia y configuración coincidente |
| CA-06 | T-07–T-11 | preflight, migrate, migrate-check, pytest y resultados separados |
| CA-07 | T-12, T-13 | GET health HTTP 200 local |
| CA-08 | T-13 | Versiones, comandos, evidencias y limitaciones documentadas |
| CA-09 | T-04, T-13 | Manifiesto único, existencia del plugin, cierre transitivo y `pip check` en Windows 10 x64; Windows 11 no probado sin bloqueo propio |
| CA-10 | T-04, T-11, T-13 | Checklist por rutas relativas, estado y evidencia; cambios tras gates |

## Condiciones de cierre

Trazabilidad completa RB-01–RB-10, CA-01–CA-10, tareas y evidencias según matrices anteriores. Cada resultado debe corresponder a ejecución real. Un fallo detiene tareas dependientes. El usuario aprobó spec v1.4, plan/tareas y autorizó la consolidación y el retiro de artefactos legacy. T-04 aprobada por Reviewer; T-05 ejecutada con instalación completa y Reviewer APROBADO. T-06 ejecutada y aprobada por Reviewer. T-07 ejecutada y aprobada por Reviewer: preflight read-only y check completo en verde tras enmienda autorizada a Django 6.0.9. T-08 ejecutada, verificada y aprobada por Reviewer: 18 migraciones aplicadas, 10 tablas y 18 filas en `django_migrations`. Se ejecuta el flujo Git autorizado conforme a `AGENTS.md` §9.
