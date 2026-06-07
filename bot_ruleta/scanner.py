"""
Loop principal del bot: escaneo de tiles, extracción y guardado de datos.
Incluye detección de sesión expirada y auto-reinicio.
"""

import os
import time
import random
from selenium.webdriver.common.by import By

from bot_ruleta.config import TABLES, DATA_DIR, LOBBY_MODE, LOBBY_URL, REDS
from bot_ruleta.credentials import load_credentials
from bot_ruleta.driver import setup_driver, login_stake
from bot_ruleta.lobby import ir_al_lobby, map_tables_dynamic
from bot_ruleta.iframe import switch_to_game_iframe
from bot_ruleta.db import init_db, guardar_resultado, obtener_ultimo_numero, obtener_ultimos_numeros
import bot_ruleta.logic as bt_logic
from bot_ruleta.debug_logger import get_logger, capture_screenshot, generate_crash_report, run_diagnostics

log = get_logger("scanner")


# ---------------------------------------------------------------------------
# Helpers internos del scanner
# ---------------------------------------------------------------------------

def extract_nums_js(driver, tile_element):
    """Extrae números visibles de un tile usando JavaScript (class-agnostic)."""
    js_script = """
        var tile = arguments[0];
        var nums = [];
        var allEls = tile.querySelectorAll('span, div');
        for (var i = 0; i < allEls.length; i++) {
            var el = allEls[i];
            var txt = el.textContent.trim();
            if (/^\\d{1,2}$/.test(txt)) {
                var num = parseInt(txt);
                if (num >= 0 && num <= 36) {
                    var childEls = el.querySelectorAll('span, div');
                    var isLeaf = true;
                    for (var j = 0; j < childEls.length; j++) {
                        if (childEls[j].textContent.trim().length > 0) {
                            isLeaf = false;
                            break;
                        }
                    }
                    if (isLeaf && el.offsetParent !== null) {
                        nums.push(txt);
                    }
                }
            }
        }
        return nums;
    """
    try:
        return driver.execute_script(js_script, tile_element)
    except Exception:
        log.debug(f"extract_nums_js fallo para tile", exc_info=True)
        return []


# ---------------------------------------------------------------------------
# Sesión Unitaria (Driver Start -> Login -> Loop -> Error)
# ---------------------------------------------------------------------------

# ── constantes del scanner ─────────────────────────────────────────────
_MIN_CHAIN = 4
_MAX_ZERO_TILES = 30
_SESSION_CHECK_INTERVAL = 30
_HEARTBEAT_INTERVAL = 60
_SOFT_REFRESH_AT = 15
_EXPIRY_CHECK_AT_ZERO_TILES = 3

# Tablas mapeadas dinamicamente (se actualizan en cada sesion/refresh)
_mapped_tables = list(TABLES)


def _run_single_session(email, password, headless=True, stop_event=None):
    """Orquestador: inicializa, escanea y maneja errores de una sesion."""
    global _mapped_tables
    driver = None
    try:
        driver, wait, tables = _initialize_session(email, password, headless)
        _mapped_tables = tables
        _scan_loop(driver, wait, stop_event)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        _handle_error(driver, e)
        raise
    finally:
        _cleanup_driver(driver)


# ── setup ──────────────────────────────────────────────────────────────

def _initialize_session(email, password, headless):
    """Setup driver + login + lobby + iframe + audio keep-alive.
    Retorna (driver, wait, mapped_tables)."""
    log.info("Iniciando nueva sesion del bot...")
    driver, wait = setup_driver(headless=headless)
    capture_screenshot(driver, "01_driver_iniciado")

    login_stake(driver, wait, email, password)
    ir_al_lobby(driver, wait)
    capture_screenshot(driver, "03_lobby_cargado")

    mapped = list(TABLES)
    if LOBBY_MODE:
        log.info("MODO ESPIA ACTIVADO: Escaneando miniaturas...")
        switch_to_game_iframe(driver)
        capture_screenshot(driver, "04_iframe_context")
        time.sleep(2)
        mapped = map_tables_dynamic(driver)
        capture_screenshot(driver, "05_mesas_mapeadas")

    _start_audio_keepalive(driver)
    return driver, wait, mapped


def _start_audio_keepalive(driver):
    """AudioContext silencioso para evitar que Chrome suspenda la página."""
    try:
        driver.execute_script("""
            window.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = window.audioCtx.createOscillator();
            var gain = window.audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, window.audioCtx.currentTime);
            gain.gain.setValueAtTime(0.0001, window.audioCtx.currentTime);
            osc.connect(gain);
            gain.connect(window.audioCtx.destination);
            osc.start();
            setInterval(() => {
                if(window.audioCtx.state === 'suspended') window.audioCtx.resume();
            }, 1000);
        """)
        log.debug("🔊 Audio keep-alive activado")
    except Exception:
        log.debug("⚠️ Audio keep-alive no disponible (no crítico)")


