import sys
import os
import logging
from flask import Flask, jsonify, request, send_from_directory, Response

log = logging.getLogger("dashboard")

# Añadir directorio raíz del proyecto al path para importar backend
# __file__ = backend/dashboard/app.py
# dirname = backend/dashboard
# dirname(dirname) = backend
# dirname(dirname(dirname)) = PROYECTO ROOT
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.config.config import TABLES, REDS
from backend.auth.credentials import load_credentials
from backend.roulette.thresholds import get_color_streak_threshold, get_number_delay_threshold
from backend.auth.gui_credentials import load_saved_credentials
from backend.backtesting.backtest import sync_backtest, sync_color_backtest, sync_number_backtest
from backend.database.db import validate_table_name, get_connection as get_db_connection
import backend.roulette.logic as bt_logic

def get_dashboard_threshold():
    """Lee el threshold de los datos guardados por la GUI. Fallback al .env"""
    saved = load_saved_credentials()
    if saved and "threshold" in saved:
        return saved["threshold"]
    _, _, _, _, threshold, _ = load_credentials()
    return threshold


def _get_validated_table(mesa_param):
    """Valida el parametro 'mesa' de un request.
    Retorna el table_name validado o lanza ValueError."""
    if not mesa_param:
        raise ValueError("Parametro 'mesa' requerido")
    return validate_table_name(mesa_param)

from backend.config.paths import get_data_dir

# Determinar rutas correctas para PyInstaller o desarrollo
if getattr(sys, 'frozen', False):
    static_dir = os.path.join(sys._MEIPASS, 'dashboard', 'static')
else:
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

DATA_DIR = get_data_dir()

app = Flask(__name__, static_url_path='', static_folder=static_dir)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Sin caché para archivos estáticos

os.makedirs(DATA_DIR, exist_ok=True)

# ── Auth middleware ──
DASHBOARD_TOKEN = os.getenv("DASHBOARD_TOKEN", "")

@app.before_request
def check_token():
    if DASHBOARD_TOKEN and request.path.startswith("/api/"):
        token = request.args.get("token", "")
        if token != DASHBOARD_TOKEN:
            return jsonify({"error": "Token invalido"}), 401


def calculate_delays(table_name, limit=None):
    """Calcula los delays de docenas y columnas para una tabla dada (USANDO LOGIC COMPARTIDA)."""
    try:
        table_name = validate_table_name(table_name)
        conn = get_db_connection()
        if limit is not None:
            cursor = conn.execute(
                f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC LIMIT ?", (limit,)
            )
        else:
            cursor = conn.execute(
                f"SELECT numero, color, timestamp FROM {table_name} ORDER BY id DESC"
            )
        rows = cursor.fetchall()
    except Exception:
        return None, []

    numeros = [dict(row) for row in rows]
    
    # Usar lógica centralizada
    delays = bt_logic.compute_delays(numeros)

    return delays, numeros


# ─── RUTAS ────────────────────────────────────────────────────────────

# SPA: todas las rutas de página sirven el mismo index.html (React Router)
@app.route('/')
@app.route('/mesa')
@app.route('/analisis')
def serve_spa():
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def spa_fallback(e):
    """Cualquier ruta que no sea /api/* sirve index.html para React Router."""
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/mesas')
def get_mesas():
    return jsonify([{"name": t["name"], "value": t["table_name"]} for t in TABLES])


