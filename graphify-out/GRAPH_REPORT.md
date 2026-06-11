# Graph Report - Bot_Stake_Recolector  (2026-06-10)

## Corpus Check
- 81 files · ~46,928 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1932 nodes · 4867 edges · 111 communities (90 shown, 21 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 591 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1289eeb4`
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
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
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
3. `_()` - 142 edges
4. `getOwnPropertyDescriptor()` - 75 edges
5. `defineProperty()` - 72 edges
6. `a()` - 69 edges
7. `pc()` - 51 edges
8. `wc()` - 35 edges
9. `bc()` - 33 edges
10. `r()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `fetchJSON()` --calls--> `fetch()`  [INFERRED]
  react-dashboard/src/lib/api.ts → bot_ruleta/dashboard/static/assets/query-BPe0xBFE.js
- `main()` --calls--> `get_number_delay_threshold()`  [INFERRED]
  scripts/verify_number_delays.py → bot_ruleta/thresholds.py
- `dO()` --calls--> `$()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-BN1VDvLw.js
- `So()` --calls--> `$()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-BN1VDvLw.js
- `Du()` --calls--> `ft()`  [INFERRED]
  bot_ruleta/dashboard/static/assets/recharts-_PnXljkz.js → bot_ruleta/dashboard/static/assets/index-BN1VDvLw.js

## Import Cycles
- 1-file cycle: `bot_ruleta/gui_app.py -> bot_ruleta/gui_app.py`

## Communities (111 total, 21 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (11): api_request(), build_executable(), create_release(), delete_release(), delete_tag(), get_file_sha(), get_release_by_tag(), main() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (34): Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py, sync_backtest(), sync_color_backtest(), sync_number_backtest(), get_color_streak_threshold(), get_number_delay_threshold(), Umbrales de alerta para rachas de color y retrasos de números. Separado de conf, Lee el umbral de racha de color. Prioridad: runtime overrides > GUI saved > .env (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (54): ah(), ap(), bh(), bm(), ch(), clamp(), cp(), cv() (+46 more)

### Community 3 - "Community 3"
Cohesion: 0.21
Nodes (12): Punto de entrada de la GUI — compatible con PyInstaller. La implementacion esta, Cliente de Telegram Bot API. Extraido de logic.py para separar el envio de mens, notify_tunnel_url(), Gestion del tunel Cloudflare compartido entre GUI y CLI. Unifica cloudflared_wa, Inicia un proceso cloudflared y retorna el proceso., Envia notificacion por Telegram cuando el URL del tunel se establece o cambia., Mantiene un tunel cloudflared vivo con auto-reinicio.      Args:         on_u, run_tunnel() (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (23): clear_table(), get_last_number(), get_last_numbers(), init_db(), int, str, Manejo de base de datos SQLite con tablas separadas por juego., Guarda un resultado en la tabla especifica del juego. (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (17): check_and_notify(), check_and_notify_color(), check_and_notify_number(), Any, int, str, Envía mensaje raw a Telegram., Si la racha de color supera el umbral, envía notificación a Telegram.     Usa c (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.43
Nodes (6): build(), build_react_dashboard(), _do_build(), Script para empaquetar Roulette Sniper Pro en un solo .exe Requiere: pip instal, Compila el dashboard React y copia los archivos a Flask static., Empaqueta el proyecto en un .exe. Si production=True, usa DEV_MODE=False.

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (26): addAngleAxis(), addRadiusAxis(), be(), ec(), Eo(), F(), Fb(), Gn() (+18 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (14): get_connection(), Retorna la conexion persistente a la BD (inicializa con WAL si es necesario)., _BacktestSyncEngine, _ColorBacktestSync, _NumberBacktestSync, Motor de sincronización incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos. (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.50
Nodes (3): human_type(), Funciones auxiliares puras: escritura simulada, persistencia CSV., Escribe texto con retardos aleatorios para simular humano.

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (11): compute_color_streak(), Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, Calcula la racha actual de un color (Rojo o Negro) basándose en los números reci, El verde (0) suma a la racha sin romperla., Un color opuesto detiene la racha desde el mas reciente.         El algoritmo l, Verdes al inicio cuentan para la racha una vez aparece el primer color., El marcador -1 detiene el conteo. (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.07
Nodes (55): Configuracion centralizada del bot de ruleta. Constantes, configuracion de mesa, capture_screenshot(), _cleanup_old_crash_reports(), _cleanup_old_screenshots(), generate_crash_report(), get_logger(), Sistema de Diagnóstico Forense — re-exportador. La implementación está en el pa, Toma un screenshot del navegador y opcionalmente guarda el HTML source.      Arg (+47 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (30): aA(), ak(), dk(), Du(), ea(), Ek(), fk(), g() (+22 more)

### Community 19 - "Community 19"
Cohesion: 0.05
Nodes (23): check_for_updates(), _cleanup_old_versions(), _get_asset_download_url(), _get_download_url(), perform_update(), Downloads the new versioned executable and spawns a bat file to replace the curr, Downloads the new versioned executable and spawns a bat file to replace the curr, Genera la URL de descarga para una versión específica. (+15 more)

### Community 20 - "Community 20"
Cohesion: 0.08
Nodes (14): attach_gui_queue(), _GUIQueueHandler, Conecta una Queue al logger para que la GUI reciba los logs.     Llamar una sola, Activa o desactiva las capturas de pantalla de diagnóstico rutinarias., Handler que envía logs a una Queue para que la GUI los lea., set_diagnostics(), DashboardScreen, LoadingScreen (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (15): bd(), bO(), ce(), ck(), es(), getOwnPropertyDescriptor(), gx(), hx() (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.18
Nodes (13): divide(), dw(), ew(), fw(), kw(), multiply(), nw(), Ow() (+5 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (9): _chain_match(), Busca empalme de MIN_CHAIN números consecutivos entre tile y DB.     Retorna li, Tests unitarios para los algoritmos de analytics:   - compute_delays   - compu, Sin historial en DB, todos los numeros del tile son nuevos., Los ultimos 4 del tile coinciden con la DB., Solo 2 coinciden, necesita _MIN_CHAIN=4., Todos los numeros del tile ya estan en la DB., El empalme comienza en el indice 0 del tile (todos nuevos desde ahi). (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.16
Nodes (15): bC(), Co(), defineProperty(), ex(), ge(), Me(), Oc(), So() (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.11
Nodes (20): _chain_match_and_save(), _check_session_expiry(), extract_nums_js(), _get_color(), _handle_zero_tiles(), str, Loop infinito de escaneo de tiles., Simula movimiento de mouse JS para evitar desconexión de Pragmatic. (+12 more)

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (20): bp(), dm(), fm(), Gm(), gp(), hm(), hp(), Im() (+12 more)

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (8): Envia mensaje raw a Telegram., Envia mensaje raw a Telegram., send_telegram_msg(), get_cf_env_vars(), Retorna (token, dominio) de Cloudflare.     Prioridad: CLOUDFLARE_TOKEN env > t, Tests para telegram.py y tunnel.py: envio de mensajes y gestion de Cloudflare., TestSendTelegramMsg, TestTunnel

### Community 29 - "Community 29"
Cohesion: 0.25
Nodes (9): clear_screen(), cloudflared_watchdog(), Dibuja la consola limpia y minimalista, Actualiza el URL del tunel: variable global, Telegram, UI., Hilo permanente que mantiene cloudflared vivo y actualiza la consola., Lee la salida del bot y actualiza la consola minimalista, render_ui(), track_bot() (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.40
Nodes (4): Any, Any, Loop supervisor que asegura que el bot se reinicie si falla.          Args:, run_bot()

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (8): bw(), constructor(), re(), setAutoFreeze(), setPrototypeOf(), setUseStrictIteration(), setUseStrictShallowCopy(), sw()

### Community 34 - "Community 34"
Cohesion: 0.29
Nodes (7): bj(), cj(), rj(), Sj(), xj(), yj(), zj()

### Community 35 - "Community 35"
Cohesion: 0.05
Nodes (42): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, react-router-dom, recharts (+34 more)

### Community 37 - "Community 37"
Cohesion: 0.29
Nodes (7): cA(), Jk(), kk(), lA(), qk(), sA(), uf()

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (7): cl(), dl(), fl(), ll(), pl(), sl(), ul()

### Community 39 - "Community 39"
Cohesion: 0.25
Nodes (4): COLUMN_ZONES, DOZEN_ZONES, ROULETTE_LAYOUT, TABLE_NAMES

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): useAnalisisGlobal(), useSignalDetail(), AnalisisGlobalPage(), AnalysisTab, fmt(), SignalModal(), TABLE_NAMES

### Community 41 - "Community 41"
Cohesion: 0.33
Nodes (6): iy(), Ly(), ny(), ry(), sy(), ty()

### Community 42 - "Community 42"
Cohesion: 0.07
Nodes (22): _client(), Tests para el dashboard React: middleware de token, rutas SPA y endpoints API., Endpoints de la API REST., Endpoint SSE para streaming en tiempo real., Restaurar el token después de cada test., Formato de respuesta del middleware de autenticación., Endpoint SSE para streaming en tiempo real., Configura SQLite en memoria para todos los tests. (+14 more)

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (6): ga(), Ja(), Ka(), qa(), uo(), Ya()

### Community 44 - "Community 44"
Cohesion: 0.11
Nodes (19): bx(), cg(), cx(), eg(), gt(), Hd(), iO(), lx() (+11 more)

### Community 45 - "Community 45"
Cohesion: 0.18
Nodes (12): ds(), ID(), iT(), kD(), LD(), Lw(), MD(), PD() (+4 more)

### Community 46 - "Community 46"
Cohesion: 0.36
Nodes (8): useBacktest(), useBacktestColor(), useBacktestNumber(), useMesaData(), useMesas(), formatTimeAgo(), MesaPopup(), MesaDetailPage()

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (5): ae(), bezierCurveTo(), lineTo(), moveTo(), point()

### Community 48 - "Community 48"
Cohesion: 0.09
Nodes (22): compilerOptions, allowImportingTsExtensions, baseUrl, erasableSyntaxOnly, ignoreDeprecations, jsx, lib, module (+14 more)

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): at(), Dt(), Et(), ht(), jT(), Tt()

### Community 50 - "Community 50"
Cohesion: 0.40
Nodes (5): bu(), Hu(), Uu(), vu(), Wu()

### Community 52 - "Community 52"
Cohesion: 0.15
Nodes (16): api, fetchJSON(), BacktestSignal, BacktestTab, ColorStreak, ColorStreakSignal, GlobalAnalysisData, LastSpin (+8 more)

### Community 53 - "Community 53"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, moduleResolution, noEmit (+9 more)

### Community 54 - "Community 54"
Cohesion: 0.40
Nodes (5): cT(), kt(), lT(), ot(), sT()

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (5): df(), ff(), hf(), mf(), pf()

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (4): copy(), gv(), hv(), mv()

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (4): Qw(), Xw(), Yw(), Zw()

### Community 60 - "Community 60"
Cohesion: 0.22
Nodes (7): useAlertSound(), useLocalStorage(), DashboardContext, DashboardProvider(), DashboardState, Thresholds, OverviewPage()

### Community 61 - "Community 61"
Cohesion: 0.67
Nodes (3): dj(), fj(), pj()

### Community 62 - "Community 62"
Cohesion: 0.16
Nodes (19): add(), clear(), concat(), finishDraft(), Fs(), gc(), ic(), Ks() (+11 more)

### Community 63 - "Community 63"
Cohesion: 0.67
Nodes (3): ed(), nd(), td()

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (11): Badge, BadgeProps, badgeVariants, Button, ButtonProps, buttonVariants, Card, CardContent (+3 more)

### Community 65 - "Community 65"
Cohesion: 0.67
Nodes (3): gS(), Hs(), US()

### Community 67 - "Community 67"
Cohesion: 0.50
Nodes (4): aS(), cS(), os(), ss()

### Community 68 - "Community 68"
Cohesion: 0.29
Nodes (8): ei(), fetch(), invalidate(), #l(), re(), reset(), setData(), setState()

### Community 69 - "Community 69"
Cohesion: 0.17
Nodes (4): _BacktestSyncEngine, _NumberBacktestSync, Motor de sincronizacion incremental compartido por todos los backtests.      M, Sincroniza eventos de retraso de numeros individuales (0-36).

### Community 70 - "Community 70"
Cohesion: 0.11
Nodes (60): a(), aa(), Ac(), ao(), bc(), bi(), ca(), cc() (+52 more)

### Community 71 - "Community 71"
Cohesion: 0.06
Nodes (71): ai(), as(), b(), Bo(), bs(), ci(), cs(), dd() (+63 more)

### Community 73 - "Community 73"
Cohesion: 0.21
Nodes (18): build(), clearInterval(), defaultQueryOptions(), ensureInfiniteQueryData(), ensureQueryData(), fetchOptimistic(), fetchQuery(), get() (+10 more)

### Community 76 - "Community 76"
Cohesion: 0.06
Nodes (58): $(), ap(), be(), dn(), dp(), dt(), Ed(), en() (+50 more)

### Community 77 - "Community 77"
Cohesion: 0.08
Nodes (59): Ae(), an(), at(), bn(), Bt(), c(), cn(), de() (+51 more)

### Community 79 - "Community 79"
Cohesion: 0.13
Nodes (37): Au(), bd(), bu(), cd(), cp(), ct(), Cu(), Eu() (+29 more)

### Community 80 - "Community 80"
Cohesion: 0.13
Nodes (37): bl(), cl(), dl(), el(), fl(), gc(), gl(), Hf() (+29 more)

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (3): Yo(), Ao(), jo()

### Community 83 - "Community 83"
Cohesion: 0.25
Nodes (23): af(), cf(), df(), ef(), ff(), gf(), go(), If() (+15 more)

### Community 87 - "Community 87"
Cohesion: 0.07
Nodes (26): compute_number_delays(), extract_numero(), nums_to_emoji(), Helpers compartidos por las funciones de analytics (logic.py). Extraidos para e, Extrae el valor numerico de un item que puede ser dict/Row o int.     Retorna e, Convierte una lista de numeros/dicts recientes en string de emojis.     items[0, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume, Calcula los delays (giros sin salir) para cada número individual 0-36.     nume (+18 more)

### Community 89 - "Community 89"
Cohesion: 0.40
Nodes (5): il(), nl(), rl(), tl(), zl()

### Community 91 - "Community 91"
Cohesion: 0.12
Nodes (7): _ColorBacktestSync, Sincroniza eventos de retraso de docenas y columnas., Sincroniza eventos de rachas de rojos/negros consecutivos., _ZoneBacktestSync, Tests para backtest.py: motores de sincronizacion incremental. Usa SQLite en me, Un gap de mas de 30 minutos entre filas debe romper la cadena y reiniciar delays, TestBacktestSync

### Community 92 - "Community 92"
Cohesion: 0.10
Nodes (27): bool, int, str, str, int, str, str, get_data_dir() (+19 more)

### Community 94 - "Community 94"
Cohesion: 0.13
Nodes (7): cleanup(), get_base_dir(), is_frozen(), Directorio raiz del ejecutable (frozen) o del source (dev)., Tests para config.py y paths.py: constantes y resolucion de rutas., TestConfig, TestPaths

### Community 96 - "Community 96"
Cohesion: 0.50
Nodes (4): bl(), vl(), xl(), yl()

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
Cohesion: 0.07
Nodes (67): ad(), Ar(), cr(), dr(), Hr(), kr(), sr(), ac() (+59 more)

### Community 252 - "Community 252"
Cohesion: 0.09
Nodes (51): pn(), w(), r(), A(), am(), b(), c(), cancel() (+43 more)

### Community 290 - "Community 290"
Cohesion: 0.60
Nodes (5): useOverview(), AppHeader(), TableFilterDropdown(), ThresholdDropdown(), useDashboard()

### Community 308 - "Community 308"
Cohesion: 0.20
Nodes (3): clsx(), cn(), ZONE_LABELS

### Community 319 - "Community 319"
Cohesion: 0.15
Nodes (11): compute_delays(), Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Calcula los delays de docenas y columnas dado una lista de números o diccionario, Caso normal: cada numero cae en su docena y columna correcta.         La logica, Si todas las zonas ya salieron, los delays son las distancias al mas reciente., El marcador -1 detiene el conteo de delays., Los ceros (0) incrementan todos los delays sin romper la busqueda.         Con (+3 more)

## Knowledge Gaps
- **126 isolated node(s):** `plugin`, `Connection`, `object`, `int`, `str` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_()` connect `Community 36` to `Community 2`, `Community 135`, `Community 8`, `Community 18`, `Community 21`, `Community 22`, `Community 24`, `Community 27`, `Community 33`, `Community 34`, `Community 37`, `Community 38`, `Community 41`, `Community 43`, `Community 44`, `Community 45`, `Community 47`, `Community 49`, `Community 50`, `Community 54`, `Community 55`, `Community 56`, `Community 58`, `Community 59`, `Community 61`, `Community 62`, `Community 63`, `Community 65`, `Community 66`, `Community 67`, `Community 70`, `Community 72`, `Community 74`, `Community 76`, `Community 81`, `Community 82`, `Community 88`, `Community 89`, `Community 90`, `Community 93`, `Community 96`, `Community 97`, `Community 98`, `Community 235`, `Community 252`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 76` to `Community 68`, `Community 36`, `Community 70`, `Community 71`, `Community 135`, `Community 235`, `Community 77`, `Community 79`, `Community 80`, `Community 81`, `Community 83`, `Community 152`, `Community 24`, `Community 252`, `Community 159`?**
  _High betweenness centrality (0.170) - this node is a cross-community bridge._
- **Why does `_()` connect `Community 135` to `Community 68`, `Community 36`, `Community 71`, `Community 73`, `Community 76`, `Community 151`, `Community 152`, `Community 153`, `Community 252`, `Community 157`, `Community 159`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `$()` (e.g. with `dO()` and `So()`) actually correct?**
  _`$()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `plugin`, `Motores de sincronizacion incremental de backtests. Extraido de db.py/logic.py`, `Motor de sincronizacion incremental compartido por todos los backtests.      M` to the rest of the system?**
  _308 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09615384615384616 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05520614954577219 - nodes in this community are weakly interconnected._