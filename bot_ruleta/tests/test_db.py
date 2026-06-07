"""
Tests para db.py: validador de tablas y operaciones CRUD.
"""
import pytest
import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bot_ruleta.config import TABLES


class TestValidateTableName:
    def test_valid_table(self):
        from bot_ruleta.db import validate_table_name
        result = validate_table_name("ruleta_latina")
        assert result == "ruleta_latina"

    def test_table_not_in_config(self):
        from bot_ruleta.db import validate_table_name
        with pytest.raises(ValueError, match="Tabla no configurada"):
            validate_table_name("tabla_inexistente")

    def test_invalid_chars_space(self):
        from bot_ruleta.db import validate_table_name
        with pytest.raises(ValueError, match="caracteres no permitidos"):
            validate_table_name("DROP TABLE")

    def test_invalid_chars_semicolon(self):
        from bot_ruleta.db import validate_table_name
        with pytest.raises(ValueError, match="caracteres no permitidos"):
            validate_table_name("ruleta;DROP")

    def test_none_raises(self):
        from bot_ruleta.db import validate_table_name
        with pytest.raises(ValueError, match="invalido"):
            validate_table_name(None)

    def test_empty_string_raises(self):
        from bot_ruleta.db import validate_table_name
        with pytest.raises(ValueError, match="invalido"):
            validate_table_name("")

    def test_all_configured_tables_valid(self):
        from bot_ruleta.db import validate_table_name
        for t in TABLES:
            result = validate_table_name(t["table_name"])
            assert result == t["table_name"]


class TestDbCRUD:
    """Usa SQLite en memoria (:memory:) para no afectar la BD real."""

    @pytest.fixture(autouse=True)
    def setup_db(self, monkeypatch):
        import bot_ruleta.db as db_module
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row

        def mock_get_connection():
            return conn

        monkeypatch.setattr(db_module, "get_connection", mock_get_connection)
        monkeypatch.setattr(db_module, "_conn", conn)
        monkeypatch.setattr(db_module, "_conn_lock", __import__("threading").Lock())

        self.conn = conn
        self.db_module = db_module
        self._create_tables()
        yield
        conn.close()

    def _create_tables(self):
        c = self.conn.cursor()
        for t in TABLES:
            c.execute(f"CREATE TABLE IF NOT EXISTS {t['table_name']} (id INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER, color TEXT, timestamp TEXT, game_id INTEGER)")
        self.conn.commit()

    def test_init_db_does_not_crash(self):
        self.db_module.init_db()

    def test_save_result_and_get_last_numbers(self):
        from bot_ruleta.db import save_result, get_last_numbers
        table = TABLES[0]
        save_result(table["name"], 5, "Red", "2026-01-01 12:00:00", 1)
        save_result(table["name"], 10, "Black", "2026-01-01 12:00:01", 2)
        results = get_last_numbers(table["name"])
        assert len(results) == 2
        assert results[0]["numero"] == 10
        assert results[1]["numero"] == 5

    def test_get_last_numbers_with_limit(self):
        from bot_ruleta.db import save_result, get_last_numbers
        table = TABLES[0]
        for i in range(5):
            save_result(table["name"], i, "Red", f"2026-01-01 12:00:0{i}", i)
        results = get_last_numbers(table["name"], limit=2)
        assert len(results) == 2

    def test_get_last_number(self):
        from bot_ruleta.db import save_result, get_last_number
        table = TABLES[0]
        save_result(table["name"], 32, "Red", "2026-01-01 12:00:00", 1)
        n = get_last_number(table["name"])
        assert n == 32

    def test_get_last_number_empty_table(self):
        from bot_ruleta.db import get_last_number
        n = get_last_number(TABLES[0]["name"])
        assert n is None

    def test_clear_table(self):
        from bot_ruleta.db import save_result, get_last_numbers, clear_table
        table = TABLES[0]
        save_result(table["name"], 1, "Red", "2026-01-01 12:00:00", 1)
        save_result(table["name"], 2, "Black", "2026-01-01 12:00:01", 2)
        clear_table(table["name"])
        results = get_last_numbers(table["name"])
        assert len(results) == 0

    def test_save_result_nonexistent_table(self):
        from bot_ruleta.db import save_result
        save_result("mesa_que_no_existe", 1, "Red", "2026-01-01", 1)

    def test_get_last_numbers_nonexistent_table(self):
        from bot_ruleta.db import get_last_numbers
        results = get_last_numbers("mesa_que_no_existe")
        assert results == []
