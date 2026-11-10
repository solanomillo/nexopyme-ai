# Especificación funcional 003 — Cuentas y multiempresa — **v1.0**

## 1. Identificación, estado y convenciones

| Campo | Valor |
|---|---|
| Funcionalidad | 003 — Cuentas y multiempresa |
| Artefacto | `specs/003-cuentas-multiempresa/spec.md` |
| Versión | 1.0 |
| Fases SDD | 1 y 2 |
| Autor | Planner |
| Estado | APROBADO — v1.0 aprobada por el usuario el 2026-11-10 |
| Fecha | 2026-11-10 |
| Artefactos activos V1 | 41 RF · 44 CA · 17 RN · 14 RNF · 13 A (10 resueltas, 3 abiertas no bloqueantes) · 8 DA aprobadas |
| Depende de | `CONSTITUTION.md`, `AGENTS.md`, `specs/001-django-project-foundation/spec.md` |
| Consumida por | `specs/002-productos-inventario/spec.md` (A-01 y A-11) y módulos futuros |

**Convenciones de marcado**

- `[F]` firme.
- `[DA-xx]` requisito que depende de una decisión ya aprobada por el usuario en §13.
- `[P-Axx]` provisional: depende de la ambigüedad `A-xx`; no aprobable ni implementable hasta resolverla.
- Los supuestos `S-xx` no son normativos.
- Toda tabla de requisitos (RF, CA, RN, RNF) lleva columna **Estado**.
- **Regla de coherencia:** ningún requisito `[F]` invoca una ambigüedad abierta. Las tres ambigüedades abiertas (`A-09`, `A-10`, `A-13`) son no bloqueantes y afectan solo a valores o extensiones, no al comportamiento central.
- Esta especificación no modifica `specs/002-productos-inventario/`; define las entidades y capacidades que 002 declara consumir.

---

## 2. Objetivo

Definir el comportamiento verificable de cuentas, empresa, membresías, roles y permisos de NexoPyme AI en V1: cada persona con su propia cuenta, un dueño que administra el negocio, empleados con permisos diferenciados según su función, control de acceso a acciones y a información, una sola empresa activa por instalación y aislamiento entre empresas sin excepciones. Esta especificación es la fuente de verdad del comportamiento observable de la etapa (Constitución, principio 2).

---

## 3. Alcance y exclusiones

### 3.1 Incluido

Autenticación con correo y contraseña · sesión y cierre de sesión · resolución del contexto de empresa activa · inicialización idempotente de la instalación · gestión de empleados por el dueño (alta, rol, cambio de rol, desactivación, reactivación, contraseña temporal) · autogestión de contraseña · recuperación del dueño por comando técnico · catálogo único de capacidades · autorización en servidor en vistas y servicios · control de acceso a la información · aislamiento entre empresas · auditoría de negocio y eventos de seguridad · separación entre el panel comercial y Django Admin · estados de interfaz (vacío, error, carga, confirmación, éxito) con accesibilidad.

### 3.2 Exclusiones

| Exclusión | Estado |
|---|---|
| Varias empresas activas, selector o cambio de empresa | Firme (`DA-03`) |
| Registro público de cuentas | Firme (`DA-04`, `DA-05`) |
| Pantalla pública de instalación | Firme (`DA-04`): la inicialización es un comando técnico |
| Invitaciones por correo, SMTP, recuperación automática de contraseña | Firme (`DA-05`, `DA-06`) |
| SSO, MFA, OAuth y proveedores externos de identidad | Firme |
| Roles personalizados editables desde la interfaz | Firme (`DA-02`) |
| Permisos por objeto o por registro | Firme |
| Más de un rol por membresía en V1 | Firme (`DA-02`) |
| Transferencia de la propiedad del negocio | Firme: fuera de V1; requiere especificación propia |
| Facturación, planes o suscripciones | Firme |
| Portal de administración de Django expuesto al usuario final | Firme (`RNF-02`, `RN-16`) |
| Borrado físico de usuarios, memberships, auditoría o eventos de seguridad | Firme |
| Módulos de productos, inventario, compras, ventas, finanzas y reportes | Firme: otras especificaciones; aquí solo se definen las capacidades que consumen |
| API pública, app móvil, multi-idioma y multi-moneda | Firme |

### 3.3 Superficies previstas (orientativas para el plan)

Acceso · recuperación asistida · perfil y cambio de contraseña · listado de usuarios · alta de empleado · detalle y edición de rol · desactivación de empleado · reactivación de empleado · regeneración de contraseña temporal · consulta de auditoría y eventos de seguridad · recuperación técnica del dueño · datos del negocio · pantalla de acceso denegado · pantalla de recurso inexistente.

---

## 4. Actores, escenarios y capacidades

### 4.1 Actores

| Actor | Definición |
|---|---|
| Dueño | Persona con rol `dueno`; administra el negocio, sus usuarios y su configuración. Exactamente uno activo en V1. |
| Encargado | Empleado con rol `encargado`; opera el negocio sin gestionar usuarios ni configuración. |
| Operador | Empleado con rol `operador`; registra movimientos y consulta información operativa. |
| Consulta | Empleado con rol `consulta`; solo lectura. |
| Superusuario técnico | Cuenta de operación técnica con acceso a Django Admin; no es una cuenta comercial. |
| Visitante | Persona sin sesión. |
| Módulo consumidor | Componente de otro módulo que autoriza operaciones mediante el servicio de capacidades. |

### 4.2 Escenarios (cobertura no exhaustiva)