# ── loop principal ─────────────────────────────────────────────────────

def _scan_loop(driver, wait, stop_event):
    """Loop infinito de escaneo de tiles."""
    log.info("📡 Comienza escaneo continuo...")
    consecutive_zero_tiles = 0
    scan_cycle = 0

    while True:
        if stop_event and stop_event.is_set():
            log.info("🛑 Bot detenido por usuario (GUI).")
            return
        scan_cycle += 1

        _simulate_mouse_move(driver)

        if scan_cycle % _SESSION_CHECK_INTERVAL == 0:
            _check_session_expiry(driver)

        tables_scanned = _scan_all_tables(driver)

        if tables_scanned == 0:
            consecutive_zero_tiles += 1
            consecutive_zero_tiles = _handle_zero_tiles(driver, wait, consecutive_zero_tiles)
            if consecutive_zero_tiles == 0:
                continue  # soft refresh hizo reset
        else:
            consecutive_zero_tiles = 0

        if scan_cycle % _HEARTBEAT_INTERVAL == 0:
            log.debug(f"💓 Heartbeat: ciclo {scan_cycle}, tiles OK: {tables_scanned}")

        print(f"📡 Escaneando... [{time.strftime('%H:%M:%S')}]", end="\r", flush=True)
        time.sleep(0.5)


def _simulate_mouse_move(driver):
    """Simula movimiento de mouse JS para evitar desconexión de Pragmatic."""
    try:
        driver.execute_script("""
            var ev = new MouseEvent('mousemove', {
                'view': window, 'bubbles': true, 'cancelable': true,
                'clientX': Math.floor(Math.random() * window.innerWidth),
                'clientY': Math.floor(Math.random() * window.innerHeight)
            });
            document.dispatchEvent(ev);
        """)
    except Exception:
        pass


# ── escaneo de mesas ───────────────────────────────────────────────────

def _scan_all_tables(driver):
    """Escanea todas las mesas mapeadas. Retorna cuantas tuvieron exito."""
    scanned = 0
    for mesa in _mapped_tables:
        if _scan_single_table(driver, mesa["name"], mesa["id"]):
            scanned += 1
    return scanned


def _scan_single_table(driver, nombre, iframe_id):
    """Escanea una mesa. Retorna True si encontró números y los procesó."""
    try:
        tile = driver.find_element(By.ID, iframe_id)
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", tile
        )
        time.sleep(0.5)

        numeros = extract_nums_js(driver, tile)
        if not numeros:
            return False

        nuevos = _chain_match_and_save(nombre, numeros)
        if nuevos:
            _send_alerts(nombre)

        return True
    except Exception as e:
        log.debug(f"Error escaneando tile '{nombre}': {e}")
        return False


def _chain_match_and_save(nombre, numeros):
    """Chain matching robusto + guardado en DB. Retorna los números nuevos."""
    nums_int = [int(n) for n in numeros]
    db_history = obtener_ultimos_numeros(nombre, limit=15)
    db_nums = [d["numero"] for d in db_history] if db_history else []

    nuevos = _chain_match(nums_int, db_nums, nombre)
    if not nuevos:
        return []

    log.info(f"🔥 {nombre}: Nuevos -> {nuevos}")
    ts_base = time.time()
    for idx, num in enumerate(nuevos):
        color = _get_color(num)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts_base - len(nuevos) + 1 + idx))
        guardar_resultado(nombre, num, color, ts, int(ts_base) + idx)

    return nuevos


def _get_color(num):
    if num == -1:
        return "Reset"
    if num == 0:
        return "Green"
    return "Red" if str(num) in REDS else "Black"


def _chain_match(nums_int, db_nums, nombre):
    """Busca empalme de MIN_CHAIN números consecutivos entre tile y DB.
    Retorna lista de números nuevos (reversed)."""
    if not db_nums:
        return list(reversed(nums_int))

    anchor_idx = -1
    for i in range(len(nums_int)):
        for j in range(len(db_nums)):
            if nums_int[i] == db_nums[j]:
                chain_len = 0
                while (i + chain_len < len(nums_int) and
                       j + chain_len < len(db_nums) and
                       nums_int[i + chain_len] == db_nums[j + chain_len]):
                    chain_len += 1
                if chain_len >= _MIN_CHAIN:
                    anchor_idx = i
                    break
        if anchor_idx != -1:
            break

    if anchor_idx > 0:
        return list(reversed(nums_int[:anchor_idx]))
    elif anchor_idx == 0:
        return []
    else:
        log.warning(f"⚠️ {nombre}: CADENA ROTA (sin empalme de {_MIN_CHAIN}+).")
        return [-1] + list(reversed(nums_int))


