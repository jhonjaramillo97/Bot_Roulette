import requests
import time
from bot_ruleta.credentials import load_credentials

# Cache para evitar spam de notificaciones
# Key: f"{table_name}_{zone}" -> Value: timestamp de última notificación
ALERT_COOLDOWN = 60 * 5  # 5 minutos entre alertas de la misma zona
_alert_cache = {}

def compute_delays(numeros):
    """
    Calcula los delays de docenas y columnas dado una lista de números o diccionarios.
    numeros[0] es el más reciente.
    """
    from datetime import datetime
    
    delays = {
        "docena_1": 0, "docena_2": 0, "docena_3": 0,
        "columna_1": 0, "columna_2": 0, "columna_3": 0
    }
    found = {k: False for k in delays}
    
    prev_time = None

    for item in numeros:
        # Extraer el número y timestamp si es un dict/Row
        timestamp_str = None
        if hasattr(item, '__getitem__') and not isinstance(item, (str, bytes, int)):
            try:
                n = item['numero']
                timestamp_str = item.get('timestamp')
            except:
                n = item
        else:
            n = item
            
        # Validación rigurosa de continuidad (Marcador oficial de cadena rota)
        if n == -1:
            break # Topamos con un agujero ciego comprobado. Hasta aquí llega el delay actual.
            
        if n == 0:
            for k in delays:
                if not found[k]:
                    delays[k] += 1
            continue

        zones = {
            "docena_1": (1 <= n <= 12),
            "docena_2": (13 <= n <= 24),
            "docena_3": (25 <= n <= 36),
            "columna_1": (n % 3 == 1),
            "columna_2": (n % 3 == 2),
            "columna_3": (n % 3 == 0),
        }

        for k, hits in zones.items():
            if hits:
                found[k] = True
            elif not found[k]:
                delays[k] += 1

        if all(found.values()):
            break
            
    return delays

def check_and_notify(table_name, delays, history=None):
    """
    Verifica si hay delays que superen el umbral y envía notificación a Telegram.
    Maneja cooldown para no spamear.
    La notificación incluye una previsualización visual de los últimos giros.
    """
    global _alert_cache
    
    # Cargar credenciales y configuración
    _, _, token, chat_id, alert_threshold, _ = load_credentials()
    
    # DEBUG LOGGING EXTREMO
    try:
        with open("bot_ruleta/logs/debug_tg.txt", "a") as f:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{ts}] CHECKING {table_name}: Threshold={alert_threshold} Delays={delays}\n")
    except:
        pass
    
    if not token or not chat_id:
        return

    # Usar SOLO el umbral del .env
    threshold = alert_threshold

    alerts = [k for k, v in delays.items() if v >= threshold]
    
    for zone in alerts:
        cache_key = f"{table_name}_{zone}"
        last_time = _alert_cache.get(cache_key, 0)
        
        if time.time() - last_time > ALERT_COOLDOWN:
            # Formatear el historial de los ultimos 10 números con emojis keycap
            hist_str = ""
            if history:
                recent_10 = history[:10]
                emojis = []
                keycap_map = {
                    "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
                    "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
                }
                for item in reversed(recent_10):
                    n = item["numero"] if isinstance(item, dict) else item
                    if n == 10:
                        emojis.append("🔟")
                    else:
                        emojis.append("".join(keycap_map[c] for c in str(n)))
                
                hist_str = " ".join(emojis)

            # Enviar alerta (Diseño sofisticado solicitado por usario)
            friendly_zone = zone.replace("_", " ").title()
            msg = f"🎰 *{table_name}*\n\n⚠️ Zona: *{friendly_zone}*"
            if hist_str:
                msg += f"\n\n📊 *Últimos 10 giros:*\n{hist_str}"
            
            if send_telegram_msg(token, chat_id, msg):
                print(f"✅ Notificación Telegram enviada: {table_name} - {zone}")
                
                try:
                    with open("bot_ruleta/logs/debug_tg.txt", "a") as f:
                         f.write(f"   >>> SENT ALERT for {zone} (Delay {delays[zone]})\n")
                except: pass
                
                _alert_cache[cache_key] = time.time()
        else:
            try:
                with open("bot_ruleta/logs/debug_tg.txt", "a") as f:
                     f.write(f"   >>> SKIPPED {zone} (Cooldown)\n")
            except: pass