| ID | Escenario |
|---|---|
| SC-01 | El dueño accede al panel con su correo y contraseña. |
| SC-02 | Un visitante intenta abrir una ruta de negocio y es redirigido al acceso. |
| SC-03 | El dueño crea un empleado con rol `operador` y le entrega una contraseña temporal. |
| SC-04 | El empleado accede por primera vez y el sistema le exige cambiar la contraseña. |
| SC-05 | Un `consulta` intenta abrir el alta de producto y recibe permiso insuficiente. |
| SC-06 | Un `operador` intenta registrar un ajuste de inventario y recibe permiso insuficiente. |
| SC-07 | Una solicitud manipulada incluye el identificador de otra empresa. |
| SC-08 | El dueño cambia el rol de un empleado y el cambio rige en la siguiente solicitud. |
| SC-09 | El dueño desactiva a un empleado que tenía la sesión abierta. |
| SC-10 | El dueño intenta desactivarse siendo el único dueño. |
| SC-11 | El dueño regenera la contraseña temporal de un empleado. |
| SC-12 | Una cuenta comercial intenta abrir Django Admin. |
| SC-13 | Se ejecuta dos veces la inicialización de la instalación. |
| SC-14 | Se revisa la auditoría de cambios de rol y de accesos denegados. |

### 4.3 Matriz de roles y capacidades

| Capacidad | dueño | encargado | operador | consulta |
|---|:--:|:--:|:--:|:--:|
| `producto.consultar` | ✅ | ✅ | ✅ | ✅ |
| `historial.consultar` | ✅ | ✅ | ✅ | ✅ |
| `producto.crear` | ✅ | ✅ | — | — |
| `producto.editar` | ✅ | ✅ | — | — |
| `producto.desactivar` | ✅ | ✅ | — | — |
| `movimiento.entrada` | ✅ | ✅ | ✅ | — |
| `movimiento.salida` | ✅ | ✅ | ✅ | — |
| `movimiento.ajustar` | ✅ | ✅ | — | — |
| `existencia.inicializar` | ✅ | ✅ | — | — |
| `auditoria.consultar` | ✅ | — | — | — |
| `usuarios.gestionar` | ✅ | — | — | — |
| `empresa.configurar` | ✅ | — | — | — |

Los nombres de capacidad son vinculantes y coinciden con `specs/002` §4.3. Los módulos futuros agregan capacidades con el patrón `recurso.accion` sin redefinir roles.

### 4.4 Modelo de acceso a la información

Toda capacidad es de lectura, de escritura o de administración. El defecto es denegar.

| Regla | Comportamiento |
|---|---|
| Lectura gobernada | Sin la capacidad `X.consultar` no se accede al listado, la búsqueda, el detalle ni la exportación de `X`, aunque se escriba la URL directa. |
| Escritura sin lectura total | Una capacidad de escritura no otorga lectura de todo el módulo; las capacidades de lectura se asignan por separado. |
| Agregados y reportes | Heredan la capacidad de lectura de sus datos de origen; no existe una capacidad genérica de «ver todo». |
| Datos sensibles | Los datos sensibles de un módulo futuro reciben su propia capacidad de lectura en lugar de reutilizar la del módulo. |
| Ocultamiento no autoritativo | La interfaz oculta lo que el servidor ya deniega; nunca es la única barrera. |

### 4.5 Modelo conceptual (restricción de diseño)

| Entidad | Contenido | Invariantes |
|---|---|---|
| Empresa | Identificador, nombre, estado, fechas | Exactamente una activa por instalación en V1 |
| Usuario | Cuenta de autenticación con correo único y último acceso | Toda persona tiene su propia cuenta |
| Membresía | Usuario, empresa, rol, estado, fechas | Una por usuario en V1; un rol por membresía |
| Evento de auditoría | Actor, empresa, entidad, acción, resultado, valores anterior y nuevo, fecha | Solo adición; sin secretos |
| Evento de seguridad | Actor interno si existe, empresa del actor si existe, empresa intentada como identificador interno, acción, resultado, fecha | Solo adición; transacción independiente; sin correo tentativo, contraseña ni token. El identificador interno de la empresa intentada no se expone ni constituye un dato de esa empresa |

Las formas concretas de tabla, índices y restricciones pertenecen al plan. La obligatoriedad de `empresa` en toda entidad de negocio es una restricción de diseño vinculante.

---

## 5. Supuestos

| ID | Supuesto |
|---|---|
| S-01 | La instalación parte sin datos operativos de negocio; la empresa se crea en la inicialización. |
| S-02 | La autenticación la provee Django; aquí solo se exige el efecto observable. |
| S-03 | La V1 se ejecuta en un entorno local con MySQL 8.x y un servidor de aplicación. |
| S-04 | No existe infraestructura de correo saliente en V1. |
| S-05 | Los módulos de negocio consumen el servicio de capacidades; no implementan su propia autorización. |
| S-06 | El superusuario técnico ya existe y no es una cuenta comercial. |
| S-07 | Los datos personales se limitan a nombre y correo de los usuarios del negocio. |
| S-08 | La zona horaria y el idioma se rigen por la configuración de la instalación. |

---

## 6. Glosario

| Término | Definición |
|---|---|
| Empresa | Organización propietaria de los datos; unidad de aislamiento |
| Empresa activa | Empresa resuelta desde la membresía del actor para la solicitud en curso |
| Cuenta comercial | Cuenta de una persona del negocio: dueño o empleado |
| Superusuario técnico | Cuenta de operación técnica, ajena a los flujos de negocio |
| Membresía | Vínculo entre un usuario y una empresa, con un rol y un estado |
| Rol | Perfil fijo que determina un conjunto de capacidades |
| Capacidad | Autorización concreta con el patrón `recurso.accion` |
| Acceso a la información | Autorización de lectura sobre datos de un módulo |
| Contexto de empresa | Empresa activa y membresía asociadas a la sesión |
| Contraseña temporal | Credencial de un solo uso que obliga a cambiarla en el primer acceso |
| Recuperación asistida | Nueva contraseña temporal generada por el dueño |
| Auditoría | Registro de solo adición de operaciones de negocio |
| Evento de seguridad | Registro de un rechazo por aislamiento, por capacidad o por credenciales inválidas |
| Panel comercial | Interfaz propia de NexoPyme AI para el dueño y sus empleados |
| Django Admin | Interfaz técnica de Django, reservada a superusuarios técnicos |
| Aislamiento | Garantía de que ninguna operación alcanza datos de otra empresa |

---

## 7. Requisitos funcionales (EARS)

