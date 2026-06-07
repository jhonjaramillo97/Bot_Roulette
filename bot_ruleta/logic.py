import time
from bot_ruleta.credentials import load_credentials
from bot_ruleta.logic_helpers import extract_numero, nums_to_emoji
from bot_ruleta.telegram import send_telegram_msg

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
        if isinstance(item, dict):
            n = item.get('numero', item)
            timestamp_str = item.get('timestamp')
        else:
            n = extract_numero(item)
            
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
            hist_str = ""
            if history:
                hist_str = nums_to_emoji(history)

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
        n = extract_numero(item)

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
            hist_str = nums_to_emoji(history)

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

