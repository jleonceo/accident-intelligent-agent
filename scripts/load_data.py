"""
Accident Intelligence Agent - Data Loader
Carga datos de accidentalidad vial de Madrid 2020 a MySQL
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import sys

# La consola de Windows usa cp1252 por defecto, y este script imprime simbolos que no caben ahi.
# Sin esta linea, `python scripts/load_data.py` moria con UnicodeEncodeError en la primera linea
# de salida, antes de leer un solo dato: el codigo funcionaba y el usuario veia un traceback.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

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

def vaciar_tablas(cursor):
    """Deja las tablas vacías antes de cargar. Es lo que el README llama «recarga».

    POR QUE (26/07/2026). Este cargador NO ERA IDEMPOTENTE, y el daño ya estaba hecho y publicado.
    Al ejecutarlo por segunda vez, cada accidente chocaba con su clave primaria y se descartaba,
    pero `involved_parties` no tiene clave única: sus filas se insertaban OTRA VEZ. Medido el
    26/07 sobre la base viva: 57.546 personas implicadas donde el Excel trae 28.773, o sea el
    doble exacto; y 41.407 accidentes, que son los 28.773 de la carga vieja y equivocada más los
    12.634 de la corregida, conviviendo en la misma tabla.

    De ahí salieron los CSV que el repositorio publica. El README anunciaba 12.634 accidentes
    desde el 21/07 mientras `data/processed/accidents.csv` tenía 41.407 filas. Es literalmente la
    lección que ese mismo README enseña: corregir la portada no corrige el proyecto.

    Se borra en el orden de las claves ajenas: primero las personas, después los accidentes.
    """
    print("🧹 Vaciando las tablas antes de recargar (el README llama a esto «recarga»)...")
    cursor.execute("DELETE FROM involved_parties")
    cursor.execute("DELETE FROM accidents")


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
        vaciar_tablas(cursor)
        accidentes, involucrados = cargar_datos(cursor, df)
        conexion.commit()

        print("\n" + "=" * 70)
        # El titular depende del resultado. Antes decía SIEMPRE «CARGA COMPLETADA EXITOSAMENTE»,
        # incluso con cero accidentes cargados y un traceback dos líneas más abajo.
        print("✅ CARGA COMPLETADA" if accidentes else "❌ NO SE HA CARGADO NINGÚN ACCIDENTE")
        print("=" * 70)
        print(f"📦 Accidentes únicos cargados:      {accidentes}")
        print(f"👥 Personas involucradas cargadas:  {involucrados}")
        print(f"💾 Base de datos:                   {os.getenv('DB_NAME')}")
        # El promedio solo existe si se cargó algo. Con cero accidentes esta línea moría con
        # ZeroDivisionError DESPUÉS de anunciar "CARGA COMPLETADA EXITOSAMENTE", que es la peor
        # combinación posible: el usuario lee que todo fue bien y acto seguido ve un traceback.
        # Cero accidentes no es un error del script, es que el Excel no trajo filas válidas, y eso
        # hay que decirlo con esas palabras.
        if accidentes:
            print(f"📊 Promedio personas por accidente: {involucrados/accidentes:.2f}")
        else:
            print("⚠️  No se ha cargado ningún accidente: revisa que el Excel de origen tenga")
            print("    filas y que las cabeceras coincidan con las que espera `_col`.")
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