### 7.1 Cuentas y acceso

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-01 | CUANDO una persona envía correo y contraseña válidos y su cuenta y membresía están activas, el sistema DEBE iniciar sesión y fijar el contexto de empresa. | CA-01 | [F][DA-01] |
| RF-02 | SI las credenciales son inválidas, o la cuenta o la membresía está inactiva, ENTONCES el sistema DEBE rechazar el acceso con un mensaje genérico, no revelar si la cuenta existe y registrar el intento fallido. | CA-02 | [F][DA-01] |
| RF-03 | CUANDO un usuario cierra sesión, el sistema DEBE invalidar la sesión y redirigirlo a la pantalla de acceso. | CA-03 | [F] |
| RF-04 | SI una solicitud a una ruta de negocio no tiene sesión válida, ENTONCES el sistema DEBE redirigir a la pantalla de acceso conservando un destino seguro y sin mostrar datos. | CA-04 | [F] |
| RF-05 | MIENTRAS un usuario conserve una contraseña temporal sin cambiar, el sistema DEBE impedir cualquier operación de negocio y exigir el cambio. | CA-05 | [F][DA-05] |
| RF-06 | CUANDO un usuario cambia su propia contraseña, el sistema DEBE exigir la contraseña actual, validar la política vigente y auditar el cambio sin registrar valores. | CA-06 | [F] |
| RF-07 | CUANDO un usuario consulta sus propios datos, el sistema DEBE mostrar solo su cuenta y membresía, sin datos de otros usuarios; SI solicita los datos de otra cuenta de la misma empresa, ENTONCES DEBE responder 403 sin mostrar información. | CA-07 | [F] |

### 7.2 Contexto de empresa y aislamiento

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-08 | CUANDO un usuario autenticado inicia una solicitud operativa, el sistema DEBE resolver la empresa activa desde su membresía y no aceptar identificadores de empresa enviados por el cliente. | CA-08 | [F][DA-03] |
| RF-09 | SI el usuario no tiene membresía activa, o la instalación no tiene empresa activa, ENTONCES el sistema DEBE responder 403 con una pantalla de acceso denegado que no expone datos y ofrece cerrar sesión. | CA-09 | [F] |
| RF-10 | CUANDO el usuario consulta un listado, búsqueda, detalle o agregado, el sistema DEBE devolver únicamente datos de la empresa activa. | CA-10 | [F] |
| RF-11 | SI un usuario solicita un recurso de otra empresa, ENTONCES el sistema DEBE responder 404 con cuerpo y mensaje idénticos a un recurso inexistente. | CA-11 | [F] |
| RF-12 | SI una solicitud operativa incluye un identificador de empresa distinto al del contexto autorizado, ENTONCES el sistema DEBE responder 404 uniforme, no aplicar cambios y registrar un evento de seguridad. | CA-12 | [F] |
| RF-13 | SI una operación intenta vincular entidades de empresas distintas, ENTONCES el sistema DEBE rechazarla antes de persistir el vínculo y sin revelar datos de la otra empresa. | CA-13 | [F] |

### 7.3 Autorización por capacidades

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-14 | SI el rol del actor carece de la capacidad requerida, ENTONCES el sistema DEBE responder 403, no aplicar cambios y mostrar un mensaje de permiso insuficiente. | CA-14 | [F][DA-02] |
| RF-15 | CUANDO se procesa una solicitud, el sistema DEBE comprobar en orden aislamiento, capacidad, estado del recurso, validación de datos, reglas de negocio, persistencia y auditoría. | CA-15 | [F] |
| RF-16 | CUANDO un módulo necesite autorizar una operación, el sistema DEBE ofrecer una verificación única por actor, empresa y capacidad, reutilizada por vistas y servicios. | CA-16 | [F] |
| RF-17 | DONDE la interfaz oculte una acción por falta de capacidad, el sistema DEBE seguir denegándola en servidor. | CA-17 | [F] |
| RF-18 | CUANDO el usuario accede a un listado, búsqueda o detalle, el sistema DEBE exigir la capacidad de lectura correspondiente al recurso. | CA-18 | [F] |
| RF-19 | CUANDO el usuario solicita un agregado o reporte, el sistema DEBE exigir la capacidad de lectura de los datos de origen. | CA-19 | [F] |
| RF-20 | El sistema DEBE mantener un catálogo único de capacidades y roles que los módulos consumen sin redefinirlos. | CA-20 | [F] |

### 7.4 Gestión de empleados

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-21 | CUANDO el dueño crea un empleado con correo, nombre y un rol válido distinto de `dueno`, el sistema DEBE crear la cuenta y la membresía activas, mostrar una contraseña temporal una sola vez y exigir su cambio en el primer acceso. | CA-21 | [F][DA-02][DA-04][DA-05] |
| RF-22 | SI el correo ya está registrado en la instalación, comparando sin distinguir mayúsculas ni espacios laterales, ENTONCES el sistema DEBE rechazar el alta con 400 y error en el campo, sin crear registros parciales. | CA-22 | [F][DA-01] |
| RF-23 | CUANDO el dueño lista usuarios, el sistema DEBE mostrar solo membresías de su empresa con correo, nombre, rol, estado y último acceso, y nunca credenciales. | CA-23 | [F] |
| RF-24 | CUANDO el dueño cambia el rol de un empleado a otro distinto de `dueno`, el sistema DEBE aplicar el nuevo conjunto de capacidades en la siguiente solicitud y auditar los valores anterior y nuevo. | CA-24 | [F][DA-02] |
| RF-25 | CUANDO el dueño desactiva a un empleado, el sistema DEBE impedir nuevas autenticaciones, retirar su acceso en la siguiente solicitud y conservar su historial y su auditoría. | CA-25 | [F] |
| RF-26 | CUANDO el dueño reactiva a un empleado, el sistema DEBE exigir una nueva contraseña temporal y el cambio obligatorio en el primer acceso. | CA-26 | [F][DA-06] |
| RF-27 | CUANDO el dueño regenera la contraseña de un empleado, el sistema DEBE invalidar la anterior, mostrar la nueva una sola vez, exigir el cambio y auditar la operación sin registrar valores. | CA-27 | [F][DA-06] |
| RF-28 | SI una operación resultaría en más de un dueño activo o en ningún dueño activo, ENTONCES el sistema DEBE rechazarla, incluidos el alta con rol `dueno`, el cambio de rol hacia `dueno` y la desactivación o degradación del último dueño. | CA-28 | [F][DA-03] |
| RF-29 | SI un usuario sin capacidad `usuarios.gestionar` intenta crear, modificar o desactivar usuarios, ENTONCES el sistema DEBE responder 403 y no aplicar cambios. | CA-29 | [F] |

