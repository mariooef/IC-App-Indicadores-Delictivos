
import pandas as pd
from config import st

def cargar_csv(ruta_archivo):
    """
    Carga un archivo CSV y devuelve un DataFrame.

    Parámetros:
    - ruta_archivo (str): La ruta del archivo CSV.

    Retorna:
    - pd.DataFrame: El DataFrame cargado desde el archivo CSV.
    """
    try:
        df = pd.read_csv(f"data/{ruta_archivo}.csv")
        return df
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None