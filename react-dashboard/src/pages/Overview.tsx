import { useMemo, useState } from "react"
import { useOverview } from "@/hooks/useApi"
import { useAlertSound } from "@/hooks/useAlert"
import { useDashboard } from "@/lib/DashboardContext"
import { TableCard } from "@/components/overview"
import { MesaPopup } from "@/components/overview/MesaPopup"
import { LoadingOverlay } from "@/components/layout/LoadingOverlay"
import { cn } from "@/lib/utils"

export default function OverviewPage() {
  const { data, isLoading } = useOverview()
  const { viewMode, filterSignals } = useDashboard()
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set())
  const [popupTable, setPopupTable] = useState<string | null>(null)

  const threshold = data?.threshold ?? 12
  const colorStreakThreshold = data?.color_streak_threshold ?? 5
  const tables = data?.tables ?? []

  const totalAlerts = useMemo(() => {
    if (!data) return 0
    return tables.reduce((acc, t) => {
      acc += t.alertas.length
      if (t.color_streak && t.color_streak.streak >= colorStreakThreshold) acc += 1
      if (t.number_alert_count > 0) acc += 1
      return acc
    }, 0)
  }, [data, tables, colorStreakThreshold])

  useAlertSound(totalAlerts)

  const isFresh = tables.some((t) => t.last_update_seconds < 300)
  const hasData = tables.length > 0

  const filteredTables = useMemo(() => {
    if (!filterSignals) return tables
    return tables.filter(
      (t) => t.alertas.length > 0 || (t.color_streak && t.color_streak.streak >= colorStreakThreshold) || t.number_alert_count > 0
    )
  }, [tables, filterSignals, colorStreakThreshold])

  const toggleExpanded = (tableName: string) => {
    setExpandedCards((prev) => {
      const next = new Set(prev)
      if (next.has(tableName)) next.delete(tableName)
      else next.add(tableName)
      return next
    })
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <LoadingOverlay hasData={hasData} isFresh={isFresh} onBypass={() => {}} />

      <div
        className={cn(
          "mx-auto w-full flex-1 overflow-y-auto px-2 py-2",
          viewMode === "grid"
            ? "grid grid-cols-[repeat(auto-fill,minmax(260px,1fr))] gap-2"
            : "flex flex-col gap-1 max-w-[900px]"
        )}
        style={{ maxHeight: "calc(100vh - 50px)" }}
      >
        {isLoading && tables.length === 0 ? (
          <div className="flex items-center justify-center py-20 text-text-secondary">
            Cargando mesas...
          </div>
        ) : (
          filteredTables.map((table) => (
            <TableCard
              key={table.table_name}
              table={table}
              threshold={threshold}
              colorStreakThreshold={colorStreakThreshold}
              viewMode={viewMode}
              isExpanded={expandedCards.has(table.table_name)}
              onToggle={() => toggleExpanded(table.table_name)}
              onNameClick={(name) => setPopupTable(name)}
            />
          ))
        )}
      </div>

      {popupTable && <MesaPopup tableName={popupTable} onClose={() => setPopupTable(null)} />}
    </div>
  )
}