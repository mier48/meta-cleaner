# tests/test_interface.py

import unittest
from PyQt5.QtWidgets import QApplication
from gui.interface import MetaCleanerApp
import sys

class TestMetaCleanerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        cls.window = MetaCleanerApp(sys.argv)

    def test_window_title(self):
        self.assertEqual(self.window.windowTitle(), "MetaCleaner")

    def test_initial_file_list_count(self):
        self.assertEqual(self.window.file_list.count(), 0)

    def test_add_supported_file(self):
        test_file = 'tests/sample.jpg'
        self.window.file_list.addItem(test_file)
        self.assertEqual(self.window.file_list.count(), 1)
        self.assertEqual(self.window.file_list.item(0).text(), test_file)

    def test_add_unsupported_file(self):
        # Este test requer interacción con la interfaz gráfica que no es trivial
        pass  # Implementar con herramientas de pruebas de GUI si es necesario

if __name__ == '__main__':
    unittest.main()
