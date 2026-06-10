"""
Resolucion centralizada de rutas para desarrollo y PyInstaller.
Elimina el patron if getattr(sys, 'frozen', False) duplicado en 10+ archivos.
"""

import os
import sys


def is_frozen():
    return getattr(sys, 'frozen', False)


def get_base_dir():
    """Directorio raiz del paquete backend (frozen) o del source (dev)."""
    if is_frozen():
        return os.path.dirname(sys.executable)
    # paths.py esta en backend/config/ → subir un nivel a backend/
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_dir():
    """Directorio data/ para BD, credenciales, logs."""
    d = os.path.join(get_base_dir(), "data")
    os.makedirs(d, exist_ok=True)
    return d

