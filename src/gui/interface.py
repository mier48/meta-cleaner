# src/gui/interface.py

import sys
import os
import logging
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFileDialog, QListWidgetItem, 
    QMessageBox, QProgressBar, QStatusBar, QAction, QToolBar, QSpacerItem, 
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from metadata_cleaner import MetadataCleaner, ReportGenerator
from utils.helpers import is_supported_file, is_image_file
from gui.file_list_widget import FileListWidget
from gui.metadata_dialog import MetadataDialog
from utils.worker_thread import WorkerThread

# Configurar el logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("metacleaner.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class MetaCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meta Cleaner")
        self.setGeometry(100, 100, 800, 600)  # Aumentar el tamaño para mejor distribución
        self.setMinimumWidth(800)  # Establecer el ancho mínimo
        self.setMinimumHeight(600)  # Establecer la altura mínima
        self.setMaximumWidth(800) # Establecer el ancho máximo
        self.setMaximumHeight(600)  # Establecer la altura máxima
        self.setWindowIcon(QIcon('icons/metacleaner.png'))  # Asegúrate de tener un icono adecuado

        # Aplicar un estilo moderno utilizando Style Sheets
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: none;
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
            QProgressBar {
                height: 20px;
                border: 1px solid #555555;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 1px;
            }
            QStatusBar {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3a3a3a;
            }
            QMenu {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #3a3a3a;
            }
        """)

        try:
            self.cleaner = MetadataCleaner()
            logging.info("MetadataCleaner inicializado correctamente.")
        except Exception as e:
            logging.critical(f"Error al inicializar MetadataCleaner: {e}")
            QMessageBox.critical(self, "Error", f"Error al inicializar MetadataCleaner: {e}")
            sys.exit(1)

        try:
            self.reporter = ReportGenerator()
            logging.info("ReportGenerator inicializado correctamente.")
        except Exception as e:
            logging.critical(f"Error al inicializar ReportGenerator: {e}")
            QMessageBox.critical(self, "Error", f"Error al inicializar ReportGenerator: {e}")
            sys.exit(1)

        self.worker = None  # Inicializar el atributo worker
        self.init_ui()

    def init_ui(self):
        # Configurar la barra de menús
        # self.menu_bar = self.menuBar()

        # # Menú Archivo
        # file_menu = self.menu_bar.addMenu("Archivo")

        # select_action = QAction(QIcon('icons/select.png'), "Seleccionar Archivos", self)
        # select_action.triggered.connect(self.select_files)
        # file_menu.addAction(select_action)

        # clear_action = QAction(QIcon('icons/clear.png'), "Limpiar Lista", self)
        # clear_action.triggered.connect(self.clear_file_list)
        # file_menu.addAction(clear_action)

        # exit_action = QAction(QIcon('icons/exit.png'), "Salir", self)
        # exit_action.triggered.connect(self.close)
        # file_menu.addAction(exit_action)

        # # Menú Procesar
        # process_menu = self.menu_bar.addMenu("Procesar")

        # process_action = QAction(QIcon('icons/process.png'), "Procesar Archivos", self)
        # process_action.triggered.connect(self.process_files)
        # process_menu.addAction(process_action)

        # # Menú Ayuda
        # help_menu = self.menu_bar.addMenu("Ayuda")

        # about_action = QAction(QIcon('icons/about.png'), "Acerca de", self)
        # about_action.triggered.connect(self.show_about_dialog)
        # help_menu.addAction(about_action)

        # # Barra de herramientas
        # self.toolbar = QToolBar("Herramientas")
        # self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # self.toolbar.addAction(select_action)
        # self.toolbar.addAction(clear_action)
        # self.toolbar.addAction(process_action)
        # self.toolbar.addAction(about_action)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # # Título
        # title = QLabel("Meta Cleaner")
        # title.setAlignment(Qt.AlignCenter)
        # title.setFont(QFont("Arial", 20, QFont.Bold))
        # main_layout.addWidget(title)

        # Instrucción
        instruction = QLabel("Arrastra y suelta archivos aquí para limpiar sus metadatos:")
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setFont(QFont("Arial", 12))
        main_layout.addWidget(instruction)

        # Lista de archivos con marco
        self.file_list = FileListWidget()
        self.file_list.files_dropped.connect(self.handle_files_dropped)
        main_layout.addWidget(self.file_list, stretch=1)

        # Botones principales
        button_layout = QHBoxLayout()

        select_button = QPushButton("Seleccionar Archivos")
        select_button.setIcon(QIcon('icons/select.png'))
        select_button.clicked.connect(self.select_files)
        button_layout.addWidget(select_button)

        remove_button = QPushButton("Eliminar Seleccionados")
        remove_button.setIcon(QIcon('icons/remove.png'))
        remove_button.clicked.connect(self.remove_selected_files)
        button_layout.addWidget(remove_button)

        clear_button = QPushButton("Limpiar Lista")
        clear_button.setIcon(QIcon('icons/clear.png'))
        clear_button.clicked.connect(self.clear_file_list)
        button_layout.addWidget(clear_button)

        process_button = QPushButton("Procesar Archivos")
        process_button.setIcon(QIcon('icons/process.png'))
        process_button.clicked.connect(self.process_files)
        button_layout.addWidget(process_button)

        show_metadata_button = QPushButton("Mostrar Metadatos")
        show_metadata_button.setIcon(QIcon('icons/show.png'))
        show_metadata_button.clicked.connect(self.show_metadata)
        button_layout.addWidget(show_metadata_button)

        # # Añadir un espaciador para alinear los botones a la izquierda
        # spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # button_layout.addItem(spacer)

        main_layout.addLayout(button_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.progress_bar)

        central_widget.setLayout(main_layout)

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def show_about_dialog(self):
        about_text = """
        <h2>Meta Cleaner</h2>
        <p>Versión 1.0</p>
        <p>Desarrollado por [Tu Nombre].</p>
        <p>Esta aplicación permite limpiar metadatos de archivos seleccionados de manera sencilla y eficiente.</p>
        """
        QMessageBox.about(self, "Acerca de Meta Cleaner", about_text)

    def handle_files_dropped(self, file_paths):
        """
        Maneja los archivos soltados a través de drag and drop.
        """
        added_files = 0
        for file_path in file_paths:
            if is_supported_file(file_path):
                if not self.is_file_already_added(file_path):
                    self.add_file_to_list(file_path)
                    added_files += 1
                    logging.debug(f"Archivo soportado añadido mediante drag and drop: {file_path}")
                else:
                    logging.info(f"Archivo ya añadido mediante drag and drop: {file_path}")
            else:
                logging.warning(f"Archivo no soportado mediante drag and drop: {file_path}")
                QMessageBox.warning(self, "Archivo no soportado", f"Tipo de archivo no soportado: {file_path}")
        if added_files > 0:
            self.status_bar.showMessage(f"{added_files} archivos añadidos mediante drag and drop.", 5000)

    def is_file_already_added(self, file_path):
        for index in range(self.file_list.count()):
            item = self.file_list.item(index)
            if item.data(Qt.UserRole) == file_path:
                return True
        return False

    def add_file_to_list(self, file_path):
        if is_image_file(file_path):
            # Crear un QPixmap y generar un thumbnail
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                thumbnail = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(thumbnail)
            else:
                # Si no se puede cargar la imagen, usar un icono genérico
                icon = QIcon('icons/image_placeholder.png')  # Asegúrate de tener este icono
        else:
            # Usar un icono genérico para otros tipos de archivos
            icon = QIcon('icons/file_generic.png')  # Asegúrate de tener este icono

        # Crear el QListWidgetItem con el icono y el nombre del archivo
        file_name = os.path.basename(file_path)
        item = QListWidgetItem(icon, file_name)
        item.setData(Qt.UserRole, file_path)  # Almacenar la ruta completa en los datos del item
        self.file_list.addItem(item)
        logging.debug(f"Archivo añadido a la lista: {file_path}")

    def select_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar Archivos", "",
            "Todos los Archivos (*);;Imágenes (*.jpg *.jpeg *.png *.gif *.bmp *.tiff);;Videos (*.mp4 *.mov *.avi *.mkv);;Documentos (*.pdf *.docx *.xlsx *.pptx *.txt)",
            options=options
        )
        if files:
            added_files = 0
            for file_path in files:
                if is_supported_file(file_path):
                    if not self.is_file_already_added(file_path):
                        self.add_file_to_list(file_path)
                        added_files += 1
                        logging.debug(f"Archivo añadido manualmente: {file_path}")
                    else:
                        logging.info(f"Archivo ya añadido manualmente: {file_path}")
                else:
                    QMessageBox.warning(self, "Archivo no soportado", f"Tipo de archivo no soportado: {file_path}")
                    logging.warning(f"Archivo no soportado añadido manualmente: {file_path}")
            self.status_bar.showMessage(f"{added_files} archivos añadidos.", 5000)

    def remove_selected_files(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Sin selección", "No hay archivos seleccionados para eliminar.")
            return
        for item in selected_items:
            self.file_list.takeItem(self.file_list.row(item))
            logging.info(f"Archivo eliminado de la lista: {item.data(Qt.UserRole)}")
        self.status_bar.showMessage("Archivos seleccionados eliminados.", 5000)

    def clear_file_list(self):
        self.file_list.clear()
        logging.info("Lista de archivos limpiada.")
        self.status_bar.showMessage("Lista de archivos limpiada.", 5000)

    def process_files(self):
        if self.file_list.count() == 0:
            QMessageBox.information(self, "No hay archivos", "No se han añadido archivos para procesar.")
            logging.info("Intento de procesar archivos sin añadir ninguno.")
            return

        files = [self.file_list.item(index).data(Qt.UserRole) for index in range(self.file_list.count())]

        # Deshabilitar botones durante el procesamiento
        self.set_buttons_enabled(False)
        self.status_bar.showMessage("Procesando archivos...")

        # Iniciar el hilo de trabajo
        self.worker = WorkerThread(files, self.cleaner, self.reporter)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.start()

    def show_metadata(self):
        if self.file_list.count() == 0:
            QMessageBox.information(self, "No hay archivos", "No se han añadido archivos para mostrar metadatos.")
            logging.info("Intento de mostrar metadatos sin añadir ninguno.")
            return

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Sin selección", "No hay archivos seleccionados para mostrar metadatos.")
            return

        for item in selected_items:
            file_path = item.data(Qt.UserRole)
            metadata = self.reporter.get_metadata(file_path)
            metadata_str = json.dumps(metadata, indent=4, ensure_ascii=False)

            # Crear y mostrar el diálogo personalizado
            dialog = MetadataDialog(os.path.basename(file_path), metadata_str, self)
            dialog.exec_()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_processing_finished(self, reports):
        self.worker = None
        self.set_buttons_enabled(True)
        self.progress_bar.setValue(100)
        self.status_bar.showMessage("Proceso completado.", 5000)

        # Generar un reporte consolidado
        report_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, 'metacleaner_report.json')
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(reports, f, indent=4, ensure_ascii=False)
            logging.info(f"Reporte generado en: {report_path}")
            QMessageBox.information(self, "Proceso Completo", f"Se ha completado el proceso.\nReporte generado en: {report_path}")
        except Exception as e:
            logging.error(f"Error al generar el reporte: {e}")
            QMessageBox.critical(self, "Error", f"Error al generar el reporte: {e}")

        logging.info(f"Reportes: {reports}")

        # Actualizar la lista de archivos con el estado
        for index in range(self.file_list.count()):
            item = self.file_list.item(index)
            file_path = item.data(Qt.UserRole)
            report = next((r for r in reports if r['file'] == file_path), None)

            if report:
                status = "Limpio" if report.get('success') else "Error"
                item.setText(f"{os.path.basename(file_path)} - {status}")
                if is_image_file(file_path):
                    # Actualizar el icono si es necesario
                    if report.get('success'):
                        # Cambiar el icono a uno que indique éxito
                        success_icon = QIcon('icons/success.png')  # Asegúrate de tener este icono
                        item.setIcon(success_icon)
                    else:
                        # Icono de error
                        error_icon = QIcon('icons/error.png')  # Asegúrate de tener este icono
                        item.setIcon(error_icon)
                else:
                    # Para otros tipos de archivos, podrías cambiar el icono o mantenerlo
                    if report.get('success'):
                        success_icon = QIcon('icons/success.png')
                        item.setIcon(success_icon)
                    else:
                        error_icon = QIcon('icons/error.png')
                        item.setIcon(error_icon)

    def on_processing_error(self, message):
        QMessageBox.warning(self, "Error durante el procesamiento", message)
        self.status_bar.showMessage("Error durante el procesamiento.", 5000)

    def set_buttons_enabled(self, enabled):
        for widget in self.findChildren(QPushButton):
            widget.setEnabled(enabled)
        # También deshabilitar las acciones del menú y la barra de herramientas
        # for action in self.menu_bar.actions():
        #     submenu = action.menu()
        #     if submenu:
        #         for sub_action in submenu.actions():
        #             sub_action.setEnabled(enabled)
        # for action in self.toolbar.actions():
        #     action.setEnabled(enabled)

    def closeEvent(self, event):
        """Reimplementa el método closeEvent para asegurar que los hilos se cierren correctamente."""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                'Salir',
                'El proceso aún se está ejecutando. ¿Deseas salir de todas formas?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.worker.stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()