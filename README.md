# Accident Intelligence Agent
**Análisis predictivo de accidentalidad vial en Madrid (2020)**
**Predictive analysis of road accidents in Madrid (2020)**

> Pipeline completo: ETL + análisis exploratorio + modelo de machine learning para predecir
> la gravedad de un accidente.

[Español](#español) · [English](#english)

---

## Español

### Resumen ejecutivo
Este proyecto analiza **28.773 accidentes de tráfico** registrados en Madrid durante 2020, en tres partes:
1. **Análisis exploratorio (EDA):** patrones temporales, geográficos y de severidad.
2. **Modelo predictivo (ML):** clasifica cada accidente como "Leve" o "Grave" con un **accuracy del 72%**.
3. **Reproducibilidad:** un ETL en Python (`scripts/export_data.py`) y notebooks autocontenidos.

**Objetivo:** aportar información accionable para autoridades de tráfico y servicios de
emergencia, de cara a la prevención y la respuesta ante siniestros.

---

### Hallazgos clave (EDA)

### 1. Patrón temporal predecible
- **Hora pico:** 19:00h (2.132 accidentes), coincidiendo con la salida laboral y el ocio.
- **Hora mínima:** 04:00h (187 accidentes).
- **Doble pico diario:** mañana (08:00-10:00h) y tarde (18:00-20:00h).

### 2. Distribución de gravedad
- Entre los datos válidos, la severidad se mantiene **estable (~50% leve / ~50% grave)** durante las 24h.
- No se detecta un aumento significativo de gravedad en horas nocturnas.
- **Calidad del dato:** cerca del 50% de los registros no traen `lesividad`. Es una limitación
  real del dato (reporte policial), y se dice abiertamente en vez de esconderla.

### 3. Factores de riesgo
- **Edad:** conductores menores de 25 y mayores de 55 muestran mayor vulnerabilidad.
- **Tipo de accidente:** atropellos y salidas de vía correlacionan con mayor gravedad.
- **Vehículo:** motocicletas y peatones presentan mayor riesgo relativo.

---

### Modelo predictivo de gravedad

### Resultados

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Accuracy global** | 72% | Acierta 72 de cada 100 predicciones |
| **Recall en graves** | 75% | Detecta 3 de cada 4 accidentes graves reales |
| **F1-Score** | 0,72 | Balance razonable entre precisión y exhaustividad |

Nota: con cerca del 50% de la lesividad ausente, estas cifras salen de los registros con dato
válido; no son un veredicto sobre el total.

### Variables más importantes
1. Edad del implicado (punto medio del rango).
2. Hora del accidente.
3. Tipo de accidente (colisión, atropello, salida de vía).
4. Distrito (ubicación geográfica).
5. Condiciones meteorológicas.
6. Tipo de vehículo.

### Cómo probar el modelo
Ejecuta el notebook `notebooks/02_modelo_predictivo_gravedad.ipynb`:
1. Celda 1: instalación automática de dependencias.
2. Kernel → Restart.
3. Cell → Run All.
4. Resultados: métricas, gráfico de importancia y modelo serializado en `models/gravedad_predictor.pkl`.

---

### Stack tecnológico

| Capa | Tecnologías |
|------|-------------|
| **Base de datos** | MySQL 8.0 |
| **ETL / ingeniería** | Python, Pandas, mysql-connector-python |
| **Análisis / ML** | Scikit-learn, Random Forest, Joblib |
| **Visualización** | Matplotlib, Seaborn, Power BI Desktop |
| **Entorno** | Jupyter Notebook, Conda, Git |

---

### Estructura del proyecto

```
accident-intelligent-agent/
├── README.md
├── requirements.txt
├── .env.example                # Plantilla de credenciales
├── EJECUTAR_ETL.bat            # Lanzador opcional (requiere compilar el ETL con PyInstaller)
│
├── scripts/
│   ├── export_data.py          # ETL: MySQL → CSV
│   └── load_data.py            # Carga del Excel a MySQL
│
├── notebooks/
│   ├── 01_eda_exploratorio.ipynb              # Análisis visual y hallazgos
│   └── 02_modelo_predictivo_gravedad.ipynb    # ML: entrenamiento y evaluación
│
├── models/
│   └── gravedad_predictor.pkl  # Modelo entrenado y serializado
│
├── accident_dashboard.pbix     # Cuadro de mando en Power BI (entregable)
│
└── data/
    ├── raw/2020_Accidentalidad.xlsx
    └── processed/              # CSVs limpios para Power BI
        ├── accidents.csv
        └── involved_parties.csv
```

---

### Cómo reproducir el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/jleonceo/accident-intelligent-agent.git
cd accident-intelligent-agent

# 2. Crear el entorno (recomendado)
conda create -n accident_agent python=3.10
conda activate accident_agent

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales MySQL
cp .env.example .env
# Editar .env con tus datos

# 5. Ejecutar el ETL
python scripts/export_data.py

# 6. Abrir el análisis
jupyter notebook notebooks/01_eda_exploratorio.ipynb
```

---

### Impacto de negocio

### Para autoridades de tráfico
- **Priorización de recursos:** el modelo detecta el 75% de los accidentes graves.
- **Prevención focalizada:** campañas en las horas y distritos de mayor riesgo.
- **Planificación urbana:** información geoespacial para rediseñar vías críticas.

### Para servicios de emergencia
- **Respuesta informada:** integrar el modelo en el despacho para pre-asignar recursos según la gravedad predicha.
- **Métricas de desempeño:** evaluación continua de la precisión predictiva.

### Para analistas de datos
- **Pipeline reproducible:** código comentado y autocontenido.
- **Caso de estudio completo:** de la extracción de datos al modelo y el cuadro de mando.

---

### Próximas mejoras (roadmap)
- [ ] Web app interactiva con Streamlit para pruebas en tiempo real.
- [ ] API REST para predicciones desde sistemas externos.
- [ ] Modelo multiclase (incluyendo "Fallecimiento" como categoría).
- [ ] Análisis de series temporales para predecir picos de accidentalidad.

---

*Parte del portfolio de [Juan Luis León](https://github.com/jleonceo) · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · [LinkedIn](https://linkedin.com/in/jlleonrodriguez/) · Licencia [MIT](LICENSE)*

---

### Repos relacionados

Este análisis es una pieza de un portfolio de casos de analítica. Las piezas hermanas:

- [lead-scoring-ml](https://github.com/jleonceo/lead-scoring-ml): predecir qué lead acaba comprando, con modelos de clasificación.
- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por recencia, frecuencia e importe.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): análisis financiero de una empresa con Python, del libro diario a las conclusiones.

## English

### Executive summary
This project works through **28,773 traffic accidents** recorded in Madrid during 2020, in three parts:
1. **Exploratory analysis (EDA):** how accidents fall across the clock, the map and the severity scale.
2. **Predictive model (ML):** labels each accident "Leve" (minor) or "Grave" (serious), with **72% accuracy**.
3. **Reproducibility:** a Python ETL (`scripts/export_data.py`) and self-contained notebooks.

**Goal:** give traffic authorities and emergency services something they can act on, both to prevent accidents and to respond to them.

---

### Key findings (EDA)

### 1. The clock is predictable
- **Busiest hour:** 19:00 (2,132 accidents), where the commute home meets evening traffic.
- **Quietest hour:** 04:00 (187 accidents).
- **Two peaks a day:** morning (08:00-10:00) and evening (18:00-20:00).

### 2. How severity is distributed
- Across the valid records, severity holds steady at **roughly 50% minor / 50% serious** around the clock.
- Night hours show no meaningful rise in severity.
- **Data quality:** close to half the records carry no `lesividad` (injury severity) value at all. That is a real limitation of police-reported data, said out loud here instead of hidden.

### 3. Risk factors
- **Age:** drivers under 25 and over 55 come out more vulnerable.
- **Accident type:** pedestrian strikes and run-off-road accidents go with higher severity.
- **Vehicle:** motorcycles and pedestrians carry the higher relative risk.

---

### Severity prediction model

### Results

| Metric | Value | What it means |
|---------|-------|----------------|
| **Overall accuracy** | 72% | 72 right calls out of every 100 |
| **Recall on serious cases** | 75% | Catches 3 of every 4 real serious accidents |
| **F1-Score** | 0.72 | A fair balance between precision and recall |

Note: with close to half the severity values missing, these figures come from the records that do carry a valid one. They are not a verdict on the whole dataset.

### What the model leans on most
1. Age of the person involved (midpoint of the range).
2. Hour of the accident.
3. Accident type (collision, pedestrian strike, run-off-road).
4. District (geographic location).
5. Weather conditions.
6. Vehicle type.

### Taking the model for a spin
Open the `notebooks/02_modelo_predictivo_gravedad.ipynb` notebook:
1. Cell 1: the dependencies install themselves.
2. Kernel → Restart.
3. Cell → Run All.
4. Out come the metrics, the feature-importance plot and the serialized model at `models/gravedad_predictor.pkl`.

---

### Tech stack

| Layer | Tools |
|------|-------------|
| **Database** | MySQL 8.0 |
| **ETL / engineering** | Python, Pandas, mysql-connector-python |
| **Analysis / ML** | Scikit-learn, Random Forest, Joblib |
| **Visualization** | Matplotlib, Seaborn, Power BI Desktop |
| **Environment** | Jupyter Notebook, Conda, Git |

---

### Project layout

```
accident-intelligent-agent/
├── README.md
├── requirements.txt
├── .env.example                # Credentials template
├── EJECUTAR_ETL.bat            # Optional launcher (needs the ETL built with PyInstaller)
│
├── scripts/
│   ├── export_data.py          # ETL: MySQL → CSV
│   └── load_data.py            # Loads the Excel file into MySQL
│
├── notebooks/
│   ├── 01_eda_exploratorio.ipynb              # Visual analysis and findings
│   └── 02_modelo_predictivo_gravedad.ipynb    # ML: training and evaluation
│
├── models/
│   └── gravedad_predictor.pkl  # Trained, serialized model
│
├── accident_dashboard.pbix     # Power BI dashboard (deliverable)
│
└── data/
    ├── raw/2020_Accidentalidad.xlsx
    └── processed/              # Clean CSVs for Power BI
        ├── accidents.csv
        └── involved_parties.csv
```

---

### Reproducing the project

```bash
# 1. Clone the repository
git clone https://github.com/jleonceo/accident-intelligent-agent.git
cd accident-intelligent-agent

# 2. Set up the environment (recommended)
conda create -n accident_agent python=3.10
conda activate accident_agent

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Point it at your MySQL
cp .env.example .env
# Edit .env with your own details

# 5. Run the ETL
python scripts/export_data.py

# 6. Open the analysis
jupyter notebook notebooks/01_eda_exploratorio.ipynb
```

---

### What it is good for

### Traffic authorities
- **Putting resources where they count:** the model catches 75% of serious accidents.
- **Targeted prevention:** campaigns aimed at the hours and districts that carry the risk.
- **Urban planning:** geospatial evidence for redesigning the streets that keep coming up.

### Emergency services
- **Dispatch that knows more:** wire the model into dispatch to pre-assign resources against predicted severity.
- **Performance tracking:** keep measuring how well the predictions hold up.

### Data analysts
- **A pipeline you can run:** commented, self-contained code.
- **A case study end to end:** from pulling the data to the model and the dashboard.

---

### Roadmap
- [ ] Interactive Streamlit web app for live testing.
- [ ] REST API so other systems can ask for predictions.
- [ ] Multiclass model, adding "Fallecimiento" (fatality) as a category.
- [ ] Time-series analysis to predict accident peaks before they arrive.


### Related repositories

This analysis is one piece of an analytics portfolio. Its sibling projects:

- [lead-scoring-ml](https://github.com/jleonceo/lead-scoring-ml): predicting which lead ends up buying, with classification models.
- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): customer segmentation by recency, frequency and monetary value.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): financial analysis of a company with Python, from the ledger to the conclusions.

---

*Part of [Juan Luis León](https://github.com/jleonceo)'s portfolio · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · [LinkedIn](https://linkedin.com/in/jlleonrodriguez/) · [MIT](LICENSE) licence*
