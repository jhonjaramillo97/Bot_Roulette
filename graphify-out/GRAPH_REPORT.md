# Graph Report - Bot_Stake_Recolector  (2026-06-06)

## Corpus Check
- 26 files · ~23,550 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 271 nodes · 505 edges · 17 communities (14 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8b9e6c87`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 16|Community 16]]

## God Nodes (most connected - your core abstractions)
1. `load_credentials()` - 19 edges
2. `get_logger()` - 15 edges
3. `capture_screenshot()` - 15 edges
4. `_run_single_session()` - 14 edges
5. `ir_al_lobby()` - 12 edges
6. `get_connection()` - 11 edges
7. `send_telegram_msg()` - 10 edges
8. `generate_crash_report()` - 10 edges
9. `DashboardScreen` - 10 edges
10. `get_color_streak_threshold()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `audit_table()` --calls--> `compute_number_delays()`  [EXTRACTED]
  verify_number_delays.py → bot_ruleta/logic.py
- `run_bot()` --calls--> `init_db()`  [EXTRACTED]
  bot_ruleta/scanner.py → bot_ruleta/db.py
- `_run_single_session()` --calls--> `obtener_ultimos_numeros()`  [EXTRACTED]
  bot_ruleta/scanner.py → bot_ruleta/db.py
- `run_diagnostics()` --calls--> `load_credentials()`  [EXTRACTED]
  bot_ruleta/debug_logger.py → bot_ruleta/config.py
- `_send_crash_report_telegram()` --calls--> `load_credentials()`  [EXTRACTED]
  bot_ruleta/debug_logger.py → bot_ruleta/config.py

## Import Cycles
- None detected.

## Communities (17 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (55): guardar_resultado(), Guarda un resultado en la tabla específica del juego., capture_screenshot(), _cleanup_old_crash_reports(), _cleanup_old_screenshots(), generate_crash_report(), get_logger(), Sistema de Diagnóstico Forense para el Bot de Ruleta. Centraliza logging, captur (+47 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (35): get_color_streak_threshold(), get_number_delay_threshold(), load_credentials(), Configuración centralizada del bot de ruleta. Constantes, configuración de mesas, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env, Lee el umbral de retraso de números individuales. Prioridad: runtime overrides >, Lee credenciales. Prioridad: runtime overrides > .env, check_and_notify() (+27 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (12): bool, Permite a la GUI inyectar credenciales sin modificar .env.     Uso: set_runtime_, set_runtime_config(), Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., set_diagnostics(), DashboardScreen, LoadingScreen, LoginScreen (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (24): UpdateScreen, clear_screen(), cloudflared_watchdog(), get_cf_env_vars(), Hilo permanente que mantiene cloudflared vivo y captura URLs nuevos.     Si clou, Lee la salida del bot y actualiza la consola minimalista, Dibuja la consola limpia y minimalista, Retorna el token y dominio de Cloudflare. Si DEV_MODE es True, devuelve None. (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (19): get_connection(), init_db(), limpiar_mesa(), obtener_ultimo_numero(), obtener_ultimos_numeros(), Manejo de base de datos SQLite con tablas separadas por juego., Obtiene el último número registrado en la tabla del juego., Obtiene los últimos N registros (número, color y timestamp). (+11 more)

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
Cohesion: 0.33
Nodes (4): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Handler que envía logs a una Queue para que la GUI los lea.

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (9): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     numer, audit_table(), format_color(), get_connection(), main(), manual_delays(), verify_number_delays.py — Auditoría de la base de datos.  Para cada mesa: 1. Cue (+1 more)

## Knowledge Gaps
- **11 isolated node(s):** `globalData`, `urlParams`, `tableSelect`, `statusDot`, `soundBtn` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_credentials()` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `DashboardScreen` connect `Community 2` to `Community 3`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `get_logger()` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `Lee el threshold de los datos guardados por la GUI. Fallback al .env`, `Calcula los delays de docenas y columnas para una tabla dada (USANDO LOGIC COMPA`, `Retorna un resumen rápido de TODAS las mesas: delay máximo y alertas.` to the rest of the system?**
  _85 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06861239119303636 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08826945412311266 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08522727272727272 - nodes in this community are weakly interconnected._