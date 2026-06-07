"""
Motores de sincronizacion incremental de backtests.
Extraido de db.py/logic.py para mantener separacion de responsabilidades:
  - db.py: CRUD y schema
  - backtest.py: logica de negocio de backtesting
  - logic.py: analytics en tiempo real (delays, streaks, alertas)
"""

from datetime import datetime
from bot_ruleta.db import get_connection, validate_table_name


class _BacktestSyncEngine:
    """Motor de sincronizacion incremental compartido por todos los backtests.

    Maneja: conexion a DB, lectura de estado de sincronizacion, batch con
    warmup, loop principal con manejo de cadena rota (-1), y guardado de
    estado incremental. Las subclases solo definen la logica de dominio:
    como inicializar delays, procesar cada fila y guardar eventos.

    Atributos que la subclase debe definir en _init_state():
        self.max_id   -- ultimo game_id procesado (se actualiza en el loop)
    """

    def __init__(self, table_name, threshold, sync_state_table, warmup=100):
        self.table_name = validate_table_name(table_name)
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


class _NumberBacktestSync(_BacktestSyncEngine):
    """Sincroniza eventos de retraso de numeros individuales (0-36)."""

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
