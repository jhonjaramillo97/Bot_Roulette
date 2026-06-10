# Graph Report - Bot_Stake_Recolector  (2026-06-09)

## Corpus Check
- 80 files · ~45,701 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1875 nodes · 4664 edges · 117 communities (92 shown, 25 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 541 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0feab783`
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
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 135|Community 135]]
- [[_COMMUNITY_Community 151|Community 151]]
- [[_COMMUNITY_Community 152|Community 152]]
- [[_COMMUNITY_Community 153|Community 153]]
- [[_COMMUNITY_Community 155|Community 155]]
- [[_COMMUNITY_Community 157|Community 157]]
- [[_COMMUNITY_Community 159|Community 159]]
- [[_COMMUNITY_Community 235|Community 235]]
- [[_COMMUNITY_Community 236|Community 236]]
- [[_COMMUNITY_Community 252|Community 252]]
- [[_COMMUNITY_Community 290|Community 290]]
- [[_COMMUNITY_Community 299|Community 299]]
- [[_COMMUNITY_Community 301|Community 301]]
- [[_COMMUNITY_Community 306|Community 306]]
- [[_COMMUNITY_Community 308|Community 308]]
- [[_COMMUNITY_Community 310|Community 310]]
- [[_COMMUNITY_Community 312|Community 312]]
- [[_COMMUNITY_Community 319|Community 319]]
- [[_COMMUNITY_Community 322|Community 322]]
- [[_COMMUNITY_Community 326|Community 326]]
- [[_COMMUNITY_Community 337|Community 337]]
- [[_COMMUNITY_Community 339|Community 339]]
- [[_COMMUNITY_Community 340|Community 340]]

## God Nodes (most connected - your core abstractions)
1. `_()` - 584 edges
2. `$()` - 380 edges
3. `_()` - 139 edges
4. `getOwnPropertyDescriptor()` - 75 edges
5. `defineProperty()` - 72 edges
6. `a()` - 68 edges
7. `pc()` - 50 edges
8. `wc()` - 34 edges
9. `bc()` - 33 edges
10. `c()` - 27 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  scripts/verify_number_delays.py → bot_ruleta/thresholds.py
- `audit_table()` --calls--> `compute_number_delays()`  [EXTRACTED]
  scripts/verify_number_delays.py → bot_ruleta/logic.py
- `TableFilterDropdown()` --calls--> `useDashboard()`  [INFERRED]
  react-dashboard/src/components/layout/AppHeader.tsx → react-dashboard/src/lib/DashboardContext.tsx
- `ThresholdDropdown()` --calls--> `useDashboard()`  [INFERRED]
  react-dashboard/src/components/layout/AppHeader.tsx → react-dashboard/src/lib/DashboardContext.tsx
- `MesaDetailPage()` --calls--> `formatTimeAgo()`  [INFERRED]
  react-dashboard/src/pages/MesaDetail.tsx → react-dashboard/src/lib/utils.ts

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (117 total, 25 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (34): Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest(), get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de conf, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (56): ah(), ap(), bh(), bm(), ch(), clamp(), cp(), cv() (+48 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (31): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui() (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (23): clear_table(), get_connection(), get_last_number(), get_last_numbers(), init_db(), int, str, Manejo de base de datos SQLite con tablas separadas por juego. (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (24): Configuracion centralizada del bot de ruleta. Constantes, configuracion de mesa, get_chrome_major_version(), _hide_chrome_window(), login_stake(), Configuración y creación del WebDriver + flujo de login., Oculta la ventana de Chrome de la barra de tareas y la mueve fuera de la pantall, Detecta la versión principal de Chrome instalada para evitar mismatch., Navega al lobby y ejecuta el flujo de login. (+16 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (26): ae(), ak(), be(), bezierCurveTo(), dk(), Du(), Ek(), Eo() (+18 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (11): _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de retraso de números individuales (0-36)., sync_backtest() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (22): am(), bp(), cm(), dm(), fm(), Gm(), gp(), hm() (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (11): compute_color_streak(), Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, El verde (0) suma a la racha sin romperla., Un color opuesto detiene la racha desde el mas reciente.         El algoritmo l, Verdes al inicio cuentan para la racha una vez aparece el primer color., El marcador -1 detiene el conteo. (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (18): cA(), ec(), F(), Fb(), Gn(), Hj(), Jc(), Jk() (+10 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (5): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36)., Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 20 - "Community 20"
Cohesion: 0.10
Nodes (29): bool, int, str, str, int, str, str, cleanup() (+21 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (6): LoadingScreen, LoginScreen, PrerequisitesScreen, Resuelve rutas de archivos empaquetados (PyInstaller) o de desarrollo., resource_path(), UpdateScreen

### Community 22 - "Community 22"
Cohesion: 0.07
Nodes (36): _chain_match(), _chain_match_and_save(), _check_session_expiry(), _cleanup_driver(), extract_nums_js(), _get_color(), _handle_error(), _handle_zero_tiles() (+28 more)

### Community 23 - "Community 23"
Cohesion: 0.16
Nodes (15): check_and_notify(), check_and_notify_color(), check_and_notify_number(), Any, int, str, Si la racha de color supera el umbral, envía notificación a Telegram.     Usa c, Si la racha de color supera el umbral, envía notificación a Telegram.     Usa c (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.19
Nodes (14): bO(), ce(), ck(), getOwnPropertyDescriptor(), gx(), hx(), lk(), nA() (+6 more)

### Community 26 - "Community 26"
Cohesion: 0.10
Nodes (31): Any, capture_screenshot(), _cleanup_old_crash_reports(), _cleanup_old_screenshots(), generate_crash_report(), get_logger(), Sistema de Diagnóstico Forense — re-exportador. La implementación está en el pa, Toma un screenshot del navegador y opcionalmente guarda el HTML source.      Arg (+23 more)

### Community 29 - "Community 29"
Cohesion: 0.17
Nodes (13): bx(), cx(), gt(), Hd(), iO(), lx(), Pg(), ro() (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (13): divide(), dw(), ew(), fw(), kw(), multiply(), nw(), Ow() (+5 more)

### Community 31 - "Community 31"
Cohesion: 0.17
Nodes (12): addAngleAxis(), addRadiusAxis(), lO(), Lr(), or(), reducer(), se(), setChartData() (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (3): Valida que un nombre de tabla sea seguro y exista en la configuracion.     Lanz, validate_table_name(), TestValidateTableName

### Community 33 - "Community 33"
Cohesion: 0.20
Nodes (6): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., Handler que envía logs a una Queue para que la GUI los lea., set_diagnostics()

### Community 34 - "Community 34"
Cohesion: 0.22
Nodes (3): attach_gui_queue(), _GUIQueueHandler, RouletteApp

### Community 35 - "Community 35"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 38 - "Community 38"
Cohesion: 0.39
Nodes (3): nums_to_emoji(), Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, TestNumsToEmoji

### Community 39 - "Community 39"
Cohesion: 0.25
Nodes (4): COLUMN_ZONES, DOZEN_ZONES, ROULETTE_LAYOUT, TABLE_NAMES

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): useAnalisisGlobal(), useSignalDetail(), AnalisisGlobalPage(), AnalysisTab, fmt(), SignalModal(), TABLE_NAMES

### Community 42 - "Community 42"
Cohesion: 0.43
Nodes (7): audit_table(), format_color(), get_connection(), main(), manual_delays(), verify_number_delays.py — Auditoria de la base de datos.  Para cada mesa: 1., Calcula delays manualmente (independiente de compute_number_delays).     numero

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (7): bj(), cj(), rj(), Sj(), xj(), yj(), zj()

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (7): bw(), constructor(), re(), setAutoFreeze(), setUseStrictIteration(), setUseStrictShallowCopy(), sw()

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (7): cl(), dl(), fl(), ll(), pl(), sl(), ul()

### Community 46 - "Community 46"
Cohesion: 0.48
Nodes (6): useBacktest(), useBacktestColor(), useBacktestNumber(), useMesaData(), useMesas(), MesaDetailPage()

### Community 47 - "Community 47"
Cohesion: 0.33
Nodes (6): at(), Dt(), Et(), ht(), jT(), Tt()

### Community 48 - "Community 48"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): ga(), Ja(), Ka(), qa(), uo(), Ya()

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (6): iy(), Ly(), ny(), ry(), sy(), ty()

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (4): formatTimeAgo(), MesaPopup(), Props, ZONES

### Community 52 - "Community 52"
Cohesion: 0.15
Nodes (15): api, BacktestSignal, BacktestTab, ColorStreak, ColorStreakSignal, GlobalAnalysisData, LastSpin, MesaData (+7 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 54 - "Community 54"
Cohesion: 0.40
Nodes (5): bu(), Hu(), Uu(), vu(), Wu()

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (5): cg(), eg(), Ng(), Og(), q()

### Community 56 - "Community 56"
Cohesion: 0.40
Nodes (5): cT(), kt(), lT(), ot(), sT()

### Community 57 - "Community 57"
Cohesion: 0.15
Nodes (10): check_for_updates(), _cleanup_old_versions(), _get_download_url(), perform_update(), Genera la URL de descarga para una versión específica., Checks GitHub for updates in a background thread.     Calls callback(new_versio, Limpia archivos de actualizaciones anteriores (.old, .update, versiones viejas)., Downloads the new versioned executable and spawns a bat file to replace the curr (+2 more)

### Community 58 - "Community 58"
Cohesion: 0.40
Nodes (5): df(), ff(), hf(), mf(), pf()

### Community 59 - "Community 59"
Cohesion: 0.40
Nodes (5): il(), nl(), rl(), tl(), zl()

### Community 60 - "Community 60"
Cohesion: 0.40
Nodes (3): DashboardContext, DashboardState, Thresholds

### Community 61 - "Community 61"
Cohesion: 0.50
Nodes (4): add(), mount(), subscribe(), trackProp()

### Community 62 - "Community 62"
Cohesion: 0.50
Nodes (4): aS(), cS(), os(), ss()

### Community 63 - "Community 63"
Cohesion: 0.50
Nodes (4): copy(), gv(), hv(), mv()

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Badge, BadgeProps, badgeVariants, Button, ButtonProps, buttonVariants, Card, CardContent (+3 more)

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (4): es(), ns(), rs(), ts()

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (4): Qw(), Xw(), Yw(), Zw()

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (3): dj(), fj(), pj()

### Community 68 - "Community 68"
Cohesion: 0.67
Nodes (3): ed(), nd(), td()

### Community 69 - "Community 69"
Cohesion: 0.67
Nodes (3): gl(), Kl(), ql()

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (3): gS(), Hs(), US()

### Community 72 - "Community 72"
Cohesion: 0.21
Nodes (6): extract_numero(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, Tests para logic_helpers.py y helpers.py: utilidades compartidas., TestExtractNumero, TestKeycapMap

### Community 87 - "Community 87"
Cohesion: 0.17
Nodes (10): compute_number_delays(), Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, 3 numeros: el delay de cada uno es su posicion desde el mas reciente., Un numero repetido resetea su delay., -1 detiene el conteo, los delays reflejan solo hasta ahi., Si todos los numeros 0-36 aparecen, el delay = posicion desde el mas reciente. (+2 more)

### Community 91 - "Community 91"
Cohesion: 0.11
Nodes (8): _ColorBacktestSync, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., Sincroniza eventos de rachas de rojos/negros consecutivos., _ZoneBacktestSync, Tests para backtest.py: motores de sincronizacion incremental. Usa SQLite en me, TestBacktestSync

### Community 106 - "Community 106"
Cohesion: 0.16
Nodes (16): bC(), bd(), Co(), defineProperty(), ex(), ge(), Me(), Oc() (+8 more)

### Community 135 - "Community 135"
Cohesion: 0.06
Nodes (19): _(), A(), defaultMutationOptions(), fetchInfiniteQuery(), findAll(), getAll(), getMutationDefaults(), getQueriesData() (+11 more)

### Community 151 - "Community 151"
Cohesion: 0.21
Nodes (14): C(), createResult(), h(), hasListeners(), onQueryUpdate(), onSubscribe(), onUnsubscribe(), q() (+6 more)

### Community 152 - "Community 152"
Cohesion: 0.19
Nodes (20): build(), clearInterval(), defaultQueryOptions(), ensureInfiniteQueryData(), ensureQueryData(), fetchOptimistic(), fetchQuery(), g() (+12 more)

### Community 153 - "Community 153"
Cohesion: 0.16
Nodes (18): addObserver(), b(), cancel(), clearGcTimeout(), clearTimeout(), destroy(), fetch(), invalidate() (+10 more)

### Community 155 - "Community 155"
Cohesion: 0.33
Nodes (6): getObserversCount(), isActive(), isDisabled(), isFetched(), isStale(), isStatic()

### Community 157 - "Community 157"
Cohesion: 0.29
Nodes (10): canRun(), continue(), execute(), find(), isFocused(), onFocus(), onOnline(), refetch() (+2 more)

### Community 159 - "Community 159"
Cohesion: 0.28
Nodes (9): D(), E(), j(), k(), N(), O(), P(), S() (+1 more)

### Community 235 - "Community 235"
Cohesion: 0.05
Nodes (77): ac(), add(), Ai(), applyPatches(), bi(), br(), Bs(), cc() (+69 more)

### Community 236 - "Community 236"
Cohesion: 0.18
Nodes (12): ds(), ID(), iT(), kD(), LD(), Lw(), MD(), PD() (+4 more)

### Community 252 - "Community 252"
Cohesion: 0.08
Nodes (53): A(), b(), c(), cancel(), d(), dispatch(), dO(), E() (+45 more)

### Community 290 - "Community 290"
Cohesion: 0.25
Nodes (8): useAlertSound(), useLocalStorage(), useOverview(), AppHeader(), TableFilterDropdown(), ThresholdDropdown(), useDashboard(), OverviewPage()

### Community 299 - "Community 299"
Cohesion: 0.06
Nodes (65): $(), ad(), ap(), cp(), cr(), dn(), dp(), dr() (+57 more)

### Community 301 - "Community 301"
Cohesion: 0.08
Nodes (75): a(), aa(), Ac(), ao(), bc(), be(), bi(), ca() (+67 more)

### Community 306 - "Community 306"
Cohesion: 0.10
Nodes (50): an(), at(), bn(), Bt(), c(), cn(), de(), Ee() (+42 more)

### Community 308 - "Community 308"
Cohesion: 0.20
Nodes (3): clsx(), cn(), ZONE_LABELS

### Community 310 - "Community 310"
Cohesion: 0.08
Nodes (47): Ae(), as(), b(), Bo(), bs(), cs(), dd(), ds() (+39 more)

### Community 312 - "Community 312"
Cohesion: 0.11
Nodes (41): Au(), bd(), bu(), cd(), ct(), Cu(), Eu(), Fa() (+33 more)

### Community 319 - "Community 319"
Cohesion: 0.15
Nodes (11): compute_delays(), Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Caso normal: cada numero cae en su docena y columna correcta.         La logica, Si todas las zonas ya salieron, los delays son las distancias al mas reciente., El marcador -1 detiene el conteo de delays., Los ceros (0) incrementan todos los delays sin romper la busqueda.         Con (+3 more)

### Community 326 - "Community 326"
Cohesion: 0.16
Nodes (33): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+25 more)

### Community 337 - "Community 337"
Cohesion: 0.26
Nodes (22): af(), cf(), df(), ef(), ff(), gf(), If(), jf() (+14 more)

### Community 339 - "Community 339"
Cohesion: 0.24
Nodes (18): ai(), ci(), di(), fi(), hi(), i(), Ii(), Ki() (+10 more)

### Community 340 - "Community 340"
Cohesion: 0.18
Nodes (12): bindMethods(), ce(), constructor(), getCurrentResult(), getDefaultOptions(), getOptimisticResult(), getQueryCache(), I() (+4 more)

## Knowledge Gaps
- **126 isolated node(s):** `ZONE_LABELS`, `TABLE_NAMES`, `AnalysisTab`, `queryClient`, `TableCardProps` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_()` connect `Community 36` to `Community 2`, `Community 135`, `Community 8`, `Community 15`, `Community 17`, `Community 24`, `Community 29`, `Community 30`, `Community 31`, `Community 43`, `Community 44`, `Community 45`, `Community 47`, `Community 49`, `Community 50`, `Community 54`, `Community 55`, `Community 56`, `Community 58`, `Community 59`, `Community 62`, `Community 63`, `Community 65`, `Community 66`, `Community 67`, `Community 68`, `Community 69`, `Community 70`, `Community 71`, `Community 73`, `Community 74`, `Community 75`, `Community 76`, `Community 77`, `Community 79`, `Community 80`, `Community 81`, `Community 82`, `Community 83`, `Community 106`, `Community 235`, `Community 236`, `Community 252`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 299` to `Community 326`, `Community 135`, `Community 301`, `Community 337`, `Community 306`, `Community 339`, `Community 340`, `Community 310`, `Community 312`, `Community 252`, `Community 159`?**
  _High betweenness centrality (0.189) - this node is a cross-community bridge._
- **Why does `_()` connect `Community 135` to `Community 340`, `Community 157`, `Community 151`, `Community 152`, `Community 153`, `Community 155`, `Community 61`, `Community 159`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **What connects `ZONE_LABELS`, `TABLE_NAMES`, `AnalysisTab` to the rest of the system?**
  _285 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09358974358974359 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05649350649350649 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.09082125603864734 - nodes in this community are weakly interconnected._