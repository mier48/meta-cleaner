# src/metadata_cleaner/cleaner.py

import subprocess
import os
from utils.helpers import is_supported_file

class MetadataCleaner:
    def __init__(self):
        # Verifica si exiftool está instalado
        if not self._is_exiftool_installed():
            raise EnvironmentError("ExifTool no está instalado o no se encuentra en el PATH.")

    def _is_exiftool_installed(self):
        try:
            subprocess.run(['exiftool', '-ver'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def clean_metadata(self, file_path):
        if not is_supported_file(file_path):
            raise ValueError(f"Tipo de archivo no soportado: {file_path}")

        # Comando para eliminar metadatos preservando el archivo original
        command = ['exiftool', '-all=', '-overwrite_original', file_path]

        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al limpiar metadatos: {e.stderr.decode()}")
            return False
