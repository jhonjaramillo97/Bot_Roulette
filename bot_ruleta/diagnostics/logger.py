"""
Logger centralizado con rotación y handler para GUI.
"""
import os
import sys
import logging
import logging.handlers
import io
from datetime import datetime
from bot_ruleta.paths import get_data_dir

LOGS_DIR = os.path.join(get_data_dir(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

_LOG_FORMAT = "[%(asctime)s.%(msecs)03d] [%(levelname)-8s] [%(name)s] %(message)s"
_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_root_logger = logging.getLogger("bot")
_root_logger.setLevel(logging.DEBUG)

if not _root_logger.handlers:
    _log_file = os.path.join(LOGS_DIR, f"bot_debug_{datetime.now().strftime('%Y-%m-%d')}.log")
    _file_handler = logging.handlers.RotatingFileHandler(
        _log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8",
    )
    _file_handler.setLevel(logging.DEBUG)
    _file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FORMAT))
    _root_logger.addHandler(_file_handler)

    try:
        _safe_stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )
    except (AttributeError, TypeError):
        _safe_stdout = sys.stdout
    _console_handler = logging.StreamHandler(_safe_stdout)
    _console_handler.setLevel(logging.INFO)
    _console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FORMAT))
    _root_logger.addHandler(_console_handler)


def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(f"bot.{module_name}")


class _GUIQueueHandler(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        try:
            msg = self.format(record)
            self.queue.put(("log", record.levelname, msg))
        except Exception:
            pass


def attach_gui_queue(queue):
    handler = _GUIQueueHandler(queue)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATE_FORMAT))
    _root_logger.addHandler(handler)
