# Graph Report - Bot_Stake_Recolector  (2026-06-07)

## Corpus Check
- 43 files · ~22,277 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 456 nodes · 867 edges · 20 communities (17 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8876d31e`
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
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 21|Community 21]]

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
- `get_logger()` --references--> `Logger`  [EXTRACTED]
  bot_ruleta/debug_logger.py → bot_ruleta/diagnostics/logger.py
- `run_bot()` --calls--> `run_diagnostics()`  [INFERRED]
  bot_ruleta/scanner.py → bot_ruleta/diagnostics/system_info.py
- `audit_table()` --calls--> `compute_number_delays()`  [EXTRACTED]
  verify_number_delays.py → bot_ruleta/logic.py

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (20 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (77): bool, Configuración centralizada del bot de ruleta. Constantes, configuración de mesa, capture_screenshot(), generate_crash_report(), get_logger(), Sistema de Diagnóstico Forense — re-exportador. La implementación está en el pa, Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., Toma un screenshot del navegador y opcionalmente guarda el HTML source.      Arg (+69 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (35): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py p, Sincroniza eventos de retraso de docenas y columnas., Motor de sincronizacion incremental compartido por todos los backtests.      Man, Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de numeros individuales (0-36). (+27 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (11): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Handler que envía logs a una Queue para que la GUI los lea., DashboardScreen, LoadingScreen, LoginScreen, PrerequisitesScreen (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (42): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), get_cf_env_vars(), Hilo permanente que mantiene cloudflared vivo y captura URLs nuevos.     Si clou, Lee la salida del bot y actualiza la consola minimalista, Dibuja la consola limpia y minimalista, Retorna el token y dominio de Cloudflare. Si DEV_MODE es True, devuelve None. (+34 more)

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
Cohesion: 0.09
Nodes (10): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest() (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.26
Nodes (11): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color(), get_connection(), main(), manual_delays() (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (24): _cleanup_old_crash_reports(), _cleanup_old_screenshots(), Mantiene solo los últimos N screenshots para no llenar el disco., Mantiene solo los últimos N crash reports., int, str, str, int (+16 more)

### Community 19 - "Community 19"
Cohesion: 0.12
Nodes (21): get_connection(), guardar_resultado(), init_db(), limpiar_mesa(), obtener_ultimo_numero(), obtener_ultimos_numeros(), Manejo de base de datos SQLite con tablas separadas por juego., Guarda un resultado en la tabla espec├¡fica del juego. (+13 more)

### Community 21 - "Community 21"
Cohesion: 0.07
Nodes (15): UpdateScreen, check_for_updates(), _cleanup_old_versions(), _get_download_url(), perform_update(), Genera la URL de descarga para una versión específica., Checks GitHub for updates in a background thread.     Calls callback(new_versio, Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas). (+7 more)

## Knowledge Gaps
- **15 isolated node(s):** `plugin`, `globalData`, `alertTimestamps`, `cachedTables`, `urlParams` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_BacktestSyncEngine` connect `Community 9` to `Community 3`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `DashboardScreen` connect `Community 21` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `get_connection()` connect `Community 19` to `Community 1`, `Community 3`, `Community 9`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `plugin`, `Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py p`, `Motor de sincronizacion incremental compartido por todos los backtests.      Man` to the rest of the system?**
  _125 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.051590483827853514 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05673076923076923 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08199643493761141 - nodes in this community are weakly interconnected._