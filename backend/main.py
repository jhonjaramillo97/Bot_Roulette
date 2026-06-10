#!/usr/bin/env python3
"""
Entrypoint del bot de ruleta.
Uso: python run.py
"""

import sys
import os

# Añadir directorio raíz del proyecto al path para importar backend como paquete
# __file__ = backend/main.py
# dirname = backend
# dirname(dirname) = PROYECTO ROOT
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.diagnostics import get_logger, run_diagnostics

log = get_logger("run")

if __name__ == "__main__":
    log.info("=" * 60)
    log.info("🚀 Bot de Ruleta iniciando...")
    log.info("=" * 60)
    
    # Diagnóstico de entorno al inicio directo
    run_diagnostics()
    
    from backend.roulette.scanner import run_bot
    run_bot()
