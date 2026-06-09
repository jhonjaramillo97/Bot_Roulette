import { useMemo, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { useMesaData, useBacktest, useBacktestColor, useBacktestNumber, useMesas } from "@/hooks/useApi"
import { Card, CardHeader, CardTitle, CardContent, Badge } from "@/components/ui/shadcn"
import { Tabs, TabsTrigger, TabsContent } from "@/components/ui/Tabs"
import { Link } from "react-router-dom"
import { cn, getDelaySeverity, getNumberColor, formatTimeAgo } from "@/lib/utils"

const ZONES = [
  { key: "docena_1", label: "1ª Doc (1-12)", type: "dozen" },
  { key: "docena_2", label: "2ª Doc (13-24)", type: "dozen" },
  { key: "docena_3", label: "3ª Doc (25-36)", type: "dozen" },
  { key: "columna_1", label: "Col 1 (1,4…)", type: "column" },
  { key: "columna_2", label: "Col 2 (2,5…)", type: "column" },
  { key: "columna_3", label: "Col 3 (3,6…)", type: "column" },
]

const ROULETTE_LAYOUT = [
  [0],
  [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
  [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
  [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
]

export default function MesaDetailPage() {
  const [searchParams] = useSearchParams()
  const table = searchParams.get("mesa") ?? ""

  const { data: mesasList } = useMesas()
  const { data } = useMesaData(table)
  const backtest = useBacktest(table)
  const backtestColor = useBacktestColor(table)
  const backtestNumber = useBacktestNumber(table)

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

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center text-text-secondary">
        Cargando datos de la mesa...
      </div>
    )
  }

  return (
    <div className="mx-auto min-h-screen max-w-[900px] px-4 py-4">
      {/* Header */}
      <div className="mb-4 flex items-center gap-3">
        <Link to="/" className="text-sm font-medium text-accent hover:text-accent-hover">← Volver</Link>
        <select
          value={table}
          onChange={(e) => {
            const url = new URL(window.location.href)
            url.searchParams.set("mesa", e.target.value)
            window.location.href = url.toString()
          }}
          className="rounded-md border border-border bg-bg-card px-3 py-1.5 text-sm text-text"
        >
          {mesasList?.map((t: string) => (
            <option key={t} value={t}>
              {t.replace(/_/g, " ").replace(/\b\w/g, (l: string) => l.toUpperCase())}
            </option>
          ))}
        </select>
        <span className="text-xs text-text-muted">
          {formatTimeAgo(data.last_update_seconds)}
        </span>
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

      {/* Dozen & Column Cards */}
      <div className="mb-4 grid grid-cols-4 gap-2" style={{ minHeight: 300 }}>
        {ZONES.filter((z) => z.type === "dozen").map((zone) => {
          const value = data.delays[zone.key] ?? 0
          const severity = getDelaySeverity(value, threshold)
          const pct = Math.min((value / (threshold * 1.5)) * 100, 100)
          return (
            <Card key={zone.key} className={cn(severity === "critical" && "border-danger/50 shadow-[0_0_12px_rgba(220,90,90,0.15)]")}>
              <CardHeader className="pb-1">
                <CardTitle className="text-text-muted">{zone.label}</CardTitle>
              </CardHeader>
              <CardContent>
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
                      "h-full rounded-full transition-all duration-500",
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
          {ZONES.filter((z) => z.type === "column").map((zone) => {
            const value = data.delays[zone.key] ?? 0
            const severity = getDelaySeverity(value, threshold)
            return (
              <Card key={zone.key} className={cn(severity === "critical" && "border-danger/50 shadow-[0_0_12px_rgba(220,90,90,0.15)]")}>
                <CardContent className="p-3">
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
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Number Grid */}
      {numberGrid && (
        <div className="mb-4 flex flex-col items-center gap-1.5 rounded-lg border border-border bg-bg-card p-4">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-text-muted">
            Retrasos por Número
          </div>
          {numberGrid.map((row, ri) => (
            <div key={ri} className="flex gap-1">
              {row.map(({ num, delay, color, severity }) => (
                <div
                  key={num}
                  className={cn(
                    "flex h-9 w-9 flex-col items-center justify-center rounded-full border text-[11px] font-bold text-white transition-transform hover:scale-110",
                    color === "red" && "bg-roulette-red border-red-800/40",
                    color === "black" && "bg-roulette-black border-white/20",
                    color === "green" && "bg-roulette-green border-green-800/40",
                    severity === "critical" && "border-critical shadow-[0_0_12px_rgba(255,59,59,0.4)] animate-pulse",
                    severity === "danger" && "border-danger shadow-[0_0_8px_rgba(220,90,90,0.3)]",
                    severity === "warn" && "border-warn/60"
                  )}
                >
                  <span>{num}</span>
                  <span className="text-[8px] opacity-80">{delay}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {/* Backtest Tabs */}
      <Card>
        <CardHeader>
          <CardTitle>Historial de Señales Detectadas</CardTitle>
        </CardHeader>
        <CardContent>
          <BacktestTabs
            backtest={backtest}
            backtestColor={backtestColor}
            backtestNumber={backtestNumber}
            threshold={threshold}
          />
        </CardContent>
      </Card>

      {/* Last spins */}
      {data.ultimos && data.ultimos.length > 0 && (
        <div className="mt-4 border-t border-border/50 pt-3">
          <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">
            Historial Reciente
          </div>
          <div className="flex gap-1">
            {data.ultimos.map((spin, i) => (
              <span
                key={i}
                className={cn(
                  "flex h-7 w-7 items-center justify-center rounded text-xs font-bold text-white",
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

function BacktestTabs({ backtest, backtestColor, backtestNumber, threshold }: any) {
  const [tab, setTab] = useState("tercios")

  return (
    <div>
      <Tabs value={tab} onValueChange={setTab}>
        <div className="flex items-center justify-between mb-3">
          <div className="flex gap-0.5">
            <TabsTrigger value="tercios">Tercios</TabsTrigger>
            <TabsTrigger value="colores">Rojos / Negros</TabsTrigger>
            <TabsTrigger value="numeros">Números</TabsTrigger>
          </div>
        </div>

        <TabsContent value="tercios">
          <div className="max-h-[400px] overflow-auto rounded-md border border-border/50">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-black/50 backdrop-blur-sm">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Zona</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Pico Delay</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Terminó en</th>
                </tr>
              </thead>
              <tbody>
                {backtest.isLoading ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando...</td></tr>
                ) : (backtest.data ?? []).map((s: any, i: number) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover">
                    <td className="px-3 py-2 text-xs">{s.start_time?.slice(0, 16)}</td>
                    <td className="px-3 py-2 text-xs">{s.zone_name}</td>
                    <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= threshold ? "text-danger" : "text-text")}>{s.max_delay}</td>
                    <td className="px-3 py-2 text-xs">{s.end_time ? s.end_time.slice(0, 16) : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </TabsContent>

        <TabsContent value="colores">
          <div className="max-h-[400px] overflow-auto rounded-md border border-border/50">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-black/50 backdrop-blur-sm">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Color</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Racha</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Terminó en</th>
                </tr>
              </thead>
              <tbody>
                {backtestColor.isLoading ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando...</td></tr>
                ) : (backtestColor.data ?? []).map((s: any, i: number) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover">
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
        </TabsContent>

        <TabsContent value="numeros">
          <div className="max-h-[400px] overflow-auto rounded-md border border-border/50">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-black/50 backdrop-blur-sm">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fecha Inicio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Número</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Delay Máx</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Estado</th>
                </tr>
              </thead>
              <tbody>
                {backtestNumber.isLoading ? (
                  <tr><td colSpan={4} className="px-3 py-6 text-center text-text-muted italic">Cargando...</td></tr>
                ) : (backtestNumber.data?.history ?? []).map((s: any, i: number) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover">
                    <td className="px-3 py-2 text-xs">{s.start_time?.slice(0, 16)}</td>
                    <td className="px-3 py-2 font-tabular-nums font-bold">{s.number}</td>
                    <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= 50 ? "text-danger" : "text-text")}>{s.max_delay}</td>
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
        </TabsContent>
      </Tabs>
    </div>
  )
}