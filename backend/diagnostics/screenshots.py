"""
Capturas de pantalla automáticas del navegador.
"""
import os
import sys
import glob
from datetime import datetime

from backend.config.paths import get_data_dir
from .logger import get_logger

SCREENSHOTS_DIR = os.path.join(get_data_dir(), "logs", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

_screenshot_counter = 0
_DIAGNOSTICS_ENABLED = False


def set_diagnostics(enabled: bool):
    global _DIAGNOSTICS_ENABLED
    _DIAGNOSTICS_ENABLED = enabled


def capture_screenshot(driver, label: str, save_html: bool = True) -> str | None:
    global _screenshot_counter
    if driver is None:
        return None

    global _DIAGNOSTICS_ENABLED
    if not _DIAGNOSTICS_ENABLED:
        if "CRITICAL" not in label.upper() and "ERROR" not in label.upper():
            return None

    log = get_logger("screenshot")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    _screenshot_counter += 1
    counter_str = f"{_screenshot_counter:03d}"
    safe_label = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in label)
    base_name = f"{counter_str}_{timestamp}_{safe_label}"

    png_path = os.path.join(SCREENSHOTS_DIR, f"{base_name}.png")
    html_path = os.path.join(SCREENSHOTS_DIR, f"{base_name}.html")

    try:
        driver.save_screenshot(png_path)
        log.info(f"📸 Screenshot guardado: {png_path}")

        if save_html:
            try:
                page_src = driver.page_source
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page_src)
                log.debug(f"📄 HTML source guardado: {html_path}")
            except Exception as e:
                log.warning(f"No se pudo guardar HTML source: {e}")

        return png_path
    except Exception as e:
        log.error(f"Error tomando screenshot '{label}': {e}")
        return None


def _cleanup_old_screenshots(max_files: int = 50):
    try:
        files = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")), key=os.path.getmtime)
        if len(files) > max_files:
            for old_file in files[:len(files) - max_files]:
                os.remove(old_file)
                html_companion = old_file.replace(".png", ".html")
                if os.path.exists(html_companion):
                    os.remove(html_companion)
    except Exception:
        pass
