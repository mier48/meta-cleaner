# tests/test_cleaner.py

import unittest
import os
from metadata_cleaner import MetadataCleaner
from utils.helpers import is_supported_file

class TestMetadataCleaner(unittest.TestCase):
    def setUp(self):
        self.cleaner = MetadataCleaner()
        self.test_file = 'tests/sample.jpg'
        # Crear un archivo de muestra si no existe
        if not os.path.exists(self.test_file):
            with open(self.test_file, 'w') as f:
                f.write('Sample image content')

    def tearDown(self):
        # Restaurar el archivo original después de la prueba
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_is_supported_file(self):
        self.assertTrue(is_supported_file('image.jpg'))
        self.assertFalse(is_supported_file('archive.zip'))

    def test_clean_metadata_success(self):
        result = self.cleaner.clean_metadata(self.test_file)
        self.assertTrue(result)

    def test_clean_metadata_unsupported_file(self):
        with self.assertRaises(ValueError):
            self.cleaner.clean_metadata('unsupported_file.exe')

if __name__ == '__main__':
    unittest.main()