@app.route('/api/overview')
def get_overview():
    """Retorna un resumen rápido de TODAS las mesas: delay máximo y alertas."""
    from datetime import datetime
    
    # Cargar threshold dinámico
    threshold = get_dashboard_threshold()
    
    result = []
    for t in TABLES:
        tn = t["table_name"]
        delays, nums = calculate_delays(tn)
        if delays is None:
            continue

        max_delay = max(delays.values())
        alertas = [k for k, v in delays.items() if v >= threshold]

        # Nombre bonito de la zona con mayor delay
        max_zone = max(delays, key=delays.get)
        zone_labels = {
            "docena_1": "1ª Docena", "docena_2": "2ª Docena", "docena_3": "3ª Docena",
            "columna_1": "Col. 1", "columna_2": "Col. 2", "columna_3": "Col. 3"
        }
        
        # Calcular tiempo desde la última actualización
        last_update_seconds = 999999
        if nums and "timestamp" in nums[0]:
            try:
                import time
                from datetime import datetime
                last_ts = datetime.strptime(nums[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
                last_ts_seconds = time.mktime(last_ts.timetuple())
                last_update_seconds = time.time() - last_ts_seconds
            except Exception as e:
                pass

        # Calcular racha de color
        color_streak = bt_logic.compute_color_streak(
            [{"numero": n["numero"], "color": n.get("color", "Green")} for n in nums]
        ) if nums else {"color": None, "streak": 0}

        # Calcular delays de números individuales
        number_delays = bt_logic.compute_number_delays(nums) if nums else {n: 0 for n in range(37)}
        number_threshold = get_number_delay_threshold()
        number_alerts = [(num, delay) for num, delay in number_delays.items() if delay >= number_threshold]
        
        result.append({
            "name": t["name"],
            "table_name": tn,
            "max_delay": max_delay,
            "max_zone": zone_labels.get(max_zone, max_zone),
            "delays": delays,
            "alertas": alertas,
            "ultimo": nums[0]["numero"] if nums else None,
            "ultimo_color": nums[0].get("color", "Green") if nums else None,
            "last_10": [{"val": n["numero"], "col": n.get("color", "Green")} for n in nums[:10]] if nums else [],
            "last_update_seconds": last_update_seconds,
            "color_streak": color_streak,
            "number_delays": number_delays,
            "number_alert_count": len(number_alerts),
            "number_alert_numbers": sorted(number_alerts, key=lambda x: -x[1])[:5]  # Top 5 retrasados
        })

    color_thresh = get_color_streak_threshold()
    number_thresh = get_number_delay_threshold()
    return jsonify({
        "threshold": threshold,
        "color_streak_threshold": color_thresh,
        "number_delay_threshold": number_thresh,
        "tables": result
    })


@app.route('/api/data')
def get_data():
    from datetime import datetime
    table_name = request.args.get('mesa', 'ruleta_latina')

    try:
        table_name = _get_validated_table(table_name)
    except ValueError:
        return jsonify({"error": "Parametro 'mesa' invalido"}), 400

    delays, numeros = calculate_delays(table_name)
    if delays is None:
        return jsonify({"error": "Error interno al leer datos"}), 500

    # Cargar threshold dinámico
    threshold = get_dashboard_threshold()

    alertas = [k for k, v in delays.items() if v >= threshold]
    
    # Calcular edad de los datos
    last_update_seconds = 999999
    if numeros and "timestamp" in numeros[0]:
        try:
            from datetime import datetime
            import time
            last_ts = datetime.strptime(numeros[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
            last_ts_seconds = time.mktime(last_ts.timetuple())
            last_update_seconds = time.time() - last_ts_seconds
        except Exception as e:
            log.warning(f"Error parsing date {numeros[0]['timestamp']}: {e}")

    # Calcular racha de color
    color_streak = bt_logic.compute_color_streak(
        [{"numero": n["numero"], "color": n.get("color", "Green")} for n in numeros]
    ) if numeros else {"color": None, "streak": 0}

    # Calcular delays de números individuales
    number_delays = bt_logic.compute_number_delays(numeros) if numeros else {n: 0 for n in range(37)}
    number_threshold = get_number_delay_threshold()
    number_alerts = [(num, delay) for num, delay in number_delays.items() if delay >= number_threshold]

    return jsonify({
        "mesa": table_name,
        "ultimos": numeros[:500],
        "delays": delays,
        "alertas": alertas,
        "threshold": threshold,
        "color_streak": color_streak,
        "color_streak_threshold": get_color_streak_threshold(),
        "number_delays": number_delays,
        "number_alert_count": len(number_alerts),
        "number_alert_numbers": sorted(number_alerts, key=lambda x: -x[1])[:5],
        "number_delay_threshold": number_threshold,
        "last_update_seconds": last_update_seconds
    })


@app.route('/api/backtest')
def get_backtest():
    table_name = request.args.get('mesa', 'ruleta_latina')
    try:
        table_name = _get_validated_table(table_name)
    except ValueError:
        return jsonify({"error": "Parametro 'mesa' invalido"}), 400

    threshold = get_dashboard_threshold()
    
    # 1. Sincronizar (procesar giros nuevos)
    try:
        sync_backtest(table_name, threshold)
    except Exception as e:
        log.warning(f"Error en sync_backtest: {e}")
        
    # 2. Leer historial
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT zone_name, start_time, end_time, max_delay FROM backtest_history WHERE table_name = ? ORDER BY id DESC LIMIT 100",
            (table_name,)
        )
        rows = cursor.fetchall()
        
        history = [dict(row) for row in rows]
        return jsonify({"mesa": table_name, "history": history})
    except Exception as e:
        log.error(f"Error en get_backtest: {e}")
        return jsonify({"error": "Error interno al leer backtest"}), 500


@app.route('/api/backtest_color')
def get_backtest_color():
    """Historial de rachas de color completadas para una mesa."""
    table_name = request.args.get('mesa', 'ruleta_latina')
    try:
        table_name = _get_validated_table(table_name)
    except ValueError:
        return jsonify({"error": "Parametro 'mesa' invalido"}), 400

    color_threshold = get_color_streak_threshold()
    
    # 1. Sincronizar
    try:
        sync_color_backtest(table_name, color_threshold)
    except Exception as e:
        log.warning(f"Error en sync_color_backtest: {e}")
        
    # 2. Leer historial
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT streak_color, streak_count, start_time, end_time FROM color_streak_history WHERE table_name = ? ORDER BY id DESC LIMIT 100",
            (table_name,)
        )
        rows = cursor.fetchall()
        
        history = [dict(row) for row in rows]
        return jsonify({"mesa": table_name, "history": history})
    except Exception as e:
        log.error(f"Error en get_backtest_color: {e}")
        return jsonify({"error": "Error interno al leer backtest de color"}), 500


@app.route('/api/backtest_number')
def get_backtest_number():
    """Historial de retrasos de numeros individuales completados + alertas activas."""
    table_name = request.args.get('mesa', 'ruleta_latina')
    try:
        table_name = _get_validated_table(table_name)
    except ValueError:
        return jsonify({"error": "Parametro 'mesa' invalido"}), 400

    number_threshold = get_number_delay_threshold()
    
    # 1. Sincronizar
    try:
        sync_number_backtest(table_name, number_threshold)
    except Exception as e:
        log.warning(f"Error en sync_number_backtest: {e}")
        
    # 2. Leer historial
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT number, start_time, end_time, max_delay, termination FROM number_delay_history WHERE table_name = ? ORDER BY id DESC LIMIT 100",
            (table_name,)
        )
        rows = cursor.fetchall()
        
        history = [dict(row) for row in rows]
        
        # 3. Calcular alertas activas (números retrasados AHORA, aún no completados)
        active_alerts = []
        try:
            _, numeros = calculate_delays(table_name)
            if numeros:
                current_delays = bt_logic.compute_number_delays(numeros)
                active_alerts = [
                    {"number": num, "max_delay": delay, "start_time": None, "end_time": None, "termination": None}
                    for num, delay in current_delays.items()
                    if delay >= number_threshold
                ]
                active_alerts.sort(key=lambda x: -x["max_delay"])
        except Exception as e:
            log.warning(f"Error calculando alertas activas: {e}")
        
        return jsonify({
            "mesa": table_name,
            "history": history,
            "active_alerts": active_alerts
        })
    except Exception as e:
        log.error(f"Error en get_backtest_number: {e}")
        return jsonify({"error": "Error interno al leer backtest de numeros"}), 500


@app.route('/api/analisis_global')
def get_analisis_global():
    threshold = get_dashboard_threshold()
    color_threshold = get_color_streak_threshold()
    
    number_threshold = get_number_delay_threshold()
    
    # 1. Sincronizar TODAS las mesas para asegurar datos frescos
    try:
        for t in TABLES:
            sync_backtest(t["table_name"], threshold)
            sync_color_backtest(t["table_name"], color_threshold)
            sync_number_backtest(t["table_name"], number_threshold)
    except Exception as e:
        log.warning(f"Error en sync global: {e}")
        
    # 2. Extraer historial de tercios
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT table_name, zone_name, start_time, end_time, max_delay FROM backtest_history ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        history = [dict(row) for row in rows]
        
        # 3. Extraer historial de rachas de color
        cursor2 = conn.execute(
            "SELECT table_name, streak_color, streak_count, start_time, end_time FROM color_streak_history ORDER BY id DESC"
        )
        color_rows = cursor2.fetchall()
        color_history = [dict(row) for row in color_rows]
        
        # 4. Extraer historial de números individuales
        cursor3 = conn.execute(
            "SELECT table_name, number, start_time, end_time, max_delay, termination FROM number_delay_history ORDER BY id DESC"
        )
        number_rows = cursor3.fetchall()
        number_history = [dict(row) for row in number_rows]
        
        # 5. Calcular delays actuales de números para cada mesa
        current_number_delays = {}
        active_number_alerts = []  # Alertas activas (aún no completadas) para análisis global
        for t in TABLES:
            tn = t["table_name"]
            try:
                _, nums = calculate_delays(tn)
                if nums:
                    nd = bt_logic.compute_number_delays(nums)
                    current_number_delays[tn] = {str(k): v for k, v in nd.items()}
                    for num, delay in nd.items():
                        if delay >= number_threshold:
                            active_number_alerts.append({
                                "table_name": tn,
                                "number": num,
                                "max_delay": delay,
                                "start_time": None,
                                "end_time": None,
                                "termination": None
                            })
            except Exception:
                current_number_delays[tn] = {}
        active_number_alerts.sort(key=lambda x: -x["max_delay"])
        
        return jsonify({
            "history": history,
            "color_history": color_history,
            "number_history": number_history,
            "current_number_delays": current_number_delays,
            "active_number_alerts": active_number_alerts,
            "threshold": threshold,
            "color_streak_threshold": color_threshold,
            "number_delay_threshold": number_threshold
        })
    except Exception as e:
        log.error(f"Error en analisis_global: {e}")
        return jsonify({"error": "Error interno en analisis global"}), 500


@app.route('/api/signal_detail')
def get_signal_detail():
    """Devuelve las jugadas individuales que componen una senal especifica."""
    table_name = request.args.get('mesa')
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    pico = request.args.get('pico', type=int)
    
    if not table_name:
        return jsonify({"error": "Parametro 'mesa' requerido"}), 400
    try:
        table_name = _get_validated_table(table_name)
    except ValueError:
        return jsonify({"error": "Parametro 'mesa' invalido"}), 400

    if pico is not None and pico <= 0:
        return jsonify({"error": "Parametro 'pico' debe ser mayor a 0"}), 400
    
    try:
        conn = get_db_connection()
        
        if pico and pico > 0:
            if end_time:
                limit = pico + 1
                cursor = conn.execute(
                    f"SELECT numero, color, timestamp FROM {table_name} "
                    f"WHERE timestamp <= ? ORDER BY id DESC LIMIT ?",
                    (end_time, limit)
                )
            else:
                limit = pico
                cursor = conn.execute(
                    f"SELECT numero, color, timestamp FROM {table_name} "
                    f"ORDER BY id DESC LIMIT ?",
                    (limit,)
                )
            rows = cursor.fetchall()
            rows.reverse()
        else:
            if not start_time:
                return jsonify({"error": "Parametro 'start' requerido si no hay 'pico'"}), 400
                
            if end_time:
                cursor = conn.execute(
                    f"SELECT numero, color, timestamp FROM {table_name} "
                    f"WHERE timestamp BETWEEN ? AND ? ORDER BY id ASC",
                    (start_time, end_time)
                )
            else:
                cursor = conn.execute(
                    f"SELECT numero, color, timestamp FROM {table_name} "
                    f"WHERE timestamp >= ? ORDER BY id ASC LIMIT 50",
                    (start_time,)
                )
            rows = cursor.fetchall()
        
        plays = [{"numero": r["numero"], "color": r["color"], "timestamp": r["timestamp"]} for r in rows]
        return jsonify({"mesa": table_name, "plays": plays})
    except Exception as e:
        log.error(f"Error en signal_detail: {e}")
        return jsonify({"error": "Error interno al leer detalle de senal"}), 500


@app.route('/api/tunnel')
def get_tunnel():
    """Retorna el link actual de Cloudflare si esta disponible"""
    tunnel_file = os.path.join(get_data_dir(), "tunnel.txt")
    if os.path.exists(tunnel_file):
        try:
            with open(tunnel_file, "r") as f:
                url = f.read().strip()
                if url:
                    return jsonify({"url": url})
        except Exception:
            pass
            
    return jsonify({"url": None})


@app.route('/api/stream')
def sse_stream():
    """Server-Sent Events endpoint para datos en tiempo real."""
    import json
    import time

    def generate():
        while True:
            try:
                overview_data = _build_overview_data()
                yield f"event: overview\ndata: {json.dumps(overview_data)}\n\n"
            except Exception as e:
                log.error(f"SSE error: {e}")
                yield f"event: error\ndata: {{}}\n\n"
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
    })


