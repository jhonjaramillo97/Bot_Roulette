"""
Gestion del tunel Cloudflare compartido entre GUI y CLI.
Unifica cloudflared_watchdog duplicado en gui/app.py y launcher.py.
"""

import os
import re
import sys
import time
import subprocess
import threading
import base64

from bot_ruleta.paths import get_data_dir

DATA_DIR = get_data_dir()
TUNNEL_FILE = os.path.join(DATA_DIR, "tunnel.txt")

DEV_MODE = os.environ.get("USE_RANDOM_TUNNEL", "true").lower() == "true"

_URL_PATTERN = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

_BUILTIN_CF_TOKEN_B64 = "ZXlKaElqb2lORGcwTWpCaU1ERTBNelE0TXpobE5EazJPREF3TnpZd09UTTFZMkkwT0RjaUxDSjBJam9pWW1NeE56QXhPRE10T1dJME5TMDBaamc1TFdJMFpESXRZV1EwTXpNd09XTmxOR1JpSWl3aWN5STZJazlVYTNoT2JWRjVUa2ROZEZwVVVURk5lVEF3VDBkU2JVeFVhR2hPZW1kMFRXcEpNbHBVU1RGWmVsbDVUbGRaTWlKOQ=="


def get_cf_env_vars():
    """Retorna (token, dominio) de Cloudflare.
    Prioridad: CLOUDFLARE_TOKEN env > token built-in > None (DEV_MODE o sin token).
    Si DEV_MODE es True, usa tunel temporal trycloudflare (sin token)."""
    if DEV_MODE:
        return None, None

    token = os.environ.get("CLOUDFLARE_TOKEN", "")
    if not token:
        token = base64.b64decode(_BUILTIN_CF_TOKEN_B64).decode()
    domain = os.environ.get("CLOUDFLARE_DOMAIN", "botstake.shop")
    return token, domain


def _start_cloudflared(token=None):
    """Inicia un proceso cloudflared y retorna el proceso."""
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

    if token and token != "":
        return subprocess.Popen(
            ["cloudflared", "tunnel", "run", "--token", token],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            creationflags=creationflags
        )
    else:
        return subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5050"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            creationflags=creationflags
        )


def _save_tunnel_url(url):
    try:
        with open(TUNNEL_FILE, "w") as f:
            f.write(url)
    except Exception:
        pass


def notify_tunnel_url(url, old_url=""):
    """Envia notificacion por Telegram cuando el URL del tunel se establece o cambia.
    Usa formato unificado para CLI y GUI."""
    try:
        from bot_ruleta.telegram import send_telegram_msg
        from bot_ruleta.credentials import load_credentials
        _, _, token, chat_id, _, _ = load_credentials()
        if not token or not chat_id or not token.strip():
            return

        is_update = old_url and "trycloudflare" in str(old_url)
        if is_update:
            msg = f"Nuevo enlace del Dashboard:\n\n{url}"
        else:
            msg = f"Dashboard Activo\n\n{url}"

        send_telegram_msg(token, chat_id, msg)
    except Exception:
        pass


def run_tunnel(on_url, stop_event=None):
    """
    Mantiene un tunel cloudflared vivo con auto-reinicio.

    Args:
        on_url: callback(url) llamado cada vez que el URL se establece o cambia
        stop_event: threading.Event opcional para apagado graceful
    """
    while True:
        if stop_event and stop_event.is_set():
            break

        try:
            token, domain = get_cf_env_vars()
            cf_proc = _start_cloudflared(token)

            if token:
                display_url = "https://botstake.shop"
                _save_tunnel_url(display_url)
                on_url(display_url)

                for line in iter(cf_proc.stderr.readline, b''):
                    if stop_event and stop_event.is_set():
                        break
            else:
                for line in iter(cf_proc.stderr.readline, b''):
                    if stop_event and stop_event.is_set():
                        break
                    line_str = line.decode('utf-8', errors='ignore')
                    match = _URL_PATTERN.search(line_str)
                    if match:
                        found_url = match.group(0)
                        _save_tunnel_url(found_url)
                        on_url(found_url)

            if stop_event and stop_event.is_set():
                try:
                    cf_proc.terminate()
                except Exception:
                    pass
                break

            cf_proc.wait()
            time.sleep(10)

        except FileNotFoundError:
            on_url("__error:no_instalado__")
            break
        except Exception:
            time.sleep(10)
