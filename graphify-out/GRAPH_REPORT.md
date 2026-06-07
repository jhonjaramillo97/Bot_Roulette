# Graph Report - Bot_Stake_Recolector  (2026-06-07)

## Corpus Check
- 45 files · ~22,010 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 467 nodes · 898 edges · 25 communities (22 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `57755ca9`
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
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 30|Community 30]]

## God Nodes (most connected - your core abstractions)
1. `_run_single_session()` - 18 edges
2. `_BacktestSyncEngine` - 16 edges
3. `_BacktestSyncEngine` - 16 edges
4. `ir_al_lobby()` - 15 edges
5. `get_logger()` - 15 edges
6. `capture_screenshot()` - 15 edges
7. `capture_screenshot()` - 14 edges
8. `DashboardScreen` - 14 edges
9. `get_connection()` - 13 edges
10. `send_telegram_msg()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  verify_number_delays.py → bot_ruleta/thresholds.py
- `_handle_error()` --calls--> `generate_crash_report()`  [INFERRED]
  bot_ruleta/scanner.py → bot_ruleta/diagnostics/crash_report.py
- `switch_to_game_iframe()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/iframe.py → bot_ruleta/diagnostics/screenshots.py
- `ir_al_lobby()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/lobby.py → bot_ruleta/diagnostics/screenshots.py
- `map_tables_dynamic()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/lobby.py → bot_ruleta/diagnostics/screenshots.py

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (25 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (18): Configuración centralizada del bot de ruleta. Constantes, configuración de mesa, cerrar_modales(), Manejo de contexto iframe y cierre de modales/popups., Intenta cambiar al iframe donde vive el lobby/juego (incluyendo anidados). Retor, Intenta cerrar modales/popups que bloquean la vista (dentro del iframe)., switch_to_game_iframe(), check_session_alive(), _click_juego_real() (+10 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (13): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py p, Sincroniza eventos de retraso de docenas y columnas., Motor de sincronizacion incremental compartido por todos los backtests.      Man, Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de numeros individuales (0-36). (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (13): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., Handler que envía logs a una Queue para que la GUI los lea., set_diagnostics(), DashboardScreen, LoadingScreen (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (46): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui() (+38 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (15): fetchBacktest(), fetchColorBacktest(), fetchNumberBacktest(), historyContainer, initAudio(), playAlertSound(), renderHistory(), renderNumberGrid() (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.20
Nodes (8): alertTimestamps, buildCards(), cachedTables, fetchOverview(), initAudio(), playAlertSound(), renderGrid(), updateCards()

### Community 7 - "Community 7"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (9): fetchGlobalData(), formatName(), globalData, openSignalDetail(), processAndRender(), renderCharts(), renderTableBreakdown(), setupGlobalTabs() (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (11): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest() (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.26
Nodes (11): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color(), get_connection(), main(), manual_delays() (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (28): guardar_resultado(), obtener_ultimos_numeros(), Guarda un resultado en la tabla espec├¡fica del juego., Obtiene los ├║ltimos N registros (n├║mero, color y timestamp). Si limit es None,, Ejecuta un diagnóstico completo del entorno y retorna el reporte como string., run_diagnostics(), _chain_match(), _chain_match_and_save() (+20 more)

### Community 18 - "Community 18"
Cohesion: 0.06
Nodes (39): limpiar_mesa(), obtener_ultimo_numero(), Manejo de base de datos SQLite con tablas separadas por juego., Obtiene el ├║ltimo n├║mero registrado en la tabla del juego., Resuelve el nombre de tabla SQLite a partir del nombre descriptivo., Elimina todos los registros de la tabla de una mesa espec├¡fica.      Usado cua, _resolve_table_name(), int (+31 more)

### Community 19 - "Community 19"
Cohesion: 0.12
Nodes (26): sync_backtest(), sync_color_backtest(), sync_number_backtest(), get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de confi, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env, Lee el umbral de retraso de números individuales. Prioridad: runtime overrides > (+18 more)

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (16): capture_screenshot(), _cleanup_old_crash_reports(), _cleanup_old_screenshots(), generate_crash_report(), get_logger(), Sistema de Diagnóstico Forense — re-exportador. La implementación está en el pa, Toma un screenshot del navegador y opcionalmente guarda el HTML source.      Arg, Mantiene solo los últimos N screenshots para no llenar el disco. (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.09
Nodes (8): check_for_updates(), Checks GitHub for updates in a background thread.     Calls callback(new_versio, DashboardScreen, LoadingScreen, LoginScreen, _resource_path(), PrerequisitesScreen, UpdateScreen

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (12): bool, str, login_stake(), Navega al lobby y ejecuta el flujo de login., human_type(), Funciones auxiliares puras: escritura simulada, persistencia CSV., Escribe texto con retardos aleatorios para simular humano., _initialize_session() (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.28
Nodes (9): _check_session_expiry(), _handle_zero_tiles(), Loop infinito de escaneo de tiles., Simula movimiento de mouse JS para evitar desconexión de Pragmatic., Maneja ciclos sin tiles: chequeo de expiración, soft refresh, fallo crítico., Detecta si la sesión expiró por inactividad., _scan_loop(), _simulate_mouse_move() (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (6): get_chrome_major_version(), _hide_chrome_window(), Oculta la ventana de Chrome de la barra de tareas y la mueve fuera de la pantall, Detecta la versión principal de Chrome instalada para evitar mismatch., Configura y retorna (driver, wait)., setup_driver()

## Knowledge Gaps
- **15 isolated node(s):** `plugin`, `globalData`, `alertTimestamps`, `cachedTables`, `urlParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_BacktestSyncEngine` connect `Community 9` to `Community 3`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `DashboardScreen` connect `Community 21` to `Community 17`, `Community 3`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `get_connection()` connect `Community 1` to `Community 17`, `Community 18`, `Community 3`, `Community 9`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `plugin`, `Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py p`, `Motor de sincronizacion incremental compartido por todos los backtests.      Man` to the rest of the system?**
  _130 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07681365576102418 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.07507507507507508 - nodes in this community are weakly interconnected._