# Roulette Sniper Pro - Documentación del Proyecto 🎰

## 1. ¿Qué hace este bot?

**Roulette Sniper Pro** es un bot analítico automatizado y un sistema de inteligencia de datos diseñado para el casino en línea **Stake**. Su función principal es extraer datos en vivo de múltiples mesas de ruleta de Pragmatic Play, analizar el historial de giros matemáticamente en tiempo real, y proveer información estratégica al usuario mediante alertas e interfaces visuales.

### Funcionalidades Principales:
- **Scraping Dinámico Multimesa:** Utiliza Selenium (con evasión Anti-Bot avanzada vía `undetected_chromedriver` y parches CDP) para leer resultados de hasta 18 mesas de ruleta de manera simultánea. En lugar de abrir múltiples ventanas, el bot extrae la información directamente de las "miniaturas" (tiles) de la sala de espera (Lobby) de Pragmatic Play.
- **Motor Analítico (Delays y Rachas):** Analiza el flujo de números para calcular "delays" (la cantidad de giros que han pasado sin que caiga una docena, columna o número específico) y monitorea "rachas" continuas de colores (rojos/negros consecutivos).
- **Señales de Números Individuales:** Nueva lógica que detecta cuando un número específico (0-36) no ha salido en un umbral configurable de giros (20-150). Muestra una grilla visual tipo tablero de ruleta con los delays de cada número.
- **Notificaciones Push en Telegram:** Cuando un retraso, racha o número retrasado supera el límite establecido por el usuario, el bot envía una notificación enriquecida (con historial de emojis) directamente a un chat de Telegram.
- **Persistencia y Backtesting:** Almacena de manera incremental todos los giros extraídos en una base de datos local `SQLite` (`ruleta.db`). Esto permite consultar el historial completo y realizar "backtesting" para ver qué mesas tuvieron los mayores retrasos estadísticos del día.
- **Dashboard Web Global:** Levanta un servidor web (Flask) que muestra un panel de control interactivo en el navegador en el puerto `:5050`. Utiliza `cloudflared` para exponer esta web a través de un túnel seguro, permitiendo al usuario monitorear el bot desde su teléfono móvil sin importar dónde se encuentre el PC servidor.
- **Interfaz Gráfica de Usuario (GUI):** Cuenta con una aplicación de escritorio visual (construida en CustomTkinter) para que los usuarios configuren parámetros (incluyendo el umbral de números individuales), guarden credenciales, enciendan el sistema y vean logs sin necesidad de interactuar con comandos de terminal.
- **Sistema de Actualizaciones OTA:** Se conecta a GitHub para verificar si hay nuevas versiones del `.exe` y las descarga e instala automáticamente.

---

## 2. Estructura y Función de Cada Archivo

### Archivos Raíz del Proyecto

- **`README.md`**: Manual de usuario con instrucciones de instalación, dependencias y explicaciones generales de uso.
- **`.env`**: Archivo de variables de entorno donde se almacenan configuraciones sensibles: credenciales de Stake, tokens de Telegram y variables de umbrales.
- **`.gitignore`**: Define qué archivos o carpetas Git no debe rastrear. Excluye `venv/`, `data/`, `build/`, `dist/`, `.env`, `github_token.txt`, logs y archivos de credenciales para seguridad.
- **`start_bot.bat`**: Script Windows que activa el entorno virtual y ejecuta `backend/launcher.py`. Lanza el bot + dashboard + túnel con una sola llamada.
- **`install.bat`**: Script Windows que crea/repara el entorno virtual `venv` e instala todas las dependencias desde `requirements.txt`.
- **`install_ubuntu.sh`**: Script Bash para VPS Ubuntu que instala Chrome, Xvfb, swap, entorno virtual y dependencias del bot.
- **`publish.py`**: Script de distribución para el desarrollador. Automatiza: compilar con `build_exe.py`, actualizar `version.txt` en GitHub, crear/eliminar releases y subir el asset `.exe`. Requiere `github_token.txt`.
- **`build_exe.py`**: Script que construye el comando de PyInstaller con todas las dependencias necesarias (`customtkinter`, `PIL`, `selenium`, datos estáticos del dashboard) y ejecuta la compilación.
- **`gen_icon.py`**: Script utilitario para gestionar o generar el ícono (`icon.ico` / `favicon.ico`) usado por el ejecutable y el dashboard web.
- **`version.txt`**: Archivo de texto plano con la versión actual del software (ej. `3.0.3`).
- **`Diseño_ruletta.png`**: Imagen de recurso utilizada como arte o esquema visual en la documentación.

