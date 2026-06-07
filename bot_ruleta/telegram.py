"""
Cliente de Telegram Bot API.
Extraido de logic.py para separar el envio de mensajes de la logica de analytics.
"""

import requests
from bot_ruleta.debug_logger import get_logger

log = get_logger("telegram")


def send_telegram_msg(token, chat_id, text):
    """Envia mensaje raw a Telegram."""
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
        log.error(f"Error enviando Telegram: {e}")
        return False
