import { useState, useMemo } from "react"
import { useAnalisisGlobal, useSignalDetail } from "@/hooks/useApi"
import { Card, CardContent } from "@/components/ui/shadcn"
import { Tabs, TabsTrigger } from "@/components/ui/Tabs"
import { Link } from "react-router-dom"
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from "recharts"
import { cn } from "@/lib/utils"

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

function fmt(name: string): string {
  return TABLE_NAMES[name] ?? name.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
}

function shortDate(d: string | null): string {
  if (!d) return "En progreso"
  return d.slice(5, 16)
}

type AnalysisTab = "tercios" | "colores" | "numeros"

export default function AnalisisGlobalPage() {
  const { data, isLoading } = useAnalisisGlobal()
  const [tab, setTab] = useState<AnalysisTab>("tercios")
  const [topLimit, setTopLimit] = useState(20)
  const [modal, setModal] = useState<{
    type: "tercios" | "colores" | "numeros"
    tableName: string
    zoneName?: string
    streakColor?: string
    streakCount?: number
    number?: number
    maxDelay: number
    startTime?: string
    endTime?: string
  } | null>(null)

  const threshold = data?.threshold ?? 12

  const sortedHistory = useMemo(() =>
    [...(data?.history ?? [])].sort((a, b) => b.max_delay - a.max_delay)
    , [data])

  const sortedColorHistory = useMemo(() =>
    [...(data?.color_history ?? [])].sort((a, b) => b.streak_count - a.streak_count)
    , [data])

  const effectiveNumberHistory = useMemo(() =>
    [...(data?.active_number_alerts ?? []), ...(data?.number_history ?? [])].sort((a, b) => b.max_delay - a.max_delay)
    , [data])

  const topTercios = useMemo(() => sortedHistory.slice(0, topLimit), [sortedHistory, topLimit])
  const topColores = useMemo(() => sortedColorHistory.slice(0, topLimit), [sortedColorHistory, topLimit])
  const topNumeros = useMemo(() => effectiveNumberHistory.slice(0, topLimit), [effectiveNumberHistory, topLimit])

  const currentData = tab === "tercios" ? topTercios : tab === "colores" ? topColores : topNumeros
  const valueKey = tab === "colores" ? "streak_count" : "max_delay"

  const stats = useMemo(() => {
    const arr = tab === "tercios" ? sortedHistory : tab === "colores" ? sortedColorHistory : effectiveNumberHistory
    const key = tab === "colores" ? "streak_count" : "max_delay"
    const values = arr.map((e: any) => e[key] as number)
    return {
      total: arr.length,
      avg: values.length > 0 ? (values.reduce((a: number, b: number) => a + b, 0) / values.length).toFixed(1) : "0",
      max: values.length > 0 ? Math.max(...values) : 0,
    }
  }, [tab, sortedHistory, sortedColorHistory, effectiveNumberHistory])

  const breakdownData = useMemo(() => {
    const arr = tab === "tercios" ? sortedHistory : tab === "colores" ? sortedColorHistory : effectiveNumberHistory
    const key = tab === "colores" ? "streak_count" : "max_delay"
    const byTable: Record<string, { name: string; count: number; sum: number; max: number }> = {}
    arr.forEach((e: any) => {
      const tn = e.table_name
      if (!byTable[tn]) byTable[tn] = { name: tn, count: 0, sum: 0, max: 0 }
      byTable[tn].count++
      byTable[tn].sum += e[key]
      if (e[key] > byTable[tn].max) byTable[tn].max = e[key]
    })
    return Object.values(byTable).sort((a, b) => b.max - a.max)
  }, [tab, sortedHistory, sortedColorHistory, effectiveNumberHistory])

  if (isLoading || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center text-text-secondary">
        Procesando la base de datos...
      </div>
    )
  }

  const chartTitle = tab === "numeros" ? "Top Retrasos — Numeros" : tab === "tercios" ? "Top Rachas — Tercios" : "Top Rachas — Rojos / Negros"
  const signalsTitle = tab === "numeros" ? "Top Senales — Numeros" : tab === "tercios" ? "Top Senales — Tercios" : "Top Senales — Rojos / Negros"

  return (
    <div className="mx-auto min-h-screen max-w-[1100px] px-4 py-4">
      {/* Header */}
      <div className="mb-4 flex items-center gap-3">
        <Link to="/" className="text-sm font-medium text-accent hover:text-accent-hover">&larr; Volver</Link>
        <h1 className="text-lg font-bold">Analisis Global</h1>
      </div>

      {/* Tabs + Top Limit */}
      <div className="mb-4 flex flex-wrap items-center justify-center gap-3">
        <Tabs value={tab} onValueChange={(v) => setTab(v as AnalysisTab)}>
          <div className="flex gap-0.5">
            <TabsTrigger value="tercios">Tercios</TabsTrigger>
            <TabsTrigger value="colores">Rojos / Negros</TabsTrigger>
            <TabsTrigger value="numeros">Numeros</TabsTrigger>
          </div>
        </Tabs>
        <div className="flex gap-0.5 rounded-lg bg-black/30 p-1">
          {[20, 50, 100].map((n) => (
            <button
              key={n}
              onClick={() => setTopLimit(n)}
              className={cn(
                "rounded-md px-3 py-1.5 text-xs font-semibold transition-colors",
                topLimit === n ? "bg-white/10 text-text shadow-sm" : "text-text-secondary hover:text-text hover:bg-white/5"
              )}
            >
              Top {n}
            </button>
          ))}
        </div>
      </div>

      {/* Stats Summary */}
      <div className="mx-auto mb-5 flex w-fit divide-x divide-border border border-border">
        <div className="flex flex-col items-center justify-center px-8 py-4">
          <span className="font-tabular-nums text-2xl font-semibold leading-none tracking-tight text-text">{stats.total}</span>
          <span className="mt-1.5 text-[11px] tracking-wide text-text-muted">Señales</span>
        </div>
        <div className="flex flex-col items-center justify-center px-8 py-4">
          <span className="font-tabular-nums text-2xl font-semibold leading-none tracking-tight text-text">{stats.avg}</span>
          <span className="mt-1.5 text-[11px] tracking-wide text-text-muted">Pico Prom.</span>
        </div>
        <div className="flex flex-col items-center justify-center px-8 py-4">
          <span className="font-tabular-nums text-2xl font-semibold leading-none tracking-tight text-text">{stats.max}</span>
          <span className="mt-1.5 text-[11px] tracking-wide text-text-muted">Peor Caso</span>
        </div>
      </div>

      {/* Chart - shows ONLY the current tab */}
      <Card className="mb-4 rounded-none">
        <CardContent className="p-0">
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-sm font-semibold">{chartTitle}</h3>
          </div>
          <div className="h-[320px] p-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={currentData as any[]} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={tab === "tercios" ? "#dc5a5a" : tab === "colores" ? "#d4a853" : "#60a5fa"} stopOpacity={0.25} />
                    <stop offset="100%" stopColor={tab === "tercios" ? "#dc5a5a" : tab === "colores" ? "#d4a853" : "#60a5fa"} stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis dataKey="table_name" tick={{ fontSize: 11, fill: "#8a8a9a" }} tickFormatter={(v: string) => fmt(v)} axisLine={false} tickLine={false} dy={8} />
                <YAxis tick={{ fontSize: 11, fill: "#8a8a9a" }} domain={["dataMin - 1", "dataMax + 2"]} axisLine={false} tickLine={false} dx={-4} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#16161d", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 6, fontSize: 12, boxShadow: "0 4px 20px rgba(0,0,0,0.4)" }}
                  labelFormatter={(v: any) => fmt(String(v))}
                  itemStyle={{ color: tab === "tercios" ? "#dc5a5a" : tab === "colores" ? "#d4a853" : "#60a5fa" }}
                  cursor={{ stroke: "rgba(255,255,255,0.08)", strokeDasharray: "4 4" }}
                />
                {tab === "tercios" && threshold > 0 && (
                  <ReferenceLine y={threshold} stroke="#dc5a5a" strokeDasharray="6 4" strokeOpacity={0.4} label={{ value: `Umbral ${threshold}`, position: "right", fill: "#dc5a5a", fontSize: 10 }} />
                )}
                <Area
                  type="monotone"
                  dataKey={valueKey}
                  stroke={tab === "tercios" ? "#dc5a5a" : tab === "colores" ? "#d4a853" : "#60a5fa"}
                  strokeWidth={2}
                  fill="url(#chartGradient)"
                  dot={{ r: 2, strokeWidth: 0 }}
                  activeDot={{ r: 5, strokeWidth: 2, stroke: "#0f0f14", fill: tab === "tercios" ? "#dc5a5a" : tab === "colores" ? "#d4a853" : "#60a5fa" }}
                  name={tab === "colores" ? "Racha" : "Pico"}
                  animationDuration={800}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Top Signals Table */}
      <Card className="mb-4 rounded-none">
        <CardContent className="p-0">
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-sm font-semibold">{signalsTitle}</h3>
          </div>
          <div className="max-h-[500px] overflow-auto">
            {tab === "tercios" && (
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm/95 backdrop-blur-sm">
                  <tr className="border-b border-border">
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">#</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Zona</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Pico</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fin</th>
                  </tr>
                </thead>
                <tbody>
                  {topTercios.map((s, i) => (
                    <tr
                      key={i}
                      className="cursor-pointer border-b border-border/30 hover:bg-bg-card/95 backdrop-blur-sm-hover"
                      onClick={() => setModal({
                        type: "tercios", tableName: s.table_name, zoneName: s.zone_name,
                        maxDelay: s.max_delay, startTime: s.start_time, endTime: s.end_time ?? undefined,
                      })}
                    >
                      <td className="px-3 py-2 text-xs text-text-muted">{i + 1}</td>
                      <td className="px-3 py-2 text-xs font-medium">{fmt(s.table_name)}</td>
                      <td className="px-3 py-2 text-xs">{s.zone_name}</td>
                      <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= threshold ? "text-danger" : "text-text")}>{s.max_delay}</td>
                      <td className="px-3 py-2 text-xs">{shortDate(s.end_time)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {tab === "colores" && (
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm/95 backdrop-blur-sm">
                  <tr className="border-b border-border">
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">#</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Color</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Racha</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fin</th>
                  </tr>
                </thead>
                <tbody>
                  {topColores.map((s, i) => (
                    <tr
                      key={i}
                      className="cursor-pointer border-b border-border/30 hover:bg-bg-card/95 backdrop-blur-sm-hover"
                      onClick={() => setModal({
                        type: "colores", tableName: s.table_name, streakColor: s.streak_color,
                        streakCount: s.streak_count, maxDelay: s.streak_count,
                        startTime: s.start_time, endTime: s.end_time ?? undefined,
                      })}
                    >
                      <td className="px-3 py-2 text-xs text-text-muted">{i + 1}</td>
                      <td className="px-3 py-2 text-xs font-medium">{fmt(s.table_name)}</td>
                      <td className="px-3 py-2">
                        <span className={cn("inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] font-bold", s.streak_color === "Red" ? "border-danger/40 bg-danger-dim text-danger" : "border-white/20 bg-white/5 text-text-secondary")}>
                          {s.streak_color === "Red" ? "Rojos" : "Negros"}
                        </span>
                      </td>
                      <td className="px-3 py-2 font-tabular-nums font-bold">{s.streak_count}</td>
                      <td className="px-3 py-2 text-xs">{shortDate(s.end_time)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {tab === "numeros" && (
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm/95 backdrop-blur-sm">
                  <tr className="border-b border-border">
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">#</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Numero</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Delay Max</th>
                    <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fin</th>
                  </tr>
                </thead>
                <tbody>
                  {topNumeros.map((s: any, i: number) => (
                    <tr
                      key={i}
                      className={cn("cursor-pointer border-b border-border/30 hover:bg-bg-card/95 backdrop-blur-sm-hover", !s.start_time && "bg-critical-dim/20")}
                      onClick={() => setModal({
                        type: "numeros", tableName: s.table_name, number: s.number,
                        maxDelay: s.max_delay, startTime: s.start_time, endTime: s.end_time ?? undefined,
                      })}
                    >
                      <td className="px-3 py-2 text-xs text-text-muted">{i + 1}</td>
                      <td className="px-3 py-2 text-xs font-medium">{fmt(s.table_name)}</td>
                      <td className="px-3 py-2">
                        <span className={cn(
                          "inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold text-white",
                          s.number === 0 ? "bg-roulette-green" : [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(s.number) ? "bg-roulette-red" : "bg-roulette-black"
                        )}>
                          {s.number}
                        </span>
                      </td>
                      <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= 50 ? "text-danger" : "text-text")}>{s.max_delay}</td>
                      <td className="px-3 py-2 text-xs">{shortDate(s.end_time)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Breakdown by Table */}
      <Card className="rounded-none">
        <CardContent className="p-0">
          <div className="border-b border-border px-4 py-3">
            <h3 className="text-sm font-semibold">Desglose por Mesa</h3>
          </div>
          <div className="overflow-auto">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm">
                <tr className="border-b border-border">
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Senales</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Pico Promedio</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Pico Maximo</th>
                </tr>
              </thead>
              <tbody>
                {breakdownData.map((row) => (
                  <tr key={row.name} className="border-b border-border/30 hover:bg-bg-card/95 backdrop-blur-sm-hover">
                    <td className="px-3 py-2 text-xs font-medium">{fmt(row.name)}</td>
                    <td className="px-3 py-2 font-tabular-nums">{row.count}</td>
                    <td className="px-3 py-2 font-tabular-nums">{(row.sum / row.count).toFixed(1)}</td>
                    <td className={cn("px-3 py-2 font-tabular-nums font-bold", row.max >= 20 ? "text-danger" : row.max >= 15 ? "text-warn" : "text-text")}>{row.max}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Signal Detail Modal */}
      {modal && <SignalModal signal={modal} onClose={() => setModal(null)} />}
    </div>
  )
}

function SignalModal({ signal, onClose }: {
  signal: {
    type: "tercios" | "colores" | "numeros"
    tableName: string
    zoneName?: string
    streakColor?: string
    streakCount?: number
    number?: number
    maxDelay: number
    startTime?: string
    endTime?: string
  }
  onClose: () => void
}) {
  const isActive = !signal.startTime
  const { data, isLoading } = useSignalDetail(
    signal.tableName,
    signal.startTime ?? "",
    signal.endTime ?? "",
    signal.maxDelay
  )

  let subtitle = ""
  if (signal.type === "tercios") {
    subtitle = `Zona: ${signal.zoneName} | Pico: ${signal.maxDelay} giros`
  } else if (signal.type === "numeros") {
    subtitle = `Numero: ${signal.number} | Pico: ${signal.maxDelay} giros`
  } else {
    const colorLabel = signal.streakColor === "Red" ? "Rojos" : "Negros"
    subtitle = `Racha: ${signal.streakCount} ${colorLabel}`
  }

  if (isActive) {
    subtitle += " | Senal activa (en progreso)"
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose} onKeyDown={(e) => e.key === "Escape" && onClose()}>
      <div role="dialog" aria-modal="true" aria-label={`Detalle de señal — ${fmt(signal.tableName)}`} className="mx-4 max-h-[70vh] w-full max-w-[500px] overflow-auto rounded-lg border border-border bg-bg-card/95 backdrop-blur-sm" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <h3 className="text-sm font-semibold">{fmt(signal.tableName)}</h3>
          <button onClick={onClose} aria-label="Cerrar modal" className="text-lg text-text-muted hover:text-danger">&times;</button>
        </div>
        <div className="border-b border-border/50 px-4 py-2 text-xs text-text-secondary">{subtitle}</div>
        <div className="max-h-[50vh] overflow-auto">
          {isLoading ? (
            <div className="py-8 text-center text-text-secondary">Cargando…</div>
          ) : data?.plays && data.plays.length > 0 ? (
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-bg-card/95 backdrop-blur-sm">
                <tr className="border-b border-border">
                  <th className="px-3 py-2 text-left text-[10px] font-semibold text-text-muted">#</th>
                  <th className="px-3 py-2 text-left text-[10px] font-semibold text-text-muted">Hora</th>
                  <th className="px-3 py-2 text-left text-[10px] font-semibold text-text-muted">Numero</th>
                  <th className="px-3 py-2 text-left text-[10px] font-semibold text-text-muted">Color</th>
                </tr>
              </thead>
              <tbody>
                {data.plays.map((s: any, i: number) => {
                  const time = s.timestamp ? s.timestamp.split(" ")[1] ?? s.timestamp : "—"
                  const colorClass = s.color === "Red" ? "bg-roulette-red" : s.color === "Black" ? "bg-roulette-black" : "bg-roulette-green"
                  return (
                    <tr key={i} className="border-b border-border/30">
                      <td className="px-3 py-1.5 text-xs text-text-muted">{i + 1}</td>
                      <td className="px-3 py-1.5 font-mono text-xs text-text-secondary">{time}</td>
                      <td className="px-3 py-1.5">
                        <span className={cn("inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold text-white", colorClass)}>
                          {s.numero}
                        </span>
                      </td>
                      <td className="px-3 py-1.5 text-xs">{s.color === "Red" ? "Rojo" : s.color === "Black" ? "Negro" : "Verde"}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          ) : (
            <div className="py-8 text-center text-text-secondary">
              {isActive
                ? "Senal activa: los datos se iran completando a medida que avancen los giros."
                : "No se encontraron jugadas en este rango."}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}