---

### Directorio Principal: `backend/`

Este directorio contiene todo el código fuente operativo del bot, dividido lógicamente en varios submódulos.

#### 🖥️ Ejecución y Coordinación

- **`run.py`**: Punto de entrada base del bot (sin GUI ni dashboard). Inicializa logs, ejecuta diagnósticos y arranca `scanner.run_bot()`. Útil para ejecutar solo el motor de scraping sin servicios adicionales.
- **`launcher.py`**: El "Director de Orquesta". Lanza tres procesos/hilos en paralelo:
  1. Subproceso del dashboard Flask (`dashboard/app.py`) en el puerto 5050.
  2. Hilo watchdog de `cloudflared` (levanta el túnel, extrae la URL pública, la guarda en `data/tunnel.txt`).
  3. Subproceso del bot principal (`run.py`) y un hilo que lee su stdout para mostrar una UI minimalista en consola.
  Además contiene una interfaz de terminal con estados de conexión visual.
- **`gui_app.py`**: Aplicación de escritorio principal construida con **CustomTkinter**. Tiene 5 pantallas/flujos:
  1. **PrerequisitesScreen**: Verifica Chrome, Cloudflared e internet; busca actualizaciones.
  2. **LoginScreen**: Formulario compacto de credenciales Stake/Telegram, tres sliders de configuración (Tercios, Color, Números), switches para headless/logs/recordar.
  3. **LoadingScreen**: Barra de progreso simulada (10 segundos).
  4. **DashboardScreen**: Muestra estado del bot, URL del túnel (copiar/abrir), consola de logs en tiempo real, botón de detener.
  5. **UpdateScreen**: Descarga e instala nuevas versiones del `.exe` desde GitHub.
- **`updater.py`**: Sistema de actualizaciones OTA. Consulta la API de GitHub (`api.github.com/repos/jhonjaramillo97/roulette-sniper-releases`) para leer `version.txt`. Si hay versión nueva, descarga el `.exe`, ejecuta un `.bat` temporal que reemplaza el archivo en ejecución y reinicia.

#### 🤖 Motor de Scraping y Automatización (Selenium)

- **`driver.py`**: Configura la instancia de Google Chrome mediante `undetected_chromedriver` para evadir Cloudflare y detección anti-bot. Incluye:
  - Inyecciones JavaScript CDP (`navigator.webdriver=false`, spoof de plugins, idiomas).
  - Rutinas automatizadas de login en Stake.
  - Lógica Win32 API para ocultar la ventana de Chrome (mueve a `-2400,-2400` y usa `TOOLWINDOW` para quitar de la barra de tareas).
- **`scanner.py`**: El corazón del bot. Bucle continuo (`while True`) que:
  - Crea el WebDriver y navega al lobby.
  - Mapea IDs dinámicos de las mesas.
  - En cada ciclo, inyecta JavaScript en los tiles para leer números sin abrir cada juego.
  - Realiza un "empalme" robusto: exige 4 coincidencias consecutivas con la base de datos para confirmar continuidad. Si no hay empalme, inserta `-1` (cadena rota) y reinicia.
  - Detecta sesión expirada por inactividad cada 30 ciclos.
  - Llama a `logic.compute_delays`, `logic.compute_color_streak`, `logic.compute_number_delays` y sus respectivas funciones de alerta y backtesting.
  - En caso de error crítico, captura screenshot, genera crash report ZIP y reinicia automáticamente.
- **`lobby.py`**: Navegación inteligente al lobby de ruletas. Limpia cookies/localStorage, hace login, busca el botón "Juego real", espera la carga de tiles y ejecuta `map_tables_dynamic()`. Esta función asocia nombres de ruletas con IDs dinámicos del HTML usando reconocimiento de texto visual para tolerar cambios en la web.
- **`iframe.py`**: Gestiona el cambio de contexto al iframe de Pragmatic Play y cierra modales/pop-ups emergentes que puedan interferir con el scraping.

#### 🧠 Lógica de Negocio y Persistencia de Datos

