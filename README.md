# Accident Intelligent Agent

**Accidentes de tráfico en Madrid durante 2020 · Portfolio TechAcces · 2026**

[Español](#español) · [English](#english)

---

## Español

### Qué problema resuelve

Alguien te encarga decir cuántos accidentes de tráfico hubo en Madrid durante 2020. El Ayuntamiento publica una hoja de cálculo con casi veintinueve mil líneas, así que la respuesta parece estar a un clic de distancia.

No lo está. Cada línea de esa hoja corresponde a una persona implicada, de modo que un accidente ocupa tantas líneas como gente hubiera dentro. En un choque entre dos coches con un pasajero hay tres líneas y un solo siniestro, así que quien cuente líneas dará una cifra que más que duplica la verdadera.

Lo peor no es el número. Si por la tarde los accidentes llevan más gente dentro, contar personas desplaza la hora de mayor riesgo, y quien reparta ambulancias por franjas horarias las colocará donde no tocan.

Este proyecto contó líneas. Durante dos meses anunció 28.773 accidentes y situó la punta a las siete de la tarde. Las cifras buenas son 12.634 accidentes y las dos del mediodía. Lo que hoy tiene más valor aquí es el registro de ese fallo y de todo lo que arrastró detrás.

### El ejemplo que lo explica todo

Un programa localiza cada columna de una hoja de cálculo por el nombre escrito en su primera fila, la **cabecera**. El Excel del Ayuntamiento escribe la columna del expediente con dos espacios, `Nº  EXPEDIENTE`, y el cargador la buscaba con uno.

Ahí está el daño entero. La instrucción `row.get` que usaba para pedir esa columna no protesta cuando no encuentra lo que le piden: devuelve un vacío y sigue adelante. Cada línea se quedaba sin número de expediente, el programa le inventaba uno, y así cada persona implicada acababa registrada como un accidente distinto. Eso se llama **fallo silencioso**. Un programa que se detiene con un aviso rojo obliga a mirar, mientras que este deja publicar.

> **Corrección del 21/07/2026.** Hasta esa fecha este README decía «28.773 accidentes» y situaba la hora punta a las 19:00. Las dos cosas eran falsas por la causa que se acaba de explicar. Las cifras reales son **12.634 accidentes** y **28.773 personas implicadas**, 2,28 de media por accidente. Al contar accidentes en lugar de personas, la hora punta se mueve de las 19:00 a las **14:00**, así que no cambiaba solo el número: cambiaba la conclusión. El cargador quedó corregido y las cifras se recalcularon contra el Excel original por una vía independiente.
>
> **Qué cuenta como un accidente:** un número de expediente. Con ese criterio salen 12.634. Tres expedientes (`2020S014759`, `2020S014760`, `2020S014761`) aparecen reutilizados en dos fechas distintas, así que con la clave más estricta de expediente más fecha serían 12.637. La diferencia es del 0,02 % y no mueve ninguna conclusión, aunque queda dicha en vez de escondida.

### Qué contiene el repositorio

Guarda quince ficheros: dos programas, dos cuadernos, un modelo entrenado, un informe de Power BI y los datos de partida. Encadena tres tareas que van una detrás de otra. Mete la hoja del Ayuntamiento en una base de datos, la explora buscando patrones por hora y por distrito, y entrena un programa que intenta adivinar si un accidente saldrá leve o grave.

Ese primer trabajo de mover datos se llama **ETL**, siglas inglesas de extraer, transformar y cargar, o sea llevar los datos de donde están hasta donde se van a usar limpiándolos por el camino. Aquí lo hacen dos programas: `load_data.py` mete el Excel en la base de datos y `export_data.py` la vacía en dos ficheros de texto separados por comas, los **CSV**, el formato que lee cualquier herramienta.

Los dos análisis viven en sendos **cuadernos**, documentos que alternan texto explicativo con trozos de programa que se ejecutan uno a uno y dejan debajo su resultado. Ambos llevan un aviso arriba del todo desde julio: los resultados que tienen guardados dentro son los antiguos.

### Los conceptos del modelo

**Entrenar** un modelo consiste en enseñarle miles de casos con la respuesta ya conocida para que deduzca la regla por su cuenta. Después se le dan casos que nunca vio y se cuenta cuántos acierta; ese porcentaje recibe el nombre de **accuracy** o acierto global.

La **etiqueta** es la respuesta correcta que se le enseña al modelo mientras aprende. Aquí sale de una columna de códigos numéricos, y el cuaderno decide que del 1 al 7 significa «leve» y que el 14 significa «grave». Todo el modelo cuelga de esa decisión. Si la etiqueta está cambiada, las cuentas siguen saliendo, los gráficos siguen dibujándose y el porcentaje de acierto sigue apareciendo, solo que describen lo contrario de lo que dicen describir.

La **importancia de una variable** mide cuánto pesa ese dato en las decisiones del modelo, repartida entre todas las variables hasta sumar el cien por cien. Es la respuesta a la pregunta de qué mira el programa antes de decidir.

### Cómo funciona por dentro

Una línea de la hoja original tiene esta pinta:

```
2020S000001  01/01/2020  01:15  SAN BLAS-CANILLEJAS  Conductor  Turismo  14
```

1. **Se carga.** `load_data.py` lee esa línea, saca el expediente `2020S000001` y crea el accidente la primera vez que lo ve. La persona queda apuntada aparte, ligada a ese expediente.
2. **Se exporta.** `export_data.py` pide a la base de datos las dos tablas y las escribe en `accidents.csv` y `involved_parties.csv`.
3. **Se analiza.** El primer cuaderno cuenta accidentes por hora y por distrito y dibuja los gráficos.
4. **Se entrena.** El segundo junta persona y accidente, convierte el rango de edad en un número, traduce el código de gravedad a la etiqueta y entrena el modelo con el 80 % de los casos para medirlo con el 20 % restante.

Son cuatro eslabones sin una sola comprobación entre ellos. Nada pregunta si el número de accidentes que sale del paso 1 se parece al esperado, ausencia que es justo la que dejó pasar el fallo de la cabecera.

### Qué está medido

Ninguna de estas cifras viene de la documentación del proyecto: todas salen de ejecutar el código el 22/07/2026.

| Comprobación | Resultado |
|---|---|
| Expedientes distintos en el Excel original | 12.634 |
| Líneas del Excel original | 28.773, o sea 2,28 personas por accidente |
| Hora con más accidentes | las 14:00, con 892 |
| Hora con menos accidentes | las 04:00, con 90 |
| El cargador corregido, ejecutado en seco | 12.634 accidentes, cero identificadores inventados |
| El modelo rehecho desde el Excel, por vía independiente | 71,6 % de acierto |
| El informe `accident_dashboard.pbix` | una página, cero gráficos |

**Actualizado el 26/07/2026, y las cifras de abajo sustituyen a las que había aquí.** Las anteriores
describían una base de datos y unos CSV que ya se han regenerado; se conservan en la sección de
afirmaciones retiradas, porque el registro del fallo es lo que este repositorio ofrece.

| Comprobación | Resultado |
|---|---|
| `accidents.csv` publicado | 12.634 filas |
| `involved_parties.csv` publicado | 28.773 filas |
| Hora punta en los CSV publicados | las 14:00, con 892 |
| Hora más floja | las 04:00, con 90 |
| Columna de gravedad en `involved_parties.csv` | rellena en 15.718 de 28.773, igual que el Excel |

De la franja horaria queda además esto, medido sobre el recuento corregido: entre las 18:00 y las 20:00 se acumulan 2.526 accidentes, frente a 1.645 entre las 08:00 y las 10:00, y la franja de 13:00 a 15:00 va casi a la par de la tarde con 2.469.

### Tres hallazgos en orden de gravedad creciente

**El arreglo no llegó a los datos, y tardó cinco días más en llegar.** El cargador quedó corregido el 21/07 y funcionaba: ejecutado sobre el Excel devolvía los 12.634 buenos. Nadie volvió a lanzarlo. La base de datos siguió con la carga vieja **y con la nueva encima**, porque el cargador no vaciaba las tablas antes de escribir: 41.407 accidentes, que son los 28.773 equivocados más los 12.634 correctos, y 57.546 personas implicadas, el doble exacto de las 28.773 que trae el Excel. De ahí salieron los CSV publicados. Durante cinco días esta página anunció 12.634 accidentes mientras el fichero de al lado tenía 41.407.

> **Cerrado el 26/07/2026.** El cargador vacía ahora las tablas antes de escribir, la base se recargó y los CSV se reexportaron. Hoy `accidents.csv` tiene 12.634 filas y `involved_parties.csv` 28.773.

**Los CSV publicados perdieron la columna que sostiene el proyecto.** El Excel trae la gravedad rellena en 15.718 de sus 28.773 líneas, y en el fichero publicado esa casilla estaba vacía las 28.773 veces. Sin ella el análisis de gravedad salía en blanco, un gráfico del cuaderno se detenía con un error y el modelo se quedaba sin casos con los que aprender. Quedaba un repositorio que publicaba su acierto en portada mientras publicaba unos datos con los que ese modelo no se podía entrenar.

> **Cerrado el 26/07/2026** por la misma recarga: la columna vuelve a estar rellena en 15.718 de 28.773, que es exactamente lo que trae el Excel. No hizo falta tocar nada del análisis; el dato llevaba dos meses perdiéndose en la carga.

**La etiqueta parece estar del revés.** Rehecho el modelo desde el Excel original sale un 71,6 % de acierto, muy cerca del 72 % que anunciaba la portada, de modo que la magnitud se sostiene. Lo que no se sostiene es a qué llama «grave». Entre los ocupantes de camión rígido lo son el 81,9 %, entre los peatones el 9,8 % y entre las motos pequeñas el 10,0 %. De 958 peatones atropellados, solo 94 llevan el código 14 que el cuaderno traduce por «grave». ¿Es creíble que un peatón atropellado salga mejor parado que quien viajaba dentro de un camión? Quien no necesitó asistencia sanitaria lleva con toda probabilidad ese 14 que el cuaderno lee como el peor de todos.

### Afirmaciones que este README ha retirado

Las cifras y conclusiones de abajo estuvieron publicadas aquí y hoy no se sostienen. Van con el motivo de la retirada al lado.

- **«Accuracy del 72 %, recall del 75 % en graves, F1 de 0,72».** El 72 % se sostiene como magnitud, porque el modelo rehecho por una vía independiente da 71,6 %. Lo que ese porcentaje mide está en duda mientras la etiqueta no se aclare, así que se presenta como lo que es. El recall y el F1 no se han vuelto a medir y cuelgan de esa misma etiqueta, por lo que salen de la portada.
- **«Las variables más importantes son la edad, la hora, el tipo de accidente, el distrito, la meteorología y el tipo de vehículo, por ese orden».** Refutado por el propio cuaderno, que ya había impreso lo contrario, y confirmado al medirlo de nuevo: tipo de vehículo 25,2 %, hora 21,2 %, distrito 21,1 %, edad 17,6 %. La portada ponía primera la variable que va cuarta y última la que va primera.
- **«Factores de riesgo: los atropellos y las motocicletas correlacionan con mayor gravedad».** Refutado por los datos del propio repositorio, donde peatones y motos pequeñas son justamente los dos grupos con menos casos marcados como graves.
- **«Los conductores menores de 25 y mayores de 55 son más vulnerables».** Sin medición que lo respalde y apoyado en la etiqueta que está en duda.
- **«La gravedad se mantiene estable, la mitad leve y la mitad grave, durante las 24 horas».** Se apoya en la misma etiqueta y en una columna que los CSV publicados no traen. Lo que sí queda medido es la calidad del dato: el Excel trae la gravedad anotada en 15.718 de sus 28.773 líneas, así que cerca de la mitad de los registros del Ayuntamiento vienen sin ella.
- **«Cuadro de mando en Power BI (entregable)».** El fichero `accident_dashboard.pbix` pesa un megabyte y por dentro tiene una página en blanco, sin un solo gráfico.
- **La sección de impacto de negocio**, que ofrecía priorización de recursos, planificación urbana y despacho de emergencias informado. Nada de eso se puede apoyar hoy en este repositorio.
- **La lista de próximas mejoras**, que proponía una web con Streamlit, una API REST, un modelo multiclase y análisis de series temporales. Añadir funciones encima de una base que no se reproduce a sí misma no arregla nada, así que la sustituye la lista de arreglos pendientes.

### Qué haría falta para que sirviera

Hacen falta tres arreglos en este orden:

1. Recargar la base de datos con el cargador ya corregido.
2. Exportar de nuevo los CSV con la columna de gravedad dentro.
3. Abrir el diccionario oficial de datos del Ayuntamiento y decidir qué significa cada código de lesividad antes de volver a entrenar nada.

Hasta entonces el repositorio no sirve para reproducir sus propios resultados, ni como cuadro de mando, ni como base para decidir dónde reforzar la vigilancia en Madrid.

### Qué abrir y en qué orden

| Orden | Fichero | Qué encontrarás |
|---|---|---|
| 1 | `scripts/load_data.py` | El cargador corregido, y el comentario del fallo de la cabecera |
| 2 | `notebooks/01_eda_exploratorio.ipynb` | El análisis por horas y distritos. Los resultados guardados son los antiguos |
| 3 | `notebooks/02_modelo_predictivo_gravedad.ipynb` | El modelo de principio a fin. Hoy no llega a entrenar con los CSV publicados |
| 4 | `scripts/export_data.py` | El volcado de la base de datos a CSV |

### Stack tecnológico

| Capa | Tecnologías |
|---|---|
| Base de datos | MySQL 8.0 |
| ETL | Python, Pandas, mysql-connector-python |
| Análisis y modelo | Scikit-learn, Random Forest, Joblib |
| Visualización | Matplotlib, Seaborn, Power BI Desktop |
| Entorno | Jupyter Notebook, Conda, Git |

### Estructura del proyecto

```
accident-intelligent-agent/
├── README.md
├── requirements.txt
├── .env.example                # Plantilla de credenciales
├── EJECUTAR_ETL.bat            # Lanzador opcional (requiere compilar el ETL con PyInstaller)
│
├── scripts/
│   ├── export_data.py          # ETL: MySQL a CSV
│   └── load_data.py            # Carga del Excel a MySQL
│
├── notebooks/
│   ├── 01_eda_exploratorio.ipynb              # Análisis visual y hallazgos
│   └── 02_modelo_predictivo_gravedad.ipynb    # Entrenamiento y evaluación
│
├── models/
│   └── gravedad_predictor.pkl  # Modelo entrenado y serializado
│
├── accident_dashboard.pbix     # Informe de Power BI, hoy con una página en blanco
│
├── sql/
│   └── schema.sql              # Crea la base de datos y las dos tablas. Ejecutar lo primero
│
└── data/
    ├── raw/2020_Accidentalidad.xlsx
    └── processed/              # CSV exportados, hoy sin la columna de gravedad
        ├── accidents.csv
        └── involved_parties.csv
```

### Cómo ejecutarlo

```bash
git clone https://github.com/jleonceo/accident-intelligent-agent.git
cd accident-intelligent-agent

conda create -n accident_agent python=3.10
conda activate accident_agent
pip install -r requirements.txt

cp .env.example .env      # editar con los datos de tu MySQL
mysql -u tu_usuario -p < sql/schema.sql   # crea la base de datos y las dos tablas
python scripts/load_data.py    # recarga la base de datos con el cargador corregido
python scripts/export_data.py  # vuelve a exportar los CSV
```

La línea del esquema **faltaba hasta el 26/07/2026**, y sin ella estos pasos no funcionaban fuera
del portátil donde nació el proyecto: `load_data.py` solo hace `USE accident_db` y da por hecho que
las tablas ya están. Quien clonara el repositorio y siguiera las instrucciones al pie de la letra
fallaba en la primera consulta.

`load_data.py` vacía las tablas antes de cargar, que es lo que significa «recarga». Hasta esa misma
fecha no lo hacía, y ejecutarlo dos veces duplicaba las personas implicadas: los accidentes chocaban
con su clave primaria y se descartaban, pero `involved_parties` no tiene clave única y sus filas
entraban otra vez. Así se publicaron unos CSV con 41.407 accidentes y 57.546 personas mientras esta
misma página anunciaba 12.634 y 28.773.

El orden importa. Ejecutar `export_data.py` sin recargar antes la base de datos sobrescribe los CSV con el recuento viejo de 28.773, que es lo que hacían las instrucciones anteriores de este README.

### Qué llevarse

**Un número que sale bien no está comprobado.** 28.773 es una cifra redonda y del tamaño que uno espera en una ciudad grande, y estuvo publicada dos meses porque nada la contrastó contra una segunda cuenta hecha por otro camino.

**Corregir la portada no corrige el proyecto.** Aquí se escribió una rectificación honrada, y aun así la base de datos, los CSV, el orden de las variables y los factores de riesgo siguieron equivocados debajo. Un aviso escrito avisa; solo una comprobación que se ejecute sola vuelve a mirar.

**La etiqueta se verifica antes que el modelo.** Un modelo con la respuesta cambiada de signo acierta igual, dibuja igual y publica igual. Lo único que cambia es hacia dónde apunta.

### Repos relacionados

Este trabajo es una pieza de un portfolio de casos de analítica. Las piezas hermanas:

- [lead-scoring-ml](https://github.com/jleonceo/lead-scoring-ml): predecir qué contacto comercial acaba comprando, con sus métricas recalculadas por un script de réplica.
- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por recencia, frecuencia e importe.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): análisis financiero de una empresa con Python, del libro diario a las conclusiones.

---

## English

### The problem it addresses

Someone asks you how many road accidents there were in Madrid during 2020. The City Council publishes a spreadsheet with almost twenty-nine thousand rows, so the answer looks like it is one click away.

It is not. Every row of that spreadsheet is one person involved, so a single accident takes up as many rows as there were people inside it. A collision between two cars carrying one passenger fills three rows and is one crash, so anyone counting rows will report a figure more than double the real one.

The number is not the worst part. If afternoon accidents carry more people inside them, counting people shifts the peak risk hour, and whoever allocates ambulances by time of day will place them where they are not needed.

This project counted rows. For two months it announced 28,773 accidents and put the peak at seven in the evening. The right figures are 12,634 accidents and two in the afternoon. What is worth most here today is the record of that mistake and of everything it dragged behind it.

### The example that explains all of it

A program finds each column of a spreadsheet by the name written in its first row, the **header**. The City Council's Excel writes the case-number column with two spaces, `Nº  EXPEDIENTE`, and the loader was looking for it with one.

That is where the whole damage sits. The `row.get` instruction it used to ask for that column does not complain when it fails to find what it was asked for: it returns an empty value and carries on. Every row was left without a case number, the program invented one for it, and so each person involved ended up recorded as a separate accident. That is called a **silent failure**. A program that stops with a red warning forces you to look, whereas this one lets you publish.

> **Correction, 21 July 2026.** Until that date this README claimed "28,773 accidents" and put the busiest hour at 19:00. Both were wrong, for the reason just explained. The real figures are **12,634 accidents** and **28,773 people involved**, 2.28 per accident. Counting accidents instead of people moves the busiest hour from 19:00 to **14:00**, so it was not just the number that changed: the conclusion changed with it. The loader was fixed and the figures were recomputed straight from the source spreadsheet by an independent route.
>
> **What counts as one accident:** one case number. That gives 12,634. Three case numbers (`2020S014759`, `2020S014760`, `2020S014761`) turn up on two different dates, so under the stricter key of case number plus date it would be 12,637. That is a 0.02% difference and it moves no conclusion, though it is said out loud rather than hidden.

### What the repository holds

It keeps fifteen files: two programs, two notebooks, a trained model, a Power BI report and the source data. It chains three tasks that run one after another. It loads the Council spreadsheet into a database, explores it for patterns by hour and by district, and trains a program that tries to guess whether an accident came out minor or serious.

That first job of moving data around is called **ETL**, for extract, transform and load, meaning to carry data from where it sits to where it will be used, cleaning it on the way. Two programs do it here: `load_data.py` puts the Excel into the database and `export_data.py` empties the database into two comma-separated text files, the **CSVs**, the format any tool can read.

Both analyses live in **notebooks**, documents that alternate explanatory text with chunks of program that run one at a time and leave their output underneath. Each of them has carried a warning at the top since July: the results saved inside them are the old ones.

### The model's concepts

**Training** a model means showing it thousands of cases whose answer is already known so that it works out the rule on its own. It is then given cases it never saw, and how many it gets right is counted, a percentage called **accuracy**.

The **label** is the correct answer shown to the model while it learns. Here it comes from a column of numeric codes, and the notebook decides that 1 through 7 means "leve" (minor) and that 14 means "grave" (serious). The entire model hangs off that decision. If the label is the wrong way round, the sums still add up, the charts still get drawn and the accuracy figure still appears, except that all of them describe the opposite of what they claim to describe.

**Feature importance** measures how much weight each piece of data carries in the model's decisions, shared across all the variables until it adds up to a hundred per cent. It answers the question of what the program looks at before deciding.

### How it works inside

One row of the original spreadsheet looks like this:

```
2020S000001  01/01/2020  01:15  SAN BLAS-CANILLEJAS  Conductor  Turismo  14
```

1. **It is loaded.** `load_data.py` reads that row, pulls out case number `2020S000001` and creates the accident the first time it sees it. The person is recorded separately, tied to that case number.
2. **It is exported.** `export_data.py` asks the database for both tables and writes them to `accidents.csv` and `involved_parties.csv`.
3. **It is analysed.** The first notebook counts accidents by hour and by district and draws the charts.
4. **It is trained on.** The second joins person to accident, turns the age range into a number, translates the severity code into the label and trains the model on 80% of the cases to measure it on the remaining 20%.

These are four links with not one check between them. Nothing asks whether the accident count coming out of step 1 resembles what was expected, an absence that is exactly what let the header bug through.

### What has been measured

None of these figures comes from the project's documentation: all of them come from running the code on 22/07/2026.

| Check | Result |
|---|---|
| Distinct case numbers in the source Excel | 12,634 |
| Rows in the source Excel | 28,773, that is 2.28 people per accident |
| Busiest hour | 14:00, with 892 |
| Quietest hour | 04:00, with 90 |
| The fixed loader, run as a dry run | 12,634 accidents, zero invented identifiers |
| The MySQL database, today | 28,773 accidents on invented identifiers, peak at 19:00 |
| Severity column in `involved_parties.csv` | empty across all 28,773 rows |
| The model notebook over those CSVs | 0 valid records, it never gets to train |
| The analysis notebook over those CSVs | hours come out right, severity charts empty, one breaks |
| The model rebuilt from the Excel by an independent route | 71.6% accuracy |
| The `accident_dashboard.pbix` report | one page, zero charts |

On the daily pattern, measured over the corrected count: 2,526 accidents fall between 18:00 and 20:00, against 1,645 between 08:00 and 10:00, and the 13:00 to 15:00 stretch runs almost level with the evening at 2,469.

### Three findings in rising order of seriousness

**The fix never reached the data.** The loader is corrected and works: run today against the Excel it returns the right 12,634. Nobody launched it again, so the database still holds the old load in full. And because the reproduction instructions told you to run `export_data.py`, anyone following them today overwrites the CSVs with the bad load and sees the 19:00 peak all over again.

**The published CSVs lost the column the project rests on.** The Excel carries severity filled in on 15,718 of its 28,773 rows. In the published file that cell is empty all 28,773 times. Without it the severity analysis comes out blank, one notebook chart stops with an error and the model is left with no cases to learn from. What remains is a repository publishing its accuracy on the front page while publishing data that model cannot be trained on.

**The label looks reversed.** Rebuilt from the original Excel, the model gives 71.6% accuracy, very close to the 72% the front page announced, so the magnitude holds up. What does not hold up is what it calls "grave". Among rigid-truck occupants 81.9% are labelled serious, among pedestrians 9.8%, and among small motorcycles 10.0%. Of 958 pedestrians struck, only 94 carry the code 14 that the notebook reads as serious. Is it believable that a pedestrian hit by a vehicle comes off better than someone travelling inside a truck? Whoever needed no medical assistance almost certainly carries that 14 which the notebook reads as the worst outcome of all.

### Claims this README has withdrawn

The figures and conclusions below were published here and no longer hold. Each comes with the reason for its withdrawal.

- **"72% accuracy, 75% recall on serious cases, F1 of 0.72".** The 72% holds as a magnitude, since the model rebuilt by an independent route gives 71.6%. What that percentage measures is in doubt while the label remains unresolved, so it is presented for what it is. The recall and the F1 have not been measured again and hang off that same label, so they come off the front page.
- **"The most important variables are age, hour, accident type, district, weather and vehicle type, in that order".** Refuted by the project's own notebook, which had already printed the opposite, and confirmed on remeasuring: vehicle type 25.2%, hour 21.2%, district 21.1%, age 17.6%. The front page put first the variable that ranks fourth and last the one that ranks first.
- **"Risk factors: pedestrian strikes and motorcycles correlate with higher severity".** Refuted by the repository's own data, where pedestrians and small motorcycles are precisely the two groups with the fewest cases marked serious.
- **"Drivers under 25 and over 55 are more vulnerable".** No measurement backs it and it leans on the label that is in doubt.
- **"Severity holds steady at roughly half minor and half serious around the clock".** It leans on the same label and on a column the published CSVs do not carry. What is measured is the data quality: the Excel has severity recorded on 15,718 of its 28,773 rows, so close to half the Council's records arrive without it.
- **"Power BI dashboard (deliverable)".** The `accident_dashboard.pbix` file weighs one megabyte and holds a single blank page inside, without one chart.
- **The business impact section**, which offered resource prioritisation, urban planning and better-informed emergency dispatch. None of that can rest on this repository today.
- **The roadmap**, which proposed a Streamlit web app, a REST API, a multiclass model and time-series analysis. Stacking features on a base that cannot reproduce itself fixes nothing, so the list of pending repairs replaces it.

### What it would take to make it useful

Three repairs are needed, in this order:

1. Reload the database with the loader that is already fixed.
2. Export the CSVs again with the severity column inside them.
3. Open the Council's official data dictionary and settle what each injury code means before training anything again.

Until then the repository does not serve to reproduce its own results, nor as a dashboard, nor as a basis for deciding where to step up road policing in Madrid.

### What to open and in what order

| Order | File | What you will find |
|---|---|---|
| 1 | `scripts/load_data.py` | The corrected loader, and the comment on the header bug |
| 2 | `notebooks/01_eda_exploratorio.ipynb` | The analysis by hour and district. The saved results are the old ones |
| 3 | `notebooks/02_modelo_predictivo_gravedad.ipynb` | The model end to end. Today it never trains on the published CSVs |
| 4 | `scripts/export_data.py` | The dump from the database to CSV |

### Tech stack

| Layer | Tools |
|---|---|
| Database | MySQL 8.0 |
| ETL | Python, Pandas, mysql-connector-python |
| Analysis and model | Scikit-learn, Random Forest, Joblib |
| Visualisation | Matplotlib, Seaborn, Power BI Desktop |
| Environment | Jupyter Notebook, Conda, Git |

### Project layout

```
accident-intelligent-agent/
├── README.md
├── requirements.txt
├── .env.example                # Credentials template
├── EJECUTAR_ETL.bat            # Optional launcher (needs the ETL built with PyInstaller)
│
├── scripts/
│   ├── export_data.py          # ETL: MySQL to CSV
│   └── load_data.py            # Loads the Excel file into MySQL
│
├── notebooks/
│   ├── 01_eda_exploratorio.ipynb              # Visual analysis and findings
│   └── 02_modelo_predictivo_gravedad.ipynb    # Training and evaluation
│
├── models/
│   └── gravedad_predictor.pkl  # Trained, serialized model
│
├── accident_dashboard.pbix     # Power BI report, today a single blank page
│
├── sql/
│   └── schema.sql              # Creates the database and the two tables. Run this first
│
└── data/
    ├── raw/2020_Accidentalidad.xlsx
    └── processed/              # Exported CSVs, today without the severity column
        ├── accidents.csv
        └── involved_parties.csv
```

### Running it

```bash
git clone https://github.com/jleonceo/accident-intelligent-agent.git
cd accident-intelligent-agent

conda create -n accident_agent python=3.10
conda activate accident_agent
pip install -r requirements.txt

cp .env.example .env           # edit it with your own MySQL details
python scripts/load_data.py    # reloads the database with the corrected loader
python scripts/export_data.py  # exports the CSVs again
```

The order matters. Running `export_data.py` without reloading the database first overwrites the CSVs with the old count of 28,773, which is exactly what the previous instructions in this README did.

### What to take away

**A number that looks right has not been checked.** 28,773 is a round figure of the size you would expect in a large city, published for two months because nothing tested it against a second count made by another route.

**Correcting the front page does not correct the project.** An honest retraction was written here, and even so the database, the CSVs, the variable ranking and the risk factors stayed wrong underneath. A written warning warns; only a check that runs by itself looks again.

**The label is verified before the model is.** A model with its answer flipped scores the same, plots the same and publishes the same. The only thing that changes is where it points.

### Related repositories

This work is one piece of an analytics portfolio whose sibling projects are these:

- [lead-scoring-ml](https://github.com/jleonceo/lead-scoring-ml): predicting which sales contact ends up buying, with its metrics recomputed by a replication script.
- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): customer segmentation by recency, frequency and monetary value.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): financial analysis of a company with Python, from the ledger to the conclusions.

---

*Parte del portfolio de / Part of [Juan Luis León](https://github.com/jleonceo)'s portfolio · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · [LinkedIn](https://linkedin.com/in/jlleonrodriguez/) · Licencia / License: [MIT](LICENSE)*
