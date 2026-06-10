"""
Almacenamiento seguro de credenciales para la GUI.
Usa Windows DPAPI (CryptProtectData) — solo el usuario actual de Windows
puede desencriptar los datos. Sin dependencias externas.
"""

import os
import sys
import json
import base64
import ctypes
from ctypes import wintypes


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_char)),
    ]


def _dpapi_encrypt(data: bytes) -> bytes:
    """Encripta datos con Windows DPAPI. Solo el usuario logueado puede desencriptar."""
    blob_in = _DATA_BLOB(
        len(data),
        ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_char)),
    )
    blob_out = _DATA_BLOB()

    crypt32 = ctypes.windll.crypt32
    if not crypt32.CryptProtectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(blob_out),
    ):
        raise OSError("CryptProtectData failed")

    result = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return result


def _dpapi_decrypt(data: bytes) -> bytes:
    """Desencripta datos protegidos con DPAPI."""
    blob_in = _DATA_BLOB(
        len(data),
        ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_char)),
    )
    blob_out = _DATA_BLOB()

    crypt32 = ctypes.windll.crypt32
    if not crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(blob_out),
    ):
        raise OSError("CryptUnprotectData failed")

    result = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return result


# --- LEGACY: XOR fallback para migrar datos viejos ---

def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def _legacy_decrypt(filepath: str) -> dict | None:
    """Intenta decodificar archivos creados con la versión anterior (XOR + sha256)."""
    try:
        import hashlib
        import platform
        machine = platform.node() or "default_machine"
        key = hashlib.sha256(machine.encode()).digest()
        with open(filepath, "rb") as f:
            encrypted = base64.b64decode(f.read())
        data = _xor_bytes(encrypted, key)
        return json.loads(data.decode("utf-8"))
    except Exception:
        return None


# --- RUTA DEL ARCHIVO ---

from backend.config.paths import get_data_dir

DATA_DIR = get_data_dir()
_CRED_FILE = os.path.join(DATA_DIR, "credentials.dat")


# --- API PUBLICA ---

def save_credentials(email, password, tg_token, tg_chat_id, threshold, headless,
                     diagnostics=False, color_streak_threshold=5, number_delay_threshold=20):
    """Guarda credenciales encriptadas con DPAPI en disco."""
    os.makedirs(os.path.dirname(_CRED_FILE), exist_ok=True)
    data = json.dumps({
        "email": email,
        "password": password,
        "tg_token": tg_token,
        "tg_chat_id": tg_chat_id,
        "threshold": threshold,
        "headless": headless,
        "diagnostics": diagnostics,
        "color_streak_threshold": color_streak_threshold,
        "number_delay_threshold": number_delay_threshold,
    }).encode("utf-8")

    encrypted = _dpapi_encrypt(data)
    with open(_CRED_FILE, "wb") as f:
        f.write(encrypted)


def load_saved_credentials():
    """Carga credenciales guardadas. Retorna dict o None.
    Si el archivo es de la versión anterior (XOR), lo migra automáticamente a DPAPI."""
    if not os.path.exists(_CRED_FILE):
        return None

    raw = None
    try:
        with open(_CRED_FILE, "rb") as f:
            raw = f.read()
    except Exception:
        return None

    if not raw:
        return None

    # 1. Intentar DPAPI (formato actual)
    try:
        data = _dpapi_decrypt(raw)
        return json.loads(data.decode("utf-8"))
    except Exception:
        pass

    # 2. Fallback: intentar XOR legacy → migrar a DPAPI
    legacy = _legacy_decrypt(_CRED_FILE)
    if legacy:
        save_credentials(
            email=legacy.get("email", ""),
            password=legacy.get("password", ""),
            tg_token=legacy.get("tg_token", ""),
            tg_chat_id=legacy.get("tg_chat_id", ""),
            threshold=legacy.get("threshold", 12),
            headless=legacy.get("headless", True),
            diagnostics=legacy.get("diagnostics", False),
            color_streak_threshold=legacy.get("color_streak_threshold", 5),
            number_delay_threshold=legacy.get("number_delay_threshold", 20),
        )
        return legacy

    return None


def has_saved_credentials():
    """Retorna True si hay credenciales guardadas."""
    return os.path.exists(_CRED_FILE)


def delete_saved_credentials():
    """Elimina las credenciales guardadas."""
    if os.path.exists(_CRED_FILE):
        os.remove(_CRED_FILE)
