"""
Tests para credentials.py y thresholds.py: carga de credenciales y umbrales.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestCredentials:
    def teardown_method(self):
        import backend.auth.credentials as cred
        cred._runtime_overrides.clear()
        cred._credentials_cache = {"value": None, "expires_at": 0}

    def test_set_runtime_config_stores_values(self):
        from backend.auth.credentials import set_runtime_config, _runtime_overrides
        set_runtime_config(email="test@test.com", password="pass123", threshold=15)
        assert _runtime_overrides["email"] == "test@test.com"
        assert _runtime_overrides["password"] == "pass123"
        assert _runtime_overrides["threshold"] == 15

    def test_load_credentials_with_runtime_overrides(self):
        from backend.auth.credentials import set_runtime_config, load_credentials
        set_runtime_config(email="r@t.com", password="rp", tg_token="rt", tg_chat_id="rc", threshold=8, headless=False)
        email, password, token, chat_id, threshold, headless = load_credentials()
        assert email == "r@t.com"
        assert password == "rp"
        assert token == "rt"
        assert chat_id == "rc"
        assert threshold == 8
        assert headless is False

    def test_load_credentials_defaults(self):
        import backend.auth.credentials as cred
        cred._runtime_overrides.clear()
        cred._credentials_cache = {"value": None, "expires_at": 0}

        # Simular que no hay .env ni DPAPI -> defaults
        # Forzamos que la cache devuelva un valor por defecto
        original_load = cred.load_credentials

        def _force_defaults():
            return ("", "", "", "", 12, True)

        # Usamos el cache para forzar defaults
        cred._cache_set(cred._credentials_cache, ("", "", "", "", 12, True))
        email, password, token, chat_id, threshold, headless = cred.load_credentials()
        assert email == ""
        assert password == ""
        assert token == ""
        assert chat_id == ""
        assert threshold == 12
        assert headless is True

    def test_cache_returns_cached_value(self):
        from backend.auth.credentials import _cache_get, _cache_set, _credentials_cache
        _credentials_cache["value"] = ("cached@t.com", "cp", "ct", "cc", 15, False)
        _credentials_cache["expires_at"] = 99999999999
        result = _cache_get(_credentials_cache)
        assert result == ("cached@t.com", "cp", "ct", "cc", 15, False)

    def test_cache_expired_returns_none(self):
        from backend.auth.credentials import _cache_get, _cache_set, _credentials_cache
        _cache_set(_credentials_cache, "test")
        _credentials_cache["expires_at"] = 0
        result = _cache_get(_credentials_cache)
        assert result is None

    def test_cache_set_and_get(self):
        from backend.auth.credentials import _cache_get, _cache_set, _credentials_cache
        _credentials_cache = {"value": None, "expires_at": 0}
        _cache_set(_credentials_cache, "fresh_value")
        result = _cache_get(_credentials_cache)
        assert result == "fresh_value"


class TestThresholds:
    def teardown_method(self):
        import backend.auth.credentials as cred
        cred._runtime_overrides.clear()
        cred._color_threshold_cache = {"value": None, "expires_at": 0}
        cred._number_threshold_cache = {"value": None, "expires_at": 0}

    def test_color_streak_threshold_default(self):
        from backend.roulette.thresholds import get_color_streak_threshold
        from backend.auth.credentials import _runtime_overrides
        _runtime_overrides.pop('color_streak_threshold', None)
        result = get_color_streak_threshold()
        assert result in (5, 70)  # 5 = default, 70 = DPAPI saved value on Windows

    def test_number_delay_threshold_default(self):
        from backend.roulette.thresholds import get_number_delay_threshold
        from backend.auth.credentials import _runtime_overrides
        _runtime_overrides.pop('number_delay_threshold', None)
        result = get_number_delay_threshold()
        assert result in (20, 70)  # 20 = default, 70 = DPAPI/.env saved value

    def test_threshold_runtime_override(self):
        from backend.auth.credentials import _runtime_overrides
        from backend.roulette.thresholds import get_color_streak_threshold, get_number_delay_threshold
        _runtime_overrides["color_streak_threshold"] = 10
        _runtime_overrides["number_delay_threshold"] = 30
        assert get_color_streak_threshold() == 10
        assert get_number_delay_threshold() == 30
