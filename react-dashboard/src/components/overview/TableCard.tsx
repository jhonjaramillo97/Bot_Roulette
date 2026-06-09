import { memo } from "react"
import type { TableData } from "@/lib/types"
import { cn, getDelaySeverity, formatTimeAgo, getZoneLabel } from "@/lib/utils"
import { Badge } from "@/components/ui/shadcn"
import { Link } from "react-router-dom"

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
  viewMode: "list" | "grid"
  isExpanded: boolean
  onToggle: () => void
}

export const TableCard = memo(function TableCard({
  table,
  threshold,
  colorStreakThreshold,
  viewMode,
  isExpanded,
  onToggle,
}: TableCardProps) {
  const hasColorStreak = table.color_streak && table.color_streak.streak >= colorStreakThreshold
  const hasNumberAlert = table.number_alert_count > 0
  const hasAnyAlert = table.alertas.length > 0 || hasColorStreak || hasNumberAlert

  const maxSeverity = hasAnyAlert
    ? table.alertas.length > 0
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
      className={cn(
        "group rounded-lg border border-border bg-bg-card transition-all hover:bg-bg-card-hover",
        viewMode === "grid" && "hover:-translate-y-0.5 hover:shadow-lg hover:shadow-black/20",
        hasAnyAlert && "border-l-2",
        getSeverityClasses(hasAnyAlert ? maxSeverity : "safe"),
        isExpanded && viewMode === "list" && "bg-bg-card-hover"
      )}
    >
      {/* Header */}
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between px-2.5 py-1.5 text-left"
      >
        <div className="flex items-center gap-1.5 min-w-0">
          <span
            className={cn(
              "h-1.5 w-1.5 shrink-0 rounded-full",
              hasAnyAlert ? "bg-danger shadow-[0_0_4px_var(--color-danger)]" : "bg-safe shadow-[0_0_4px_var(--color-safe)]"
            )}
          />
          <span className="truncate text-xs font-semibold">{table.name}</span>
          <span className="shrink-0 text-[10px] text-text-muted">
            {formatTimeAgo(table.last_update_seconds)}
          </span>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          {hasNumberAlert && (
            <Badge variant="danger" className="text-[9px] px-1 py-0 leading-tight">
              {table.number_alert_count}N
            </Badge>
          )}
          {hasColorStreak && table.color_streak && (
            <Badge variant={table.color_streak.color === "Red" ? "red" : "black"} className="text-[9px] px-1 py-0 leading-tight">
              {table.color_streak.color === "Red" ? "R" : "B"}{table.color_streak.streak}
            </Badge>
          )}
          {table.alertas.length > 0 && (
            <Badge variant="danger" className="text-[9px] px-1 py-0 leading-tight">
              {table.alertas.length}
            </Badge>
          )}
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
                  "flex flex-col items-center justify-center rounded border py-1 transition-all duration-300",
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

        {/* Footer: last numbers + link */}
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
          <Link
            to={`/mesa?mesa=${table.table_name}`}
            className="text-[10px] font-medium text-text-muted transition-colors hover:text-accent"
          >
            Abrir →
          </Link>
        </div>
      </div>
    </div>
  )
})