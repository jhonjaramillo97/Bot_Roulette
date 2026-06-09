import { useMemo } from "react"
import { useMesaData } from "@/hooks/useApi"
import { cn, getNumberColor, getDelaySeverity, formatTimeAgo } from "@/lib/utils"
import { Link } from "react-router-dom"

const ZONES = [
  { key: "docena_1", label: "1ª Doc", col: 1, row: "1 / 4" },
  { key: "docena_2", label: "2ª Doc", col: 2, row: "1 / 4" },
  { key: "docena_3", label: "3ª Doc", col: 3, row: "1 / 4" },
  { key: "columna_3", label: "Col 3", col: 4, row: "1" },
  { key: "columna_2", label: "Col 2", col: 4, row: "2" },
  { key: "columna_1", label: "Col 1", col: 4, row: "3" },
]

interface Props {
  tableName: string
  onClose: () => void
}

function getChipBg(severity: string): string {
  switch (severity) {
    case "critical": return "bg-critical-dim border-critical/30 text-critical"
    case "danger": return "bg-danger-dim border-danger/20 text-danger"
    case "warn": return "bg-warn-dim border-warn/20 text-warn"
    default: return "bg-white/[0.03] border-border text-text"
  }
}

export function MesaPopup({ tableName, onClose }: Props) {
  const { data } = useMesaData(tableName)

  const threshold = data?.threshold ?? 12

  const topNumbers = useMemo(() => {
    if (!data?.number_delays) return null
    const entries: { num: number; delay: number }[] = []
    for (const [numStr, delay] of Object.entries(data.number_delays)) {
      const num = Number(numStr)
      if (isNaN(num) || delay <= 0) continue
      entries.push({ num, delay })
    }
    entries.sort((a, b) => b.delay - a.delay)
    const maxShow = data.number_alert_numbers?.length > 0 ? Math.max(data.number_alert_numbers.length, 6) : 10
    return entries.slice(0, maxShow)
  }, [data])

  const hasAnyAlert = (data?.alertas?.length ?? 0) > 0 || (data?.color_streak && data.color_streak.streak >= 5)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose} onKeyDown={(e) => e.key === "Escape" && onClose()}>
      <div role="dialog" aria-modal="true" aria-label={`Vista rápida de ${tableName.replace(/_/g, " ")}`} className="mx-4 max-h-[85vh] w-full max-w-[620px] overflow-auto rounded-sm border border-border bg-bg-card shadow-xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-border bg-bg-card/95 px-4 py-3 backdrop-blur-sm">
          <div className="flex items-center gap-2 min-w-0">
            <span className={cn("h-2 w-2 shrink-0 rounded-full", hasAnyAlert ? "bg-danger shadow-[0_0_4px_var(--color-danger)]" : "bg-safe shadow-[0_0_4px_var(--color-safe)]")} />
            <h3 className="truncate text-sm font-semibold text-text">{tableName.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}</h3>
            {data && <span className="shrink-0 text-[10px] text-text-muted">{formatTimeAgo(data.last_update_seconds)}</span>}
          </div>
          <button onClick={onClose} aria-label="Cerrar" className="text-lg text-text-muted hover:text-text">×</button>
        </div>

        {!data ? (
          <div className="py-10 text-center text-text-muted text-sm">Cargando…</div>
        ) : (
          <div className="px-4 py-3">
            {/* Delay grid - table layout: 3 dozens + column stack */}
            <div className="grid grid-cols-4 grid-rows-3 gap-1.5 mb-3" style={{ minHeight: 160 }}>
              {ZONES.map((zone) => {
                const value = data.delays[zone.key] ?? 0
                const severity = getDelaySeverity(value, threshold)
                const pct = Math.min((value / (threshold * 1.5)) * 100, 100)
                return (
                  <div
                    key={zone.key}
                    className={cn(
                      "flex flex-col items-center justify-center rounded-sm border py-2 transition-colors",
                      zone.key.startsWith("col") ? "" : "",
                      getChipBg(severity),
                      severity === "critical" && "animate-pulse",
                    )}
                    style={{ gridColumn: zone.col, gridRow: zone.row }}
                  >
                    <span className="font-tabular-nums text-lg font-bold leading-none">{value}</span>
                    <span className="mt-0.5 text-[9px] uppercase tracking-wider text-text-muted">{zone.label}</span>
                    <div className="mt-1.5 h-1 w-3/4 overflow-hidden rounded-full bg-white/10">
                      <div className={cn("h-full rounded-full transition-[width] duration-500", severity === "critical" ? "bg-critical" : severity === "danger" ? "bg-danger" : severity === "warn" ? "bg-warn" : "bg-safe")} style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Color streak */}
            {data.color_streak && data.color_streak.streak >= 5 && (
              <div className={cn("mb-3 flex items-center justify-center gap-2 rounded-sm border px-3 py-2 text-xs font-medium", data.color_streak.color === "Red" ? "border-danger/40 bg-danger-dim text-danger" : "border-white/20 bg-white/5 text-text-secondary")}>
                Racha {data.color_streak.color === "Red" ? "Rojos" : "Negros"}: {data.color_streak.streak} consecutivos
              </div>
            )}

            {/* Top number delays */}
            {topNumbers && topNumbers.length > 0 && (
              <div className="mb-3 rounded-sm border border-border/30 bg-black/20 p-3">
                <div className="mb-2 text-[9px] font-semibold uppercase tracking-wider text-text-muted">Mayores Retrasos por Número</div>
                <div className="flex flex-wrap gap-1.5">
                  {topNumbers.map(({ num, delay }) => {
                    const color = getNumberColor(num)
                    const severity = getDelaySeverity(delay, data.number_delay_threshold)
                    return (
                      <div
                        key={num}
                        className={cn(
                          "flex h-10 w-10 flex-col items-center justify-center rounded-full border text-[11px] font-bold text-white",
                          color === "red" && "bg-roulette-red border-red-800/40",
                          color === "black" && "bg-roulette-black border-white/20",
                          color === "green" && "bg-roulette-green border-green-800/40",
                          severity === "critical" && "border-critical shadow-[0_0_12px_rgba(255,0,0,0.5)] animate-pulse",
                          severity === "danger" && "border-danger shadow-[0_0_8px_rgba(255,68,68,0.4)]",
                          severity === "warn" && "border-warn/60 shadow-[0_0_6px_rgba(255,165,0,0.3)]"
                        )}
                      >
                        <span>{num}</span>
                        <span className="text-[8px] opacity-80 leading-none">{delay}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Alertas activas */}
            {data.alertas && data.alertas.length > 0 && (
              <div className="mb-3 rounded-sm border border-danger/20 bg-danger-dim/50 px-3 py-2">
                <div className="text-[10px] font-semibold uppercase tracking-wider text-danger mb-1">Señales Activas</div>
                <div className="flex flex-wrap gap-1">
                  {data.alertas.map((a: string, i: number) => (
                    <span key={i} className="rounded-sm border border-danger/20 bg-danger-dim px-2 py-0.5 text-[10px] text-danger">
                      {a.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Recent history */}
            {data.ultimos && data.ultimos.length > 0 && (
              <div className="mb-3">
                <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Historial Reciente</div>
                <div className="flex gap-1 flex-wrap">
                  {data.ultimos.slice(0, 20).map((spin, i) => (
                    <span
                      key={i}
                      className={cn(
                        "flex h-7 w-7 items-center justify-center rounded-sm text-[10px] font-bold text-white",
                        spin.color === "Red" ? "bg-roulette-red" : spin.color === "Black" ? "bg-roulette-black" : "bg-roulette-green"
                      )}
                    >
                      {spin.numero}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="sticky bottom-0 border-t border-border bg-bg-card/95 px-4 py-2.5 backdrop-blur-sm">
          <Link
            to={`/mesa?mesa=${tableName}`}
            onClick={onClose}
            className="flex items-center justify-center gap-1.5 rounded-sm border border-border bg-bg-card-hover px-4 py-2 text-xs font-semibold text-text-secondary transition-colors hover:border-border-hover hover:text-text"
          >
            Ver detalle completo →
          </Link>
        </div>
      </div>
    </div>
  )
}