def send_telegram_msg(token, chat_id, text):
    """Envía mensaje raw a Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Error enviando Telegram: {e}")
        return False


# ─── SEÑALES DE RACHAS DE COLOR (ROJOS/NEGROS) ───────────────────────

def compute_color_streak(numeros):
    """
    Calcula la racha actual de un color (Rojo o Negro) basándose en los números recientes.
    El verde (0) es un comodín: suma a la racha sin romperla.
    Retorna un dict: {"color": "Red"|"Black", "streak": int}
    """
    streak_color = None
    streak_count = 0
    greens_at_start = 0
    
    for item in numeros:
        # Extraer color del item
        if hasattr(item, '__getitem__') and not isinstance(item, (str, bytes, int)):
            try:
                color = item.get('color', item.get('col', ''))
                n = item.get('numero', item.get('val', -1))
            except:
                continue
        else:
            continue
        
        # Marcador de cadena rota — detener
        if n == -1:
            break
        
        # Verde (0) = comodín, suma a la racha
        if color == "Green" or n == 0:
            if streak_color is None:
                greens_at_start += 1
            else:
                streak_count += 1
            continue
        
        if color not in ("Red", "Black"):
            continue
        
        if streak_color is None:
            # Primer color real encontrado — inicia la racha
            streak_color = color
            streak_count = 1 + greens_at_start
        elif color == streak_color:
            # Mismo color — la racha sigue
            streak_count += 1
        else:
            # Color opuesto — la racha se rompe, ya no necesitamos seguir
            break
    
    return {"color": streak_color, "streak": streak_count}


def check_and_notify_color(table_name, streak_data, history=None):
    """
    Si la racha de color supera el umbral, envía notificación a Telegram.
    Usa cooldown independiente con cache key 'tablename_color_Red/Black'.
    """
    global _alert_cache
    
    from bot_ruleta.thresholds import get_color_streak_threshold
    
    color = streak_data.get("color")
    streak = streak_data.get("streak", 0)
    threshold = get_color_streak_threshold()
    
    if not color or streak < threshold:
        return
    
    _, _, token, chat_id, _, _ = load_credentials()
    if not token or not chat_id:
        return
    
    cache_key = f"{table_name}_color_{color}"
    last_time = _alert_cache.get(cache_key, 0)
    
    if time.time() - last_time > ALERT_COOLDOWN:
        # Emoji según color
        color_emoji = "🔴" if color == "Red" else "⚫"
        color_name = "Rojos" if color == "Red" else "Negros"
        opposite = "Negro" if color == "Red" else "Rojo"
        
        # Historial visual
        hist_str = ""
        if history:
            recent_10 = history[:10]
            chips = []
            for item in reversed(recent_10):
                n = item.get("numero", item.get("val", "?"))
                c = item.get("color", item.get("col", ""))
                if c == "Red":
                    chips.append(f"🔴{n}")
                elif c == "Black":
                    chips.append(f"⚫{n}")
                else:
                    chips.append(f"🟢{n}")
            hist_str = " ".join(chips)
        
        msg = (
            f"🎰 *{table_name}*\n\n"
            f"{color_emoji} Racha: *{streak} {color_name}* consecutivos\n"
            f"💡 Señal para apostar al *{opposite}*"
        )
        if hist_str:
            msg += f"\n\n📊 *Últimos giros:*\n{hist_str}"
        
        if send_telegram_msg(token, chat_id, msg):
            print(f"✅ Alerta de color enviada: {table_name} - {streak} {color_name}")
            _alert_cache[cache_key] = time.time()


from datetime import datetime
from bot_ruleta.db import get_connection


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

    # ── setup / teardown ──────────────────────────────────────────

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

    # ── método principal (llamado por las subclases) ────────────────

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

    # ── métodos que las subclases deben implementar ─────────────────

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
            else:  # columna
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
                (self.table_name, self.current_color, self.current_count, self.current_start_ts, end_ts, self.threshold)
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


# ─── SEÑALES DE NÚMEROS INDIVIDUALES ─────────────────────────────────

def compute_number_delays(numeros):
    """
    Calcula los delays (giros sin salir) para cada número individual 0-36.
    numeros[0] es el más reciente.
    Si encuentra un -1 (cadena rota), ignora todo lo posterior.
    Retorna un dict: {0: delay_0, 1: delay_1, ..., 36: delay_36}
    """
    last_seen = {n: None for n in range(37)}
    total_processed = 0

    for idx, item in enumerate(numeros):
        if hasattr(item, '__getitem__') and not isinstance(item, (str, bytes, int)):
            try:
                n = item['numero']
            except:
                n = item
        else:
            n = item

        if n == -1:
            break

        total_processed = idx + 1

        if last_seen[n] is None:
            last_seen[n] = idx

        if None not in last_seen.values():
            break

    delays = {}
    for num in range(37):
        if last_seen[num] is None:
            delays[num] = total_processed
        else:
            delays[num] = last_seen[num]

    return delays


def check_and_notify_number(table_name, delays, history=None):
    """
    Verifica si hay números individuales que superen el umbral de retraso.
    Envía UNA notificación consolidada por mesa (no un mensaje por número).
    Cooldown independiente de 5 minutos.
    """
    global _alert_cache

    from bot_ruleta.thresholds import get_number_delay_threshold

    threshold = get_number_delay_threshold()
    alert_numbers = [(num, delay) for num, delay in delays.items() if delay >= threshold]

    if not alert_numbers:
        return

    _, _, token, chat_id, _, _ = load_credentials()
    if not token or not chat_id:
        return

    cache_key = f"{table_name}_numbers"
    last_time = _alert_cache.get(cache_key, 0)

    if time.time() - last_time > ALERT_COOLDOWN:
        nums_str = ", ".join([f"{num} ({delay})" for num, delay in sorted(alert_numbers, key=lambda x: -x[1])])

        hist_str = ""
        if history:
            recent_10 = history[:10]
            emojis = []
            keycap_map = {
                "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
                "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
            }
            for item in reversed(recent_10):
                n = item["numero"] if isinstance(item, dict) else item
                if n == 10:
                    emojis.append("🔟")
                else:
                    emojis.append("".join(keycap_map[c] for c in str(n)))
            hist_str = " ".join(emojis)

        msg = (
            f"🎰 *{table_name}*\n\n"
            f"🔢 *Números retrasados:* {nums_str}\n"
            f"📊 Umbral: {threshold} giros"
        )
        if hist_str:
            msg += f"\n\n📊 *Últimos 10 giros:*\n{hist_str}"

        if send_telegram_msg(token, chat_id, msg):
            print(f"✅ Alerta de números enviada: {table_name} - {len(alert_numbers)} números")
            _alert_cache[cache_key] = time.time()


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
