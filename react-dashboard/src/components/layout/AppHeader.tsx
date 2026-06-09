import { Link, useLocation } from "react-router-dom"
import { Activity, BarChart3, LayoutGrid, List, Filter } from "lucide-react"
import { Button } from "@/components/ui/shadcn"
import { useOverview } from "@/hooks/useApi"
import { useDashboard } from "@/lib/DashboardContext"

export function AppHeader() {
  const location = useLocation()
  const { data } = useOverview()
  const { viewMode, setViewMode, filterSignals, setFilterSignals } = useDashboard()
  const isOverview = location.pathname === "/"

  const links = [
    { to: "/", label: "Overview", icon: LayoutGrid },
    { to: "/analisis", label: "Analisis Global", icon: BarChart3 },
  ]

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between border-b border-border bg-bg/80 px-4 py-2 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <img src="/logo.png" alt="Roulette Sniper" className="h-7" />
        <div className="flex items-center gap-1.5">
          <Activity className="h-2.5 w-2.5 text-safe" aria-hidden="true" />
          <span className="text-xs text-text-secondary">
            {data?.tables ? `${data.tables.length} mesas` : "Conectando…"}
          </span>
        </div>
      </div>

      <nav className="flex items-center gap-1">
        {links.map((link) => {
          const Icon = link.icon
          const isActive = location.pathname === link.to
          return (
            <Link key={link.to} to={link.to}>
              <Button
                variant={isActive ? "default" : "ghost"}
                size="sm"
                className="gap-1.5"
              >
                <Icon className="h-3.5 w-3.5" aria-hidden="true" />
                {link.label}
              </Button>
            </Link>
          )
        })}

        {isOverview && (
          <>
            <div className="mx-1 h-5 w-px bg-border" aria-hidden="true" />
            <Button
              variant={filterSignals ? "danger" : "ghost"}
              size="sm"
              onClick={() => setFilterSignals(!filterSignals)}
              className="gap-1.5"
              aria-label={filterSignals ? "Mostrar todas las mesas" : "Filtrar solo mesas con señales"}
              aria-pressed={filterSignals}
            >
              <Filter className="h-3.5 w-3.5" aria-hidden="true" />
              {filterSignals ? "Todas" : "Señales"}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setViewMode(viewMode === "list" ? "grid" : "list")}
              className="gap-1.5"
              aria-label={viewMode === "list" ? "Cambiar a vista de cuadrícula" : "Cambiar a vista de lista"}
            >
              {viewMode === "list" ? <LayoutGrid className="h-3.5 w-3.5" aria-hidden="true" /> : <List className="h-3.5 w-3.5" aria-hidden="true" />}
              {viewMode === "list" ? "Grid" : "Lista"}
            </Button>
          </>
        )}
      </nav>
    </header>
  )
}