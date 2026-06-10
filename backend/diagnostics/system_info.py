"""
Diagnóstico completo del entorno (OS, Chrome, RAM, disco, red, dependencias).
"""
import os
import sys
import time
import platform
import shutil
from datetime import datetime

from backend.config.paths import get_data_dir, get_base_dir
from .logger import get_logger

_BASE_DIR = get_base_dir()
LOGS_DIR = os.path.join(get_data_dir(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def run_diagnostics() -> str:
    log = get_logger("diagnostics")
    lines = []

    def _add(key, value):
        lines.append(f"  {key:<22} {value}")

    lines.append("=" * 60)
    lines.append("  🔍 DIAGNÓSTICO DE ENTORNO")
    lines.append(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    try:
        os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    except Exception:
        os_info = "No disponible"
    _add("OS:", os_info)
    _add("Python:", f"{sys.version.split()[0]} ({sys.executable})")

    chrome_version = "No detectado"
    try:
        if platform.system() == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            chrome_version = version
        else:
            import subprocess
            result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True, timeout=5)
            chrome_version = result.stdout.strip()
    except Exception as e:
        chrome_version = f"Error: {e}"
    _add("Chrome:", chrome_version)

    try:
        import psutil
        mem = psutil.virtual_memory()
        _add("RAM Total:", f"{mem.total / (1024**3):.1f} GB")
        _add("RAM Disponible:", f"{mem.available / (1024**3):.1f} GB ({mem.percent}% en uso)")
    except ImportError:
        _add("RAM:", "psutil no instalado (instalar para más info)")
    except Exception as e:
        _add("RAM:", f"Error: {e}")

    try:
        disk = shutil.disk_usage(_BASE_DIR)
        _add("Disco Libre:", f"{disk.free / (1024**3):.1f} GB de {disk.total / (1024**3):.1f} GB")
    except Exception as e:
        _add("Disco:", f"Error: {e}")

    env_path = os.path.join(os.path.dirname(_BASE_DIR), ".env")
    if os.path.exists(env_path):
        try:
            from backend.auth.credentials import load_credentials
            email, password, tg_token, tg_chat_id, threshold, headless = load_credentials()
            email_masked = email[:3] + "***" + email[email.index("@"):] if "@" in email else "???"
            _add(".env:", "✅ Encontrado")
            _add("  Email:", email_masked)
            _add("  Password:", "✅ Presente" if password else "❌ VACÍO")
            _add("  TG Token:", "✅ Presente" if tg_token else "❌ VACÍO")
            _add("  TG Chat ID:", "✅ Presente" if tg_chat_id else "❌ VACÍO")
            _add("  Threshold:", str(threshold))
            _add("  Headless:", str(headless))
        except Exception as e:
            _add(".env:", f"⚠️ Error leyendo: {e}")
    else:
        _add(".env:", "❌ NO ENCONTRADO")

    for d_name, d_path in [("data/", os.path.join(_BASE_DIR, "data")), ("logs/", LOGS_DIR)]:
        try:
            test_file = os.path.join(d_path, ".write_test")
            os.makedirs(d_path, exist_ok=True)
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            _add(f"Permisos {d_name}:", "✅ Escritura OK")
        except Exception as e:
            _add(f"Permisos {d_name}:", f"❌ SIN ESCRITURA: {e}")

    try:
        import urllib.request
        start_t = time.time()
        urllib.request.urlopen("https://stake.com.co", timeout=10)
        latency = (time.time() - start_t) * 1000
        _add("Red (stake.com.co):", f"✅ Accesible ({latency:.0f}ms)")
    except Exception as e:
        _add("Red (stake.com.co):", f"❌ NO ACCESIBLE: {e}")

    try:
        import undetected_chromedriver as uc
        _add("UC Driver:", f"✅ v{uc.__version__}" if hasattr(uc, "__version__") else "✅ Instalado")
    except ImportError:
        _add("UC Driver:", "❌ NO INSTALADO")

    try:
        import selenium
        _add("Selenium:", f"✅ v{selenium.__version__}")
    except ImportError:
        _add("Selenium:", "❌ NO INSTALADO")

    lines.append("=" * 60)
    report = "\n".join(lines)

    diag_path = os.path.join(LOGS_DIR, "diagnostico_inicio.txt")
    try:
        with open(diag_path, "w", encoding="utf-8") as f:
            f.write(report)
    except Exception:
        pass

    for line in lines:
        log.info(line)

    return report