def _build_overview_data():
    """Construye los datos del overview como dict (sin jsonify)."""
    from datetime import datetime
    import time as _time

    threshold = get_dashboard_threshold()
    result = []
    for t in TABLES:
        tn = t["table_name"]
        delays, nums = calculate_delays(tn)
        if delays is None:
            continue

        max_delay = max(delays.values())
        alertas = [k for k, v in delays.items() if v >= threshold]
        max_zone = max(delays, key=delays.get)
        zone_labels = {
            "docena_1": "1ª Docena", "docena_2": "2ª Docena", "docena_3": "3ª Docena",
            "columna_1": "Col. 1", "columna_2": "Col. 2", "columna_3": "Col. 3"
        }

        last_update_seconds = 999999
        if nums and "timestamp" in nums[0]:
            try:
                last_ts = datetime.strptime(nums[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
                last_update_seconds = _time.time() - (_time.mktime(last_ts.timetuple()))
            except Exception:
                pass

        color_streak = bt_logic.compute_color_streak(
            [{"numero": n["numero"], "color": n.get("color", "Green")} for n in nums]
        ) if nums else {"color": None, "streak": 0}

        number_delays = bt_logic.compute_number_delays(nums) if nums else {n: 0 for n in range(37)}
        number_threshold = get_number_delay_threshold()
        number_alerts = [(num, delay) for num, delay in number_delays.items() if delay >= number_threshold]

        result.append({
            "name": t["name"],
            "table_name": tn,
            "max_delay": max_delay,
            "max_zone": zone_labels.get(max_zone, max_zone),
            "delays": delays,
            "alertas": alertas,
            "ultimo": nums[0]["numero"] if nums else None,
            "ultimo_color": nums[0].get("color", "Green") if nums else None,
            "last_10": [{"val": n["numero"], "col": n.get("color", "Green")} for n in nums[:10]] if nums else [],
            "last_update_seconds": last_update_seconds,
            "color_streak": color_streak,
            "number_delays": number_delays,
            "number_alert_count": len(number_alerts),
            "number_alert_numbers": sorted(number_alerts, key=lambda x: -x[1])[:5]
        })

    return {
        "threshold": threshold,
        "color_streak_threshold": get_color_streak_threshold(),
        "number_delay_threshold": get_number_delay_threshold(),
        "tables": result
    }


if __name__ == '__main__':
    log.info("Iniciando dashboard en puerto 5050...")
    app.run(port=5050, host='0.0.0.0', use_reloader=False)