- **`config.py`**: Repositorio de variables globales. Contiene:
  - `TABLES`: Lista maestra de 18 mesas de ruleta con nombres, IDs, `table_name` para SQLite.
  - `LOBBY_URL`: URL del lobby de Stake.
  - `REDS`: Lista de números rojos de la ruleta.
  - Constantes de umbrales: `COLOR_STREAK_THRESHOLD = 5`, `NUMBER_DELAY_THRESHOLD = 50`.
  - `load_credentials()`: Lee `.env` con soporte para formato antiguo (líneas sin `=`) y moderno (`KEY=VALUE`).
  - `set_runtime_config()`: Permite a la GUI inyectar credenciales y umbrales en memoria sin modificar archivos.
  - `get_color_streak_threshold()` y `get_number_delay_threshold()`: Lectura de umbrales con prioridad: runtime > GUI saved > `.env` > default.
- **`logic.py`**: Motor analítico y alertas. Funciones clave:
  - `compute_delays(numeros)`: Calcula giros sin salir para docenas y columnas.
  - `compute_color_streak(numeros)`: Calcula racha actual de rojos/negros (0 es comodín).
  - `compute_number_delays(numeros)`: **Nueva.** Calcula para cada número 0-36 cuántos giros han pasado desde su última aparición.
  - `check_and_notify()`: Envía alertas de tercios a Telegram con cooldown de 5 minutos.
  - `check_and_notify_color()`: Envía alertas de rachas de color.
  - `check_and_notify_number()`: **Nueva.** Envía UNA alerta consolidada por mesa con todos los números retrasados que superan el umbral.
  - `sync_backtest()`: Procesa giros nuevos de una mesa para guardar eventos históricos de delays de tercios.
  - `sync_color_backtest()`: Lo mismo para rachas de color.
  - `sync_number_backtest()`: **Nueva.** Procesa giros nuevos para guardar eventos históricos de retrasos de números individuales.
- **`db.py`**: Persistencia SQLite. Funciones:
  - `init_db()`: Crea todas las tablas necesarias si no existen:
    - Una tabla por mesa (`ruleta_latina`, `mega_roulette`, etc.) con columnas `id`, `numero`, `color`, `timestamp`, `game_id`.
    - `backtest_history`: Eventos completados de delays de tercios.
    - `sync_state`: Estado de sincronización incremental para tercios.
    - `color_streak_history`: Eventos completados de rachas de color.
    - `color_sync_state`: Estado de sincronización para colores.
    - `number_delay_history`: **Nueva.** Eventos completados de retrasos de números.
    - `number_sync_state`: **Nueva.** Estado de sincronización para números.
  - `guardar_resultado()`: Inserta un giro en la tabla correspondiente.
  - `obtener_ultimos_numeros()`: Devuelve los últimos N registros de una mesa.
- **`gui_credentials.py`**: Guarda/lee credenciales en `data/credentials.dat` usando XOR con una clave derivada de `platform.node()` (nombre de la máquina) + Base64. Ofuscación simple para evitar exposición accidental.
- **`helpers.py`**: Utilidades misceláneas. `human_type()` simula tipeo humano con demoras aleatorias para evitar detección anti-bot.
- **`scan_lobby_ids.py`**: Herramienta de desarrollo. Abre Chrome, hace login y lista los IDs y títulos de todos los tiles del lobby. Útil para recalibrar cuando Pragmatic Play cambia la estructura HTML.
- **`debug_logger.py`**: Framework centralizado de logging. Gestiona salidas a consola, escritura en `.log`, capturas de pantalla automáticas en fallos, y generación de reportes HTML/crash para diagnóstico forense.

#### 🌐 Web Dashboard: `bot_ruleta/dashboard/`

- **`app.py`**: Backend Flask (puerto 5050). Endpoints REST:
  - `GET /api/overview`: Resumen global de todas las mesas. Incluye delays de tercios, rachas de color, **delays de números individuales** y conteo de alertas. Devuelve `number_delay_threshold` para que el frontend sepa el umbral configurado.
  - `GET /api/data?mesa=...`: Detalle de una mesa específica. Devuelve últimos 20 giros, delays de tercios, racha de color, **delays de números (dict completo 0-36)** y top 5 números retrasados.
  - `GET /api/backtest?mesa=...`: Historial de señales de tercios completadas.
  - `GET /api/backtest_color?mesa=...`: Historial de rachas de color completadas.
  - `GET /api/backtest_number?mesa=...`: **Nuevo.** Historial de retrasos de números individuales completados.
  - `GET /api/analisis_global`: Datos cruzados de TODO el historial (tercios, colores, **números**). Sincroniza todas las mesas antes de responder.
  - `GET /api/signal_detail?mesa=&start=&end=&pico=`: Devuelve las jugadas individuales que componen una señal específica (útil para el modal de detalle).
  - `GET /api/tunnel`: Lee `data/tunnel.txt` y devuelve la URL pública de Cloudflare.
  - `GET /api/mesas`: Lista de mesas disponibles.