### 7.5 Configuración de la empresa

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-30 | CUANDO se ejecuta el comando de gestión de inicialización, el sistema DEBE crear una única empresa activa y su dueño, solicitar la contraseña inicial de forma interactiva sin aceptarla como argumento ni registrarla, exigir su cambio en el primer acceso, y la ejecución repetida DEBE ser idempotente. | CA-30 | [F][DA-04][DA-05] |
| RF-31 | CUANDO el dueño, con capacidad `empresa.configurar`, guarda un nombre de empresa válido, el sistema DEBE persistirlo y auditar el valor anterior y el nuevo. | CA-31 | [F][DA-08] |
| RF-32 | SI se intenta crear una segunda empresa activa en V1, ENTONCES el sistema DEBE rechazarlo. | CA-32 | [F][DA-03] |

### 7.6 Separación entre panel comercial y Django Admin

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-33 | El sistema DEBE ofrecer todas las funciones de negocio en el panel comercial propio, sin depender de Django Admin. | CA-33 | [F] |
| RF-34 | DONDE exista una cuenta comercial, el sistema DEBE impedirle el acceso a Django Admin y no asignarle permisos de personal ni de superusuario. | CA-34 | [F] |
| RF-35 | DONDE exista un superusuario técnico, el sistema DEBE permitirle Django Admin sin convertirlo en cuenta comercial ni otorgarle membresía de negocio. | CA-35 | [F] |
| RF-36 | El sistema DEBE mantener los modelos de negocio y de auditoría fuera de Django Admin como superficie de edición; Django Admin se limita a la operación técnica y no ofrece flujos de creación o cambio de cuentas, roles ni empresa. | CA-36 | [F] |

### 7.7 Auditoría y eventos de seguridad

| ID | Enunciado | CA | Estado |
|---|---|---|---|
| RF-37 | CUANDO se crea, modifica, desactiva o reactiva una cuenta o membresía, el sistema DEBE auditar actor, empresa, sujeto, acción, resultado, valores anterior y nuevo y fecha. | CA-37 | [F][DA-08] |
| RF-38 | CUANDO se rechaza un acceso por capacidad insuficiente, credenciales inválidas o empresa ajena, el sistema DEBE registrar un evento de seguridad en transacción independiente, sin almacenar la contraseña ni el correo introducido. | CA-38 | [F][DA-08] |
| RF-39 | CUANDO un usuario con capacidad `auditoria.consultar` consulta la auditoría o los eventos de seguridad, el sistema DEBE mostrar solo registros de su empresa; los eventos sin actor o con actor de otra empresa no se muestran y el identificador de la empresa intentada nunca se expone. | CA-39 | [F] |
| RF-40 | El sistema DEBE impedir la modificación o el borrado de auditoría y eventos de seguridad desde la aplicación y desde Django Admin, exponerlos a lo sumo en modo de solo lectura para superusuarios técnicos, y no DEBE registrar contraseñas, tokens ni secretos. | CA-40 | [F][DA-08] |
| RF-41 | SI el dueño pierde el acceso, ENTONCES un comando técnico documentado y auditado DEBE generar una contraseña temporal para el dueño con cambio obligatorio, sin exponerla en el panel ni en registros y sin crear cuentas nuevas. | CA-41 | [F] |

---

## 8. Criterios de aceptación

