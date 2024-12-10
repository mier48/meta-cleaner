# Documentación de la API de MetaCleaner

MetaCleaner está diseñado con una arquitectura modular, lo que facilita su extensión y personalización. A continuación, se detalla la API interna de los principales módulos.

## Módulo: `metadata_cleaner`

### Clase: `MetadataCleaner`

Encargada de la eliminación de metadatos de los archivos.

#### Métodos

- **`__init__()`**

  Inicializa la instancia y verifica si ExifTool está instalado.

  ```python
  def __init__(self):
      ...
  ```

- **`clean_metadata(file_path: str) -> bool`**

  Elimina todos los metadatos del archivo especificado.

  **Parámetros:**
  
  - `file_path` (str): Ruta al archivo a procesar.

  **Retorna:**
  
  - `bool`: `True` si la operación fue exitosa, `False` en caso contrario.

- **`_is_exiftool_installed() -> bool`**

  Verifica si ExifTool está instalado y accesible.

  **Retorna:**
  
  - `bool`: `True` si ExifTool está disponible, `False` en caso contrario.

### Clase: `ReportGenerator`

Encargada de generar reportes de los metadatos eliminados.

#### Métodos

- **`__init__()`**

  Inicializa la instancia.

  ```python
  def __init__(self):
      ...
  ```

- **`get_metadata(file_path: str) -> dict`**

  Obtiene los metadatos actuales de un archivo.

  **Parámetros:**
  
  - `file_path` (str): Ruta al archivo.

  **Retorna:**
  
  - `dict`: Diccionario con los metadatos del archivo.

- **`generate_report(original_metadata: dict, cleaned_metadata: dict, file_path: str) -> dict`**

  Genera un reporte de los metadatos eliminados.

  **Parámetros:**
  
  - `original_metadata` (dict): Metadatos antes de la limpieza.
  - `cleaned_metadata` (dict): Metadatos después de la limpieza.
  - `file_path` (str): Ruta al archivo procesado.

  **Retorna:**
  
  - `dict`: Reporte con los metadatos eliminados.

## Módulo: `gui`

### Clase: `MetaCleanerApp`

Encargada de la interfaz gráfica de usuario.

#### Métodos

- **`__init__(argv)`**

  Inicializa la aplicación y configura la interfaz.

  **Parámetros:**
  
  - `argv`: Argumentos de la línea de comandos.

- **`init_ui()`**

  Configura los elementos de la interfaz gráfica.

- **`drag_enter_event(event)`**

  Maneja el evento de arrastrar archivos sobre la lista.

- **`drop_event(event)`**

  Maneja el evento de soltar archivos en la lista.

- **`process_files()`**

  Procesa todos los archivos listados, eliminando sus metadatos y generando el reporte.

## Módulo: `utils`

### Funciones

- **`is_supported_file(file_path: str) -> bool`**

  Verifica si el archivo tiene una extensión soportada.

  **Parámetros:**
  
  - `file_path` (str): Ruta al archivo.

  **Retorna:**
  
  - `bool`: `True` si el archivo es soportado, `False` en caso contrario.

## Ejemplo de Uso

```python
from metadata_cleaner import MetadataCleaner, ReportGenerator

# Inicializar
cleaner = MetadataCleaner()
reporter = ReportGenerator()

# Ruta al archivo
file_path = 'path/to/your/file.jpg'

# Obtener metadatos originales
original_metadata = reporter.get_metadata(file_path)

# Limpiar metadatos
if cleaner.clean_metadata(file_path):
    cleaned_metadata = reporter.get_metadata(file_path)
    report = reporter.generate_report(original_metadata, cleaned_metadata, file_path)
    print(report)
else:
    print("Error al limpiar metadatos.")
