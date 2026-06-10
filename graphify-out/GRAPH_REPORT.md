# Graph Report - Bot_Stake_Recolector  (2026-06-10)

## Corpus Check
- 81 files · ~46,610 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3378 nodes · 10880 edges · 110 communities (99 shown, 11 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 1864 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ed5d0eb5`
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
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 94|Community 94]]
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
- [[_COMMUNITY_Community 252|Community 252]]
- [[_COMMUNITY_Community 290|Community 290]]
- [[_COMMUNITY_Community 308|Community 308]]
- [[_COMMUNITY_Community 319|Community 319]]
- [[_COMMUNITY_Community 322|Community 322]]

## God Nodes (most connected - your core abstractions)
1. `_()` - 588 edges
2. `$()` - 387 edges
3. `$()` - 380 edges
4. `$()` - 380 edges
5. `$()` - 380 edges
6. `$()` - 380 edges
7. `_()` - 142 edges
8. `getOwnPropertyDescriptor()` - 75 edges
9. `defineProperty()` - 72 edges
10. `a()` - 69 edges

## Surprising Connections (you probably didn't know these)
- `fetchJSON()` --calls--> `fetch()`  [INFERRED]
  react-dashboard/src/lib/api.ts → bot_ruleta/dashboard/static/assets/query-BPe0xBFE.js
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  scripts/verify_number_delays.py → bot_ruleta/thresholds.py
- `dO()` --calls--> `$()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-Dkx9vjP1.js
- `So()` --calls--> `$()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-Dkx9vjP1.js
- `Du()` --calls--> `ft()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-Dkx9vjP1.js

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (110 total, 11 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (34): Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest(), get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de conf, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (56): ah(), ap(), bh(), bm(), ch(), clamp(), cp(), cv() (+48 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (32): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (20): clear_table(), get_connection(), get_last_number(), get_last_numbers(), int, str, Guarda un resultado en la tabla especifica del juego., Obtiene el ultimo numero registrado en la tabla del juego. (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (81): Any, Configuracion centralizada del bot de ruleta. Constantes, configuracion de mesa, init_db(), Manejo de base de datos SQLite con tablas separadas por juego., Inicializa la base de datos creando las tablas configuradas., attach_gui_queue(), capture_screenshot(), _cleanup_old_crash_reports() (+73 more)

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (4): build(), build_react_dashboard(), Script para empaquetar Roulette Sniper Pro en un solo .exe Requiere: pip instal, Compila el dashboard React y copia los archivos a Flask static.

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (30): Ze(), ak(), be(), dk(), Du(), ec(), Ek(), Eo() (+22 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (8): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest(), sync_number_backtest(), _ZoneBacktestSync

### Community 15 - "Community 15"
Cohesion: 0.07
Nodes (33): bp(), divide(), dm(), dw(), ew(), fm(), fw(), Gm() (+25 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (26): check_and_notify(), check_and_notify_color(), check_and_notify_number(), compute_color_streak(), Any, int, str, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci (+18 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (71): a(), aa(), Ac(), ao(), bc(), be(), bi(), cc() (+63 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (71): a(), aa(), Ac(), ao(), bc(), be(), bi(), cc() (+63 more)

### Community 19 - "Community 19"
Cohesion: 0.07
Nodes (63): ai(), as(), b(), Bo(), bs(), ci(), cs(), dd() (+55 more)

### Community 20 - "Community 20"
Cohesion: 0.07
Nodes (41): $(), ad(), ca(), cr(), dr(), Ed(), en(), fn() (+33 more)

### Community 21 - "Community 21"
Cohesion: 0.06
Nodes (59): $(), Ae(), an(), bd(), bn(), bs(), Bt(), cd() (+51 more)

### Community 22 - "Community 22"
Cohesion: 0.08
Nodes (59): aa(), Ac(), af(), bc(), be(), c(), ca(), cc() (+51 more)

### Community 23 - "Community 23"
Cohesion: 0.10
Nodes (37): at(), Au(), cs(), Cu(), Du(), Eu(), Fa(), fs() (+29 more)

### Community 24 - "Community 24"
Cohesion: 0.04
Nodes (88): at(), bC(), bd(), bj(), bl(), bO(), bu(), ce() (+80 more)

### Community 26 - "Community 26"
Cohesion: 0.10
Nodes (31): a(), bu(), cn(), d(), dn(), Ed(), f(), fd() (+23 more)

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (26): ai(), bi(), ci(), dd(), di(), fi(), gi(), hi() (+18 more)

### Community 28 - "Community 28"
Cohesion: 0.09
Nodes (8): DashboardScreen, LoadingScreen, LoginScreen, PrerequisitesScreen, Resuelve rutas de archivos empaquetados (PyInstaller) o de desarrollo., resource_path(), RouletteApp, UpdateScreen

### Community 29 - "Community 29"
Cohesion: 0.08
Nodes (25): bx(), cg(), cx(), eg(), gt(), Hd(), iO(), iy() (+17 more)

### Community 30 - "Community 30"
Cohesion: 0.10
Nodes (52): Ae(), an(), at(), bn(), Bt(), c(), cn(), de() (+44 more)

### Community 31 - "Community 31"
Cohesion: 0.11
Nodes (41): Au(), bd(), bu(), cd(), ct(), Cu(), Eu(), Fa() (+33 more)

### Community 32 - "Community 32"
Cohesion: 0.11
Nodes (31): ap(), cp(), ct(), dp(), es(), Et(), hu(), ip() (+23 more)

### Community 33 - "Community 33"
Cohesion: 0.07
Nodes (63): ai(), as(), b(), Bo(), bs(), ci(), cs(), dd() (+55 more)

### Community 34 - "Community 34"
Cohesion: 0.07
Nodes (41): $(), ad(), ca(), cr(), dr(), Ed(), en(), fn() (+33 more)

### Community 35 - "Community 35"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 36 - "Community 36"
Cohesion: 0.01
Nodes (64): _(), aA(), ae(), An(), bezierCurveTo(), bw(), cA(), closePath() (+56 more)

### Community 37 - "Community 37"
Cohesion: 0.16
Nodes (33): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+25 more)

### Community 38 - "Community 38"
Cohesion: 0.12
Nodes (28): ap(), cp(), dn(), dp(), ep(), Et(), f(), ip() (+20 more)

### Community 39 - "Community 39"
Cohesion: 0.25
Nodes (4): COLUMN_ZONES, DOZEN_ZONES, ROULETTE_LAYOUT, TABLE_NAMES

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): useAnalisisGlobal(), useSignalDetail(), AnalisisGlobalPage(), AnalysisTab, fmt(), SignalModal(), TABLE_NAMES

### Community 41 - "Community 41"
Cohesion: 0.10
Nodes (52): Ae(), an(), at(), bn(), Bt(), c(), cn(), de() (+44 more)

### Community 42 - "Community 42"
Cohesion: 0.07
Nodes (22): _client(), Tests para el dashboard React: middleware de token, rutas SPA y endpoints API., Endpoints de la API REST., Endpoint SSE para streaming en tiempo real., Restaurar el token después de cada test., Formato de respuesta del middleware de autenticación., Endpoint SSE para streaming en tiempo real., Configura SQLite en memoria para todos los tests. (+14 more)

### Community 43 - "Community 43"
Cohesion: 0.11
Nodes (41): Au(), bd(), bu(), cd(), ct(), Cu(), Eu(), Fa() (+33 more)

### Community 44 - "Community 44"
Cohesion: 0.16
Nodes (33): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+25 more)

### Community 45 - "Community 45"
Cohesion: 0.08
Nodes (71): a(), aa(), Ac(), ao(), bc(), be(), bi(), cc() (+63 more)

### Community 46 - "Community 46"
Cohesion: 0.36
Nodes (8): useBacktest(), useBacktestColor(), useBacktestNumber(), useMesaData(), useMesas(), formatTimeAgo(), MesaPopup(), MesaDetailPage()

### Community 47 - "Community 47"
Cohesion: 0.12
Nodes (28): ap(), cp(), dn(), dp(), ep(), Et(), f(), ip() (+20 more)

### Community 48 - "Community 48"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.26
Nodes (22): af(), cf(), df(), ef(), ff(), gf(), If(), jf() (+14 more)

### Community 50 - "Community 50"
Cohesion: 0.07
Nodes (63): ai(), as(), b(), Bo(), bs(), ci(), cs(), dd() (+55 more)

### Community 52 - "Community 52"
Cohesion: 0.15
Nodes (16): api, fetchJSON(), BacktestSignal, BacktestTab, ColorStreak, ColorStreakSignal, GlobalAnalysisData, LastSpin (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 54 - "Community 54"
Cohesion: 0.07
Nodes (41): $(), ad(), ca(), cr(), dr(), Ed(), en(), fn() (+33 more)

### Community 55 - "Community 55"
Cohesion: 0.26
Nodes (22): af(), cf(), df(), ef(), ff(), gf(), If(), jf() (+14 more)

### Community 56 - "Community 56"
Cohesion: 0.10
Nodes (52): Ae(), an(), at(), bn(), Bt(), c(), cn(), de() (+44 more)

### Community 57 - "Community 57"
Cohesion: 0.11
Nodes (41): Au(), bd(), bu(), cd(), ct(), Cu(), Eu(), Fa() (+33 more)

### Community 58 - "Community 58"
Cohesion: 0.16
Nodes (33): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+25 more)

### Community 59 - "Community 59"
Cohesion: 0.12
Nodes (28): ap(), cp(), dn(), dp(), ep(), Et(), f(), ip() (+20 more)

### Community 60 - "Community 60"
Cohesion: 0.22
Nodes (7): useAlertSound(), useLocalStorage(), DashboardContext, DashboardProvider(), DashboardState, Thresholds, OverviewPage()

### Community 61 - "Community 61"
Cohesion: 0.19
Nodes (16): cl(), fl(), Il(), Ll(), ma(), Nl(), no(), pl() (+8 more)

### Community 62 - "Community 62"
Cohesion: 0.15
Nodes (19): add(), clear(), concat(), finishDraft(), Fs(), gc(), ic(), Kc() (+11 more)

### Community 63 - "Community 63"
Cohesion: 0.08
Nodes (39): bl(), dl(), ef(), el(), en(), Fr(), gf(), gl() (+31 more)

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Badge, BadgeProps, badgeVariants, Button, ButtonProps, buttonVariants, Card, CardContent (+3 more)

### Community 65 - "Community 65"
Cohesion: 0.26
Nodes (22): af(), cf(), df(), ef(), ff(), gf(), If(), jf() (+14 more)

### Community 66 - "Community 66"
Cohesion: 0.14
Nodes (9): extract_numero(), nums_to_emoji(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, Tests para logic_helpers.py y helpers.py: utilidades compartidas., TestExtractNumero, TestKeycapMap (+1 more)

### Community 67 - "Community 67"
Cohesion: 0.17
Nodes (12): addAngleAxis(), addRadiusAxis(), aS(), cS(), lO(), os(), reducer(), se() (+4 more)

### Community 68 - "Community 68"
Cohesion: 0.29
Nodes (8): ei(), fetch(), invalidate(), #l(), re(), reset(), setData(), setState()

### Community 69 - "Community 69"
Cohesion: 0.17
Nodes (4): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 70 - "Community 70"
Cohesion: 0.08
Nodes (71): a(), aa(), Ac(), ao(), bc(), be(), bi(), cc() (+63 more)

### Community 71 - "Community 71"
Cohesion: 0.07
Nodes (63): ai(), as(), b(), Bo(), bs(), ci(), cs(), dd() (+55 more)

### Community 72 - "Community 72"
Cohesion: 0.18
Nodes (12): ds(), ID(), iT(), kD(), LD(), Lw(), MD(), PD() (+4 more)

### Community 73 - "Community 73"
Cohesion: 0.21
Nodes (18): build(), clearInterval(), defaultQueryOptions(), ensureInfiniteQueryData(), ensureQueryData(), fetchOptimistic(), fetchQuery(), get() (+10 more)

### Community 74 - "Community 74"
Cohesion: 0.27
Nodes (4): Valida que un nombre de tabla sea seguro y exista en la configuracion.     Lanz, validate_table_name(), Tests para db.py: validador de tablas y operaciones CRUD., TestValidateTableName

### Community 75 - "Community 75"
Cohesion: 0.20
Nodes (10): _chain_match_and_save(), extract_nums_js(), _get_color(), str, Escanea una mesa. Retorna True si encontró números y los procesó., Chain matching robusto + guardado en DB. Retorna los números nuevos., Envía alertas de delay, color y números a Telegram., Extrae números visibles de un tile usando JavaScript (class-agnostic). (+2 more)

### Community 76 - "Community 76"
Cohesion: 0.07
Nodes (41): $(), ad(), ca(), cr(), dr(), Ed(), en(), fn() (+33 more)

### Community 77 - "Community 77"
Cohesion: 0.10
Nodes (52): Ae(), an(), at(), bn(), Bt(), c(), cn(), de() (+44 more)

### Community 79 - "Community 79"
Cohesion: 0.11
Nodes (41): Au(), bd(), bu(), cd(), ct(), Cu(), Eu(), Fa() (+33 more)

### Community 80 - "Community 80"
Cohesion: 0.16
Nodes (33): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+25 more)

### Community 81 - "Community 81"
Cohesion: 0.11
Nodes (29): as(), b(), Bo(), componentDidCatch(), ds(), ec(), gs(), Ha() (+21 more)

### Community 82 - "Community 82"
Cohesion: 0.12
Nodes (28): ap(), cp(), dn(), dp(), ep(), Et(), f(), ip() (+20 more)

### Community 83 - "Community 83"
Cohesion: 0.26
Nodes (22): af(), cf(), df(), ef(), ff(), gf(), If(), jf() (+14 more)

### Community 85 - "Community 85"
Cohesion: 0.27
Nodes (10): ao(), fc(), hs(), Lo(), mo(), ms(), oo(), po() (+2 more)

### Community 86 - "Community 86"
Cohesion: 0.07
Nodes (14): check_for_updates(), _cleanup_old_versions(), _get_download_url(), perform_update(), Genera la URL de descarga para una versión específica., Checks GitHub for updates in a background thread.     Calls callback(new_versio, Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas)., Downloads the new versioned executable and spawns a bat file to replace the curr (+6 more)

### Community 87 - "Community 87"
Cohesion: 0.13
Nodes (17): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, audit_table(), format_color(), get_connection(), main() (+9 more)

### Community 91 - "Community 91"
Cohesion: 0.12
Nodes (7): _ColorBacktestSync, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., _ZoneBacktestSync, Tests para backtest.py: motores de sincronizacion incremental. Usa SQLite en me, Un gap de mas de 30 minutos entre filas debe romper la cadena y reiniciar delays, TestBacktestSync

### Community 92 - "Community 92"
Cohesion: 0.09
Nodes (31): bool, int, str, str, int, str, str, cleanup() (+23 more)

### Community 135 - "Community 135"
Cohesion: 0.06
Nodes (20): _(), A(), defaultMutationOptions(), fetchInfiniteQuery(), findAll(), getMutationDefaults(), getObserversCount(), getQueriesData() (+12 more)

### Community 151 - "Community 151"
Cohesion: 0.14
Nodes (19): C(), createResult(), h(), hasListeners(), j(), k(), mount(), onQueryUpdate() (+11 more)

### Community 152 - "Community 152"
Cohesion: 0.20
Nodes (11): bindMethods(), ce(), constructor(), getCurrentResult(), getDefaultOptions(), getOptimisticResult(), getQueryCache(), I() (+3 more)

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
Cohesion: 0.06
Nodes (70): ad(), Ar(), cr(), dr(), Hr(), kr(), Or(), sr() (+62 more)

### Community 252 - "Community 252"
Cohesion: 0.08
Nodes (54): pn(), w(), r(), A(), am(), b(), c(), cancel() (+46 more)

### Community 290 - "Community 290"
Cohesion: 0.60
Nodes (5): useOverview(), AppHeader(), TableFilterDropdown(), ThresholdDropdown(), useDashboard()

### Community 308 - "Community 308"
Cohesion: 0.20
Nodes (3): clsx(), cn(), ZONE_LABELS

### Community 319 - "Community 319"
Cohesion: 0.08
Nodes (20): compute_delays(), Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, _chain_match(), Busca empalme de MIN_CHAIN números consecutivos entre tile y DB.     Retorna li, Tests unitarios para los algoritmos de analytics:   - compute_delays   - compu, Sin historial en DB, todos los numeros del tile son nuevos. (+12 more)

## Knowledge Gaps
- **126 isolated node(s):** `TABLE_NAMES`, `AnalysisTab`, `TableCardProps`, `plugin`, `Connection` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_()` connect `Community 36` to `Community 2`, `Community 67`, `Community 135`, `Community 8`, `Community 72`, `Community 235`, `Community 15`, `Community 81`, `Community 21`, `Community 22`, `Community 24`, `Community 252`, `Community 29`, `Community 62`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 34` to `Community 33`, `Community 135`, `Community 41`, `Community 43`, `Community 44`, `Community 47`, `Community 17`, `Community 49`, `Community 152`, `Community 252`, `Community 159`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 54` to `Community 65`, `Community 135`, `Community 45`, `Community 50`, `Community 56`, `Community 57`, `Community 58`, `Community 59`, `Community 252`, `Community 152`, `Community 159`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `$()` (e.g. with `dO()` and `So()`) actually correct?**
  _`$()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `TABLE_NAMES`, `AnalysisTab`, `TableCardProps` to the rest of the system?**
  _298 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09615384615384616 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05649350649350649 - nodes in this community are weakly interconnected._