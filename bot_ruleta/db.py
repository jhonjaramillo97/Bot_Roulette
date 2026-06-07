"""
Manejo de base de datos SQLite con tablas separadas por juego.
"""

import sqlite3
import os
import re
import threading
from bot_ruleta.config import TABLES

import sys

from bot_ruleta.paths import get_data_dir
from bot_ruleta.debug_logger import get_logger

log = get_logger("db")

_VALID_TABLE_NAMES = {t["table_name"] for t in TABLES}
_TABLE_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

DB_NAME = "ruleta.db"
DATA_DIR = get_data_dir()
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

_conn = None
_conn_lock = threading.Lock()


def get_connection():
    """Retorna la conexion persistente a la BD (inicializa con WAL si es necesario)."""
    global _conn
    if _conn is None:
        with _conn_lock:
            if _conn is None:
                _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
                _conn.execute("PRAGMA journal_mode=WAL;")
    return _conn


def validate_table_name(name):
    """Valida que un nombre de tabla sea seguro y exista en la configuracion.
    Lanza ValueError si no es valido."""
    if not name or not isinstance(name, str):
        raise ValueError(f"Nombre de tabla invalido: {name!r}")
    if not _TABLE_NAME_RE.match(name):
        raise ValueError(f"Nombre de tabla con caracteres no permitidos: {name!r}")
    if name not in _VALID_TABLE_NAMES:
        raise ValueError(f"Tabla no configurada: {name!r}")
    return name


def init_db():
    """Inicializa la base de datos creando las tablas configuradas."""
    log.info(f"Inicializando base de datos en: {DB_PATH}")
    conn = get_connection()
    cursor = conn.cursor()

    for mesa in TABLES:
        table_name = mesa.get("table_name")
        if not table_name:
            continue
        table_name = validate_table_name(table_name)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                numero      INTEGER NOT NULL,
                color       TEXT NOT NULL,
                timestamp   TEXT NOT NULL,
                game_id     INTEGER
            )
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_ts 
            ON {table_name}(timestamp)
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backtest_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name      TEXT NOT NULL,
            zone_name       TEXT NOT NULL,
            start_time      TEXT NOT NULL,
            end_time        TEXT,
            max_delay       INTEGER NOT NULL,
            threshold_used  INTEGER NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_backtest_table ON backtest_history(table_name)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS color_streak_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name      TEXT NOT NULL,
            streak_color    TEXT NOT NULL,
            streak_count    INTEGER NOT NULL,
            start_time      TEXT NOT NULL,
            end_time        TEXT,
            threshold_used  INTEGER NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_color_streak_table ON color_streak_history(table_name)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS color_sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS number_delay_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name      TEXT NOT NULL,
            number          INTEGER NOT NULL,
            start_time      TEXT NOT NULL,
            end_time        TEXT,
            max_delay       INTEGER NOT NULL,
            threshold_used  INTEGER NOT NULL,
            termination     TEXT DEFAULT 'normal'
        )
    """)
    try:
        cursor.execute("ALTER TABLE number_delay_history ADD COLUMN termination TEXT DEFAULT 'normal'")
    except sqlite3.OperationalError:
        pass
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_number_delay_table ON number_delay_history(table_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_number_delay_number ON number_delay_history(number)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS number_sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    conn.commit()
    log.info("Tablas verificadas/creadas.")


def guardar_resultado(mesa_nombre, numero, color, timestamp, game_id):
    """Guarda un resultado en la tabla especifica del juego."""
    table_name = None
    for t in TABLES:
        if t["name"] == mesa_nombre or t["table_name"] == mesa_nombre:
            table_name = t["table_name"]
            break
    
    if not table_name:
        log.error(f"No se encontro tabla para '{mesa_nombre}'")
        return

    table_name = validate_table_name(table_name)

    try:
        with _conn_lock:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {table_name} (numero, color, timestamp, game_id)
                VALUES (?, ?, ?, ?)
            """, (numero, color, timestamp, game_id))
            conn.commit()
    except Exception as e:
        log.error(f"Error guardando en BD ({table_name}): {e}")


def obtener_ultimo_numero(mesa_nombre):
    """Obtiene el ultimo numero registrado en la tabla del juego."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return None
    table_name = validate_table_name(table_name)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT numero FROM {table_name} ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return row[0]
    except Exception:
        pass
    return None


def obtener_ultimos_numeros(mesa_nombre, limit=None):
    """Obtiene los ultimos N registros (numero, color y timestamp). Si limit es None, obtiene todos."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return []

    table_name = validate_table_name(table_name)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        if limit is not None:
            cursor.execute(f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC LIMIT ?", (limit,))
        else:
            cursor.execute(f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC")
        rows = cursor.fetchall()
        return [{"numero": r[0], "color": r[1], "timestamp": r[2]} for r in rows]
    except Exception as e:
        log.error(f"Error obtener_ultimos_numeros: {e}")
        return []


def _resolve_table_name(mesa_nombre):
    """Resuelve el nombre de tabla SQLite a partir del nombre descriptivo."""
    for t in TABLES:
        if t["name"] == mesa_nombre or t["table_name"] == mesa_nombre:
            return t["table_name"]
    return None


def limpiar_mesa(mesa_nombre):
    """Elimina todos los registros de la tabla de una mesa especifica."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return

    table_name = validate_table_name(table_name)

    try:
        with _conn_lock:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()
        log.info(f"Historial limpiado para la mesa '{mesa_nombre}' (Sesion Stale detectada)")
    except Exception as e:
        log.error(f"Error limpiando BD ({table_name}): {e}")