| ID | Criterio | Origen | Estado |
|---|---|---|---|
| CA-01 | Un usuario activo con membresía activa inicia sesión y accede al panel con su empresa activa. | RF-01 | [F] |
| CA-02 | Credenciales inválidas, cuenta inactiva y membresía inactiva producen el mismo mensaje genérico y dejan evento de seguridad. | RF-02 | [F] |
| CA-03 | Cerrar sesión invalida la sesión y redirige al acceso; el botón atrás no recupera datos. | RF-03 | [F] |
| CA-04 | Una ruta de negocio sin sesión redirige al acceso con destino seguro y sin datos. | RF-04 | [F] |
| CA-05 | Con contraseña temporal pendiente, toda ruta de negocio redirige al cambio obligatorio. | RF-05 | [F] |
| CA-06 | El cambio de contraseña exige la actual, aplica la política y audita sin valores. | RF-06 | [F] |
| CA-07 | El perfil muestra solo la cuenta y membresía del propio usuario; abrir el perfil de otra cuenta de la misma empresa responde 403 sin datos. | RF-07 | [F] |
| CA-08 | Una solicitud con `company_id` del cliente se resuelve con la empresa de la sesión y no con el valor enviado; la prueba registra una sola resolución de contexto por solicitud. | RF-08 | [F] |
| CA-09 | Sin membresía activa o sin empresa activa, el sistema responde 403 con pantalla de acceso denegado, sin datos y con opción de cerrar sesión. | RF-09 | [F] |
| CA-10 | Listados, búsquedas, detalles y agregados devuelven solo datos de la empresa activa. | RF-10 | [F] |
| CA-11 | Un recurso de otra empresa responde 404 idéntico al de un recurso inexistente. | RF-11 | [F] |
| CA-12 | Un identificador de empresa inyectado responde 404 uniforme y deja evento de seguridad. | RF-12 | [F] |
| CA-13 | Un vínculo entre entidades de empresas distintas se rechaza antes de persistir. | RF-13 | [F] |
| CA-14 | Un `consulta` recibe 403 en alta de producto y no se persiste nada. | RF-14 | [F] |
| CA-15 | Ante aislamiento y capacidad fallidos a la vez, prevalece el 404 uniforme del aislamiento. | RF-15 | [F] |
| CA-16 | Vista y servicio invocan la misma verificación de capacidad y ambos deniegan por separado. | RF-16 | [F] |
| CA-17 | Una acción oculta en la interfaz sigue denegada al invocarse por URL directa. | RF-17 | [F] |
| CA-18 | Un usuario sin `historial.consultar` recibe 403 en el historial. | RF-18 | [F] |
| CA-19 | Un listado agregado sin la capacidad de lectura de origen responde 403. | RF-19 | [F] |
| CA-20 | Un módulo consume el catálogo sin declarar roles ni capacidades propias divergentes. | RF-20 | [F] |
| CA-21 | El dueño crea un empleado y este accede con la contraseña temporal y el cambio obligatorio. | RF-21 | [F] |
| CA-22 | Un correo duplicado devuelve 400 con error en el campo y no crea cuenta ni membresía. | RF-22 | [F] |
| CA-23 | El listado de usuarios muestra solo la empresa del dueño y ninguna credencial. | RF-23 | [F] |
| CA-24 | Cambiar el rol surte efecto en la siguiente solicitud y la auditoría registra ambos roles. | RF-24 | [F] |
| CA-25 | Un empleado desactivado no inicia sesión y pierde acceso en su siguiente solicitud. | RF-25 | [F] |
| CA-26 | La reactivación exige nueva contraseña temporal y cambio en el primer acceso. | RF-26 | [F] |
| CA-27 | La regeneración invalida la contraseña anterior y no registra valores en auditoría. | RF-27 | [F] |
| CA-28 | El alta con rol `dueno`, el cambio de rol hacia `dueno` y la desactivación o degradación del último dueño se rechazan; la empresa conserva exactamente un dueño activo. | RF-28 | [F] |
| CA-29 | Un `encargado` recibe 403 al intentar gestionar usuarios. | RF-29 | [F] |
| CA-30 | Dos ejecuciones de la inicialización dejan una empresa y un dueño; la contraseña inicial no aparece en argumentos ni registros y exige cambio en el primer acceso. | RF-30 | [F] |
| CA-31 | El cambio de nombre de la empresa se audita con valor anterior y nuevo. | RF-31 | [F] |
| CA-32 | Un intento de crear una segunda empresa activa se rechaza. | RF-32 | [F] |
| CA-33 | Todas las funciones de negocio están disponibles en el panel comercial sin abrir Django Admin. | RF-33 | [F] |
| CA-34 | Una cuenta comercial recibe denegación en `/admin/` y no tiene `is_staff` ni `is_superuser`. | RF-34 | [F] |
| CA-35 | El superusuario técnico accede a `/admin/` y no aparece como membresía de la empresa. | RF-35 | [F] |
| CA-36 | Los modelos de negocio y de auditoría no son editables desde `/admin/`; el Admin no ofrece flujos de alta o cambio de cuentas, roles ni empresa. | RF-36 | [F] |
| CA-37 | Alta, cambio de rol, desactivación, reactivación y cambio de nombre quedan auditados con actor, empresa y fecha. | RF-37 | [F] |
| CA-38 | Un rechazo por capacidad, credencial o empresa ajena deja evento de seguridad aunque la operación se revierta, sin almacenar la contraseña ni el correo introducido. | RF-38 | [F] |
| CA-39 | La consulta de auditoría y de eventos muestra solo registros de la empresa del actor; no expone eventos sin actor ni de otra empresa, ni el identificador de la empresa intentada. | RF-39 | [F] |
| CA-40 | Auditoría y eventos no se modifican ni se borran desde la aplicación ni desde `/admin/`; se exponen a lo sumo en solo lectura y no contienen contraseñas ni tokens. Los logs técnicos están separados de la auditoría y no contienen secretos ni datos sensibles. | RF-40 | [F] |
| CA-41 | El comando técnico de recuperación genera una contraseña temporal para el dueño con cambio obligatorio, sin exponerla en el panel ni en registros y sin crear cuentas nuevas. | RF-41 | [F] |
| CA-42 | La interfaz cumple los criterios de accesibilidad de RNF-07, verificados con teclado, foco, contraste, zoom 200 % y lector de estructura. | RNF-07 | [F] |
| CA-43 | Los estados vacío, error, carga, confirmación y éxito están implementados y validados visualmente en las superficies de la etapa. | RNF-08 | [F] |
| CA-44 | `ruff check .` sin errores y las pruebas automatizadas de la etapa en verde, con cobertura de las reglas firmes. | RNF-09 | [F] |

---

## 9. Reglas de negocio

| ID | Regla | Estado |
|---|---|---|
| RN-01 | En V1 la instalación opera con una única empresa activa y no existe selección ni cambio de contexto. Pueden existir empresas inactivas solo por migración o por fixtures de prueba; la unicidad de la empresa activa se impone en los servicios de negocio y, si el plan lo decide, también en la base de datos. | [F][DA-03] |
| RN-02 | En V1 cada usuario tiene una sola membresía, y debe estar activa para operar. | [F] |
| RN-03 | Cada membresía tiene exactamente un rol. | [F][DA-02] |
| RN-04 | Debe existir exactamente un dueño activo; ninguna operación puede crear un segundo dueño activo ni dejar a la empresa sin dueño activo. | [F][DA-03] |
| RN-05 | Las capacidades de cada rol son fijas; en V1 no existen permisos individuales ni excepciones por usuario. | [F][DA-02] |
| RN-06 | El defecto es denegar: toda capacidad no concedida se considera no otorgada. | [F] |
| RN-07 | La empresa activa proviene de la membresía del actor; ningún dato del cliente puede ampliar ni cambiar ese alcance. | [F][DA-03] |
| RN-08 | Falta de capacidad en recurso propio produce 403; recurso de otra empresa produce 404 uniforme. | [F] |
| RN-09 | El orden de comprobaciones es aislamiento, capacidad, estado del recurso, validación, reglas de negocio, persistencia y auditoría. | [F] |
| RN-10 | Las capacidades se resuelven en cada solicitud; no se almacenan en la sesión. | [F] |
| RN-11 | La desactivación de una cuenta o membresía surte efecto en la siguiente solicitud del usuario. | [F] |
| RN-12 | Toda contraseña temporal es de un solo uso y deja de ser válida al cambiarla. | [F][DA-05] |
| RN-13 | El correo es el identificador de acceso, único en toda la instalación. La comparación elimina espacios laterales y no distingue mayúsculas ni minúsculas, incluida la parte local. | [F][DA-01] |
| RN-14 | Auditoría y eventos de seguridad son de solo adición y no contienen secretos ni datos personales innecesarios. | [F][DA-08] |
| RN-15 | La interfaz no autoriza: solo presenta u oculta lo que el servidor ya resolvió. | [F] |
| RN-16 | Django Admin queda reservado a superusuarios técnicos; las cuentas comerciales no son personal ni superusuarios. | [F] |
| RN-17 | Toda entidad de negocio lleva empresa obligatoria y toda consulta se filtra por ella. | [F] |

