# src/metadata_cleaner/reporter.py

import subprocess
import json

class ReportGenerator:
    def __init__(self):
        pass

    def get_metadata(self, file_path):
        command = ['exiftool', '-j', file_path]
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            metadata = json.loads(result.stdout.decode())[0]
            return metadata
        except subprocess.CalledProcessError as e:
            print(f"Error al obtener metadatos: {e.stderr.decode()}")
            return {}

    def generate_report(self, original_metadata, cleaned_metadata, file_path):
        removed_data = {k: original_metadata[k] for k in original_metadata if k not in cleaned_metadata}
        report = {
            'file': file_path,
            'removed_metadata': removed_data
        }
        report['success'] = bool(cleaned_metadata)
        return report
