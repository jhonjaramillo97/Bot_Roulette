import { useState, useMemo } from "react"
import { useOverview } from "@/hooks/useApi"
import { useAlertSound, useLocalStorage } from "@/hooks/useAlert"
import { TableCard } from "@/components/overview"
import { LoadingOverlay } from "@/components/layout/LoadingOverlay"
import { Button } from "@/components/ui/shadcn"
import { LayoutGrid, List, Filter } from "lucide-react"
import { cn } from "@/lib/utils"

export default function OverviewPage() {
  const { data, isLoading } = useOverview()
  const [viewMode, setViewMode] = useLocalStorage<"list" | "grid">("dashboardView", "list")
  const [filterSignals, setFilterSignals] = useState(false)
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set())

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

  const isFresh = tables.some((t) => t.last_update_seconds < 60)

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
    <div className="flex min-h-screen flex-col">
      <LoadingOverlay isFresh={isFresh} onBypass={() => {}} />

      {/* Header */}
      <div className="border-b border-border px-4 py-4 text-center">
        <img src="/logo.png" alt="Roulette Sniper" className="mx-auto mb-2 h-12" />
        <p className="text-sm text-text-secondary">
          Monitoreo en tiempo real — Click en una mesa para ver detalles
        </p>
        <div className="mt-3 flex items-center justify-center gap-2">
          <Button
            variant={filterSignals ? "danger" : "outline"}
            size="sm"
            onClick={() => setFilterSignals(!filterSignals)}
            className="gap-1.5"
          >
            <Filter className="h-3.5 w-3.5" />
            {filterSignals ? "Mostrar Todas" : "Solo Señales"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setViewMode(viewMode === "list" ? "grid" : "list")}
            className="gap-1.5"
          >
            {viewMode === "list" ? <LayoutGrid className="h-3.5 w-3.5" /> : <List className="h-3.5 w-3.5" />}
            {viewMode === "list" ? "Cuadrícula" : "Lista"}
          </Button>
        </div>
      </div>

      {/* Grid */}
      <div
        className={cn(
          "mx-auto w-full max-w-[1200px] flex-1 overflow-y-auto px-2 py-3",
          viewMode === "grid"
            ? "grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-3"
            : "flex flex-col gap-1.5 max-w-[800px]"
        )}
        style={{ maxHeight: "calc(100vh - 140px)" }}
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
            />
          ))
        )}
      </div>
    </div>
  )
}