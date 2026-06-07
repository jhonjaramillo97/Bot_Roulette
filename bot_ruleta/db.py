"""
Manejo de base de datos SQLite con tablas separadas por juego.
"""

import sqlite3
import os
from datetime import datetime
from bot_ruleta.config import TABLES

import sys

DB_NAME = "ruleta.db"
if getattr(sys, 'frozen', False):
    DATA_DIR = os.path.join(os.path.dirname(sys.executable), "data")
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, DB_NAME)


def get_connection():
    """Retorna una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Inicializa la base de datos creando las tablas configuradas."""
    print(f"🗄️  Inicializando base de datos en: {DB_PATH}")
    conn = get_connection()
    cursor = conn.cursor()

    for mesa in TABLES:
        table_name = mesa.get("table_name")
        if not table_name:
            continue

        # Crear tabla específica para cada juego
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                numero      INTEGER NOT NULL,
                color       TEXT NOT NULL,
                timestamp   TEXT NOT NULL,
                game_id     INTEGER
            )
        """)
        # Índice básico por timestamp
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_ts 
            ON {table_name}(timestamp)
        """)

    # Tabla global para historial de backtesting (señales completadas)
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

    # Tabla para estado de sincronización incremental
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    # Tabla global para historial de rachas de color (señales completadas)
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

    # Tabla para estado de sincronización de rachas de color
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS color_sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    # Tabla global para historial de retrasos de números individuales
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
    # Migración: agregar columna termination si no existe en tablas viejas
    try:
        cursor.execute("ALTER TABLE number_delay_history ADD COLUMN termination TEXT DEFAULT 'normal'")
    except sqlite3.OperationalError:
        pass  # Ya existe, ignorar
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_number_delay_table ON number_delay_history(table_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_number_delay_number ON number_delay_history(number)")

    # Tabla para estado de sincronización de retrasos de números
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS number_sync_state (
            table_name      TEXT PRIMARY KEY,
            last_game_id    INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas verificadas/creadas.")


def guardar_resultado(mesa_nombre, numero, color, timestamp, game_id):
    """Guarda un resultado en la tabla específica del juego."""
    # Buscar el table_name correspondiente al nombre descriptivo o usar directo si ya viene
    table_name = None
    for t in TABLES:
        if t["name"] == mesa_nombre or t["table_name"] == mesa_nombre:
            table_name = t["table_name"]
            break
    
    if not table_name:
        print(f"⚠️ Error BD: No se encontró tabla para '{mesa_nombre}'")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # INSERT directo a la tabla del juego
        cursor.execute(f"""
            INSERT INTO {table_name} (numero, color, timestamp, game_id)
            VALUES (?, ?, ?, ?)
        """, (numero, color, timestamp, game_id))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error guardando en BD ({table_name}): {e}")


def obtener_ultimo_numero(mesa_nombre):
    """Obtiene el último número registrado en la tabla del juego."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT numero FROM {table_name} ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    except:
        pass
    return None


def obtener_ultimos_numeros(mesa_nombre, limit=None):
    """Obtiene los últimos N registros (número, color y timestamp). Si limit es None, obtiene todos."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return []

    try:
        conn = get_connection()
        cursor = conn.cursor()
        if limit is not None:
            cursor.execute(f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC LIMIT ?", (limit,))
        else:
            cursor.execute(f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"numero": r[0], "color": r[1], "timestamp": r[2]} for r in rows]
    except Exception as e:
        print(f"Error obtener_ultimos_numeros: {e}")
        return []


def _resolve_table_name(mesa_nombre):
    """Resuelve el nombre de tabla SQLite a partir del nombre descriptivo."""
    for t in TABLES:
        if t["name"] == mesa_nombre or t["table_name"] == mesa_nombre:
            return t["table_name"]
    return None

def limpiar_mesa(mesa_nombre):
    """Elimina todos los registros de la tabla de una mesa específica. 
    Usado cuando se detecta que el bot estuvo apagado mucho tiempo y los datos en pantalla no empalman."""
    table_name = _resolve_table_name(mesa_nombre)
    if not table_name:
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        conn.close()
        print(f"🧹 Historial limpiado para la mesa '{mesa_nombre}' (Sesión Stale detectada)")
    except Exception as e:
        print(f"⚠️ Error limpiando BD ({table_name}): {e}")


# ═══════════════════════════════════════════════════════════════════════
# Motor genérico de sincronización de backtests
# ═══════════════════════════════════════════════════════════════════════

class _BacktestSyncEngine:
    """Motor de sincronización incremental compartido por todos los backtests.

    Maneja: conexión a DB, lectura de estado de sincronización, batch con
    warmup, loop principal con manejo de cadena rota (-1), y guardado de
    estado incremental. Las subclases solo definen la lógica de dominio:
    cómo inicializar delays, procesar cada fila y guardar eventos.

    Atributos que la subclase debe definir en _init_state():
        self.max_id   -- último game_id procesado (se actualiza en el loop)
    """

    def __init__(self, table_name, threshold, sync_state_table, warmup=100):
        self.table_name = table_name
        self.threshold = threshold
        self.sync_state_table = sync_state_table
        self.warmup = warmup
        self.conn = None
        self.cursor = None
        self.last_game_id = 0

    def _open(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def _load_state(self):
        self.cursor.execute(
            f"SELECT last_game_id FROM {self.sync_state_table} "
            f"WHERE table_name = ?", (self.table_name,)
        )
        row = self.cursor.fetchone()
        self.last_game_id = row[0] if row else 0

    def _fetch_rows(self, columns):
        lo = max(0, self.last_game_id - self.warmup)
        self.cursor.execute(
            f"SELECT {columns} FROM {self.table_name} "
            f"WHERE id > ? ORDER BY id ASC", (lo,)
        )
        return self.cursor.fetchall()

    def _is_new(self, db_id):
        return db_id > self.last_game_id

    def _save_state(self):
        self.cursor.execute(
            f"REPLACE INTO {self.sync_state_table} (table_name, last_game_id) "
            f"VALUES (?, ?)", (self.table_name, self.max_id)
        )

    def _close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def run(self, columns='id, numero, timestamp'):
        self._open()
        self._load_state()
        rows = self._fetch_rows(columns)

        if not rows:
            self._close()
            return

        self._init_state()
        self.max_id = self.last_game_id

        for row in rows:
            db_id, n = row[0], row[1]
            extra = row[2:] if len(row) > 2 else ()
            ts = row[-1]
            self.max_id = max(self.max_id, db_id)
            is_new = self._is_new(db_id)

            if n == -1:
                self._handle_chain_break(ts, is_new)
                self._init_state()
                continue

            self._process_row(db_id, n, extra, ts, is_new)

        self._save_state()
        self._close()

    def _init_state(self):
        raise NotImplementedError

    def _process_row(self, db_id, n, extra, ts, is_new):
        raise NotImplementedError

    def _handle_chain_break(self, ts, is_new):
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
# Backtest: docenas / columnas
# ═══════════════════════════════════════════════════════════════════════

class _ZoneBacktestSync(_BacktestSyncEngine):
    """Sincroniza eventos de retraso de docenas y columnas."""

    _ZONES = {
        "docena_1": (1, 12), "docena_2": (13, 24), "docena_3": (25, 36),
        "columna_1": (1, 1), "columna_2": (2, 2), "columna_3": (0, 0),
    }

    def __init__(self, table_name, threshold):
        super().__init__(table_name, threshold, 'sync_state')

    def _init_state(self):
        self.delays = {k: 0 for k in self._ZONES}
        self.active = {}

    def _handle_chain_break(self, ts, is_new):
        for k in list(self.active.keys()):
            evt = self.active[k]
            if self.delays[k] >= self.threshold:
                evt["max_delay"] = max(evt["max_delay"], self.delays[k])
                if is_new or evt.get("is_new", False):
                    self.cursor.execute(
                        "INSERT INTO backtest_history "
                        "(table_name, zone_name, start_time, end_time, max_delay, threshold_used) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (self.table_name, k, evt["start_time"], ts, evt["max_delay"], self.threshold)
                    )
        self.active.clear()

    def _process_row(self, db_id, n, extra, ts, is_new):
        if n == 0:
            for k in self.delays:
                self.delays[k] += 1
            for k in self.active:
                if self.delays[k] >= self.threshold:
                    self.active[k]["max_delay"] = max(self.active[k]["max_delay"], self.delays[k])
            return

        for k, zone in self._ZONES.items():
            if k.startswith("docena"):
                hits = zone[0] <= n <= zone[1]
            else:
                hits = (n % 3 == zone[0] % 3 or (zone[0] == 0 and n % 3 == 0))

            if hits:
                if self.delays[k] >= self.threshold and k in self.active:
                    evt = self.active.pop(k)
                    if is_new or evt.get("is_new", False):
                        self.cursor.execute(
                            "INSERT INTO backtest_history "
                            "(table_name, zone_name, start_time, end_time, max_delay, threshold_used) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (self.table_name, k, evt["start_time"], ts, evt["max_delay"], self.threshold)
                        )
                else:
                    self.active.pop(k, None)
                self.delays[k] = 0
            else:
                self.delays[k] += 1
                if self.delays[k] >= self.threshold:
                    if k not in self.active:
                        self.active[k] = {"start_time": ts, "max_delay": self.delays[k], "is_new": is_new}
                    else:
                        self.active[k]["max_delay"] = max(self.active[k]["max_delay"], self.delays[k])


def sync_backtest(table_name, threshold):
    _ZoneBacktestSync(table_name, threshold).run()


# ═══════════════════════════════════════════════════════════════════════
# Backtest: rachas de color
# ═══════════════════════════════════════════════════════════════════════

class _ColorBacktestSync(_BacktestSyncEngine):
    """Sincroniza eventos de rachas de rojos/negros consecutivos."""

    def __init__(self, table_name, threshold):
        super().__init__(table_name, threshold, 'color_sync_state', warmup=50)

    def _init_state(self):
        self.current_color = None
        self.current_count = 0
        self.current_start_ts = None
        self.active_is_new = False

    def _handle_chain_break(self, ts, is_new):
        self._save_streak(ts, is_new)
        self.current_color = None
        self.current_count = 0
        self.current_start_ts = None
        self.active_is_new = False

    def _save_streak(self, end_ts, is_end_new):
        if self.current_color and self.current_count >= self.threshold and (self.active_is_new or is_end_new):
            self.cursor.execute(
                "INSERT INTO color_streak_history "
                "(table_name, streak_color, streak_count, start_time, end_time, threshold_used) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (self.table_name, self.current_color, self.current_count,
                 self.current_start_ts, end_ts, self.threshold)
            )

    def _process_row(self, db_id, n, extra, ts, is_new):
        color = extra[0] if extra else ''

        if color == "Green" or n == 0:
            if self.current_color is not None:
                self.current_count += 1
                if is_new:
                    self.active_is_new = True
            return

        if color not in ("Red", "Black"):
            return

        if self.current_color is None:
            self.current_color = color
            self.current_count = 1
            self.current_start_ts = ts
            self.active_is_new = is_new
        elif color == self.current_color:
            self.current_count += 1
            if is_new:
                self.active_is_new = True
        else:
            self._save_streak(ts, is_new)
            self.current_color = color
            self.current_count = 1
            self.current_start_ts = ts
            self.active_is_new = is_new


def sync_color_backtest(table_name, threshold):
    _ColorBacktestSync(table_name, threshold).run(columns='id, numero, color, timestamp')


# ═══════════════════════════════════════════════════════════════════════
# Backtest: números individuales
# ═══════════════════════════════════════════════════════════════════════

class _NumberBacktestSync(_BacktestSyncEngine):
    """Sincroniza eventos de retraso de números individuales (0-36)."""

    def __init__(self, table_name, threshold):
        super().__init__(table_name, threshold, 'number_sync_state')

    def _init_state(self):
        self.delays = {n: 0 for n in range(37)}
        self.delay_start_times = {n: None for n in range(37)}
        self.active = {}

    def _handle_chain_break(self, ts, is_new):
        for num in list(self.active.keys()):
            evt = self.active[num]
            if self.delays[num] >= self.threshold:
                evt["max_delay"] = max(evt["max_delay"], self.delays[num])
                if is_new or evt.get("is_new", False):
                    self.cursor.execute(
                        "INSERT INTO number_delay_history "
                        "(table_name, number, start_time, end_time, max_delay, threshold_used, termination) "
                        "VALUES (?, ?, ?, ?, ?, ?, 'cadena_rota')",
                        (self.table_name, num, evt["start_time"], ts, evt["max_delay"], self.threshold)
                    )
        self.active.clear()

    def _process_row(self, db_id, n, extra, ts, is_new):
        for num in range(37):
            if num == n:
                if self.delays[num] >= self.threshold and num in self.active:
                    evt = self.active.pop(num)
                    if is_new or evt.get("is_new", False):
                        self.cursor.execute(
                            "INSERT INTO number_delay_history "
                            "(table_name, number, start_time, end_time, max_delay, threshold_used, termination) "
                            "VALUES (?, ?, ?, ?, ?, ?, 'normal')",
                            (self.table_name, num, evt["start_time"], ts, evt["max_delay"], self.threshold)
                        )
                self.delays[num] = 0
                self.delay_start_times[num] = None
            else:
                prev_delay = self.delays[num]
                self.delays[num] += 1
                if prev_delay == 0:
                    self.delay_start_times[num] = ts
                if self.delays[num] >= self.threshold:
                    if num not in self.active:
                        self.active[num] = {
                            "start_time": self.delay_start_times[num] or ts,
                            "max_delay": self.delays[num],
                            "is_new": is_new
                        }
                    else:
                        self.active[num]["max_delay"] = max(self.active[num]["max_delay"], self.delays[num])


def sync_number_backtest(table_name, threshold):
    _NumberBacktestSync(table_name, threshold).run()
