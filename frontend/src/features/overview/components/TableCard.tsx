import { memo } from "react"
import type { TableData } from "@/lib/types"
import { cn, getDelaySeverity, formatTimeAgo, getZoneLabel, getNumberColor, playClickSound } from "@/lib/utils"
import { Badge } from "@/components/ui/shadcn"

function getSeverityClasses(severity: string) {
  switch (severity) {
    case "critical":
      return "border-l-critical bg-critical-dim/50"
    case "danger":
      return "border-l-danger bg-danger-dim/30"
    case "warn":
      return "border-l-warn bg-warn-dim/20"
    default:
      return "border-l-safe/40"
  }
}

function getChipBg(severity: string) {
  switch (severity) {
    case "critical":
      return "bg-critical-dim border-critical/30 text-critical"
    case "danger":
      return "bg-danger-dim border-danger/20 text-danger"
    case "warn":
      return "bg-warn-dim border-warn/20 text-warn"
    default:
      return "bg-white/[0.03] border-border text-text"
  }
}

interface TableCardProps {
  table: TableData
  threshold: number
  colorStreakThreshold: number
  numberDelayThreshold?: number
  viewMode: "list" | "grid"
  isExpanded: boolean
  onToggle: () => void
  onNameClick?: (tableName: string) => void
}

export const TableCard = memo(function TableCard({
  table,
  threshold,
  colorStreakThreshold,
  numberDelayThreshold = 70,
  viewMode,
  isExpanded,
  onToggle,
  onNameClick,
}: TableCardProps) {
  const hasColorStreak = table.color_streak && table.color_streak.streak >= colorStreakThreshold
  const topAlertNums = (table.number_alert_numbers ?? []).filter(([, delay]) => delay >= numberDelayThreshold).slice(0, 3)
  const hasNumberAlert = (table.number_alert_numbers ?? []).some(([, delay]) => delay >= numberDelayThreshold)
  const hasDozenAlert = table.alertas.some((a) => (table.delays[a] ?? 0) >= threshold)
  const hasAnyAlert = hasDozenAlert || hasColorStreak || hasNumberAlert

  const maxSeverity = hasAnyAlert
    ? hasDozenAlert
      ? "danger"
      : hasColorStreak
        ? "warn"
        : "safe"
    : "safe"

  const zoneKeys = ["docena_1", "docena_2", "docena_3", "columna_3", "columna_2", "columna_1"]
  const zoneGridClasses: Record<string, string> = {
    docena_1: "col-start-1 row-start-1 row-end-4",
    docena_2: "col-start-2 row-start-1 row-end-4",
    docena_3: "col-start-3 row-start-1 row-end-4",
    columna_3: "col-start-4 row-start-1",
    columna_2: "col-start-4 row-start-2",
    columna_1: "col-start-4 row-start-3",
  }

  return (
    <div
      onClick={() => { playClickSound(); onNameClick?.(table.table_name) }}
      className={cn(
        "group cursor-pointer rounded-sm border border-border bg-bg-card shadow-sm transition-colors hover:border-border-hover hover:bg-bg-card-hover",
        viewMode === "grid" && "hover:-translate-y-0.5 hover:shadow-lg hover:shadow-black/20",
        hasAnyAlert && "border-l-2",
        getSeverityClasses(hasAnyAlert ? maxSeverity : "safe"),
        isExpanded && viewMode === "list" && "bg-bg-card-hover"
      )}
    >
      {/* Header */}
      <button
        onClick={(e) => { e.stopPropagation(); onToggle() }}
        className="flex w-full items-center justify-between px-2.5 py-1.5 text-left"
      >
        <div className="flex items-center gap-1.5 min-w-0">
          <span
            className={cn(
              "h-1.5 w-1.5 shrink-0 rounded-full",
              hasAnyAlert ? "bg-danger shadow-[0_0_4px_var(--color-danger)]" : "bg-safe shadow-[0_0_4px_var(--color-safe)]"
            )}
          />
          <span
            onClick={(e) => { e.stopPropagation(); onNameClick?.(table.table_name) }}
            className="cursor-pointer truncate text-xs font-semibold transition-colors hover:text-accent"
          >{table.name}</span>
          <span className="shrink-0 text-[10px] text-text-muted">
            {formatTimeAgo(table.last_update_seconds)}
          </span>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          {topAlertNums.length > 0 && topAlertNums.map(([num, delay]) => {
            const numColor = getNumberColor(num)
            return (
              <span key={num} className="group/tip relative flex items-center">
                <span
                  className={cn(
                    "flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold text-white cursor-default",
                    numColor === "red" && "bg-roulette-red",
                    numColor === "black" && "bg-[#2a2a3a]",
                    numColor === "green" && "bg-roulette-green"
                  )}
                >
                  {num}
                </span>
                <span className="pointer-events-none absolute top-5 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-sm border border-border bg-bg-card px-2 py-1 text-[10px] text-text-secondary opacity-0 shadow-lg transition-opacity group-hover/tip:opacity-100 z-[9999]">
                  N°{num} — {delay} giros
                </span>
              </span>
            )
          })}
          {viewMode === "list" && (
            <span className={cn("text-text-muted text-[10px] transition-transform", isExpanded && "rotate-180")}>
              ▼
            </span>
          )}
        </div>
      </button>

      {/* Body */}
      <div
        className={cn(
          "px-2.5 pb-2",
          viewMode === "list" && !isExpanded && "hidden"
        )}
      >
        {/* Delay grid */}
        <div className="grid grid-cols-4 grid-rows-3 gap-px" style={{ minHeight: viewMode === "grid" ? "90px" : undefined }}>
          {zoneKeys.map((key) => {
            const value = table.delays[key]
            if (value === undefined) return null
            const severity = getDelaySeverity(value, threshold)
            return (
              <div
                key={key}
                className={cn(
                  "flex flex-col items-center justify-center rounded-sm border py-1 transition-colors duration-300",
                  zoneGridClasses[key],
                  getChipBg(severity),
                  severity === "critical" && "animate-pulse"
                )}
              >
                <span className="font-tabular-nums text-sm font-bold leading-none">{value}</span>
                <span className="mt-0 text-[8px] uppercase tracking-wider text-text-muted">
                  {getZoneLabel(key)}
                </span>
              </div>
            )
          })}
        </div>

        {/* Footer: last numbers + color streak */}
        <div className="flex items-center justify-between border-t border-border/50 pt-1.5 mt-1.5">
          <div className="flex items-center gap-0.5">
            {table.last_10?.slice(0, 8).map((spin, i) => (
              <span
                key={i}
                className={cn(
                  "flex h-4 w-4 items-center justify-center rounded text-[9px] font-bold text-white",
                  spin.col === "Red"
                    ? "bg-roulette-red"
                    : spin.col === "Black"
                      ? "bg-roulette-black"
                      : "bg-roulette-green"
                )}
              >
                {spin.val}
              </span>
            ))}
          </div>
          {hasColorStreak && table.color_streak && (
            <Badge variant={table.color_streak.color === "Red" ? "red" : "black"} className="text-[9px] px-1.5 py-0 leading-tight shrink-0">
              {table.color_streak.color === "Red" ? "Rojo" : "Negro"} x{table.color_streak.streak}
            </Badge>
          )}
        </div>
      </div>
    </div>
  )
})