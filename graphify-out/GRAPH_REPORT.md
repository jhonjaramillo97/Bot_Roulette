# Graph Report - Bot_Stake_Recolector  (2026-06-08)

## Corpus Check
- 82 files · ~64,273 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2955 nodes · 8216 edges · 101 communities (92 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 605 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d374f42b`
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
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]

## God Nodes (most connected - your core abstractions)
1. `_()` - 576 edges
2. `$()` - 381 edges
3. `$()` - 373 edges
4. `$()` - 373 edges
5. `$()` - 373 edges
6. `_()` - 141 edges
7. `defineProperty()` - 80 edges
8. `getOwnPropertyDescriptor()` - 77 edges
9. `a()` - 67 edges
10. `a()` - 61 edges

## Surprising Connections (you probably didn't know these)
- `MesaDetailPage()` --calls--> `cn()`  [INFERRED]
  react-dashboard/src/pages/MesaDetail.tsx → bot_ruleta/dashboard/static/assets/index-DzzgQmSc.js
- `OverviewPage()` --calls--> `cn()`  [INFERRED]
  react-dashboard/src/pages/Overview.tsx → bot_ruleta/dashboard/static/assets/index-DzzgQmSc.js
- `fetchJSON()` --calls--> `fetch()`  [INFERRED]
  react-dashboard/src/lib/api.ts → bot_ruleta/dashboard/static/assets/query-rRwWEUS_.js
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  scripts/verify_number_delays.py → bot_ruleta/thresholds.py
- `MesaDetailPage()` --calls--> `useBacktest()`  [INFERRED]
  react-dashboard/src/pages/MesaDetail.tsx → react-dashboard/src/hooks/useApi.ts

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (101 total, 9 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (34): Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest(), get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de conf, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (51): $(), ad(), ai(), bi(), ca(), componentDidCatch(), cr(), dr() (+43 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (32): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (15): fetchBacktest(), fetchColorBacktest(), fetchNumberBacktest(), historyContainer, initAudio(), playAlertSound(), renderHistory(), renderNumberGrid() (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.20
Nodes (8): alertTimestamps, buildCards(), cachedTables, fetchOverview(), initAudio(), playAlertSound(), renderGrid(), updateCards()

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (9): fetchGlobalData(), formatName(), globalData, openSignalDetail(), processAndRender(), renderCharts(), renderTableBreakdown(), setupGlobalTabs() (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (11): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.04
Nodes (68): $(), ad(), ae(), bd(), bi(), bs(), cd(), componentDidCatch() (+60 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (20): compute_color_streak(), Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, _chain_match(), Busca empalme de MIN_CHAIN números consecutivos entre tile y DB.     Retorna li, Tests unitarios para los algoritmos de analytics:   - compute_delays   - compu, El verde (0) suma a la racha sin romperla. (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.20
Nodes (10): _chain_match_and_save(), extract_nums_js(), _get_color(), str, Escanea una mesa. Retorna True si encontró números y los procesó., Chain matching robusto + guardado en DB. Retorna los números nuevos., Envía alertas de delay, color y números a Telegram., Extrae números visibles de un tile usando JavaScript (class-agnostic). (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.11
Nodes (8): _ColorBacktestSync, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de rachas de rojos/negros consecutivos., _ZoneBacktestSync, Tests para backtest.py: motores de sincronizacion incremental. Usa SQLite en me, TestBacktestSync

### Community 19 - "Community 19"
Cohesion: 0.01
Nodes (80): _(), aj(), Al(), ar(), arc(), BD(), bezierCurveTo(), Bs() (+72 more)

### Community 20 - "Community 20"
Cohesion: 0.09
Nodes (29): bool, int, str, str, int, str, cleanup(), get_base_dir() (+21 more)

### Community 21 - "Community 21"
Cohesion: 0.05
Nodes (24): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., Handler que envía logs a una Queue para que la GUI los lea., set_diagnostics(), DashboardScreen, LoadingScreen (+16 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (19): clear_table(), get_connection(), get_last_number(), get_last_numbers(), int, str, Guarda un resultado en la tabla especifica del juego., Obtiene el ultimo numero registrado en la tabla del juego. (+11 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (26): check_and_notify(), check_and_notify_color(), check_and_notify_number(), compute_delays(), Any, int, str, Calcula los delays de docenas y columnas dado una lista de números o diccionario (+18 more)

### Community 24 - "Community 24"
Cohesion: 0.10
Nodes (62): aa(), Ac(), ae(), ao(), bc(), be(), _c(), cc() (+54 more)

### Community 26 - "Community 26"
Cohesion: 0.05
Nodes (77): Any, Configuracion centralizada del bot de ruleta. Constantes, configuracion de mesa, init_db(), Manejo de base de datos SQLite con tablas separadas por juego., Inicializa la base de datos creando las tablas configuradas., capture_screenshot(), _cleanup_old_crash_reports(), _cleanup_old_screenshots() (+69 more)

### Community 27 - "Community 27"
Cohesion: 0.05
Nodes (46): $(), ad(), ae(), bd(), cd(), De(), dt(), Ee() (+38 more)

### Community 29 - "Community 29"
Cohesion: 0.07
Nodes (55): a(), ap(), as(), Au(), Bo(), ci(), ct(), Cu() (+47 more)

### Community 30 - "Community 30"
Cohesion: 0.07
Nodes (47): ae(), an(), bn(), Bt(), ce(), cn(), De(), dt() (+39 more)

### Community 31 - "Community 31"
Cohesion: 0.07
Nodes (55): a(), ap(), as(), at(), Au(), Bo(), ci(), Cu() (+47 more)

### Community 32 - "Community 32"
Cohesion: 0.08
Nodes (61): ai(), gr(), qr(), aa(), Ac(), Ap(), applyPatches(), bc() (+53 more)

### Community 33 - "Community 33"
Cohesion: 0.06
Nodes (66): A(), ag(), b(), be(), bv(), c(), cancel(), copy() (+58 more)

### Community 34 - "Community 34"
Cohesion: 0.16
Nodes (19): b(), ds(), gs(), ie(), ks(), n(), na(), qf() (+11 more)

### Community 35 - "Community 35"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 36 - "Community 36"
Cohesion: 0.07
Nodes (71): a(), aa(), Ac(), ao(), bc(), be(), _c(), ca() (+63 more)

### Community 37 - "Community 37"
Cohesion: 0.06
Nodes (14): _(), A(), findAll(), getAll(), getQueriesData(), isFetching(), isMutating(), isOnline() (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.07
Nodes (44): Am(), bh(), bm(), bp(), Ch(), clamp(), Cm(), dh() (+36 more)

### Community 39 - "Community 39"
Cohesion: 0.13
Nodes (25): at(), bi(), componentDidCatch(), Du(), ec(), ei(), Ha(), hi() (+17 more)

### Community 40 - "Community 40"
Cohesion: 0.06
Nodes (23): useAlertSound(), useLocalStorage(), useAnalisisGlobal(), useBacktest(), useBacktestColor(), useBacktestNumber(), useMesaData(), useMesas() (+15 more)

### Community 41 - "Community 41"
Cohesion: 0.09
Nodes (38): ap(), bs(), ci(), cp(), ct(), dd(), di(), dn() (+30 more)

### Community 42 - "Community 42"
Cohesion: 0.04
Nodes (71): $(), as(), bl(), Bo(), cl(), cs(), dl(), el() (+63 more)

### Community 43 - "Community 43"
Cohesion: 0.13
Nodes (23): bu(), cr(), d(), dr(), Ed(), f(), gn(), it() (+15 more)

### Community 44 - "Community 44"
Cohesion: 0.08
Nodes (27): Aw(), bi(), bl(), ce(), constructor(), Di(), Ew(), finishDraft() (+19 more)

### Community 45 - "Community 45"
Cohesion: 0.08
Nodes (30): Vd(), add(), ak(), bk(), Ck(), df(), divide(), Ef() (+22 more)

### Community 46 - "Community 46"
Cohesion: 0.13
Nodes (23): bindMethods(), build(), ce(), constructor(), defaultMutationOptions(), defaultQueryOptions(), fetchOptimistic(), get() (+15 more)

### Community 47 - "Community 47"
Cohesion: 0.04
Nodes (96): Ao(), as(), ay(), bA(), bw(), cd(), Cw(), Dd() (+88 more)

### Community 48 - "Community 48"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.08
Nodes (39): ai(), an(), bn(), Bt(), cn(), E(), ei(), fd() (+31 more)

### Community 50 - "Community 50"
Cohesion: 0.09
Nodes (39): aa(), af(), bc(), be(), cf(), dc(), Do(), ff() (+31 more)

### Community 51 - "Community 51"
Cohesion: 0.22
Nodes (19): af(), df(), ef(), ff(), gf(), go(), If(), jf() (+11 more)

### Community 52 - "Community 52"
Cohesion: 0.16
Nodes (15): api, BacktestSignal, BacktestTab, ColorStreak, ColorStreakSignal, GlobalAnalysisData, LastSpin, MesaData (+7 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 54 - "Community 54"
Cohesion: 0.13
Nodes (28): ad(), Au(), bd(), cd(), Cu(), et(), Eu(), Fa() (+20 more)

### Community 55 - "Community 55"
Cohesion: 0.17
Nodes (16): canRun(), continue(), execute(), fetch(), find(), invalidate(), isFocused(), #l() (+8 more)

### Community 56 - "Community 56"
Cohesion: 0.10
Nodes (37): aa(), af(), bc(), be(), cf(), dc(), Do(), ff() (+29 more)

### Community 57 - "Community 57"
Cohesion: 0.12
Nodes (4): DashboardScreen, LoadingScreen, LoginScreen, _resource_path()

### Community 58 - "Community 58"
Cohesion: 0.09
Nodes (54): a(), as(), b(), Bo(), bs(), bu(), ce(), ci() (+46 more)

### Community 59 - "Community 59"
Cohesion: 0.19
Nodes (15): C(), createResult(), h(), hasListeners(), onQueryUpdate(), onSubscribe(), onUnsubscribe(), q() (+7 more)

### Community 60 - "Community 60"
Cohesion: 0.09
Nodes (45): an(), bn(), Bt(), cn(), De(), dn(), Ee(), en() (+37 more)

### Community 61 - "Community 61"
Cohesion: 0.20
Nodes (14): add(), addObserver(), cancel(), clearGcTimeout(), clearTimeout(), destroy(), mount(), notify() (+6 more)

### Community 62 - "Community 62"
Cohesion: 0.14
Nodes (14): By(), Cf(), cy(), gx(), hx(), iy(), ly(), ry() (+6 more)

### Community 63 - "Community 63"
Cohesion: 0.11
Nodes (37): Ac(), b(), _c(), ca(), cc(), ea(), eo(), gc() (+29 more)

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Badge, BadgeProps, badgeVariants, Button, ButtonProps, buttonVariants, Card, CardContent (+3 more)

### Community 65 - "Community 65"
Cohesion: 0.40
Nodes (5): Gl(), hl(), ml(), Na(), wl()

### Community 66 - "Community 66"
Cohesion: 0.22
Nodes (10): b(), g(), getObserversCount(), isActive(), isDisabled(), isFetched(), isServer(), isStale() (+2 more)

### Community 67 - "Community 67"
Cohesion: 0.29
Nodes (10): clearInterval(), ensureInfiniteQueryData(), ensureQueryData(), fetchInfiniteQuery(), fetchQuery(), isStaleByTime(), m(), prefetchInfiniteQuery() (+2 more)

### Community 68 - "Community 68"
Cohesion: 0.09
Nodes (34): ai(), an(), bn(), Bt(), ce(), cn(), E(), fd() (+26 more)

### Community 69 - "Community 69"
Cohesion: 0.11
Nodes (39): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+31 more)

### Community 70 - "Community 70"
Cohesion: 0.12
Nodes (32): Au(), bd(), cd(), ct(), Cu(), di(), Eu(), Fa() (+24 more)

### Community 71 - "Community 71"
Cohesion: 0.28
Nodes (9): D(), E(), j(), k(), N(), O(), P(), S() (+1 more)

### Community 72 - "Community 72"
Cohesion: 0.14
Nodes (9): extract_numero(), nums_to_emoji(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, Tests para logic_helpers.py y helpers.py: utilidades compartidas., TestExtractNumero, TestKeycapMap (+1 more)

### Community 73 - "Community 73"
Cohesion: 0.11
Nodes (27): ap(), at(), cp(), dp(), ep(), f(), fi(), ip() (+19 more)

### Community 74 - "Community 74"
Cohesion: 0.13
Nodes (32): Ac(), b(), _c(), ca(), cc(), eo(), gc(), gi() (+24 more)

### Community 75 - "Community 75"
Cohesion: 0.10
Nodes (30): at(), bu(), cp(), cr(), d(), dn(), dp(), dr() (+22 more)

### Community 76 - "Community 76"
Cohesion: 0.29
Nodes (7): bo(), da(), gw(), La(), pa(), vw(), zt()

### Community 77 - "Community 77"
Cohesion: 0.09
Nodes (30): bi(), bs(), ce(), componentDidCatch(), ec(), ep(), hi(), i() (+22 more)

### Community 79 - "Community 79"
Cohesion: 0.11
Nodes (29): bu(), cp(), cr(), d(), dn(), dp(), dr(), Ed() (+21 more)

### Community 80 - "Community 80"
Cohesion: 0.15
Nodes (23): cl(), dl(), fl(), gl(), Il(), kl(), Ll(), ma() (+15 more)

### Community 81 - "Community 81"
Cohesion: 0.11
Nodes (23): bl(), ef(), el(), en(), gf(), Hf(), hl(), If() (+15 more)

### Community 82 - "Community 82"
Cohesion: 0.15
Nodes (23): cl(), dl(), fl(), gl(), Il(), kl(), Ll(), ma() (+15 more)

### Community 83 - "Community 83"
Cohesion: 0.13
Nodes (20): bl(), df(), ef(), el(), en(), gf(), Hf(), If() (+12 more)

### Community 85 - "Community 85"
Cohesion: 0.13
Nodes (20): cs(), ds(), Du(), fs(), Fu(), gs(), ic(), Iu() (+12 more)

### Community 86 - "Community 86"
Cohesion: 0.15
Nodes (18): cs(), ds(), Du(), fs(), Fu(), gs(), ic(), Iu() (+10 more)

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (17): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color(), get_connection(), main() (+9 more)

### Community 88 - "Community 88"
Cohesion: 0.19
Nodes (14): ao(), fc(), ko(), mo(), na(), oo(), po(), qf() (+6 more)

### Community 89 - "Community 89"
Cohesion: 0.36
Nodes (8): ao(), ea(), fc(), mo(), oo(), po(), uc(), wa()

### Community 90 - "Community 90"
Cohesion: 0.25
Nodes (24): af(), cf(), df(), dt(), ef(), ff(), gf(), go() (+16 more)

### Community 91 - "Community 91"
Cohesion: 0.16
Nodes (5): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36)., Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 92 - "Community 92"
Cohesion: 0.12
Nodes (17): aE(), gk(), GS(), hk(), Hs(), jk(), mk(), mn() (+9 more)

### Community 93 - "Community 93"
Cohesion: 0.18
Nodes (14): cs(), dd(), fs(), Fu(), Iu(), mu(), ns(), Nu() (+6 more)

### Community 94 - "Community 94"
Cohesion: 0.27
Nodes (4): Valida que un nombre de tabla sea seguro y exista en la configuracion.     Lanz, validate_table_name(), Tests para db.py: validador de tablas y operaciones CRUD., TestValidateTableName

## Knowledge Gaps
- **126 isolated node(s):** `api`, `ZONES`, `ROULETTE_LAYOUT`, `TABLE_NAMES`, `LoadingOverlayProps` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `$()` connect `Community 15` to `Community 33`, `Community 68`, `Community 37`, `Community 71`, `Community 46`, `Community 79`, `Community 81`, `Community 50`, `Community 82`, `Community 86`, `Community 88`, `Community 31`, `Community 63`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 2` to `Community 33`, `Community 90`, `Community 70`, `Community 69`, `Community 37`, `Community 73`, `Community 71`, `Community 46`, `Community 24`, `Community 58`, `Community 60`, `Community 93`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `_()` connect `Community 19` to `Community 32`, `Community 33`, `Community 65`, `Community 36`, `Community 37`, `Community 38`, `Community 42`, `Community 44`, `Community 45`, `Community 76`, `Community 47`, `Community 92`, `Community 62`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `$()` (e.g. with `ak()` and `tk()`) actually correct?**
  _`$()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `api`, `ZONES`, `ROULETTE_LAYOUT` to the rest of the system?**
  _285 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09716599190283401 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.06246799795186892 - nodes in this community are weakly interconnected._