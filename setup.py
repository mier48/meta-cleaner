from setuptools import setup, find_packages

setup(
    name='Meta Cleaner',
    version='0.1.0',
    author='Alberto Mier',
    author_email='info@albertomier.com',
    description='Una herramienta para eliminar metadatos de imágenes, videos y documentos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mier48/meta-cleaner',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5>=5.15.0',
        'exiftool>=1.3.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'metacleaner=main:main',
        ],
    },
)
