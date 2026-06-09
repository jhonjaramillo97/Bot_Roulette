import { useMemo, useState } from "react"
import { useSearchParams, useNavigate, Link } from "react-router-dom"
import { useMesaData, useBacktest, useBacktestColor, useBacktestNumber, useMesas } from "@/hooks/useApi"
import { useLocalStorage } from "@/hooks/useAlert"
import type { BacktestSignal, ColorStreakSignal, NumberDelaySignal } from "@/lib/types"
import { Card, CardHeader, CardTitle, CardContent, Badge } from "@/components/ui/shadcn"
import { Tabs, TabsTrigger } from "@/components/ui/Tabs"
import { cn, getDelaySeverity, getNumberColor, formatTimeAgo } from "@/lib/utils"
import { Volume2, VolumeX, BarChart3 } from "lucide-react"

const DOZEN_ZONES = [
  { key: "docena_1", label: "1ª Doc (1-12)" },
  { key: "docena_2", label: "2ª Doc (13-24)" },
  { key: "docena_3", label: "3ª Doc (25-36)" },
]

const COLUMN_ZONES = [
  { key: "columna_3", label: "Col 3 (3,6…)" },
  { key: "columna_2", label: "Col 2 (2,5…)" },
  { key: "columna_1", label: "Col 1 (1,4…)" },
]

