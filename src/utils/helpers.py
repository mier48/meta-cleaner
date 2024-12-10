# src/utils/helpers.py

import os

SUPPORTED_EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt']
}

def is_supported_file(file_path):
    _, ext = os.path.splitext(file_path.lower())
    for category in SUPPORTED_EXTENSIONS:
        if ext in SUPPORTED_EXTENSIONS[category]:
            return True
    return False

def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in image_extensions