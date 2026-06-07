"""
Configuración centralizada del bot de ruleta.
Constantes, configuración de mesas, URLs.
"""

import os

from bot_ruleta.credentials import (
    _runtime_overrides, _cache_get, _cache_set,
    _color_threshold_cache, _number_threshold_cache,
)

# --- MODO DE OPERACIÓN ---
LOBBY_MODE = True  # False = modo clásico (desactivado)

# --- MESAS CONFIGURADAS ---
# Los IDs se actualizan dinámicamente al iniciar (map_tables_dynamic).
# Los valores aquí son fallback en caso de que el escaneo falle.
TABLES = [
    {"name": "Ruleta Latina", "id": "roulerw234rwl292-234", "op_id": "234", "table_name": "ruleta_latina"},
    {"name": "Mega Roulette", "id": "1hl65ce1lxuqdrkr-204", "op_id": "204", "table_name": "mega_roulette"},
    {"name": "Brazilian Roulette", "id": "rwbrzportrwa16rg-237", "op_id": "237", "table_name": "brazilian_roulette"},
    {"name": "Roulette 1", "id": "g03y1t9vvuhrfytl-227", "op_id": "227", "table_name": "roulette_1"},
    {"name": "Roulette 3", "id": "chroma229rwltr22-230", "op_id": "230", "table_name": "roulette_3"},
    {"name": "Roulette Macao", "id": "yqpz3ichst2xg439-206", "op_id": "206", "table_name": "roulette_macao"},
     
    # Nuevas mesas añadidas a petición del usuario
    {"name": "Roulette 2 Extra Time", "id": "5kvxlw4c1qm3xcyn-201", "op_id": "201", "table_name": "roulette_2_extra_time"},
    {"name": "Brazilian Mega Roulette", "id": "mrbras531mrbr532-287", "op_id": "287", "table_name": "brazilian_mega_roulette"},
    {"name": "Lucky 6 Roulette", "id": "lucky6roulettea3-211a1", "op_id": "211a1", "table_name": "lucky_6_roulette"},
    {"name": "Auto Roulette", "id": "5bzl2835s5ruvweg-225", "op_id": "225", "table_name": "auto_roulette"},

    # Lote de ruletas regionales
    {"name": "Stake Roulette", "id": "rw321stakerws321-236", "op_id": "236", "table_name": "stake_roulette"},
    {"name": "Turkish Roulette", "id": "p8l1j84prrmxzyic-224", "op_id": "224", "table_name": "turkish_roulette"},
    {"name": "German Roulette", "id": "s2x6b4jdeqza2ge2-222", "op_id": "222", "table_name": "german_roulette"},
    {"name": "Romanian Roulette", "id": "romania233rwl291-233", "op_id": "233", "table_name": "romanian_roulette"},
    {"name": "Roulette Italia Tricolore", "id": "v1c52fgw7yy02upz-223", "op_id": "223", "table_name": "roulette_italia_tricolore"},
    {"name": "Russian Roulette", "id": "t4jzencinod6iqwi-221", "op_id": "221", "table_name": "russian_roulette"},
    {"name": "Gates of Olympus Roulette", "id": "gatesofolympus01-2244", "op_id": "2244", "table_name": "gates_of_olympus_roulette"},
    {"name": "Turkish Mega Roulette", "id": "megar0ul3tt3trk1-208", "op_id": "208", "table_name": "turkish_mega_roulette"},
    {"name": "Mega Roulette 3000", "id": "megaroulette3k01-2901", "op_id": "2901", "table_name": "mega_roulette_3000"},
]

# --- URLs ---
LOBBY_URL = "https://stake.com.co/es/casino/juego/roulette-lobby-571"

# --- DIRECTORIOS ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# --- INTERVALOS ---
AFK_INTERVAL = 300  # segundos (300 = 5 min producción)

# --- COLORES DE RULETA ---
REDS = ['1', '3', '5', '7', '9', '12', '14', '16', '18',
        '19', '21', '23', '25', '27', '30', '32', '34', '36']

# --- SEÑALES DE RACHA DE COLOR ---
COLOR_STREAK_THRESHOLD = 5  # Default: señal a partir de 5 consecutivos del mismo color

# --- SEÑALES DE NÚMEROS INDIVIDUALES ---
NUMBER_DELAY_THRESHOLD = 20  # Default: señal cuando un número no sale en 20 giros

def get_color_streak_threshold():
    """Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env > default.
    Cachea el resultado por 30s para evitar lecturas repetidas de .env."""
    # 1. Runtime overrides (GUI en sesión activa) — sin cache
    if 'color_streak_threshold' in _runtime_overrides:
        return _runtime_overrides['color_streak_threshold']
    
    # 2. Credenciales guardadas por la GUI — sin cache
    try:
        from bot_ruleta.gui_credentials import load_saved_credentials
        saved = load_saved_credentials()
        if saved and 'color_streak_threshold' in saved:
            return saved['color_streak_threshold']
    except Exception:
        pass
    
    # 3. Cache de .env (el fallback más caro)
    cached = _cache_get(_color_threshold_cache)
    if cached is not None:
        return cached

    # 4. Variable de entorno (.env)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("COLOR_STREAK_THRESHOLD="):
                    val = line.split("=", 1)[1].split("#")[0].strip()
                    result = int(val)
                    _cache_set(_color_threshold_cache, result)
                    return result
    except Exception:
        pass
    
    # 5. Default
    result = COLOR_STREAK_THRESHOLD
    _cache_set(_color_threshold_cache, result)
    return result


def get_number_delay_threshold():
    """Lee el umbral de retraso de números individuales. Prioridad: runtime overrides > GUI saved > .env > default.
    Cachea el resultado por 30s para evitar lecturas repetidas de .env."""
    # 1. Runtime overrides (GUI en sesión activa) — sin cache
    if 'number_delay_threshold' in _runtime_overrides:
        return _runtime_overrides['number_delay_threshold']
    
    # 2. Credenciales guardadas por la GUI — sin cache
    try:
        from bot_ruleta.gui_credentials import load_saved_credentials
        saved = load_saved_credentials()
        if saved and 'number_delay_threshold' in saved:
            return saved['number_delay_threshold']
    except Exception:
        pass
    
    # 3. Cache de .env (el fallback más caro)
    cached = _cache_get(_number_threshold_cache)
    if cached is not None:
        return cached

    # 4. Variable de entorno (.env)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("NUMBER_DELAY_THRESHOLD="):
                    val = line.split("=", 1)[1].split("#")[0].strip()
                    result = int(val)
                    _cache_set(_number_threshold_cache, result)
                    return result
    except Exception:
        pass
    
    # 5. Default
    result = NUMBER_DELAY_THRESHOLD
    _cache_set(_number_threshold_cache, result)
    return result
