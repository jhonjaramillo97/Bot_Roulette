"""
Punto de entrada de la GUI — compatible con PyInstaller.
La implementacion esta en gui/app.py.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_ruleta.gui.app import RouletteApp
from bot_ruleta.gui.screens import (
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

        from bot_ruleta.dashboard.app import app as flask_app
        import logging
        log_werkzeug = logging.getLogger('werkzeug')
        log_werkzeug.setLevel(logging.ERROR)

        from waitress import serve
        import subprocess, time as _time
        for attempt in range(5):
            try:
                serve(flask_app, host='0.0.0.0', port=5050, clear_untrusted_proxy_headers=False)
                break
            except OSError as e:
                if attempt < 4 and "10048" in str(e) or "Address already in use" in str(e):
                    # Matar proceso que ocupa el puerto 5050
                    try:
                        out = subprocess.check_output('netstat -ano | findstr :5050', shell=True, text=True)
                        for line in out.strip().split('\n'):
                            parts = line.strip().split()
                            if parts and 'LISTENING' in line:
                                pid = parts[-1]
                                subprocess.call(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except Exception:
                        pass
                    _time.sleep(5)
                else:
                    raise
        sys.exit(0)

    app = RouletteApp()
    app.mainloop()
