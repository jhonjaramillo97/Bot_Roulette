"""
Umbrales de alerta para rachas de color y retrasos de números.
Separado de config.py para romper el acoplamiento con gui_credentials.
"""

import os

from bot_ruleta.credentials import (
    _runtime_overrides, _cache_get, _cache_set,
    _color_threshold_cache, _number_threshold_cache,
)

COLOR_STREAK_THRESHOLD = 5
NUMBER_DELAY_THRESHOLD = 20


def get_color_streak_threshold():
    """Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env > default.
    Cachea el resultado por 30s para evitar lecturas repetidas de .env."""
    if 'color_streak_threshold' in _runtime_overrides:
        return _runtime_overrides['color_streak_threshold']

    try:
        from bot_ruleta.gui_credentials import load_saved_credentials
        saved = load_saved_credentials()
        if saved and 'color_streak_threshold' in saved:
            return saved['color_streak_threshold']
    except Exception:
        pass

    cached = _cache_get(_color_threshold_cache)
    if cached is not None:
        return cached

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

    result = COLOR_STREAK_THRESHOLD
    _cache_set(_color_threshold_cache, result)
    return result


def get_number_delay_threshold():
    """Lee el umbral de retraso de números individuales. Prioridad: runtime overrides > GUI saved > .env > default.
    Cachea el resultado por 30s para evitar lecturas repetidas de .env."""
    if 'number_delay_threshold' in _runtime_overrides:
        return _runtime_overrides['number_delay_threshold']

    try:
        from bot_ruleta.gui_credentials import load_saved_credentials
        saved = load_saved_credentials()
        if saved and 'number_delay_threshold' in saved:
            return saved['number_delay_threshold']
    except Exception:
        pass

    cached = _cache_get(_number_threshold_cache)
    if cached is not None:
        return cached

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

    result = NUMBER_DELAY_THRESHOLD
    _cache_set(_number_threshold_cache, result)
    return result
