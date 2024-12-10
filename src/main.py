# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.interface import MetaCleanerApp

def main():
    app = QApplication(sys.argv)  # Crear QApplication primero
    window = MetaCleanerApp()     # Luego crear la ventana principal
    window.show()                 # Mostrar la ventana
    sys.exit(app.exec_())         # Ejecutar el bucle de la aplicación

if __name__ == '__main__':
    main()