---

## 10. Requisitos no funcionales

| ID | Requisito | Verificación | Estado |
|---|---|---|---|
| RNF-01 | Aislamiento sin excepciones: toda vista, servicio y consulta aplica el filtro de empresa, y cada uno tiene al menos una prueba automatizada de acceso cruzado. La segunda empresa de la prueba se crea por fixture u ORM en el entorno de pruebas, fuera de los servicios de negocio, y permanece inactiva. | CA-08 a CA-13, CA-39 | [F][DA-07] |
| RNF-02 | Autorización en servidor para toda operación; el panel comercial es la única superficie de negocio y Django Admin no se expone al usuario final. | CA-14 a CA-19, CA-29, CA-33 a CA-36 | [F] |
| RNF-03 | Protección de sesión, CSRF, cookies y secretos conforme a Django; no se almacenan ni registran credenciales ni tokens. | CA-01 a CA-06, CA-25, CA-27, CA-40 | [F] |
| RNF-04 | Auditoría de solo adición y consultable con la capacidad correspondiente. La retención se define antes del plan (`A-13`). | CA-37 a CA-40 | [F]; retención [P-A13] |
| RNF-05 | Logging técnico separado de la auditoría, sin datos personales sensibles ni secretos; niveles, destinos, formato y retención se definen antes del plan. | CA-38, CA-40 | [F] |
| RNF-06 | El contexto de sesión, membresía y capacidades se resuelve una vez por solicitud, sin consultas repetidas por elemento de la interfaz. | CA-08 (conteo de consultas), CA-10, CA-23 | [F] |
| RNF-07 | Accesibilidad verificable: teclado completo y foco lógico; foco visible; etiquetas programáticas; errores asociados al campo con resumen enlazado; contraste de texto ≥ 4,5:1 y de componentes ≥ 3:1; color no exclusivo; estados anunciados; objetivos táctiles ≥ 24×24 px; tablas con encabezados y `scope`; zoom 200 % sin pérdida; `lang="es"`. | CA-42 | [F] |
| RNF-08 | Validación visual registrada de estados vacío, error, carga, confirmación y éxito. | CA-43 | [F] |
| RNF-09 | Mantenibilidad: separación entre modelo, servicio y vista; type hints; PEP 8; Ruff sin errores; pruebas pytest que cubren las reglas firmes; sin lógica de negocio en plantillas. | CA-44 | [F] |
| RNF-10 | Interfaz en español, con terminología uniforme y mensajes accionables sin detalles técnicos ni nombres de tablas. | CA-42, CA-43 | [F] |
| RNF-11 | Sin dependencias nuevas: autenticación, sesiones y validadores de Django cubren la V1. | CA-44 | [F] |
| RNF-12 | Datos operativos exclusivamente en MySQL 8.x; SQLite solo para el checkpointer de LangGraph, sin datos operativos. | Revisión de configuración en el plan | [F] |
| RNF-13 | El panel comercial no depende de Unfold; Unfold permanece solo en Django Admin para superusuarios técnicos. | CA-34, CA-36 | [F] |
| RNF-14 | Toda modificación de cuentas, roles o empresa se ejecuta mediante servicios de negocio, salvo los datos de prueba del entorno de pruebas; la administración técnica de superusuario no habilita la edición de cuentas, roles ni empresa desde Admin. | CA-21, CA-24, CA-31, CA-36 | [F] |

---

## 11. Aislamiento entre empresas

El aislamiento es obligatorio y no admite excepciones ni confirmación humana (`AGENTS.md` §7; Constitución, principio 5). Se distingue entre comportamiento observable (RF) y restricción de diseño (para el plan).

**11.1 Restricciones de diseño**

1. Toda entidad de negocio lleva identificador de empresa obligatorio.
2. Las relaciones entre entidades se validan intra-empresa en la capa de servicio.
3. El acceso a datos se realiza exclusivamente por ORM, migraciones y servicios; sin SQL manual ni acceso de agentes a la base.
4. El checkpointer de LangGraph no almacena datos operativos y, si se usa, queda sujeto al mismo aislamiento.
5. La base de datos puede reforzar el aislamiento con restricciones propias; su forma pertenece al plan.
6. Ninguna consulta de negocio se ejecuta sin el filtro de empresa resuelto desde la sesión.

**11.2 Comportamiento observable**

Alcance desde la sesión (RF-08), filtro obligatorio (RF-10), 404 uniforme (RF-11), rechazo de identificadores inyectados (RF-12), vínculos intra-empresa (RF-13) y evento de seguridad (RF-12, RF-38).

**11.3 Contexto en V1 y preparación futura**

En V1 cada instalación administra una empresa activa y no ofrece selección ni cambio. La arquitectura debe admitir varias empresas en el futuro sin rediseñar el núcleo: la membresía existe desde V1 y toda entidad lleva empresa. Un futuro flujo de selección requerirá especificación propia y no se anticipa aquí.

**11.4 Verificación**

