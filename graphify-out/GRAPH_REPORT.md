# Graph Report - Bot_Stake_Recolector  (2026-06-10)

## Corpus Check
- 89 files · ~46,563 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2246 nodes · 5074 edges · 122 communities (102 shown, 20 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 242 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `003f242b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 135|Community 135]]
- [[_COMMUNITY_Community 151|Community 151]]
- [[_COMMUNITY_Community 152|Community 152]]
- [[_COMMUNITY_Community 153|Community 153]]
- [[_COMMUNITY_Community 157|Community 157]]
- [[_COMMUNITY_Community 159|Community 159]]
- [[_COMMUNITY_Community 235|Community 235]]
- [[_COMMUNITY_Community 236|Community 236]]
- [[_COMMUNITY_Community 252|Community 252]]
- [[_COMMUNITY_Community 290|Community 290]]
- [[_COMMUNITY_Community 308|Community 308]]
- [[_COMMUNITY_Community 319|Community 319]]
- [[_COMMUNITY_Community 322|Community 322]]
- [[_COMMUNITY_Community 340|Community 340]]

## God Nodes (most connected - your core abstractions)
1. `_()` - 588 edges
2. `$()` - 387 edges
3. `_()` - 142 edges
4. `getOwnPropertyDescriptor()` - 75 edges
5. `defineProperty()` - 72 edges
6. `a()` - 61 edges
7. `pc()` - 40 edges
8. `r()` - 30 edges
9. `get()` - 28 edges
10. `l()` - 27 edges

## Surprising Connections (you probably didn't know these)
- `fetchJSON()` --calls--> `fetch()`  [INFERRED]
  frontend/src/lib/api.ts → backend/dashboard/static/assets/query-BPe0xBFE.js
- `_handle_error()` --calls--> `generate_crash_report()`  [INFERRED]
  bot_ruleta/scanner.py → backend/diagnostics/crash_report.py
- `go_to_lobby()` --calls--> `Exception`  [INFERRED]
  bot_ruleta/lobby.py → backend/diagnostics/crash_report.py
- `login_stake()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/driver.py → backend/diagnostics/screenshots.py
- `switch_to_game_iframe()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/iframe.py → backend/diagnostics/screenshots.py

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (122 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (39): Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest(), Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest() (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (54): ah(), ap(), bh(), bm(), ch(), clamp(), cp(), cv() (+46 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (24): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (22): int, str, Guarda un resultado en la tabla especifica del juego., save_result(), clear_table(), get_connection(), get_last_number(), get_last_numbers() (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (18): close_modals(), Manejo de contexto iframe y cierre de modales/popups., Intenta cambiar al iframe donde vive el lobby/juego (incluyendo anidados). Retor, Intenta cerrar modales/popups que bloquean la vista (dentro del iframe)., switch_to_game_iframe(), check_session_alive(), _click_juego_real(), go_to_lobby() (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (4): build(), build_react_dashboard(), Script para empaquetar Roulette Sniper Pro en un solo .exe Requiere: pip instal, Compila el dashboard React y copia los archivos a Flask static.

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (28): aA(), ak(), dk(), Du(), ea(), Ek(), fk(), g() (+20 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (10): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest() (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (20): bp(), dm(), fm(), Gm(), gp(), hm(), hp(), Im() (+12 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (14): compute_color_streak(), Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, compute_color_streak(), Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Tests unitarios para los algoritmos de analytics:   - compute_delays   - compu, El verde (0) suma a la racha sin romperla. (+6 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (36): str, str, capture_screenshot(), get_chrome_major_version(), _hide_chrome_window(), login_stake(), Configuración y creación del WebDriver + flujo de login., Oculta la ventana de Chrome de la barra de tareas y la mueve fuera de la pantall (+28 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (4): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 20 - "Community 20"
Cohesion: 0.16
Nodes (17): cleanup(), cleanup(), get_base_dir(), get_data_dir(), is_frozen(), Resolucion centralizada de rutas para desarrollo y PyInstaller. Elimina el patr, Directorio raiz del ejecutable (frozen) o del source (dev)., Directorio data/ para BD, credenciales, logs. (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (42): $(), ao(), bn(), ce(), cs(), ds(), Er(), fc() (+34 more)

### Community 22 - "Community 22"
Cohesion: 0.08
Nodes (67): a(), aa(), Ac(), af(), as(), bc(), be(), bi() (+59 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (41): Au(), bd(), bu(), cd(), cp(), ct(), Cu(), Eu() (+33 more)

### Community 24 - "Community 24"
Cohesion: 0.04
Nodes (81): at(), bC(), bd(), bj(), bO(), bu(), ce(), cj() (+73 more)

### Community 26 - "Community 26"
Cohesion: 0.18
Nodes (10): Any, _cleanup_driver(), _handle_error(), Any, Distingue sesión expirada de error real y genera crash report si aplica., Cierra el navegador de forma segura., Loop supervisor que asegura que el bot se reinicie si falla.          Args:, Orquestador: inicializa, escanea y maneja errores de una sesion. (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.08
Nodes (47): Ae(), an(), Bt(), cn(), de(), Ee(), en(), fd() (+39 more)

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (39): ai(), ci(), dd(), di(), es(), fi(), Fu(), hi() (+31 more)

### Community 29 - "Community 29"
Cohesion: 0.08
Nodes (25): bx(), cg(), cx(), eg(), gt(), Hd(), iO(), iy() (+17 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (13): divide(), dw(), ew(), fw(), kw(), multiply(), nw(), Ow() (+5 more)

### Community 31 - "Community 31"
Cohesion: 0.09
Nodes (27): int, str, str, int, str, Any, bool, int (+19 more)

### Community 32 - "Community 32"
Cohesion: 0.22
Nodes (11): b(), ec(), Ha(), Hd(), ie(), le(), r(), re() (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.09
Nodes (34): ap(), bs(), d(), dn(), dp(), Ed(), ep(), Et() (+26 more)

### Community 34 - "Community 34"
Cohesion: 0.11
Nodes (28): cl(), dl(), el(), fl(), gl(), Il(), kl(), Ll() (+20 more)

### Community 35 - "Community 35"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 36 - "Community 36"
Cohesion: 0.01
Nodes (57): Yo(), _(), ae(), An(), Ao(), bezierCurveTo(), bl(), bw() (+49 more)

### Community 37 - "Community 37"
Cohesion: 0.16
Nodes (19): bl(), df(), ef(), gf(), Hf(), hl(), If(), jf() (+11 more)

### Community 38 - "Community 38"
Cohesion: 0.17
Nodes (9): perform_update(), Downloads the new versioned executable and spawns a bat file to replace the curr, UpdateScreen, _cleanup_old_versions(), _get_download_url(), perform_update(), Genera la URL de descarga para una versión específica., Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas). (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.25
Nodes (4): COLUMN_ZONES, DOZEN_ZONES, ROULETTE_LAYOUT, TABLE_NAMES

### Community 40 - "Community 40"
Cohesion: 0.15
Nodes (12): AnalisisGlobalPage(), AnalysisTab, fmt(), SignalModal(), TABLE_NAMES, useAnalisisGlobal(), useSignalDetail(), AnalisisGlobalPage() (+4 more)

### Community 41 - "Community 41"
Cohesion: 0.10
Nodes (29): str, _chain_match(), _chain_match_and_save(), _check_session_expiry(), _cleanup_driver(), extract_nums_js(), _get_color(), _handle_error() (+21 more)

### Community 42 - "Community 42"
Cohesion: 0.07
Nodes (22): _client(), Tests para el dashboard React: middleware de token, rutas SPA y endpoints API., Endpoints de la API REST., Endpoint SSE para streaming en tiempo real., Restaurar el token después de cada test., Formato de respuesta del middleware de autenticación., Endpoint SSE para streaming en tiempo real., Configura SQLite en memoria para todos los tests. (+14 more)

### Community 43 - "Community 43"
Cohesion: 0.10
Nodes (20): clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui(), track_bot() (+12 more)

### Community 44 - "Community 44"
Cohesion: 0.15
Nodes (27): ad(), Ai(), cc(), dc(), delete(), deleteProperty(), fc(), fd() (+19 more)

### Community 45 - "Community 45"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 46 - "Community 46"
Cohesion: 0.38
Nodes (10): MesaPopup(), useBacktest(), useBacktestColor(), useBacktestNumber(), useMesaData(), useMesas(), formatTimeAgo(), MesaDetailPage() (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.16
Nodes (19): clear_table(), get_connection(), get_last_number(), get_last_numbers(), init_db(), int, str, Manejo de base de datos SQLite con tablas separadas por juego. (+11 more)

### Community 48 - "Community 48"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.17
Nodes (4): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 50 - "Community 50"
Cohesion: 0.17
Nodes (14): Configuracion centralizada del bot de ruleta. Constantes, configuracion de mesa, get_chrome_major_version(), _hide_chrome_window(), login_stake(), Configuración y creación del WebDriver + flujo de login., Oculta la ventana de Chrome de la barra de tareas y la mueve fuera de la pantall, Detecta la versión principal de Chrome instalada para evitar mismatch., Navega al lobby y ejecuta el flujo de login. (+6 more)

### Community 52 - "Community 52"
Cohesion: 0.15
Nodes (16): api, fetchJSON(), BacktestSignal, BacktestTab, ColorStreak, ColorStreakSignal, GlobalAnalysisData, LastSpin (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 54 - "Community 54"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 55 - "Community 55"
Cohesion: 0.23
Nodes (9): Valida que un nombre de tabla sea seguro y exista en la configuracion.     Lanz, validate_table_name(), get_signal_detail(), _get_validated_table(), Valida el parametro 'mesa' de un request.     Retorna el table_name validado o, Devuelve las jugadas individuales que componen una senal especifica., Valida que un nombre de tabla sea seguro y exista en la configuracion.     Lanz, validate_table_name() (+1 more)

### Community 56 - "Community 56"
Cohesion: 0.13
Nodes (15): addAngleAxis(), addRadiusAxis(), aS(), cS(), getPrototypeOf(), js(), lO(), os() (+7 more)

### Community 58 - "Community 58"
Cohesion: 0.29
Nodes (11): Any, int, str, check_and_notify(), check_and_notify_color(), check_and_notify_number(), compute_delays(), Calcula los delays de docenas y columnas dado una lista de números o diccionario (+3 more)

### Community 59 - "Community 59"
Cohesion: 0.40
Nodes (5): il(), nl(), rl(), tl(), zl()

### Community 60 - "Community 60"
Cohesion: 0.40
Nodes (4): DashboardContext, DashboardProvider(), DashboardState, Thresholds

### Community 61 - "Community 61"
Cohesion: 0.13
Nodes (5): DashboardScreen, LoadingScreen, Resuelve rutas de archivos empaquetados (PyInstaller) o de desarrollo., resource_path(), RouletteApp

### Community 62 - "Community 62"
Cohesion: 0.11
Nodes (26): ac(), add(), Bs(), clear(), concat(), Fs(), gc(), hc() (+18 more)

### Community 63 - "Community 63"
Cohesion: 0.29
Nodes (6): extract_numero(), Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, extract_numero(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, TestExtractNumero

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Badge, BadgeProps, badgeVariants, Button, ButtonProps, buttonVariants, Card, CardContent (+3 more)

### Community 65 - "Community 65"
Cohesion: 0.27
Nodes (11): at(), componentDidCatch(), ic(), qu(), rc(), st(), tc(), Ti() (+3 more)

### Community 66 - "Community 66"
Cohesion: 0.22
Nodes (8): check_for_updates(), _cleanup_old_versions(), _get_download_url(), Genera la URL de descarga para una versión específica., Checks GitHub for updates in a background thread.     Calls callback(new_versio, Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas)., check_for_updates(), Checks GitHub for updates in a background thread.     Calls callback(new_versio

### Community 68 - "Community 68"
Cohesion: 0.15
Nodes (17): _chain_match(), _chain_match_and_save(), extract_nums_js(), _get_color(), str, Loop principal del bot: escaneo de tiles, extracción y guardado de datos. Inclu, AudioContext silencioso para evitar que Chrome suspenda la página., Escanea todas las mesas mapeadas. Retorna cuantas tuvieron exito. (+9 more)

### Community 69 - "Community 69"
Cohesion: 0.28
Nodes (9): _check_session_expiry(), _handle_zero_tiles(), Loop infinito de escaneo de tiles., Simula movimiento de mouse JS para evitar desconexión de Pragmatic., Maneja ciclos sin tiles: chequeo de expiración, soft refresh, fallo crítico., Detecta si la sesión expiró por inactividad., _scan_loop(), _simulate_mouse_move() (+1 more)

### Community 70 - "Community 70"
Cohesion: 0.25
Nodes (4): COLUMN_ZONES, DOZEN_ZONES, ROULETTE_LAYOUT, TABLE_NAMES

### Community 71 - "Community 71"
Cohesion: 0.33
Nodes (3): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, PrerequisitesScreen, UpdateScreen

### Community 85 - "Community 85"
Cohesion: 0.22
Nodes (8): nums_to_emoji(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, nums_to_emoji(), Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, Tests para logic_helpers.py y helpers.py: utilidades compartidas., TestKeycapMap, TestNumsToEmoji

### Community 86 - "Community 86"
Cohesion: 0.29
Nodes (8): ei(), fetch(), invalidate(), #l(), re(), reset(), setData(), setState()

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (19): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color() (+11 more)

### Community 88 - "Community 88"
Cohesion: 0.16
Nodes (15): check_and_notify(), check_and_notify_color(), check_and_notify_number(), Any, int, str, Si la racha de color supera el umbral, envía notificación a Telegram.     Usa c, Si la racha de color supera el umbral, envía notificación a Telegram.     Usa c (+7 more)

### Community 89 - "Community 89"
Cohesion: 0.18
Nodes (6): Sin historial en DB, todos los numeros del tile son nuevos., Los ultimos 4 del tile coinciden con la DB., Solo 2 coinciden, necesita _MIN_CHAIN=4., Todos los numeros del tile ya estan en la DB., El empalme comienza en el indice 0 del tile (todos nuevos desde ahi)., TestChainMatch

### Community 91 - "Community 91"
Cohesion: 0.14
Nodes (7): Sincroniza eventos de retraso de docenas y columnas., _ZoneBacktestSync, Sincroniza eventos de retraso de docenas y columnas., _ZoneBacktestSync, Tests para backtest.py: motores de sincronizacion incremental. Usa SQLite en me, Un gap de mas de 30 minutos entre filas debe romper la cadena y reiniciar delays, TestBacktestSync

### Community 92 - "Community 92"
Cohesion: 0.14
Nodes (13): Envia mensaje raw a Telegram., Envia mensaje raw a Telegram., send_telegram_msg(), get_cf_env_vars(), Retorna (token, dominio) de Cloudflare.     Prioridad: CLOUDFLARE_TOKEN env > t, Cliente de Telegram Bot API. Extraido de logic.py para separar el envio de mens, Envia mensaje raw a Telegram., send_telegram_msg() (+5 more)

### Community 135 - "Community 135"
Cohesion: 0.06
Nodes (20): _(), A(), defaultMutationOptions(), fetchInfiniteQuery(), findAll(), getMutationDefaults(), getObserversCount(), getQueriesData() (+12 more)

### Community 151 - "Community 151"
Cohesion: 0.14
Nodes (19): C(), createResult(), h(), hasListeners(), j(), k(), mount(), onQueryUpdate() (+11 more)

### Community 152 - "Community 152"
Cohesion: 0.21
Nodes (18): build(), clearInterval(), defaultQueryOptions(), ensureInfiniteQueryData(), ensureQueryData(), fetchOptimistic(), fetchQuery(), get() (+10 more)

### Community 153 - "Community 153"
Cohesion: 0.16
Nodes (17): add(), addObserver(), b(), cancel(), clearGcTimeout(), clearTimeout(), destroy(), g() (+9 more)

### Community 157 - "Community 157"
Cohesion: 0.25
Nodes (11): canRun(), continue(), execute(), find(), getAll(), isFocused(), onFocus(), onOnline() (+3 more)

### Community 159 - "Community 159"
Cohesion: 0.38
Nodes (7): D(), E(), N(), O(), P(), S(), T()

### Community 235 - "Community 235"
Cohesion: 0.11
Nodes (35): Ar(), cr(), dr(), Hr(), kr(), Or(), sr(), vr() (+27 more)

### Community 236 - "Community 236"
Cohesion: 0.07
Nodes (29): Ze(), be(), ds(), ec(), Eo(), F(), Fb(), Gn() (+21 more)

### Community 252 - "Community 252"
Cohesion: 0.10
Nodes (46): w(), A(), am(), b(), c(), cancel(), cm(), d() (+38 more)

### Community 290 - "Community 290"
Cohesion: 0.26
Nodes (9): useAlertSound(), useLocalStorage(), useOverview(), AppHeader(), TableFilterDropdown(), ThresholdDropdown(), useDashboard(), OverviewPage() (+1 more)

### Community 308 - "Community 308"
Cohesion: 0.20
Nodes (3): clsx(), cn(), ZONE_LABELS

### Community 319 - "Community 319"
Cohesion: 0.15
Nodes (11): compute_delays(), Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Caso normal: cada numero cae en su docena y columna correcta.         La logica, Si todas las zonas ya salieron, los delays son las distancias al mas reciente., El marcador -1 detiene el conteo de delays., Los ceros (0) incrementan todos los delays sin romper la busqueda.         Con (+3 more)

### Community 340 - "Community 340"
Cohesion: 0.20
Nodes (11): bindMethods(), ce(), constructor(), getCurrentResult(), getDefaultOptions(), getOptimisticResult(), getQueryCache(), I() (+3 more)

## Knowledge Gaps
- **219 isolated node(s):** `int`, `str`, `Logger`, `str`, `int` (+214 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_()` connect `Community 36` to `Community 2`, `Community 135`, `Community 8`, `Community 235`, `Community 44`, `Community 28`, `Community 236`, `Community 15`, `Community 21`, `Community 22`, `Community 30`, `Community 56`, `Community 24`, `Community 59`, `Community 252`, `Community 29`, `Community 62`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 21` to `Community 135`, `Community 22`, `Community 23`, `Community 24`, `Community 27`, `Community 28`, `Community 159`, `Community 32`, `Community 33`, `Community 34`, `Community 36`, `Community 37`, `Community 44`, `Community 65`, `Community 340`, `Community 86`, `Community 235`, `Community 236`, `Community 252`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `_()` connect `Community 135` to `Community 36`, `Community 340`, `Community 21`, `Community 86`, `Community 151`, `Community 152`, `Community 153`, `Community 28`, `Community 157`, `Community 159`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `$()` (e.g. with `dO()` and `So()`) actually correct?**
  _`$()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Lee el threshold de los datos guardados por la GUI. Fallback al .env`, `Valida el parametro 'mesa' de un request.     Retorna el table_name validado o`, `Calcula los delays de docenas y columnas para una tabla dada (USANDO LOGIC COMPA` to the rest of the system?**
  _460 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08880666049953746 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05520614954577219 - nodes in this community are weakly interconnected._