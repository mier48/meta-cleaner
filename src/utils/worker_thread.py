# src/utils/worker_thread.py

import sys
import logging
from PyQt5.QtCore import QThread, pyqtSignal

# Configurar el logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("metacleaner.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, files, cleaner, reporter):
        super().__init__()
        self.files = files
        self.cleaner = cleaner
        self.reporter = reporter
        self._is_running = True

    def run(self):
        reports = []
        total_files = len(self.files)
        for index, file_path in enumerate(self.files, start=1):
            if not self._is_running:
                logging.info("WorkerThread ha sido detenido.")
                break
            try:
                logging.info(f"Procesando archivo: {file_path}")
                original_metadata = self.reporter.get_metadata(file_path)
                success = self.cleaner.clean_metadata(file_path)
                if success:
                    cleaned_metadata = self.reporter.get_metadata(file_path)
                    report = self.reporter.generate_report(original_metadata, cleaned_metadata, file_path)
                    reports.append(report)
                    logging.info(f"Metadatos eliminados exitosamente de: {file_path}")
                else:
                    logging.error(f"Error al eliminar metadatos de: {file_path}")
                    report = {
                        'file': file_path,
                        'success': False,
                        'error': 'No se pudieron eliminar los metadatos.'
                    }
                    reports.append(report)
                self.progress.emit(int((index / total_files) * 100))
            except Exception as e:
                error_msg = f"Error al procesar {file_path}: {e}"
                logging.error(error_msg)
                self.error.emit(error_msg)
        self.finished.emit(reports)

    def stop(self):
        self._is_running = False
        self.wait()  # Espera a que el hilo termine