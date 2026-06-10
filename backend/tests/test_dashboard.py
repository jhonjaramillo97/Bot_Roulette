"""
Tests para el dashboard React: middleware de token, rutas SPA y endpoints API.
"""
import pytest
import os
import sys
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import backend.dashboard.app as dashboard_app
from backend.config.config import TABLES


@pytest.fixture(autouse=True)
def _setup_test_db(monkeypatch):
    """Configura SQLite en memoria para todos los tests."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    for mesa in TABLES:
        tn = mesa.get("table_name", "")
        if not tn:
            continue
        c.execute(f"CREATE TABLE {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER, color TEXT, timestamp TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS backtest_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, zone_name TEXT, start_time TEXT, end_time TEXT, max_delay INTEGER, threshold_used INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS color_streak_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, streak_color TEXT, streak_count INTEGER, start_time TEXT, end_time TEXT, threshold_used INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS number_delay_history (id INTEGER PRIMARY KEY AUTOINCREMENT, table_name TEXT, number INTEGER, start_time TEXT, end_time TEXT, max_delay INTEGER, threshold_used INTEGER, termination TEXT DEFAULT 'normal')")
    c.execute("CREATE TABLE IF NOT EXISTS sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS color_sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS number_sync_state (table_name TEXT PRIMARY KEY, last_game_id INTEGER)")
    conn.commit()

    monkeypatch.setattr(dashboard_app, "get_db_connection", lambda: conn)
    yield
    conn.close()


@pytest.fixture(autouse=True)
def reset_token():
    """Restaurar el token después de cada test."""
    original = dashboard_app.DASHBOARD_TOKEN
    yield
    dashboard_app.DASHBOARD_TOKEN = original


def _client():
    dashboard_app.app.config["TESTING"] = True
    return dashboard_app.app.test_client()


class TestTokenMiddleware:
    """Middleware de autenticación por token (?token=)."""

    def test_api_without_token_param_returns_401(self):
        dashboard_app.DASHBOARD_TOKEN = "test123"
        res = _client().get("/api/mesas")
        assert res.status_code == 401

    def test_api_with_wrong_token_returns_401(self):
        dashboard_app.DASHBOARD_TOKEN = "test123"
        res = _client().get("/api/mesas?token=wrong")
        assert res.status_code == 401

    def test_api_with_correct_token_returns_ok(self):
        dashboard_app.DASHBOARD_TOKEN = "test123"
        res = _client().get("/api/mesas?token=test123")
        assert res.status_code == 200

    def test_api_without_token_env_passes(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/mesas")
        assert res.status_code == 200

    def test_api_overview_requires_token(self):
        dashboard_app.DASHBOARD_TOKEN = "test123"
        res = _client().get("/api/overview")
        assert res.status_code == 401
        res2 = _client().get("/api/overview?token=test123")
        assert res2.status_code == 200

    def test_non_api_routes_not_affected(self):
        dashboard_app.DASHBOARD_TOKEN = "test123"
        res = _client().get("/")
        assert res.status_code in (200, 302)


class TestSpaRoutes:
    """Rutas SPA: Flask debe servir index.html para rutas del frontend."""

    def test_root_serves_html(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/")
        assert res.status_code == 200
        assert b"<!DOCTYPE html" in res.data or b'<div id="root"' in res.data

    def test_mesa_route_serves_spa(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/mesa")
        assert res.status_code == 200

    def test_analisis_route_serves_spa(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/analisis")
        assert res.status_code == 200

    def test_404_fallback_serves_spa(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/ruta-inexistente")
        assert res.status_code == 200


class TestApiEndpoints:
    """Endpoints de la API REST."""

    def test_overview_returns_json(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/overview")
        assert res.status_code == 200
        data = res.get_json()
        assert "tables" in data
        assert "threshold" in data

    def test_mesas_returns_list(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/mesas")
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)

    def test_data_endpoint_defaults_to_ruleta_latina(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/data")
        assert res.status_code == 200
        data = res.get_json()
        assert "mesa" in data

    def test_data_endpoint_with_valid_table(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/data?mesa=stake_roulette")
        assert res.status_code == 200
        data = res.get_json()
        assert "mesa" in data
        assert "delays" in data

    def test_analisis_global_returns_json(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/analisis_global")
        assert res.status_code == 200
        data = res.get_json()
        assert "history" in data


class TestSseEndpoint:
    """Endpoint SSE para streaming en tiempo real."""

    def test_stream_returns_event_stream(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/stream")
        assert res.status_code == 200
        assert "text/event-stream" in res.content_type

    def test_stream_emits_overview_event(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        res = _client().get("/api/stream")
        chunks = []
        for i, chunk in enumerate(res.response):
            chunks.append(chunk.decode("utf-8", errors="replace"))
            if len(chunks) >= 5:
                break
        body = "".join(chunks)
        assert "event: overview" in body or "data:" in body


class TestAuthResponse:
    """Formato de respuesta del middleware de autenticación."""

    def test_401_response_is_json(self):
        dashboard_app.DASHBOARD_TOKEN = "secret2026"
        res = _client().get("/api/overview")
        assert res.status_code == 401
        data = res.get_json()
        assert "error" in data

    def test_token_env_empty_allows_all(self):
        dashboard_app.DASHBOARD_TOKEN = ""
        c = _client()
        assert c.get("/api/overview").status_code == 200
        assert c.get("/api/mesas").status_code == 200
        assert c.get("/api/stream").status_code == 200
