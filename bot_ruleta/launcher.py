import subprocess
import threading
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_ruleta.debug_logger import run_diagnostics, get_logger
from bot_ruleta.tunnel import run_tunnel, TUNNEL_FILE
from bot_ruleta.paths import is_frozen, get_base_dir

log = get_logger("launcher")

# Forzar codificación UTF-8 para la salida de la consola (Evitar crasheos de emojis en Windows)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Variables globales para la UI de consola
public_url = "Generando..."
last_log_line = "Iniciando sistema..."
tables_found_status = "Mesas: Esperando mapeo (Anti-AFK)..."
lock = threading.Lock()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_ui():
    """Dibuja la consola limpia y minimalista"""
    global public_url, last_log_line, tables_found_status
    
    with lock:
        clear_screen()
        print("=========================================================")
        print("              🎰 ROULETTE SNIPER BOT 🎰")
        print("=========================================================")
        print(f" 🏠 Dashboard Local: http://127.0.0.1:5050")
        print(f" 🌍 Acceso Remoto:   {public_url}")
        print("=========================================================")
        print(f" 🗂️  {tables_found_status}")
        print("=========================================================")
        print("\n ⚡ [ ESTADO ACTUAL DEL BOT ] ⚡\n")
        print(f" > {last_log_line}")
        print("\n=========================================================")
        print(" (Presiona Ctrl+C para apagar todo)")

def _update_tunnel_url(found_url):
    """Actualiza el URL del tunel: variable global, Telegram, UI."""
    global public_url

    with lock:
        old_url = public_url
        public_url = found_url

        if found_url != old_url:
            from bot_ruleta.tunnel import notify_tunnel_url
            notify_tunnel_url(found_url, old_url)

    render_ui()

def cloudflared_watchdog():
    """Hilo permanente que mantiene cloudflared vivo y actualiza la consola."""
    global public_url

    def _on_url(url):
        if url == "__error:no_instalado__":
            log.error("\u274c cloudflared no esta instalado")
            with lock:
                public_url = "ERROR: No esta instalado cloudflared"
            render_ui()
            return
        _update_tunnel_url(url)

    run_tunnel(on_url=_on_url)
            
def track_bot(process):
    """Lee la salida del bot y actualiza la consola minimalista"""
    global last_log_line, tables_found_status
    for line in iter(process.stdout.readline, b''):
        # Ya no eliminamos los emojis, solo limpiamos los saltos de línea
        cleaned_line = line.decode('utf-8', errors='ignore').replace('\r', '').replace('\n', '').strip()
        
        if cleaned_line: # No mostrar lineas vacias
            with lock:
                if "tiles totales" in cleaned_line or "Mesas mapeadas:" in cleaned_line:
                    tables_found_status = cleaned_line

                last_log_line = cleaned_line[-150:] # Mostrar un poco más de texto si hay emojis largos
            render_ui()

def cleanup():
    # Eliminar archivo tunnel.txt si queda
    if os.path.exists(TUNNEL_FILE):
        try: os.remove(TUNNEL_FILE)
        except Exception:
            pass
        
    import threading
    import time
    
    def _do_cleanup():
        import glob
        exe_dir = get_base_dir()
        current_exe = os.path.abspath(sys.executable) if is_frozen() else None
        
        cleanup_patterns = ["*.old", "*.update", "restart_update.bat"]
        
        # Intentar borrar hasta 5 veces (cada 2 segundos) para asegurar que se liberen los bloqueos
        for _ in range(5):
            all_clean = True
            
            for pattern in cleanup_patterns:
                for old_file in glob.glob(os.path.join(exe_dir, pattern)):
                    try: 
                        os.remove(old_file)
                    except Exception: 
                        all_clean = False
            
            # Limpiar versiones viejas versionadas (RouletteSniperPro_v*.exe) excepto la actual
            for old_file in glob.glob(os.path.join(exe_dir, "RouletteSniperPro_v*.exe")):
                if current_exe and os.path.abspath(old_file) == current_exe:
                    continue
                    try: 
                        os.remove(old_file)
                    except Exception: 
                        all_clean = False
            
            if all_clean:
                break
                
            time.sleep(2)
            
    threading.Thread(target=_do_cleanup, daemon=True).start()

if __name__ == "__main__":
    # Limpiar archivo viejo
    cleanup()
    
    # =====================================================
    # PASO 0: Diagnóstico de Entorno (ANTES de lanzar nada)
    # =====================================================
    print("=" * 60)
    print("  🔍 EJECUTANDO DIAGNÓSTICO DE ENTORNO...")
    print("=" * 60)
    diag_report = run_diagnostics()
    print(diag_report)
    print("\n  ✅ Diagnóstico completado. Guardado en logs/diagnostico_inicio.txt")
    print("=" * 60)
    time.sleep(3)  # Dar tiempo a leer el diagnóstico
    
# 1. Iniciar Dashboard (via gui_app.py --run-dashboard, mismo handler que la GUI)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gui_app_path = os.path.join(base_dir, "gui_app.py")
    
    dashboard_log = open(os.path.join(base_dir, "logs", "dashboard.log"), "a")
    dashboard_proc = subprocess.Popen([sys.executable, gui_app_path, "--run-dashboard"], 
                                       stdout=dashboard_log, 
                                       stderr=subprocess.STDOUT)
    
    # Watchdog para reiniciar Flask si se cae
    _dashboard_ref = [dashboard_proc]  # mutable para el closure
    def dashboard_watchdog():
        while True:
            _dashboard_ref[0].wait()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log.warning(f"[{timestamp}] Dashboard Flask se ha detenido. Reiniciando en 3 segundos...")
            time.sleep(3)
            _dashboard_ref[0] = subprocess.Popen([sys.executable, gui_app_path, "--run-dashboard"],
                                                  stdout=dashboard_log,
                                                  stderr=subprocess.STDOUT)
    threading.Thread(target=dashboard_watchdog, daemon=True).start()
    
    # 2. Iniciar Cloudflared (con watchdog que auto-reinicia)
    threading.Thread(target=cloudflared_watchdog, daemon=True).start()
    
    render_ui()
    time.sleep(2) # Esperar que levante web
    
    # 3. Iniciar Bot Principal con flag -u (unbuffered) y env UTF-8
    run_py_path = os.path.join(base_dir, "run.py")
    
    bot_env = os.environ.copy()
    bot_env["PYTHONIOENCODING"] = "utf-8"
    
    bot_proc = subprocess.Popen([sys.executable, "-u", run_py_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                env=bot_env)
    
    # Hilo para leer bot
    threading.Thread(target=track_bot, args=(bot_proc,), daemon=True).start()
    
    try:
        # Mantener vivo el programa principal mientras el bot esté corriendo
        bot_proc.wait()
    except KeyboardInterrupt:
        with lock:
            last_log_line = "APAGANDO SISTEMA..."
        render_ui()
    finally:
        # Cerrar todo ordenadamente
        try: bot_proc.terminate()
        except Exception: pass
        try: _dashboard_ref[0].terminate()
        except Exception: pass
        # cloudflared se cierra solo porque el hilo watchdog es daemon
        cleanup()
