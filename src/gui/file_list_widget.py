# src/gui/file_list_widget.py

import sys
import logging
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import pyqtSignal, QSize

# Configurar el logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("metacleaner.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class FileListWidget(QListWidget):
    """
    Subclase de QListWidget para manejar eventos de drag and drop.
    """
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)  # No es necesario permitir el arrastre desde la lista
        self.setDropIndicatorShown(True)
        self.setIconSize(QSize(64, 64))
        self.setDragDropMode(QListWidget.DropOnly)  # Configurar el modo de drag and drop
        self.setSpacing(10)
        self.setStyleSheet("""
            QListWidget {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            logging.debug("Drag Enter Event: URLs detectados.")
            event.acceptProposedAction()
        else:
            logging.debug("Drag Enter Event: No se detectaron URLs.")
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            logging.debug("Drag Move Event: URLs detectados.")
            event.acceptProposedAction()
        else:
            logging.debug("Drag Move Event: No se detectaron URLs.")
            event.ignore()

    def dropEvent(self, event):
        logging.debug("Drop Event: Procesando archivos soltados.")
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                logging.debug(f"Archivo detectado: {file_path}")
                files.append(file_path)
            self.files_dropped.emit(files)
            logging.debug(f"Se emitieron {len(files)} archivos mediante files_dropped.")
        else:
            logging.debug("Drop Event: No se detectaron URLs.")
            event.ignore()