const ROULETTE_LAYOUT = [
  [0],
  [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
  [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
  [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
]

const TABLE_NAMES: Record<string, string> = {
  ruleta_latina: "Ruleta Latina",
  mega_roulette: "Mega Roulette",
  brazilian_roulette: "Brazilian Roulette",
  roulette_1: "Roulette 1",
  roulette_3: "Roulette 3",
  roulette_macao: "Roulette Macao",
  roulette_2_extra_time: "Roulette 2 ET",
  brazilian_mega_roulette: "Brazilian Mega",
  lucky_6_roulette: "Lucky 6",
  auto_roulette: "Auto Roulette",
  stake_roulette: "Stake Roulette",
  turkish_roulette: "Turkish Roulette",
  german_roulette: "German Roulette",
  romanian_roulette: "Romanian Roulette",
  roulette_italia_tricolore: "Italia Tricolore",
  russian_roulette: "Russian Roulette",
  gates_of_olympus_roulette: "Gates of Olympus",
  turkish_mega_roulette: "Turkish Mega",
  mega_roulette_3000: "Mega 3000",
}

function formatTableName(name: string): string {
  return TABLE_NAMES[name] ?? name.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
}

export default function MesaDetailPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const table = searchParams.get("mesa") ?? ""

  const { data: mesasList } = useMesas()
  const { data, isLoading } = useMesaData(table)
  const backtest = useBacktest(table)
  const backtestColor = useBacktestColor(table)
  const backtestNumber = useBacktestNumber(table)
  const [soundEnabled, setSoundEnabled] = useLocalStorage("soundEnabled", true)

  const threshold = data?.threshold ?? 12
  const numberDelayThreshold = data?.number_delay_threshold ?? 50

  const numberGrid = useMemo(() => {
    if (!data?.number_delays) return null
    return ROULETTE_LAYOUT.map((row) =>
      row.map((num) => {
        const delay = data.number_delays[String(num)] ?? data.number_delays[num] ?? 0
        const color = getNumberColor(num)
        const severity = delay >= numberDelayThreshold ? "critical" : delay >= numberDelayThreshold - 5 ? "danger" : delay >= numberDelayThreshold - 10 ? "warn" : "safe"
        return { num, delay, color, severity }
      })
    )
  }, [data, numberDelayThreshold])

  if (!table) {
    return (
      <div className="flex min-h-screen items-center justify-center text-text-secondary">
        <div className="text-center">
          <p className="text-lg font-medium mb-2">No se especificó una mesa</p>
          <Link to="/" className="text-accent hover:text-accent-hover text-sm">← Volver al Overview</Link>
        </div>
      </div>
    )
  }

  if (isLoading || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center text-text-secondary">
        Cargando datos de la mesa...
      </div>
    )
  }

  return (
    <div className="mx-auto min-h-screen max-w-[900px] px-4 py-4">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="text-sm font-semibold text-accent hover:text-accent-hover transition-opacity">← Volver</Link>
          <div className="relative">
            <select
              value={table}
              onChange={(e) => navigate(`/mesa?mesa=${e.target.value}`)}
              className="appearance-none rounded-md border border-border bg-bg-card px-3 py-1.5 pr-8 text-sm text-text transition-colors hover:border-border-hover focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
              aria-label="Seleccionar mesa"
            >
              {(mesasList ?? []).map((t: string) => (
                <option key={t} value={t}>
                  {formatTableName(t)}
                </option>
              ))}
            </select>
            <svg className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <span className="text-xs text-text-muted">
            {formatTimeAgo(data.last_update_seconds)}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Link
            to="/analisis"
            className="flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-semibold text-text-secondary transition-colors hover:border-white/20 hover:bg-white/10 hover:text-text"
          >
            <BarChart3 className="h-3.5 w-3.5" />
            Análisis Global
          </Link>
          <button
            onClick={() => setSoundEnabled(!soundEnabled)}
            className="rounded-md border border-border bg-bg-card px-2 py-1.5 text-sm text-text-secondary transition-colors hover:bg-bg-card-hover hover:text-text"
            aria-label={soundEnabled ? "Desactivar sonido de alertas" : "Activar sonido de alertas"}
            title={soundEnabled ? "Sonido activado" : "Sonido desactivado"}
          >
            {soundEnabled ? <Volume2 className="h-4 w-4" aria-hidden="true" /> : <VolumeX className="h-4 w-4" aria-hidden="true" />}
          </button>
        </div>
      </div>

      {/* Betting Table Layout: 3 Dozens + Column Stack */}
      <div className="mb-4 grid grid-cols-4 gap-3" style={{ minHeight: 320 }}>
        {DOZEN_ZONES.map((zone) => {
          const value = data.delays[zone.key] ?? 0
          const severity = getDelaySeverity(value, threshold)
          const pct = Math.min((value / (threshold * 1.5)) * 100, 100)
          return (
            <Card key={zone.key} className={cn("flex flex-col justify-between", severity === "critical" && "border-danger/50 shadow-[0_0_12px_rgba(220,90,90,0.15)]")}>
              <CardHeader className="pb-1">
                <CardTitle className="text-text-muted text-[10px] uppercase tracking-wider">{zone.label}</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-1 flex-col justify-center">
                <div
                  className={cn(
                    "font-tabular-nums text-4xl font-extrabold leading-none",
                    severity === "critical" && "text-critical",
                    severity === "danger" && "text-danger",
                    severity === "warn" && "text-warn",
                    severity === "safe" && "text-safe"
                  )}
                >
                  {value}
                </div>
                <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                  <div
                    className={cn(
                      "h-full rounded-full transition-[width] duration-500",
                      severity === "critical" && "bg-critical",
                      severity === "danger" && "bg-danger",
                      severity === "warn" && "bg-warn",
                      severity === "safe" && "bg-safe"
                    )}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </CardContent>
            </Card>
          )
        })}
        <div className="flex flex-col gap-2">
          {COLUMN_ZONES.map((zone) => {
            const value = data.delays[zone.key] ?? 0
            const severity = getDelaySeverity(value, threshold)
            const pct = Math.min((value / (threshold * 1.5)) * 100, 100)
            return (
              <Card key={zone.key} className={cn("flex-1", severity === "critical" && "border-danger/50 shadow-[0_0_12px_rgba(220,90,90,0.15)]")}>
                <div className="p-3">
                  <div className="text-[10px] uppercase tracking-wider text-text-muted">{zone.label}</div>
                  <div
                    className={cn(
                      "font-tabular-nums text-2xl font-extrabold leading-none",
                      severity === "critical" && "text-critical",
                      severity === "danger" && "text-danger",
                      severity === "warn" && "text-warn",
                      severity === "safe" && "text-safe"
                    )}
                  >
                    {value}
                  </div>
                  <div className="mt-1.5 h-1 w-full overflow-hidden rounded-full bg-white/10">
                    <div
                      className={cn(
                        "h-full rounded-full transition-[width] duration-500",
                        severity === "critical" && "bg-critical",
                        severity === "danger" && "bg-danger",
                        severity === "warn" && "bg-warn",
                        severity === "safe" && "bg-safe"
                      )}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Color Streak Banner */}
      {data.color_streak && data.color_streak.streak >= 5 && (
        <div
          className={cn(
            "mb-4 flex items-center justify-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium",
            data.color_streak.color === "Red"
              ? "border-danger/40 bg-danger-dim text-danger"
              : "border-white/20 bg-white/5 text-text-secondary"
          )}
        >
          Racha {data.color_streak.color === "Red" ? "Rojos" : "Negros"}: {data.color_streak.streak} consecutivos
        </div>
      )}

      {/* Backtest Section */}
      <div className="mt-6 rounded-xl border border-border/50 bg-bg-card p-5">
        <BacktestTabs
          backtest={backtest}
          backtestColor={backtestColor}
          backtestNumber={backtestNumber}
          numberGrid={numberGrid}
          numberDelayThreshold={numberDelayThreshold}
          threshold={threshold}
        />
      </div>

      {/* Last spins footer */}
      {data.ultimos && data.ultimos.length > 0 && (
        <div className="mt-6 rounded-t-lg border-t border-border/50 bg-black/20 px-4 py-3">
          <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">
            Historial Reciente
          </div>
          <div className="flex gap-1.5 overflow-x-auto pb-1">
            {data.ultimos.map((spin, i) => (
              <span
                key={i}
                className={cn(
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-xs font-bold text-white",
                  spin.color === "Red"
                    ? "bg-roulette-red"
                    : spin.color === "Black"
                      ? "bg-roulette-black"
                      : "bg-roulette-green"
                )}
              >
                {spin.numero}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function NumberGrid({ grid }: { grid: { num: number; delay: number; color: "red" | "black" | "green"; severity: string }[][] }) {
  return (
    <div className="flex flex-col items-center gap-1.5 rounded-lg border border-border/30 bg-black/20 p-4">
      <div className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-text-muted">
        Retrasos por Número
      </div>
      {grid.map((row, ri) => (
        <div key={ri} className="flex gap-1">
          {row.map(({ num, delay, color, severity }) => (
            <div
              key={num}
              className={cn(
                "flex h-10 w-10 flex-col items-center justify-center rounded-full border text-[11px] font-bold text-white transition-transform hover:scale-110",
                color === "red" && "bg-roulette-red border-red-800/40",
                color === "black" && "bg-roulette-black border-white/20",
                color === "green" && "bg-roulette-green border-green-800/40",
                severity === "critical" && "border-critical shadow-[0_0_16px_rgba(255,0,0,0.6)] animate-pulse",
                severity === "danger" && "border-danger shadow-[0_0_12px_rgba(255,68,68,0.6)]",
                severity === "warn" && "border-warn/60 shadow-[0_0_8px_rgba(255,165,0,0.5)]"
              )}
            >
              <span>{num}</span>
              <span className="text-[8px] opacity-80">{delay}</span>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

function BacktestTabs({ backtest, backtestColor, backtestNumber, numberGrid, numberDelayThreshold, threshold }: {
  backtest: { data?: BacktestSignal[] | null; isLoading: boolean }
  backtestColor: { data?: ColorStreakSignal[] | null; isLoading: boolean }
  backtestNumber: { data?: { history: NumberDelaySignal[]; active: any[] } | null; isLoading: boolean }
  numberGrid: { num: number; delay: number; color: "red" | "black" | "green"; severity: string }[][] | null
  numberDelayThreshold: number
  threshold: number
}) {
  const [tab, setTab] = useState("tercios")

  return (
    <div>
      {/* Header with title + tabs side by side */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold tracking-wide text-text">
          Historial de Señales Detectadas
        </h2>
        <div className="flex gap-0.5">
          <Tabs value={tab} onValueChange={setTab}>
            <TabsTrigger value="tercios">Tercios</TabsTrigger>
            <TabsTrigger value="colores">Rojos / Negros</TabsTrigger>
            <TabsTrigger value="numeros">Números</TabsTrigger>
          </Tabs>
        </div>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        {/* Tercios */}
        {tab === "tercios" && (
          <div className="max-h-[400px] overflow-auto rounded-md border border-border/50">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Zona</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Delay alcanzado (Pico)</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Ganó en</th>
                </tr>
              </thead>
              <tbody>
                {backtest.isLoading ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando historial…</td></tr>
                ) : (backtest.data ?? []).length === 0 ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Sin señales detectadas</td></tr>
                ) : (backtest.data ?? []).map((s: any, i: number) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover transition-colors">
                    <td className="px-3 py-2 text-xs">{s.start_time?.slice(0, 16)}</td>
                    <td className="px-3 py-2 text-xs">{s.zone_name}</td>
                    <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= threshold ? "text-danger" : "text-text")}>{s.max_delay}</td>
                    <td className="px-3 py-2 text-xs">{s.end_time ? s.end_time.slice(0, 16) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Colores */}
        {tab === "colores" && (
          <div className="max-h-[400px] overflow-auto rounded-md border border-border/50">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Color</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Racha (consecutivos)</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Terminó en</th>
                </tr>
              </thead>
              <tbody>
                {backtestColor.isLoading ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando historial…</td></tr>
                ) : (backtestColor.data ?? []).length === 0 ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Sin señales detectadas</td></tr>
                ) : (backtestColor.data ?? []).map((s: any, i: number) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover transition-colors">
                    <td className="px-3 py-2 text-xs">{s.start_time?.slice(0, 16)}</td>
                    <td className="px-3 py-2">
                      <Badge variant={s.streak_color === "Red" ? "red" : "black"} className="text-[10px]">
                        {s.streak_color === "Red" ? "Rojos" : "Negros"}
                      </Badge>
                    </td>
                    <td className="px-3 py-2 font-tabular-nums font-bold">{s.streak_count}</td>
                    <td className="px-3 py-2 text-xs">{s.end_time ? s.end_time.slice(0, 16) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Números: number grid + table */}
        {tab === "numeros" && (
          <div>
            {numberGrid && <NumberGrid grid={numberGrid} />}
            <div className="mt-4 max-h-[400px] overflow-auto rounded-md border border-border/50">
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm">
                  <tr>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Número</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Delay Máximo</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {backtestNumber.isLoading ? (
                    <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando historial…</td></tr>
                  ) : (backtestNumber.data?.history ?? []).length === 0 ? (
                    <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Sin señales detectadas</td></tr>
                  ) : (backtestNumber.data?.history ?? []).map((s: any, i: number) => (
                    <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover transition-colors">
                      <td className="px-3 py-2 text-xs">{s.start_time?.slice(0, 16)}</td>
                      <td className="px-3 py-2 font-tabular-nums font-bold">{s.number}</td>
                      <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= numberDelayThreshold ? "text-danger" : "text-text")}>{s.max_delay}</td>
                      <td className="px-3 py-2">
                        <Badge variant={s.termination === "normal" ? "safe" : "warn"} className="text-[10px]">
                          {s.termination === "normal" ? "Normal" : "Cadena"}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </Tabs>
    </div>
  )
}