- **`static/index.html`**: Vista global (Overview). Muestra tarjetas de todas las mesas con delays de tercios, badges compactos de alertas (🔴N, 🔢N, 🔴N), historial miniatura y botones para cambiar a vista lista/cuadrícula y filtrar "Solo Señales".
- **`static/app.js`**: Lógica del Overview. Hace polling cada 1 segundo a `/api/overview`, actualiza las tarjetas dinámicamente, maneja el filtro de señales con ordenamiento por timestamp de alerta, y reproduce sonido de alerta cuando aparecen nuevas señales.
- **`static/mesa.html`**: Vista de detalle de una mesa individual. Muestra:
  - Layout visual de docenas y columnas con barras de progreso.
  - Banner de racha de color (rojos/negros).
  - Tabs de backtesting: **Tercios**, **Rojos/Negros**, **Números**.
  - En el tab "Números": una **grilla visual tipo tablero de ruleta** con 37 celdas (0 + 3 filas de 12). Cada celda muestra el número y su delay actual. Los números retrasados se iluminan con colores de severidad (amarillo → naranja → rojo pulsante).
  - Tabla de historial de señales de números debajo de la grilla.
- **`static/mesa.js`**: Lógica de la vista de detalle. Polling cada 1 segundo, renderiza la grilla de números, actualiza barras de progreso, y carga historiales de backtest para los tres tabs.
- **`static/analisis.html`**: Vista de Análisis Global. Muestra:
  - Toggle de vistas: **Tercios**, **Rojos/Negros**, **Números**.
  - KPIs resumidos (total señales, pico promedio, pico máximo global).
  - Gráfico de líneas (Chart.js) con los top retrasos históricos según la vista seleccionada.
  - Tablas de top señales críticas y desglose por mesa.
  - Modal de detalle de señal al hacer click en una fila.
- **`static/analisis.js`**: Lógica del análisis global. Maneja los tres tabs, renderiza gráficos Chart.js, procesa datos históricos y abre el modal de detalle con las jugadas individuales de cada señal.
- **`static/style.css`**: Hoja de estilos unificada para todo el dashboard. Diseño dark-mode premium con variables CSS, animaciones de pulso, responsividad para móviles, y clases para badges de colores.

---

## 3. Flujo de Datos y Arquitectura

### Diagrama conceptual:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                  │
│  (Ejecutable .exe / Python directo)                             │
└──────────────┬────────────────────────────────┬───────────────────┘
               │                                │
    ┌──────────▼──────────┐          ┌──────────▼──────────┐
    │   GUI (gui_app.py)  │          │  Launcher/Run       │
    │   CustomTkinter     │          │  (launcher.py)      │
    └──────────┬──────────┘          └──────────┬──────────┘
               │                                │
               └──────────────┬─────────────────┘
                              │
               ┌──────────────▼──────────────────┐
               │     Scanner Principal             │
               │     (scanner.py)                  │
               │  while True:                      │
               │    1. Leer tiles del lobby        │
               │    2. Extraer números vía JS      │
               │    3. Guardar en SQLite (db.py)   │
               │    4. Calcular delays             │
               │    5. Si umbral superado:         │
               │       → Alerta Telegram           │
               │    6. Sincronizar backtest        │
               └──────────────┬────────────────────┘
                              │
               ┌──────────────▼──────────────────┐
               │     Base de Datos SQLite        │
               │     (ruleta.db)                 │
               │  • Giros por mesa               │
               │  • Historial tercios            │
               │  • Historial colores            │
               │  • Historial números            │
               │  • Estados de sync              │
               └──────────────┬────────────────────┘
                              │
               ┌──────────────▼──────────────────┐
               │     Dashboard Flask             │
               │     (dashboard/app.py) :5050    │
               │  REST API → frontend consume    │
               └──────────────┬────────────────────┘
                              │
               ┌──────────────▼──────────────────┐
               │     Cloudflare Tunnel           │
               │     (cloudflared)               │
               │  Exponer :5050 a internet       │
               └─────────────────────────────────┘
