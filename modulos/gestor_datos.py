# Importamos el módulo 'json' para poder leer y escribir datos en formato JSON
import json
# Importamos el módulo 'os' para interactuar con el sistema operativo (ej. verificar si un archivo existe o crear carpetas)
import os

def cargar_datos(ruta_archivo):
    """Carga datos desde un archivo JSON. Si no existe, retorna una lista vacía."""
    # Verificamos si el archivo especificado en la ruta existe en el disco duro
    if not os.path.exists(ruta_archivo):
        # Si el archivo no existe, retornamos una lista vacía para evitar errores de lectura
        return []
    
    # Iniciamos un bloque try-except para manejar posibles errores al leer el JSON
    try:
        # Abrimos el archivo en modo lectura ('r') y especificamos la codificación 'utf-8' para soportar caracteres especiales (como tildes)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            # Usamos json.load() para convertir el texto JSON del archivo en una lista/diccionario de Python y lo retornamos
            return json.load(f)
    # Si el archivo existe pero su contenido no es un JSON válido (por ejemplo, está vacío o corrupto), capturamos el error
    except json.JSONDecodeError:
        # En caso de error de decodificación, retornamos una lista vacía de forma segura
        return []

def guardar_datos(ruta_archivo, datos):
    """Guarda datos en un archivo JSON."""
    # os.path.dirname obtiene la carpeta contenedora del archivo. 
    # os.makedirs crea esa carpeta (y las anteriores si no existen). exist_ok=True evita errores si la carpeta ya está creada.
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    
    # Abrimos el archivo en modo escritura ('w') con codificación 'utf-8'. Si el archivo ya existía, se sobreescribirá.
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        # json.dump toma los datos de Python (lista/diccionario) y los escribe en el archivo 'f'
        # indent=4 agrega sangrías para que el archivo sea legible por humanos
        # ensure_ascii=False asegura que las tildes y caracteres especiales se guarden tal cual y no como códigos unicode
        json.dump(datos, f, indent=4, ensure_ascii=False)
