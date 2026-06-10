"""
Punto de entrada de la GUI — compatible con PyInstaller.
La implementacion esta en gui/app.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.desktop.screens.base import RouletteApp
from backend.desktop.screens import (
    PrerequisitesScreen, LoginScreen, LoadingScreen, DashboardScreen, UpdateScreen
)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    if len(sys.argv) > 1 and sys.argv[1] == "--run-dashboard":
        if getattr(sys, 'stdout', None) is None:
            sys.stdout = open(os.devnull, 'w')
        if getattr(sys, 'stderr', None) is None:
            sys.stderr = open(os.devnull, 'w')

        from backend.dashboard.app import app as flask_app
        import logging
        log_werkzeug = logging.getLogger('werkzeug')
        log_werkzeug.setLevel(logging.ERROR)

        from waitress import serve
        serve(flask_app, host='0.0.0.0', port=5050, clear_untrusted_proxy_headers=False)
        sys.exit(0)

    app = RouletteApp()
    app.mainloop()
