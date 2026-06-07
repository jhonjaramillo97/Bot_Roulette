"""
Tests para config.py y paths.py: constantes y resolucion de rutas.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestConfig:
    def test_tables_count(self):
        from bot_ruleta.config import TABLES
        assert len(TABLES) == 19

    def test_all_tables_have_required_keys(self):
        from bot_ruleta.config import TABLES
        for t in TABLES:
            assert "name" in t
            assert "id" in t
            assert "op_id" in t
            assert "table_name" in t

    def test_reds_count(self):
        from bot_ruleta.config import REDS
        assert len(REDS) == 18

    def test_reds_are_strings(self):
        from bot_ruleta.config import REDS
        for r in REDS:
            assert isinstance(r, str)
            assert int(r) in range(1, 37)

    def test_lobby_url_configured(self):
        from bot_ruleta.config import LOBBY_URL
        assert "stake.com" in LOBBY_URL
        assert "roulette-lobby" in LOBBY_URL

    def test_lobby_mode_is_bool(self):
        from bot_ruleta.config import LOBBY_MODE
        assert isinstance(LOBBY_MODE, bool)

    def test_afk_interval_positive(self):
        from bot_ruleta.config import AFK_INTERVAL
        assert AFK_INTERVAL > 0

    def test_table_names_are_unique(self):
        from bot_ruleta.config import TABLES
        names = [t["table_name"] for t in TABLES]
        assert len(names) == len(set(names))


class TestPaths:
    def test_is_frozen_false_in_dev(self):
        from bot_ruleta.paths import is_frozen
        assert is_frozen() is False

    def test_get_base_dir_returns_valid_path(self):
        from bot_ruleta.paths import get_base_dir
        path = get_base_dir()
        assert os.path.exists(path)

    def test_get_data_dir_exists(self):
        from bot_ruleta.paths import get_data_dir
        data_dir = get_data_dir()
        assert os.path.exists(data_dir)