def _send_alerts(nombre):
    """Envía alertas de delay, color y números a Telegram."""
    try:
        history = obtener_ultimos_numeros(nombre)
        if not history:
            return
        bt_logic.check_and_notify(nombre, bt_logic.compute_delays(history), history)
        bt_logic.check_and_notify_color(nombre, bt_logic.compute_color_streak(history), history)
        bt_logic.check_and_notify_number(nombre, bt_logic.compute_number_delays(history), history)
    except Exception as e:
        log.error(f"Error TG: {e}")


# ── salud del escaneo ──────────────────────────────────────────────────

def _handle_zero_tiles(driver, wait, consecutive):
    """Maneja ciclos sin tiles: chequeo de expiración, soft refresh, fallo crítico."""
    if consecutive % 5 == 0:
        log.warning(f"⚠️ 0 tiles por {consecutive} ciclos...")

    if consecutive >= _EXPIRY_CHECK_AT_ZERO_TILES:
        _check_session_expiry(driver)

    if consecutive >= _MAX_ZERO_TILES:
        capture_screenshot(driver, "CRITICAL_max_zero_tiles")
        raise Exception("MAX_ZERO_TILES alcanzado: bot ciego o desconectado.")

    if consecutive == _SOFT_REFRESH_AT:
        _soft_refresh_lobby(driver, wait)
        return 0  # reset contador

    return consecutive


def _check_session_expiry(driver):
    """Detecta si la sesión expiró por inactividad."""
    try:
        driver.switch_to.default_content()
        elements = driver.find_elements(
            By.XPATH,
            "//*[contains(text(), 'sesión ha finalizado')] | "
            "//*[contains(text(), 'falta de inactividad')] | "
            "//*[contains(text(), 'session has expired')] | "
            "//*[contains(text(), 'vuelve a iniciar sesión')]"
        )
        for el in elements:
            if el.is_displayed():
                log.warning("⏰ Sesión expirada por inactividad. Reiniciando...")
                raise Exception("SESIÓN EXPIRADA: Reinicio automático")
        switch_to_game_iframe(driver)
    except Exception as e:
        if "SESIÓN EXPIRADA" in str(e):
            raise
        switch_to_game_iframe(driver, max_wait=3)


def _soft_refresh_lobby(driver, wait):
    """Soft refresh: recarga el lobby sin re-login."""
    global _mapped_tables
    log.warning("15 ciclos sin tiles. Soft Refresh...")
    driver.switch_to.default_content()
    driver.get(LOBBY_URL)
    time.sleep(5)
    ir_al_lobby(driver, wait, from_anti_afk=False)
    if LOBBY_MODE:
        switch_to_game_iframe(driver)
        time.sleep(2)
        _mapped_tables = map_tables_dynamic(driver)


# ── error / cleanup ────────────────────────────────────────────────────

def _handle_error(driver, e):
    """Distingue sesión expirada de error real y genera crash report si aplica."""
    error_msg = str(e)
    if "SESIÓN EXPIRADA" in error_msg:
        log.warning(f"⏰ {error_msg}")
        log.info("🔄 Preparando reinicio rápido de sesión...")
    else:
        log.critical(f"❌ Error crítico en sesión: {e}")
        log.critical(f"Traceback completo:\n{__import__('traceback').format_exc()}")
        generate_crash_report(driver=driver, error=e)


def _cleanup_driver(driver):
    """Cierra el navegador de forma segura."""
    if driver:
        log.info("🛑 Cerrando navegador...")
        try:
            driver.quit()
        except Exception:
            log.debug("Error al cerrar driver", exc_info=True)


# ---------------------------------------------------------------------------
# Loop Supervisor (Entry Point)
# ---------------------------------------------------------------------------

def run_bot(stop_event=None):
    """Loop supervisor que asegura que el bot se reinicie si falla.
    
    Args:
        stop_event: threading.Event opcional para detener el bot desde la GUI.
    """
    
    # Cargar config inicial
    email, password, _, _, _, headless = load_credentials()
    init_db()

    # Ejecutar diagnóstico de entorno
    log.info("=" * 60)
    log.info("🔧 Ejecutando diagnóstico de entorno...")
    run_diagnostics()
    log.info("=" * 60)

    log.info(f"🤖 Bot Supervisor Iniciado - Headless: {headless}")

    session_count = 0
    while True:
        if stop_event and stop_event.is_set():
            log.info("👋 Bot detenido por GUI.")
            break
        session_count += 1
        log.info(f"🔄 Iniciando sesión #{session_count}...")
        try:
            _run_single_session(email, password, headless=headless, stop_event=stop_event)
        except KeyboardInterrupt:
            log.info("👋 Deteniendo bot por usuario.")
            break
        except Exception as e:
            if stop_event and stop_event.is_set():
                break
            error_msg = str(e)
            if "SESIÓN EXPIRADA" in error_msg:
                log.info("🔄 Reiniciando sesión en 5 segundos... (el link del dashboard sigue activo)")
                time.sleep(5)
            else:
                log.critical(f"🔄 REINICIANDO BOT EN 15 SEGUNDOS POR ERROR: {e}")
                time.sleep(15)
