"""
Accident Intelligence Agent - Data Exporter
Exporta datos de MySQL a CSV limpios para Power BI y análisis en Python
"""
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("✅ Conexión exitosa a MySQL")
        return conexion
    except Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

def exportar_tabla(conexion, query, nombre_archivo, carpeta_salida):
    df = pd.read_sql(query, conexion)
    ruta = os.path.join(carpeta_salida, nombre_archivo)
    df.to_csv(ruta, index=False, encoding='utf-8-sig')
    print(f"✅ {nombre_archivo} exportado — {len(df):,} registros → {ruta}")
    return df

def main():
    print("=" * 70)
    print("📤 ACCIDENT INTELLIGENCE AGENT - DATA EXPORTER")
    print("=" * 70)
    
    carpeta_salida = os.path.join('data', 'processed')
    os.makedirs(carpeta_salida, exist_ok=True)

    conexion = conectar_mysql()
    if not conexion:
        return

    try:
        exportar_tabla(
            conexion,
            """
            SELECT 
                id_accident,
                DATE(fecha) AS fecha,
                HOUR(hora) AS hora,
                calle,
                distrito,
                tipo_accidente,
                estado_meteorologico
            FROM accidents
            WHERE hora IS NOT NULL
            ORDER BY fecha, hora
            """,
            'accidents.csv',
            carpeta_salida
        )

        exportar_tabla(
            conexion,
            """
            SELECT
                id_involved,
                id_accident,
                tipo_persona,
                tipo_vehiculo,
                sexo,
                edad,
                lesividad
            FROM involved_parties
            ORDER BY id_involved
            """,
            'involved_parties.csv',
            carpeta_salida
        )

        print("\n" + "=" * 70)
        print("✅ EXPORTACIÓN COMPLETADA")
        print("=" * 70)
        print(f"📁 Archivos en: {os.path.abspath(carpeta_salida)}")
        print("   → accidents.csv")
        print("   → involved_parties.csv")
        print("💡 Abre Power BI y refresca para ver los datos actualizados")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error durante la exportación: {e}")
        raise

    finally:
        conexion.close()
        print("\n🔌 Conexión a MySQL cerrada")

if __name__ == "__main__":
    main()