```

---

## 4. Tecnologías y Dependencias

| Capa | Tecnología | Versión |
|------|------------|---------|
| Lenguaje | Python | 3.9+ (testado en 3.14) |
| Scraping | Selenium + undetected-chromedriver | 4.44.0 / 3.5.5 |
| Backend Web | Flask (dev) + Waitress (prod) | 3.1.3 / 3.0.2 |
| Base de Datos | SQLite3 (nativo Python) | - |
| GUI Escritorio | CustomTkinter + Pillow | 5.2.2 / 12.2.0 |
| Notificaciones | Telegram Bot API (requests) | 2.34.2 |
| Empaquetado | PyInstaller | 6.20.0 |
| Túnel/Proxy | Cloudflared (binario externo) | - |
| Frontend Web | HTML5, CSS3, JavaScript vanilla + Chart.js | - |
| Otros | Win32 API (ctypes), colorama | - |

### Dependencias Python (`requirements.txt`)
```
selenium
undetected-chromedriver
flask
waitress
customtkinter
Pillow
requests
pyinstaller
colorama
setuptools
```

---

## 5. Configuración y Credenciales

### GUI LoginScreen (Sliders)
| Parámetro | Rango | Default | Descripción |
|-----------|-------|---------|-------------|
| Tercios | 5-25 | 12 | Giros sin salir de una docena/columna para alertar |
| Color | 3-15 | 5 | Rojos/negros consecutivos para alertar |
| Números | 20-150 | 50 | Giros sin salir de un número individual para alertar |

### Archivo `.env` (formato soportado)
```
STAKE_EMAIL=tu_email@stake.com
STAKE_PASSWORD=TuPassword
TELEGRAM_TOKEN=123456789:ABC...
TELEGRAM_CHAT_ID=00000000
ALERT_THRESHOLD=12
HEADLESS=true
COLOR_STREAK_THRESHOLD=5
NUMBER_DELAY_THRESHOLD=50
CLOUDFLARE_TOKEN=tu_token_jwt
CLOUDFLARE_DOMAIN=botstake.shop
USE_RANDOM_TUNNEL=true
```

### GUI Saved Credentials
- Guardado en `backend/data/credentials.dat`.
- Ofuscado con XOR + Base64, clave derivada del nombre de la máquina.
- Incluye email, password, token Telegram, chat ID, umbrales de los tres sliders, headless y diagnósticos.

---

## 6. Seguridad y Advertencias

- **Credenciales en `.env`**: El archivo `.env` existe en la raíz del proyecto pero está protegido por `.gitignore`. Nunca lo subas a GitHub.
- **Automatización de casino**: Este bot interactúa automatizadamente con Stake, lo cual puede violar sus Términos de Servicio. Existe riesgo de ban permanente o confiscación de fondos. Úsalo bajo tu propia responsabilidad.
- **Tokens expuestos**: `github_token.txt` y el `.env` contienen secretos en texto plano local. Mantén el repo en privado y protege el acceso al PC servidor.

---

## 7. Cómo Compilar

Para generar el `.exe` para distribución o pruebas:

```bash
# Desde la raíz del proyecto, con el venv activado
python scripts/build_exe.py
```

El ejecutable resultante estará en:
```
dist/RouletteSniperPro.exe
```

Para publicar una nueva versión (requiere `github_token.txt`):
```bash
python publish.py v3.0.4
```

---

## 8. Actualizaciones Recientes (Changelog)

- **v3.x**: Agregada lógica de **números individuales** con grilla visual en el dashboard, alertas Telegram consolidadas, backtesting histórico y análisis global con tercer tab.
- **v3.x**: Rediseño compacto de la pantalla de login para acomodar tres sliders sin perder visibilidad del botón.
- **v3.x**: Badges de alerta en overview ultra-compactos para no romper la vista de cuadrícula.
- **v3.x**: Fix en el cálculo de delays de números para evitar valores congelados incorrectos.

---

*Documentación generada para Roulette Sniper Pro. Última actualización: Junio 2026.*
