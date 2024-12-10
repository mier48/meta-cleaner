# Uso de MetaCleaner

MetaCleaner ofrece una interfaz gráfica sencilla para eliminar metadatos de tus archivos multimedia y documentos. A continuación, se explica cómo utilizar la herramienta.

## Iniciar la Aplicación

Después de la instalación, puedes iniciar MetaCleaner de las siguientes maneras:

- **Desde la Terminal/CMD:**

  ```bash
  metacleaner
  ```

- **Directamente con Python:**

  ```bash
  python src/main.py
  ```

## Interfaz de Usuario

La interfaz principal consta de los siguientes elementos:

- **Área de Arrastrar y Soltar:** Aquí puedes arrastrar los archivos que deseas procesar.
- **Lista de Archivos:** Muestra los archivos añadidos y su estado de procesamiento.
- **Botón "Procesar Archivos":** Inicia el proceso de eliminación de metadatos para los archivos listados.

## Pasos para Eliminar Metadatos

1. **Añadir Archivos:**
   - Arrastra y suelta los archivos soportados (imágenes, videos, documentos) en el área designada.
   - Alternativamente, puedes implementar una funcionalidad para seleccionar archivos mediante un diálogo si así lo deseas.

2. **Procesar Archivos:**
   - Haz clic en el botón "Procesar Archivos".
   - La aplicación eliminará los metadatos de cada archivo y actualizará el estado en la lista.

3. **Revisar Reporte:**
   - Al finalizar, se generará un archivo `metacleaner_report.json` en el directorio actual.
   - Este archivo contiene detalles de los metadatos eliminados de cada archivo procesado.

## Notas Adicionales

- **Soporte de Archivos:** Asegúrate de que los archivos que intentas procesar estén en los formatos soportados (consulta `utils/helpers.py` para una lista completa).
- **Permisos:** Asegúrate de tener los permisos necesarios para leer y escribir en los archivos que deseas procesar.
- **Respaldo:** Es recomendable mantener copias de seguridad de tus archivos originales antes de procesarlos.

---

Si encuentras algún problema o tienes sugerencias, no dudes en [abrir un issue](https://github.com/mier48/meta-cleaner/issues) en el repositorio de GitHub.
