# ESQUEMA PRINCIPAL:
*JUEGO* (
    anio_olimpiada,
    pais_olimpiada,
    nombre_deportista,
    pais_deportista,
    nombre_disciplina,
    asistente
)

## DEPENDENCIAS(DFs):
DF1: anio_olimpiada -> pais_olimpiada

DF2: nombre_deportista -> pais_deportista

DF3: anio_olimpiada y nombre_deportista -> nombre_deportista

DF4: anio_olimpiada y nombre_deportista -> asistente


## CLAVES CANDIDATAS:
`anio_olimpiada` y `nombre_deportista`
### JUSTIFICACION: 
Se seleccionaron ambas ya que:
 - Se respeta DF1, y DF2.
 - Se evitan redundancias ejemplo: si se seleccionara el nombre del deportista, no podriamos diferenciar a este de otro con el mismo nombre o en que anio participo
 Lo mismo pasa con anio_olimpiada, no podriamos distinguir entre los deportista implicados en ese anio.
Lo mejor seria que cada deportista tenga un ID, pero al no tenerlo, elegimos usar la combinacion de anio_olimpiada + nombre_deportista para identificar de manera unica a cada deportista.

**Conclusion:**
La clave candidata del esquema JUEGO es:
(`anio_olimpiada`, `nombre_deportista`)
debido a que garantiza la unicidad de cada fila en la tabla.

 ## NORMALIZACIONES
- En el esquema original encontramos redundancias, y dependecias funcionales sin organizar.
- 1NF: El esquema cumple con esta regla, ya que todos los valores son atomicos y únicos.
- 2NF: Primero dividimos el esquema en 3 tablas:

 *JUEGOS* (
    anio_olimpiada **PK**,
    pais_olimpiada
 )

 *DEPORTISTA* (
    nombre_deportista **PK**,
    pais_deportista
 )

 *PARTICIPACIONES* (
    anio_olimpiada,
    nombre_deportista,
    nombre_disciplina,
    asistente,
    **PK** (anio_olimpiada, nombre_deportista)
    **FK** (anio_olimpiada) REFERENCES JUEGOS (anio_olimpiada),
    **FK** (nombre_deportista) REFRENCES DEPORTISTA (nombre_deportista)
 )

- 3NF: Cumple con la regla de que no hay dependencias transitivas

## RELACIONES ENTRE TABLAS:
   JUEGOS Y PARTICIPACIONES: RELACION 1:N.
   JUEGOS Y DEPORTISTAS (Por medio de participaciones): N:N.
   DEPORTISTAS Y PARTICIPACIONES: 1:N