Cada vista y servicio de la etapa requiere al menos una prueba automatizada de acceso cruzado. La segunda empresa de la prueba se crea por fixture u ORM en el entorno de pruebas, fuera de los servicios de negocio, y permanece inactiva. `DA-07` es una autorización específica de esta etapa: no modifica `specs/001` ni sus guardas (`config/settings_test.py`, `conftest.py`, `pytest.ini`, `tests/test_db_guards.py`) y no habilita otras bases ni usos.

---

## 12. Ambigüedades y decisiones pendientes

| ID | Ambigüedad | Estado | Impacto |
|---|---|---|---|
| A-01 | Identificador de acceso y unicidad del correo | Resuelta: correo único, normalizado, como identificador (`DA-01`) | RF-01, RF-02, RF-21, RF-22, RN-13 |
| A-02 | Cantidad y composición de roles | Resuelta: cuatro roles fijos (`DA-02`) | §4.3, RF-14, RF-20, RF-24, RF-29, RN-03, RN-05 |
| A-03 | Cantidad de dueños y alcance multiempresa | Resuelta: un dueño y una empresa activa (`DA-03`) | RF-08, RF-28, RF-32, RN-01, RN-04, RN-07 |
| A-04 | Inicialización de la instalación | Resuelta: comando idempotente (`DA-04`) | RF-30 |
| A-05 | Alta de empleados y credencial inicial | Resuelta: contraseña temporal (`DA-05`) | RF-05, RF-21, RF-26, RF-27, RN-12 |
| A-06 | Recuperación sin correo saliente | Resuelta: regeneración por el dueño (`DA-06`); la recuperación del propio dueño se resuelve por comando técnico (`RF-41`) | RF-26, RF-27, RF-41 |
| A-07 | Base de datos de pruebas | Resuelta: autorización acotada a esta etapa (`DA-07`) | RNF-01, §11.4 |
| A-08 | Ubicación de la auditoría | Resuelta: módulo compartido `apps/audit` (`DA-08`) | RF-37 a RF-40, RNF-04 |
| A-09 | ¿Campos adicionales de la empresa en V1 (identificación fiscal, contacto, logo)? | Abierta, no bloqueante | RF-31 admite solo nombre; los campos adicionales son aditivos |
| A-10 | Valores concretos de política de contraseñas y duración de sesión | Abierta, no bloqueante | RF-06 y RNF-03 se remiten a la configuración vigente |
| A-11 | ¿Un rol por membresía? | Resuelta: un rol por membresía (`DA-02` y confirmación del usuario) | RN-03 |
| A-12 | ¿Acceso del dueño a Django Admin? | Resuelta: reservado a superusuarios técnicos (confirmación del usuario) | RF-34 a RF-36, RN-16 |
| A-13 | Retención de auditoría y eventos de seguridad | Abierta, no bloqueante | RNF-04; no afecta al comportamiento central |

**Bloqueantes abiertas: ninguna.** Las tres ambigüedades abiertas son no bloqueantes y se resuelven antes del plan.

**Consecuencias conocidas y notas de alcance**

- **Correo único por instalación (`DA-01`):** en un futuro escenario multiempresa, el error de alta por correo duplicado permitiría inferir que ese correo ya existe en otra empresa. En V1 no aplica porque hay una sola empresa; se revisará al especificar multiempresa.
- **Autorización de pruebas (`DA-07`):** es específica de esta etapa y no altera `specs/001` ni sus guardas. El plan debe declarar el alcance exacto de las pruebas con base de datos.
- **Recuperación del dueño (`RF-41`):** se resuelve por comando técnico; no existe recuperación automática ni autoservicio en V1.

---

## 13. Decisiones aprobadas incorporadas

Todas fueron aprobadas por el usuario el 2026-11-10 antes de redactar esta versión.

| ID | Decisión aprobada | Efecto en esta especificación |
|---|---|---|
| DA-01 | Correo electrónico único como identificador de acceso | RF-01, RF-02, RF-22, RN-13; el alta rechaza correos duplicados |
| DA-02 | Cuatro roles fijos: dueño, encargado, operador y consulta | §4.3, RF-14, RF-20, RF-24, RF-29, RN-03, RN-05 |
| DA-03 | Exactamente un dueño y una empresa activa por instalación en V1 | RF-08, RF-28, RF-32, RN-01, RN-04, RN-07 |
| DA-04 | Inicialización mediante comando de gestión idempotente | RF-30, CA-30 |
| DA-05 | Contraseña temporal con cambio obligatorio en el primer acceso | RF-05, RF-21, RN-12 |
| DA-06 | Recuperación mediante nueva contraseña temporal generada por el dueño | RF-26, RF-27 |
| DA-07 | Uso de `nexopyme_bootstrap_test` exclusivamente para pruebas de esta etapa, respetando las guardas | RNF-01, §11.4; no habilita otras bases ni usos |
| DA-08 | Módulo compartido `apps/audit` | RF-37 a RF-41, RNF-04 |

**Confirmaciones adicionales del usuario:** el dueño y los empleados usan el panel propio de NexoPyme AI; Django Admin (Unfold) queda reservado a superusuarios técnicos; las cuentas comerciales no acceden a Django Admin; cada empleado tiene su propia cuenta y permisos según su rol.

---

## 14. Trazabilidad consolidada

