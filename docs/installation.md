# Instalación de MetaCleaner

## Requisitos Previos

- **Python 3.7 o superior**: Asegúrate de tener Python instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **ExifTool**: Necesario para la manipulación de metadatos.

### Instalación de ExifTool

#### Windows

1. Descarga ExifTool desde [ExifTool for Windows](https://exiftool.org/).
2. Extrae el archivo descargado y renombra `exiftool(-k).exe` a `exiftool.exe`.
3. Coloca `exiftool.exe` en una carpeta que esté en tu `PATH`, por ejemplo, `C:\Windows\`.

#### macOS

Puedes instalar ExifTool usando Homebrew:

```bash
brew install exiftool
```

#### Linux

En la mayoría de las distribuciones de Linux, puedes instalar ExifTool usando el gestor de paquetes:

```bash
sudo apt-get install libimage-exiftool-perl
```

##### Arch Linux
```bash
sudo pacman -S perl-image-exiftool
```

## Clonar el Repositorio

```bash
git clone https://github.com/mier48/meta-cleaner.git
cd MetaCleaner
```

## Crear un Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

## Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Instalación del Paquete

```bash
python setup.py install
```

## Verificar la Instalación

Puedes ejecutar la aplicación usando:

```bash
python src/main.py
```

O si configuraste los scripts de consola en `setup.py`, simplemente:

```bash
metacleaner
```

---

¡Ahora estás listo para usar MetaCleaner!
