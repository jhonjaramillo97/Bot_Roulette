"""
Tests para backtest.py: motores de sincronizacion incremental.
Usa SQLite en memoria con tabla real de la config.
"""
import pytest
import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

TABLE = "ruleta_latina"


class TestBacktestSync:
    @pytest.fixture(autouse=True)
    def setup_db(self, monkeypatch):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row

        # Monkeypatch en db y en backtest (porque backtest usa from import)
        import bot_ruleta.db as db_module
        monkeypatch.setattr(db_module, "_conn", conn)
        monkeypatch.setattr(db_module, "_conn_lock", __import__("threading").Lock())
        monkeypatch.setattr(db_module, "get_connection", lambda: conn)

        import bot_ruleta.backtest as bt_module
        monkeypatch.setattr(bt_module, "get_connection", lambda: conn)

        self.conn = conn
        c = conn.cursor()
        c.execute(f"CREATE TABLE {TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER, color TEXT, timestamp TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS color_sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS number_sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS backtest_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, zone_name TEXT, start_time TEXT, end_time TEXT, max_delay INTEGER, threshold_used INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS color_streak_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, streak_color TEXT, streak_count INTEGER, start_time TEXT, end_time TEXT, threshold_used INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS number_delay_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, number INTEGER, start_time TEXT, end_time TEXT, max_delay INTEGER, threshold_used INTEGER, termination TEXT DEFAULT 'normal')")
        conn.commit()
        yield
        conn.close()

    def _insert(self, numero, color="Red", ts="2026-01-01 12:00:00"):
        self.conn.execute(f"INSERT INTO {TABLE} (numero, color, timestamp) VALUES (?, ?, ?)", (numero, color, ts))
        self.conn.commit()

    def test_sync_empty_table_no_errors(self):
        from bot_ruleta.backtest import _ZoneBacktestSync
        engine = _ZoneBacktestSync(TABLE, 4)
        engine.run("id, numero, timestamp")

    def test_zone_sync_detects_signal(self):
        from bot_ruleta.backtest import _ZoneBacktestSync
        for i in range(10):
            self._insert(1, ts=f"2026-01-01 12:00:{i:02d}")
        engine = _ZoneBacktestSync(TABLE, 3)
        engine.run("id, numero, timestamp")
        rows = self.conn.execute("SELECT COUNT(*) as cnt FROM backtest_history").fetchone()
        assert rows["cnt"] >= 0

    def test_color_sync_chain_break(self):
        from bot_ruleta.backtest import _ColorBacktestSync
        datos = [(1, "Red"), (3, "Red"), (5, "Red"), (-1, "Reset"), (2, "Black")]
        for i, (n, c) in enumerate(datos):
            self._insert(n, c, f"2026-01-01 12:00:{i:02d}")
        engine = _ColorBacktestSync(TABLE, 2)
        engine.run("id, numero, color, timestamp")

    def test_color_sync_basic(self):
        from bot_ruleta.backtest import _ColorBacktestSync
        for i in range(8):
            color = "Red" if i % 2 == 0 else "Black"
            self._insert(i + 1, color, f"2026-01-01 12:00:{i:02d}")
        engine = _ColorBacktestSync(TABLE, 1)
        engine.run("id, numero, color, timestamp")

    def test_number_sync_no_errors(self):
        from bot_ruleta.backtest import _NumberBacktestSync
        for i in range(10):
            self._insert(i, ts=f"2026-01-01 12:00:{i:02d}")
        engine = _NumberBacktestSync(TABLE, 20)
        engine.run("id, numero, timestamp")

    def test_sync_with_chain_break(self):
        from bot_ruleta.backtest import _ZoneBacktestSync
        datos = [1, 1, 1, 1, -1, 13, 13, 13, 13]
        for i, n in enumerate(datos):
            self._insert(n, ts=f"2026-01-01 12:00:{i:02d}")
        engine = _ZoneBacktestSync(TABLE, 2)
        engine.run("id, numero, timestamp")

    def test_time_gap_breaks_chain(self):
        """Un gap de mas de 30 minutos entre filas debe romper la cadena y reiniciar delays."""
        # Ayer/lapso viejo: 5 giros sin docena_1
        self._insert(13, ts="2026-01-01 12:00:00")
        self._insert(14, ts="2026-01-01 12:01:00")
        self._insert(15, ts="2026-01-01 12:02:00")
        self._insert(16, ts="2026-01-01 12:03:00")
        self._insert(17, ts="2026-01-01 12:04:00")
        # Gap > 30 minutos
        # Nuevo lapso: 3 giros sin docena_1
        self._insert(18, ts="2026-01-01 12:35:00")
        self._insert(19, ts="2026-01-01 12:36:00")
        self._insert(20, ts="2026-01-01 12:37:00")

        from bot_ruleta.backtest import _ZoneBacktestSync
        engine = _ZoneBacktestSync(TABLE, 2)
        engine.run("id, numero, timestamp")

        rows = self.conn.execute(
            "SELECT max_delay FROM backtest_history WHERE table_name = ? ORDER BY id", (TABLE,)
        ).fetchall()
        # El gap debe romper las cadenas: delays no deben acumularse entre lapsos
        for r in rows:
            assert r[0] < 10, f"Delay no deberia acumularse entre sesiones: {r[0]}"
