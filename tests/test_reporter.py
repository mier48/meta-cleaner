# tests/test_reporter.py

import unittest
import os
from metadata_cleaner import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.reporter = ReportGenerator()
        self.test_file = 'tests/sample.jpg'
        # Crear un archivo de muestra si no existe
        if not os.path.exists(self.test_file):
            with open(self.test_file, 'w') as f:
                f.write('Sample image content')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_get_metadata(self):
        metadata = self.reporter.get_metadata(self.test_file)
        self.assertIsInstance(metadata, dict)

    def test_generate_report(self):
        original_metadata = {'Author': 'John Doe', 'Description': 'Sample Image'}
        cleaned_metadata = {}
        report = self.reporter.generate_report(original_metadata, cleaned_metadata, self.test_file)
        expected_report = {
            'file': self.test_file,
            'removed_metadata': original_metadata
        }
        self.assertEqual(report, expected_report)

if __name__ == '__main__':
    unittest.main()