| RF | CA | RN | RNF | Estado |
|---|---|---|---|---|
| RF-01 | CA-01 | RN-13 | RNF-03 | [F] |
| RF-02 | CA-02 | RN-14 | RNF-03 | [F] |
| RF-03 | CA-03 | — | RNF-03 | [F] |
| RF-04 | CA-04 | — | RNF-03 | [F] |
| RF-05 | CA-05 | RN-12 | RNF-03 | [F] |
| RF-06 | CA-06 | — | RNF-03 | [F] |
| RF-07 | CA-07 | — | — | [F] |
| RF-08 | CA-08 | RN-07 | RNF-01 | [F] |
| RF-09 | CA-09 | RN-02 | RNF-01 | [F] |
| RF-10 | CA-10 | RN-17 | RNF-01 | [F] |
| RF-11 | CA-11 | RN-08 | RNF-01 | [F] |
| RF-12 | CA-12 | RN-07, RN-08 | RNF-01 | [F] |
| RF-13 | CA-13 | RN-17 | RNF-01 | [F] |
| RF-14 | CA-14 | RN-06, RN-08 | RNF-02 | [F] |
| RF-15 | CA-15 | RN-09 | RNF-01, RNF-02 | [F] |
| RF-16 | CA-16 | RN-06 | RNF-02, RNF-14 | [F] |
| RF-17 | CA-17 | RN-15 | RNF-02 | [F] |
| RF-18 | CA-18 | RN-06 | RNF-01 | [F] |
| RF-19 | CA-19 | RN-06 | RNF-01 | [F] |
| RF-20 | CA-20 | RN-05 | RNF-14 | [F] |
| RF-21 | CA-21 | RN-03, RN-12, RN-13 | RNF-03 | [F] |
| RF-22 | CA-22 | RN-13 | — | [F] |
| RF-23 | CA-23 | RN-07 | RNF-01 | [F] |
| RF-24 | CA-24 | RN-03, RN-05, RN-10 | RNF-14 | [F] |
| RF-25 | CA-25 | RN-11 | RNF-03 | [F] |
| RF-26 | CA-26 | RN-11, RN-12 | RNF-03 | [F] |
| RF-27 | CA-27 | RN-12, RN-14 | RNF-03 | [F] |
| RF-28 | CA-28 | RN-03, RN-04 | — | [F] |
| RF-29 | CA-29 | RN-06 | RNF-02 | [F] |
| RF-30 | CA-30 | RN-01 | RNF-14 | [F] |
| RF-31 | CA-31 | RN-14 | RNF-14 | [F] |
| RF-32 | CA-32 | RN-01 | RNF-14 | [F] |
| RF-33 | CA-33 | RN-16 | RNF-02, RNF-13 | [F] |
| RF-34 | CA-34 | RN-16 | RNF-02, RNF-13 | [F] |
| RF-35 | CA-35 | RN-16 | RNF-13 | [F] |
| RF-36 | CA-36 | RN-16 | RNF-02 | [F] |
| RF-37 | CA-37 | RN-14 | RNF-04 | [F] |
| RF-38 | CA-38 | RN-14 | RNF-04 | [F] |
| RF-39 | CA-39 | RN-14, RN-17 | RNF-01, RNF-04 | [F] |
| RF-40 | CA-40 | RN-14 | RNF-04 | [F] |
| RF-41 | CA-41 | RN-12, RN-14 | RNF-03, RNF-04 | [F] |

Cobertura: 41 RF con 41 CA directos; CA-42, CA-43 y CA-44 verifican los RNF transversales de accesibilidad, validación visual y calidad. Los 14 RNF tienen criterio de verificación declarado en §10.

---

## 15. Preguntas priorizadas para el usuario

**Prioridad 1 — bloquean la aprobación:** ninguna. Las ocho decisiones aprobadas resolvieron todas las ambigüedades bloqueantes.

**Prioridad 2 — no bloqueantes, resolución previa al plan**

1. **A-09** ¿La empresa necesita identificación fiscal, contacto o logo en V1, además del nombre? Recomendación: solo nombre.
2. **A-10** ¿Se aceptan los valores por defecto de Django para política de contraseñas y duración de sesión, documentados por entorno? Recomendación: sí.
3. **A-13** ¿Qué retención se aplica a auditoría y eventos de seguridad? Recomendación: sin purga automática en V1.

La transferencia de propiedad del negocio está excluida de V1 de forma firme (§3.2) y no requiere confirmación adicional.

---

## 16. Registro de cambios

| Versión | Cambio |
|---|---|
| v1.0 (2026-11-10) | Creación de la especificación a partir de la propuesta revisada. Se incorporan las decisiones `DA-01` a `DA-08` y las confirmaciones del usuario sobre el panel comercial y Django Admin. Se cierran A-01 a A-08, A-11 y A-12; quedan abiertas y no bloqueantes A-09, A-10 y A-13. Se adoptan los nombres de capacidad de `specs/002` §4.3 como catálogo vinculante. No se modifica `specs/002`. |
| v1.0 (revisión técnica previa a la aprobación) | Se corrigen los hallazgos del Reviewer: invariante de dueño único verificable (RF-21, RF-24, RF-28, CA-28, RN-04); separación Admin/panel comprobable (RF-36, RF-40, CA-36, CA-40, RNF-02, RNF-14); inicialización por comando con credencial interactiva (RF-30, CA-30); recuperación del dueño (RF-41, CA-41); segunda empresa de prueba creada por fixture inactiva (RNF-01, RN-01, §11.4); trazabilidad RN/RNF completa y CA de accesibilidad, validación visual y calidad (CA-42 a CA-44, §10, §14); eventos de seguridad sin correo tentativo y con visibilidad acotada (RF-38, RF-39, CA-38, CA-39, §4.5); normalización del correo (RN-13); ajustes menores de alcance y trazabilidad; y ajustes editoriales posteriores al dictamen (recuperación del dueño, verificación de RNF transversales, superficies y capacidad `empresa.configurar`). |

---

## 17. Estado de la propuesta

- **Estado:** **APROBADA** v1.0 (2026-11-10); revisión técnica y aprobación humana registradas.
- **Aprobación explícita:** la v1.0 fue aprobada por el usuario el 2026-11-10; la existencia del documento no sustituye esa aprobación.
- **Plan y tareas:** `plan.md` v1.2 y `tasks.md` v1.2 aprobados el 2026-11-10; la implementación avanza por tarea con autorización explícita.
- **Implementación:** T-01 completada; sin modelos, migraciones ni cambios en MySQL; G-2 pendiente de autorización, G-4 autorizado para la etapa y G-1 requerido para la tarea siguiente.
- **Fuera de alcance de esta entrega:** `specs/002-productos-inventario/` permanece intacta; los módulos de negocio quedan para sus propias especificaciones.
