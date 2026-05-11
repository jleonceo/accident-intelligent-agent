# 🚗 Accident Intelligence Agent
**Análisis Exploratorio de Accidentalidad Vial en Madrid (2020)**

## 📋 Resumen Ejecutivo
Este proyecto analiza **28,773 accidentes de tráfico** registrados en Madrid durante 2020, con el objetivo de identificar patrones temporales y de severidad para optimizar la prevención vial. Mediante un pipeline ETL robusto (MySQL → Python → CSV) y análisis exploratorio interactivo, se han descubierto insights accionables para autoridades y urbanistas.

## 🔍 Hallazgos Clave
### 1. ⏰ Patrón Temporal Predecible
- **Hora Pico:** 19:00h (2,132 accidentes) coincidiendo con la salida laboral y ocio.
- **Hora Mínima:** 04:00h (187 accidentes).
- **Doble Pico Diario:** Mañana (08:00-10:00h) y Tarde (18:00-20:00h).

### 2. 📊 Distribución de Gravedad
- Entre los datos válidos, la severidad se mantiene **estable (~50% Leve / ~50% Grave)** durante las 24h del día.
- **Insight Sorprendente:** No se detecta un aumento significativo de gravedad en horas nocturnas, desmintiendo el mito de que la noche es intrínsecamente más peligrosa en términos de proporción de lesiones graves.
- **Calidad del Dato:** ~50% de los registros carecen de información de lesividad ("Sin dato"), lo que revela una oportunidad crítica de mejora en los protocolos de reporte policial.

### 3. 🗺️ Análisis Geográfico (Pendiente)
- *Nota: El cruce por distritos y mapa de calor se incorporará en la próxima iteración del dashboard Power BI.*

## 🛠️ Metodología & Stack
- **Extracción:** MySQL + `mysql-connector-python`
- **Transformación:** Python (Pandas) para limpieza, tipado y feature engineering (`HOUR(fecha)`, `gravedad_cat`).
- **Análisis:** Jupyter Notebook + Seaborn/Matplotlib para visualización estadística.
- **Visualización:** Power BI Desktop para dashboard ejecutivo interactivo.

## 📁 Estructura del Proyecto
accident-intelligent-agent/
├── README.md # 📖 Esta documentación
├── requirements.txt # 📦 Dependencias Python
├── .env.example # 🔑 Plantilla de credenciales
├── 📁 scripts/
│ └── export_data.py # ETL: MySQL → CSV optimizado
├── 📁 notebooks/
│ └── 01_eda_exploratorio.ipynb # 🔍 Análisis detallado paso a paso
── 📁 data/processed/ # 📊 CSVs listos para Power BI
└── 📁 powerbi/ # 📈 Dashboard ejecutivo


##  Cómo Reproducir
1. Clona el repositorio: `git clone <tu-repo>`
2. Instala dependencias: `pip install -r requirements.txt`
3. Configura credenciales: Renombra `.env.example` a `.env` y completa los datos de MySQL.
4. Ejecuta ETL: `python scripts/export_data.py`
5. Abre el análisis: `jupyter notebook notebooks/01_eda_exploratorio.ipynb`
6. Carga `accidents.csv` e `involved_parties.csv` en Power BI para interactuar con los datos.

##  Impacto de Negocio
- **Recursos Policiales:** Refuerzo preventivo en franjas 08:00-10:00h y 18:00-20:00h.
- **Campañas de Prevención:** Enfocadas en la estabilidad de la gravedad (la prevención debe ser constante, no solo nocturna).
- **Mejora de Datos:** Protocolo urgente para registrar el campo `lesividad` y reducir el 50% de datos nulos.

---
*Desarrollado con fines analíticos y de portfolio. Datos anonimizados y agregados.*