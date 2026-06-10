"""
Manejo de credenciales y runtime overrides del bot.
Separado de config.py para romper el god node central.
"""

import os
import time

# --- RUNTIME OVERRIDES (set by GUI) ---
_runtime_overrides = {}

# --- CACHE DE CREDENCIALES ---
_CACHE_TTL = 30
_credentials_cache = {"value": None, "expires_at": 0}
_color_threshold_cache = {"value": None, "expires_at": 0}
_number_threshold_cache = {"value": None, "expires_at": 0}


def _cache_get(cache):
    now = time.time()
    if cache["value"] is not None and now < cache["expires_at"]:
        return cache["value"]
    return None


def _cache_set(cache, value):
    cache["value"] = value
    cache["expires_at"] = time.time() + _CACHE_TTL


def set_runtime_config(**kwargs):
    """Permite a la GUI inyectar credenciales sin modificar .env.
    Uso: set_runtime_config(email='x', password='y', ...)
    """
    _runtime_overrides.update(kwargs)


def load_credentials():
    """Lee credenciales. Prioridad: runtime overrides > .env > DPAPI (gui_credentials).
    Cachea el resultado por 30s para evitar lecturas repetidas."""
    # Si la GUI ya configuró las credenciales, usarlas directamente (sin cache)
    if _runtime_overrides:
        return (
            _runtime_overrides.get('email', ''),
            _runtime_overrides.get('password', ''),
            _runtime_overrides.get('tg_token', ''),
            _runtime_overrides.get('tg_chat_id', ''),
            _runtime_overrides.get('threshold', 12),
            _runtime_overrides.get('headless', True),
        )

    # Usar cache si está vigente
    cached = _cache_get(_credentials_cache)
    if cached is not None:
        return cached

    # Defaults
    email = ""
    password = ""
    tg_token = ""
    tg_chat_id = ""
    alert_threshold = 12
    headless = True

    # 1. Intentar leer desde .env (fallback legacy)
    # credentials.py esta en backend/auth/ → subir 3 niveles para llegar a la raiz del proyecto
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    env_loaded = False
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    parts = line.split("=", 1)
                    key = parts[0].strip()
                    val = parts[1].split("#")[0].strip()

                    if key == "STAKE_EMAIL" or key == "CORREO":
                        email = val
                        env_loaded = True
                    elif key == "STAKE_PASSWORD" or key == "CONTRASEÑA" or key == "CONTRASENA":
                        password = val
                    elif key == "TELEGRAM_TOKEN":
                        tg_token = val
                    elif key == "TELEGRAM_CHAT_ID":
                        tg_chat_id = val
                    elif key == "ALERT_THRESHOLD":
                        try:
                            alert_threshold = int(val)
                        except Exception:
                            pass
                    elif key == "HEADLESS":
                        headless = (val.lower() == "true")
        except Exception:
            pass

    # 2. Si no se cargó desde .env, intentar DPAPI (gui_credentials)
    if not env_loaded and not (email and password):
        try:
            from backend.auth.gui_credentials import load_saved_credentials
            saved = load_saved_credentials()
            if saved:
                email = saved.get("email", email)
                password = saved.get("password", password)
                tg_token = saved.get("tg_token", tg_token)
                tg_chat_id = saved.get("tg_chat_id", tg_chat_id)
                alert_threshold = saved.get("threshold", alert_threshold)
                headless = saved.get("headless", headless)
        except Exception:
            pass

    result = (email, password, tg_token, tg_chat_id, alert_threshold, headless)
    _cache_set(_credentials_cache, result)
    return result
