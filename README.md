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
pip install -r backend/requirements.txt
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
├── backend/
│   ├── roulette/             # Motor de ruleta (driver, scanner, lobby, iframe, logic)
│   ├── database/             # SQLite con WAL + conexion persistente
│   ├── backtesting/          # Motor de sincronizacion incremental
│   ├── scanner_tools/        # Scanner de lobby IDs
│   ├── notifier/             # Telegram + Cloudflare Tunnel
│   ├── dashboard/            # Backend Flask + static React SPA
│   │   └── static/           # Build del dashboard React
│   ├── desktop/              # GUI CustomTkinter
│   │   └── screens/          # Pantallas: prerequisites, login, loading, dashboard, update
│   ├── auth/                 # Credenciales DPAPI + .env
│   ├── diagnostics/          # Logger, screenshots, crash reports, system info
│   ├── config/               # Constantes y resolucion de rutas
│   ├── shared/               # Utilidades compartidas
│   ├── tests/                # Tests unitarios (pytest)
│   ├── data/                 # SQLite DB + logs + credenciales (gitignored)
│   ├── launcher.py           # Orquestador CLI
│   ├── updater.py            # Auto-updater desde GitHub Releases
│   ├── main.py               # Entry point CLI
│   └── requirements.txt
│
├── frontend/                 # Dashboard React (Vite + TypeScript)
│   └── src/
│       ├── features/         # Dominios: overview, mesa-detail, analytics, auth
│       ├── components/       # UI compartidos (layout, ui)
│       ├── hooks/            # useApi, useSSE, useAlert
│       └── lib/              # Tipos, API client, contexto
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
pytest backend/tests/ -v
```

---

## Aviso de Responsabilidad

Este software es una herramienta estrictamente analitica. Los valores presentados estan basados en informacion expuesta visualmente por los proveedores en vivo. El autor asume toda responsabilidad por el uso y mantenimiento de las credenciales inyectadas al Bot.
