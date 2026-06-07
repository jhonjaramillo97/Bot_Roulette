"""
Crash Report: ZIP con diagnóstico + envío por Telegram.
"""
import os
import sys
import glob
import zipfile
import traceback
from datetime import datetime

from bot_ruleta.diagnostics.logger import get_logger
from bot_ruleta.diagnostics.screenshots import capture_screenshot, _cleanup_old_screenshots

if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGS_DIR = os.path.join(_BASE_DIR, "data", "logs")
SCREENSHOTS_DIR = os.path.join(LOGS_DIR, "screenshots")
CRASH_REPORTS_DIR = os.path.join(LOGS_DIR, "crash_reports")
os.makedirs(CRASH_REPORTS_DIR, exist_ok=True)


def generate_crash_report(driver=None, error: Exception = None) -> str | None:
    log = get_logger("crash_report")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    zip_name = f"debug_report_{timestamp}.zip"
    zip_path = os.path.join(CRASH_REPORTS_DIR, zip_name)

    log.critical(f"🚨 Generando crash report: {zip_name}")

    try:
        if driver:
            try:
                capture_screenshot(driver, f"CRITICAL_crash_{timestamp}", save_html=True)
            except Exception:
                pass

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            diag_file = os.path.join(LOGS_DIR, "diagnostico_inicio.txt")
            if os.path.exists(diag_file):
                zf.write(diag_file, "diagnostico_inicio.txt")

            log_files = sorted(glob.glob(os.path.join(LOGS_DIR, "bot_debug_*.log")), key=os.path.getmtime)
            if log_files:
                latest_log = log_files[-1]
                try:
                    with open(latest_log, "r", encoding="utf-8", errors="ignore") as f:
                        all_lines = f.readlines()
                        last_500 = all_lines[-500:] if len(all_lines) > 500 else all_lines
                    zf.writestr("bot_debug_recent.log", "".join(last_500))
                except Exception:
                    pass

            screenshots = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")), key=os.path.getmtime)
            for ss in screenshots[-10:]:
                zf.write(ss, f"screenshots/{os.path.basename(ss)}")
                html_comp = ss.replace(".png", ".html")
                if os.path.exists(html_comp):
                    zf.write(html_comp, f"screenshots/{os.path.basename(html_comp)}")

            env_path = os.path.join(os.path.dirname(_BASE_DIR), ".env")
            if os.path.exists(env_path):
                try:
                    with open(env_path, "r", encoding="utf-8") as f:
                        env_lines = f.readlines()
                    sanitized = []
                    for line in env_lines:
                        stripped = line.strip()
                        if "=" in stripped and not stripped.startswith("#"):
                            key = stripped.split("=", 1)[0].strip()
                            if "PASSWORD" in key.upper() or "TOKEN" in key.upper():
                                sanitized.append(f"{key}=********\n")
                            else:
                                sanitized.append(line)
                        else:
                            sanitized.append(line)
                    zf.writestr("env_sanitized.txt", "".join(sanitized))
                except Exception:
                    pass

            if error:
                tb_str = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                zf.writestr("traceback.txt", tb_str)

            if driver:
                try:
                    zf.writestr("page_source_error.html", driver.page_source)
                except Exception:
                    pass

        log.critical(f"📦 Crash report generado: {zip_path}")
        _send_crash_report_telegram(zip_path, error)
        _cleanup_old_crash_reports()
        return zip_path

    except Exception as e:
        log.error(f"Error generando crash report: {e}")
        return None


def _send_crash_report_telegram(zip_path: str, error: Exception = None):
    log = get_logger("crash_report")
    try:
        from bot_ruleta.credentials import load_credentials
        _, _, token, chat_id, _, _ = load_credentials()

        if not token or not chat_id:
            log.warning("No hay credenciales de Telegram configuradas. Crash report no enviado.")
            return

        import requests

        error_summary = str(error)[:200] if error else "Error desconocido"
        caption = (
            f"🚨 *CRASH REPORT*\n\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"❌ {error_summary}\n\n"
            f"📎 Revisa el ZIP adjunto para diagnóstico completo."
        )

        url = f"https://api.telegram.org/bot{token}/sendDocument"
        with open(zip_path, "rb") as f:
            files = {"document": (os.path.basename(zip_path), f)}
            data = {"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"}
            response = requests.post(url, files=files, data=data, timeout=30)

        if response.status_code == 200:
            log.info("✅ Crash report enviado por Telegram")
        else:
            log.warning(f"⚠️ Telegram respondió {response.status_code}: {response.text[:200]}")

    except Exception as e:
        log.error(f"Error enviando crash report por Telegram: {e}")


def _cleanup_old_crash_reports(max_reports: int = 10):
    try:
        zips = sorted(glob.glob(os.path.join(CRASH_REPORTS_DIR, "debug_report_*.zip")), key=os.path.getmtime)
        if len(zips) > max_reports:
            for old_zip in zips[:len(zips) - max_reports]:
                os.remove(old_zip)
    except Exception:
        pass
