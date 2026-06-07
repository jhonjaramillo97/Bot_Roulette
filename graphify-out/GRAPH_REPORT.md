# Graph Report - Bot_Stake_Recolector  (2026-06-07)

## Corpus Check
- 40 files · ~22,274 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 405 nodes · 765 edges · 21 communities (17 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `07ce5482`
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
- [[_COMMUNITY_Community 21|Community 21]]

## God Nodes (most connected - your core abstractions)
1. `_run_single_session()` - 18 edges
2. `_BacktestSyncEngine` - 16 edges
3. `ir_al_lobby()` - 15 edges
4. `get_logger()` - 15 edges
5. `capture_screenshot()` - 15 edges
6. `capture_screenshot()` - 14 edges
7. `DashboardScreen` - 14 edges
8. `send_telegram_msg()` - 13 edges
9. `get_logger()` - 12 edges
10. `LoginScreen` - 12 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  verify_number_delays.py → bot_ruleta/thresholds.py
- `get_logger()` --references--> `Logger`  [EXTRACTED]
  bot_ruleta/debug_logger.py → bot_ruleta/diagnostics/logger.py
- `login_stake()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/driver.py → bot_ruleta/diagnostics/screenshots.py
- `switch_to_game_iframe()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/iframe.py → bot_ruleta/diagnostics/screenshots.py
- `ir_al_lobby()` --calls--> `capture_screenshot()`  [INFERRED]
  bot_ruleta/lobby.py → bot_ruleta/diagnostics/screenshots.py

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (21 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (75): Configuración centralizada del bot de ruleta. Constantes, configuración de mesa, guardar_resultado(), init_db(), obtener_ultimo_numero(), Manejo de base de datos SQLite con tablas separadas por juego., Guarda un resultado en la tabla específica del juego., Obtiene el último número registrado en la tabla del juego., Inicializa la base de datos creando las tablas configuradas. (+67 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (23): get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de confi, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env, Lee el umbral de retraso de números individuales. Prioridad: runtime overrides >, calcular_delays(), get_analisis_global(), get_backtest() (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (8): DashboardScreen, LoadingScreen, LoginScreen, PrerequisitesScreen, Resuelve rutas de archivos empaquetados (PyInstaller) o de desarrollo., resource_path(), RouletteApp, UpdateScreen

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (29): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), get_cf_env_vars(), Hilo permanente que mantiene cloudflared vivo y captura URLs nuevos.     Si clou, Lee la salida del bot y actualiza la consola minimalista, Dibuja la consola limpia y minimalista, Retorna el token y dominio de Cloudflare. Si DEV_MODE es True, devuelve None. (+21 more)

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
Nodes (13): get_connection(), Retorna una conexión a la base de datos., _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos. (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (10): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color(), get_connection(), main(), manual_delays(), verify_number_delays.py — Auditoria de la base de datos.  Para cada mesa: 1. Cue (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (27): bool, _cleanup_old_screenshots(), Mantiene solo los últimos N screenshots para no llenar el disco., int, str, str, int, str (+19 more)

### Community 19 - "Community 19"
Cohesion: 0.10
Nodes (21): limpiar_mesa(), obtener_ultimos_numeros(), Obtiene los últimos N registros (número, color y timestamp). Si limit es None, o, Resuelve el nombre de tabla SQLite a partir del nombre descriptivo., Resuelve el nombre de tabla SQLite a partir del nombre descriptivo., Elimina todos los registros de la tabla de una mesa específica.      Usado cuand, Elimina todos los registros de la tabla de una mesa específica.      Usado cuand, _resolve_table_name() (+13 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (14): check_for_updates(), _cleanup_old_versions(), _get_download_url(), perform_update(), Genera la URL de descarga para una versión específica., Checks GitHub for updates in a background thread.     Calls callback(new_versio, Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas)., Downloads the new versioned executable and spawns a bat file to replace the curr (+6 more)

## Knowledge Gaps
- **15 isolated node(s):** `plugin`, `globalData`, `alertTimestamps`, `cachedTables`, `urlParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_BacktestSyncEngine` connect `Community 9` to `Community 3`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `DashboardScreen` connect `Community 21` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `DashboardScreen` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `plugin`, `Script para empaquetar Roulette Sniper Pro en un solo .exe Requiere: pip install`, `Configuración centralizada del bot de ruleta. Constantes, configuración de mesa` to the rest of the system?**
  _111 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05041797283176593 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.12807881773399016 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.09655172413793103 - nodes in this community are weakly interconnected._