# Accident Intelligence Agent
**Análisis predictivo de accidentalidad vial en Madrid (2020)**

> Pipeline completo: ETL + análisis exploratorio + modelo de machine learning para predecir
> la gravedad de un accidente.

---

## Resumen ejecutivo
Este proyecto analiza **28.773 accidentes de tráfico** registrados en Madrid durante 2020, en tres partes:
1. **Análisis exploratorio (EDA):** patrones temporales, geográficos y de severidad.
2. **Modelo predictivo (ML):** clasifica cada accidente como "Leve" o "Grave" con un **accuracy del 72%**.
3. **Reproducibilidad:** un ETL en Python (`scripts/export_data.py`) y notebooks autocontenidos.

**Objetivo:** aportar información accionable para autoridades de tráfico y servicios de
emergencia, de cara a la prevención y la respuesta ante siniestros.

---

## Hallazgos clave (EDA)

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

## Modelo predictivo de gravedad

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

## Stack tecnológico

| Capa | Tecnologías |
|------|-------------|
| **Base de datos** | MySQL 8.0 |
| **ETL / ingeniería** | Python, Pandas, mysql-connector-python |
| **Análisis / ML** | Scikit-learn, Random Forest, Joblib |
| **Visualización** | Matplotlib, Seaborn, Power BI Desktop |
| **Entorno** | Jupyter Notebook, Conda, Git |

---

## Estructura del proyecto

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

## Cómo reproducir el proyecto

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

## Impacto de negocio

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

## Próximas mejoras (roadmap)
- [ ] Web app interactiva con Streamlit para pruebas en tiempo real.
- [ ] API REST para predicciones desde sistemas externos.
- [ ] Modelo multiclase (incluyendo "Fallecimiento" como categoría).
- [ ] Análisis de series temporales para predecir picos de accidentalidad.

---

*Parte del portfolio de [Juan Luis León](https://github.com/jleonceo) · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · [LinkedIn](https://linkedin.com/in/jlleonrodriguez/) · Licencia [MIT](LICENSE)*
