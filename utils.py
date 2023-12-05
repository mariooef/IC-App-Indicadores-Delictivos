from config import st
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def cargar_csv(ruta_archivo):
    """
    Carga un archivo CSV y devuelve un DataFrame.

    Parámetros:
    - ruta_archivo (str): La ruta del archivo CSV.

    Retorna:
    - pd.DataFrame: El DataFrame cargado desde el archivo CSV.
    """
    try:
        df = pd.read_csv(f"data/csv/{ruta_archivo}.csv")
        return df
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None
    
def cargar_parquet(ruta_archivo):
    """
    Carga un archivo Parquet y devuelve un DataFrame.

    Parámetros:
    - ruta_archivo (str): La ruta del archivo CSV.

    Retorna:
    - pd.DataFrame: El DataFrame cargado desde el archivo Parquet.
    """
    try:
        df = pq.read_table(f"data/parquet/{ruta_archivo}.parquet").to_pandas()
        return df
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None
    
def transforma_a_parquet(ruta_archivo, df):
    """
    Carga un archivo CSV y devuelve un DataFrame.

    Parámetros:
    - ruta_archivo (str): La ruta del archivo CSV.

    Retorna:
    - pd.DataFrame: El DataFrame cargado desde el archivo CSV.
    """
    try:
        archivo_parquet = f"data/parquet/{ruta_archivo}.parquet"
        pq.write_table(pa.Table.from_pandas(df), archivo_parquet)
        return True
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
        return False
    except Exception as e:
        print(f"Error al generar el archivo parquet: {e}")
        return False