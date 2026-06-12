# 🚗 Accident Intelligence Agent
**Análisis Predictivo de Accidentalidad Vial en Madrid (2020)**

> Pipeline completo: ETL automatizado + Análisis Exploratorio + Modelo de Machine Learning para predecir gravedad de accidentes.

---

## Resumen Ejecutivo
Este proyecto analiza **28.773 accidentes de tráfico** registrados en Madrid durante 2020, combinando:
1. 🔍 **Análisis Exploratorio (EDA):** Identificación de patrones temporales, geográficos y de severidad.
2. 🤖 **Modelo Predictivo (ML):** Clasificación de accidentes como "Leves" o "Graves" con **71,84% de precisión**.
3. ⚡ **Automatización:** ETL ejecutable (.exe) + notebook autocontenido para reproducibilidad total.

**Objetivo:** Proporcionar insights accionables para autoridades de tráfico y servicios de emergencia, optimizando la prevención y respuesta ante siniestros viales.

---

## Hallazgos Clave (EDA)

### 1. Patrón Temporal Predecible
- **Hora Pico:** 19:00h (2.132 accidentes) coincidiendo con salida laboral y ocio.
- **Hora Mínima:** 04:00h (187 accidentes).
- **Doble Pico Diario:** Mañana (08:00-10:00h) y Tarde (18:00-20:00h).

### 2. Distribución de Gravedad
- Entre datos válidos, la severidad se mantiene **estable (~50% Leve / ~50% Grave)** durante las 24h.
- **Insight Sorprendente:** No se detecta aumento significativo de gravedad en horas nocturnas (desmintiendo mitos populares).
- **Calidad del Dato:** ~50% de registros carecen de información de `lesividad` → oportunidad crítica de mejora en reporte policial.

### 3. Factores de Riesgo Identificados
- **Edad:** Conductores <25 años y >55 años muestran mayor vulnerabilidad.
- **Tipo de accidente:** Atropellos y salidas de vía correlacionan con mayor gravedad.
- **Vehículo:** Motocicletas y peatones presentan mayor riesgo relativo.

---

## Modelo Predictivo de Gravedad (Machine Learning)

### Resultados Clave

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Accuracy Global** | 71,84% | Acierta 72 de cada 100 predicciones |
| **Recall en Graves** | 75% | Detecta 3 de cada 4 accidentes graves reales |
| **F1-Score** | 0,72 | Balance óptimo entre precisión y exhaustividad |

### Variables Más Importantes
1. 🎂 **Edad del implicado** (punto medio del rango)
2. ⏰ **Hora del accidente**
3. 🚗 **Tipo de accidente** (colisión, atropello, salida de vía)
4. 📍 **Distrito** (ubicación geográfica)
5. 🌦️ **Condiciones meteorológicas**
6. 🛵 **Tipo de vehículo**

### Cómo Probar el Modelo
Ejecuta el notebook `notebooks/02_modelo_predictivo_gravedad.ipynb`:
1. Celda 1: Instalación automática de dependencias
2. Menú → Kernel → Restart
3. Menú → Cell → Run All
4. Resultados: Métricas, gráfico de importancia y modelo guardado en `models/gravedad_predictor.pkl`

---

## Stack Tecnológico

| Capa | Tecnologías |
|------|-------------|
| **Base de Datos** | MySQL 8.0 |
| **ETL / Ingeniería** | Python, Pandas, mysql-connector-python, PyInstaller |
| **Análisis / ML** | Scikit-learn, Random Forest, Joblib |
| **Visualización** | Matplotlib, Seaborn, Power BI Desktop |
| **Entorno** | Jupyter Notebook, Conda, Git |

---

## Estructura del Proyecto

```
accident-intelligent-agent/
├── README.md                  # 📖 Esta documentación
├── requirements.txt           # 📦 Dependencias Python
├── .env.example               # 🔑 Plantilla de credenciales
├── .gitignore
│
├── scripts/
│   └── export_data.py         # ⚙️ ETL: MySQL → CSV
│
├── notebooks/
│   ├── 01_eda_exploratorio.ipynb              # 🔍 Análisis visual y hallazgos
│   └── 02_modelo_predictivo_gravedad.ipynb    # 🤖 ML: Entrenamiento y evaluación
│
├── models/
│   └── gravedad_predictor.pkl # 💾 Modelo entrenado listo para producción
│
└── data/
    └── processed/             # 📊 CSVs limpios para Power BI
        ├── accidents.csv
        └── involved_parties.csv
```

---

## Cómo Reproducir el Proyecto

```bash
# 1. Clonar repositorio
git clone https://github.com/jleonceo/accident-intelligent-agent.git
cd accident-intelligent-agent

# 2. Crear entorno (recomendado)
conda create -n accident_agent python=3.10
conda activate accident_agent

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales MySQL
cp .env.example .env
# Editar .env con tus datos

# 5. Ejecutar ETL
python scripts/export_data.py

# 6. Abrir análisis
jupyter notebook notebooks/01_eda_exploratorio.ipynb
```

---

## Impacto de Negocio

### Para Autoridades de Tráfico
- 🚨 **Priorización de recursos:** El modelo detecta el 75% de accidentes graves, permitiendo activar protocolos de alta complejidad de forma proactiva.
- 📊 **Prevención focalizada:** Campañas específicas en horas/distritos de mayor riesgo identificado.
- 🗺️ **Planificación urbana:** Insights geoespaciales para rediseño de vías críticas.

### Para Servicios de Emergencia
- ⚡ **Respuesta inteligente:** Integración del modelo en sistemas de despacho para pre-asignar recursos según gravedad predicha.
- 📈 **Métricas de desempeño:** Evaluación continua de la precisión predictiva para mejora iterativa.

### Para Analistas de Datos
- 🔧 **Pipeline reproducible:** Código limpio, comentado y autocontenido.
- 🎓 **Caso de estudio completo:** Desde extracción de datos hasta modelo en producción.

---

## Próximas Mejoras (Roadmap)
- [ ] Integración del modelo en dashboard Power BI (Python Visual)
- [ ] Web App interactiva con Streamlit para pruebas en tiempo real
- [ ] API REST para predicciones desde sistemas externos
- [ ] Modelo multiclase (incluyendo "Fallecimiento" como categoría)
- [ ] Análisis de series temporales para predicción de picos de accidentalidad

---

*Juan Luis León Rodríguez · [LinkedIn](https://linkedin.com/in/jlleonrodriguez/) · [GitHub](https://github.com/jleonceo)*
