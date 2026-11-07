# Constitución de NexoPyme AI

Principios vinculantes para toda especificación, plan, tarea e implementación. Solo el usuario puede modificarlos y no sustituyen sus aprobaciones.

1. Simplicidad: no se añadirá dependencia, infraestructura ni abstracción sin una necesidad demostrada y registrada en la especificación o el plan, y sin la aprobación que exige AGENTS.md.
2. Fuente de verdad: la especificación aprobada es vinculante; ningún comportamiento observable nuevo se implementará sin figurar en ella.
3. Desacoplamiento: la lógica de negocio no dependerá de la interfaz, la infraestructura ni el proveedor de IA, que será sustituible mediante adaptadores sin modificar la lógica de negocio.
4. Calidad: toda tarea exigirá pruebas ejecutadas y verificaciones de calidad en verde; toda modificación de interfaz requerirá validación visual y funcional registrada, conforme a AGENTS.md.
5. Seguridad: el aislamiento entre empresas no admitirá excepciones; toda operación de IA que modifique datos del negocio exigirá confirmación humana previa; los agentes no accederán directamente a la base de datos ni expondrán secretos; las operaciones relevantes quedarán registradas de forma trazable conforme a AGENTS.md, garantizando la confidencialidad e integridad de los datos.
6. Consistencia: la interfaz cumplirá los criterios de accesibilidad verificables de cada especificación y mantendrá terminología y patrones de interacción uniformes; el idioma y las convenciones se rigen por AGENTS.md.
