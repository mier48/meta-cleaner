# src/gui/metadata_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt

class MetadataDialog(QDialog):
    def __init__(self, file_name, metadata, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Metadatos de {file_name}")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setMaximumHeight(750)  # Establecer la altura máxima aquí

        layout = QVBoxLayout()

        # Widget de texto para mostrar los metadatos
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(metadata)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2e2e2e;
                color: #ffffff;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.text_edit)

        # Botón para cerrar el diálogo
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #2e2e2e;
            }
        """)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)
