# Roulette Sniper - Bot Analitico para Stake

Bot automatizado avanzado para extraer datos en vivo de multiples mesas de ruleta de Pragmatic Play via Stake, calcular delays estadisticos de docenas/columnas, emitir alertas en Telegram, y proveer un Dashboard web en tiempo real.

---

## Caracteristicas Principales

- **Web Scraping Dinamico:** Usa Selenium (`undetected_chromedriver`) para evadir medidas Anti-Bot y extraer el feed en vivo del Lobby.
- **Multimesa Simultaneo:** Rastrea 19 mesas simultaneamente (Ruleta Latina, Mega Roulette, Brazilian Roulette, Roulette Macao, etc.).
- **Gestion de Sesion:** Limpieza de cookies/LocalStorage, modulo Anti-AFK integrado, auto-reinicio ante sesion expirada.
- **Base de Datos Persistente:** SQLite con WAL mode, conexion persistente y tablas separadas por juego.
- **Backtesting en Tiempo Real:** Motor de sincronizacion incremental con historial de senales completadas.
- **Alertas en Telegram:** Notificaciones de docenas/columnas retrasadas, rachas de color y numeros individuales con cooldown de 5 min.
- **Dashboard Interactivo:** Panel web en Flask + Waitress en puerto `:5050` con vistas globales y detalladas.
- **GUI Desktop:** Interfaz CustomTkinter con wizard de configuracion y credenciales encriptadas con Windows DPAPI.
- **Tunel Cloudflare:** Acceso remoto al dashboard via Cloudflare Tunnel.
- **Auto-Updater:** Descarga e instalacion automatica de nuevas versiones desde GitHub Releases.

---

## Requisitos

- **Python 3.9+**
- **Google Chrome** instalado
- **pip**

---

## Instalacion

```bash
git clone <repo>
cd Bot_Stake_Recolector
pip install -r bot_ruleta/requirements.txt
```

### Credenciales

**GUI (.exe):** Las credenciales se ingresan en la pantalla de login y se guardan encriptadas con DPAPI (`data/credentials.dat`).

**CLI (.env):** Copia `.env.example` a `.env` y completa los valores. El CLI usa `.env` como fallback si no hay credenciales DPAPI guardadas.

---

## Uso

### Ejecutable (.exe)
```bash
# Construir
python scripts/build_exe.py

# Ejecutar
scripts/dist/RouletteSniperPro.exe
```

### Desde codigo fuente
```bash
# Windows
start_bot.bat

# Ubuntu/VPS
bash install_ubuntu.sh
```

Dashboard en `http://localhost:5050`.

---

## Estructura del Proyecto

```
Bot_Stake_Recolector/
├── .env.example              # Plantilla de configuracion
├── start_bot.bat             # Lanzador Windows
├── install_ubuntu.sh         # Instalador Ubuntu/VPS
├── README.md
├── version.txt
│
├── bot_ruleta/
│   ├── config.py             # Constantes y configuracion de mesas
│   ├── db.py                 # SQLite con WAL + conexion persistente
│   ├── logic.py              # Algoritmos de delays, rachas y alertas
│   ├── scanner.py            # Loop principal de escaneo
│   ├── driver.py             # Selenium + anti-deteccion
│   ├── lobby.py              # Navegacion y mapeo dinamico de mesas
│   ├── iframe.py             # Manejo de iframes y modales
│   ├── telegram.py           # Cliente de Telegram Bot API
│   ├── tunnel.py             # Cloudflare Tunnel
│   ├── credentials.py        # Carga de credenciales (runtime > DPAPI > .env)
│   ├── thresholds.py         # Umbrales de alerta
│   ├── backtest.py           # Motor de sincronizacion incremental
│   ├── updater.py            # Auto-updater desde GitHub Releases
│   ├── launcher.py           # Orquestador CLI
│   ├── gui_app.py            # Entry point GUI (PyInstaller)
│   ├── run.py                # Entry point CLI
│   ├── logic_helpers.py      # Utilidades compartidas
│   ├── helpers.py            # human_type
│   ├── paths.py              # Resolucion de rutas (frozen vs dev)
│   ├── debug_logger.py       # Re-exportador de diagnostics
│   ├── gui_credentials.py    # DPAPI encrypt/decrypt (Windows)
│   │
│   ├── gui/
│   │   ├── app.py            # Orquestador GUI (CustomTkinter)
│   │   └── screens/          # Pantallas: prerequisites, login, loading, dashboard, update
│   │
│   ├── dashboard/
│   │   ├── app.py            # Backend Flask
│   │   └── static/           # Frontend HTML/CSS/JS
│   │
│   ├── diagnostics/          # Logger, screenshots, crash reports, system info
│   ├── tests/                # Tests unitarios (pytest)
│   └── data/                 # SQLite DB + logs + credenciales (gitignored)
│
├── scripts/
│   ├── build_exe.py          # Builder PyInstaller
│   ├── publish.py            # Publicador GitHub Releases
│   ├── gen_icon.py           # Generador de icono
│   └── verify_number_delays.py
│
├── docs/
│   └── Documentacion_Bot_Stake.md
│
└── graphify-out/             # Knowledge graph (auto-generado)
```

---

## Tests

```bash
pytest bot_ruleta/tests/ -v
```

---

## Aviso de Responsabilidad

Este software es una herramienta estrictamente analitica. Los valores presentados estan basados en informacion expuesta visualmente por los proveedores en vivo. El autor asume toda responsabilidad por el uso y mantenimiento de las credenciales inyectadas al Bot.
