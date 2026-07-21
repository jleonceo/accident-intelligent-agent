"""
Accident Intelligence Agent - Data Loader
Carga datos de accidentalidad vial de Madrid 2020 a MySQL
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

def _col(row, nombre):
    """Busca una columna casando por espacios NORMALIZADOS, no por igualdad exacta.

    El Excel del Ayuntamiento de Madrid escribe la cabecera del expediente con dos
    espacios ('Nº  EXPEDIENTE'). Buscarla con uno devolvía None en todas las filas y
    nadie se enteraba, porque `row.get` no falla: devuelve el valor por defecto. Un
    fallo silencioso de este tipo costó dos meses de una cifra publicada tres veces
    mayor que la real. Casar por espacios normalizados lo cierra para siempre.
    """
    objetivo = " ".join(str(nombre).split()).upper()
    for clave in row.index:
        if " ".join(str(clave).split()).upper() == objetivo:
            return row[clave]
    return None


def limpiar(valor):
    """Convierte NaN/NaT a None para que MySQL inserte NULL"""
    if valor is None:
        return None
    try:
        if pd.isna(valor):
            return None
    except (TypeError, ValueError):
        pass
    return valor

def conectar_mysql():
    """Conectar a MySQL Server"""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("✅ Conexión exitosa a MySQL")
        return conexion
    except Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

def crear_base_datos(cursor):
    """Usar la base de datos"""
    db_name = os.getenv('DB_NAME')
    cursor.execute(f"USE {db_name}")
    print(f"✅ Base de datos '{db_name}' lista")

def leer_excel(ruta_archivo):
    """Leer y limpiar el Excel"""
    print(f"📖 Leyendo archivo: {ruta_archivo}")

    df = pd.read_excel(ruta_archivo)
    df = df.dropna(how='all')

    print(f"📊 Registros leídos: {len(df)}")
    print(f"📋 Columnas encontradas: {list(df.columns)}")

    return df

def cargar_datos(cursor, df):
    """Cargar datos a las tablas"""

    accidentes_cargados = 0
    involucrados_cargados = 0
    accidentes_map = {}

    print("⏳ Procesando datos (esto puede tardar unos minutos)...")

    for index, row in df.iterrows():
        try:
            # ===========================================
            # 1. DATOS DEL ACCIDENTE
            # ===========================================
            # El Excel del Ayuntamiento escribe la cabecera con DOS espacios:
            # 'Nº  EXPEDIENTE'. Este código buscaba 'Nº EXPEDIENTE' con uno, así que
            # `row.get` devolvía None SIEMPRE y cada fila caía al `ACC_{index}` de abajo.
            # Efecto: cada persona implicada se contaba como un accidente distinto, y el
            # proyecto publicó 28.773 accidentes cuando son 12.634 (2,28 implicados de
            # media por accidente). Corregido el 21/07/2026 casando la cabecera por
            # espacios normalizados, para que no vuelva a romperse si cambian el formato.
            expediente   = _col(row, 'Nº EXPEDIENTE')
            fecha        = limpiar(row.get('FECHA', None))
            hora         = limpiar(row.get('HORA', None))
            calle        = limpiar(row.get('CALLE', None))
            distrito     = limpiar(row.get('DISTRITO', None))
            tipo_acc     = limpiar(row.get('TIPO ACCIDENTE', None))
            estado_meteo = limpiar(row.get('ESTADO METEREOLÓGICO', None))

            clave_accidente = str(expediente) if pd.notna(expediente) else f"ACC_{index}"

            if clave_accidente not in accidentes_map:
                cursor.execute("""
                INSERT INTO accidents
                    (id_accident, fecha, hora, calle, distrito, tipo_accidente, estado_meteorologico)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (clave_accidente, fecha, hora, calle, distrito, tipo_acc, estado_meteo))

                accidentes_map[clave_accidente] = clave_accidente
                accidentes_cargados += 1

            # ===========================================
            # 2. DATOS DE LA PERSONA INVOLUCRADA
            # ===========================================
            id_acc        = accidentes_map[clave_accidente]
            tipo_persona  = limpiar(row.get('TIPO PERSONA', None))
            tipo_vehiculo = limpiar(row.get('TIPO VEHÍCULO', None))
            sexo          = limpiar(row.get('SEXO', None))
            rango_edad    = limpiar(row.get('RANGO DE EDAD', None))
            lesividad     = limpiar(row.get('LESIVIDAD*', None))

            cursor.execute("""
            INSERT INTO involved_parties
                (id_accident, tipo_persona, tipo_vehiculo, sexo, edad, lesividad)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_acc, tipo_persona, tipo_vehiculo, sexo, rango_edad, lesividad))

            involucrados_cargados += 1

            if involucrados_cargados % 5000 == 0:
                print(f"   → Procesados: {involucrados_cargados} registros...")

        except Exception as e:
            print(f"⚠️ Error en fila {index}: {e}")
            continue

    return accidentes_cargados, involucrados_cargados

def main():
    print("=" * 70)
    print("🚗 ACCIDENT INTELLIGENCE AGENT - DATA LOADER")
    print("=" * 70)

    ruta_excel = os.path.join('data', 'raw', '2020_Accidentalidad.xlsx')

    if not os.path.exists(ruta_excel):
        print(f"❌ Error: No se encuentra el archivo: {ruta_excel}")
        print("💡 Verifica que el archivo esté en: data/raw/2020_Accidentalidad.xlsx")
        return

    conexion = conectar_mysql()
    if not conexion:
        return

    cursor = conexion.cursor()

    try:
        crear_base_datos(cursor)
        df = leer_excel(ruta_excel)
        accidentes, involucrados = cargar_datos(cursor, df)
        conexion.commit()

        print("\n" + "=" * 70)
        print("✅ CARGA COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print(f"📦 Accidentes únicos cargados:      {accidentes}")
        print(f"👥 Personas involucradas cargadas:  {involucrados}")
        print(f"💾 Base de datos:                   {os.getenv('DB_NAME')}")
        print(f"📊 Promedio personas por accidente: {involucrados/accidentes:.2f}")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()
        print("\n🔌 Conexión a MySQL cerrada")

if __name__ == "__main__":
    main()
