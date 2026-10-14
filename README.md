English version: [README.en.md](README.en.md)

# Accidentes de tráfico en Madrid, 2020 · ETL, análisis y modelo

Lleva los datos abiertos de accidentalidad del Ayuntamiento de Madrid de una hoja de cálculo a una base de datos,
los analiza por hora y distrito, y entrena un modelo que estima si una persona implicada necesitará asistencia
sanitaria.

**Resultado:** 12.634 accidentes con 28.773 personas implicadas. La franja con más accidentes es la de las 14 h. El
modelo acierta el 71 % de los casos, frente al 53 % de decir siempre la respuesta más frecuente.

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_eda_exploratorio.ipynb
jupyter notebook notebooks/02_modelo_predictivo_gravedad.ipynb
```

Los dos cuadernos leen los CSV de `data/processed/` y se ejecutan sin base de datos.

## El problema de partida

La hoja del Ayuntamiento tiene una línea por persona implicada, no por accidente: un choque de dos coches con un
pasajero ocupa tres líneas. Contar líneas da 28.773 «accidentes» y mueve la hora punta a la tarde. El cargador
agrupa por número de expediente, que es lo que identifica un accidente, y salen 12.634.

## Qué hay dentro

1. `scripts/load_data.py` carga el Excel en MySQL, con un accidente por expediente y las personas aparte.
2. `scripts/export_data.py` exporta las dos tablas a `data/processed/`.
3. `notebooks/01_eda_exploratorio.ipynb` analiza los accidentes por hora y distrito y la lesividad de las personas.
4. `notebooks/02_modelo_predictivo_gravedad.ipynb` entrena un bosque aleatorio con la hora, la edad, el distrito, el
   tipo de accidente, el tiempo y el vehículo.

## Lo que sale

- La franja de las 14 h es la de más accidentes, con 892; la de las 4 h, la de menos, con 90.
- Salamanca es el distrito con más accidentes, 965.
- De las personas con la lesividad anotada, la mayoría no necesitó asistencia sanitaria; los graves y fallecidos
  suman 399 de 28.773.
- En el modelo, la variable que más pesa es el tipo de vehículo.

## Qué predice el modelo

Los códigos de lesividad siguen la estructura oficial de los datos del Ayuntamiento: del 1 al 7 hubo asistencia
sanitaria (el 3 es grave y el 4, fallecido) y el 14 significa sin asistencia sanitaria. El modelo distingue a quien
necesitó asistencia de quien no la necesitó. Los graves y fallecidos son demasiado pocos para un modelo propio.

## Límites

- Cerca de la mitad de las personas implicadas no tiene la lesividad anotada en el origen, y quedan fuera del
  modelo.
- La edad viene en rangos de cinco años; el modelo usa el punto medio de cada rango.
- Un 71 % de acierto sirve para ordenar casos por probabilidad, no para decidir caso a caso.
- Para recargar la base de datos hace falta MySQL: `sql/schema.sql` crea las tablas y `.env.example` es la plantilla
  de la conexión.

## Datos

`data/raw/2020_Accidentalidad.xlsx` procede del portal de datos abiertos del Ayuntamiento de Madrid. Los CSV de
`data/processed/` salen de él con los scripts de este repositorio.

## Repositorios relacionados

- [lead-scoring-ml](https://github.com/jleonceo/lead-scoring-ml): ordenar contactos comerciales por su probabilidad
  de compra.
- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por
  recencia, frecuencia e importe.
- [de-datos-en-bruto-a-decisiones](https://github.com/jleonceo/de-datos-en-bruto-a-decisiones): un fichero de ventas
  en bruto convertido en respuestas de negocio y en un cuadro de mando.

---

*Parte del portfolio de [Juan Luis León](https://github.com/jleonceo) · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · Licencia [MIT](LICENSE)*
