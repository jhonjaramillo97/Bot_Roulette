import { useState, useEffect, useRef } from "react"
import { Link, useLocation } from "react-router-dom"
import { Activity, BarChart3, LayoutGrid, List, Filter, Eye, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/shadcn"
import { useOverview } from "@/hooks/useApi"
import { useDashboard } from "@/lib/DashboardContext"
import { cn } from "@/lib/utils"

function TableFilterDropdown() {
  const { data } = useOverview()
  const { hiddenTables, toggleTable, showAllTables } = useDashboard()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    if (open) document.addEventListener("mousedown", handler)
    return () => document.removeEventListener("mousedown", handler)
  }, [open])

  const tables = data?.tables ?? []
  const allHidden = tables.length > 0 && tables.every((t) => hiddenTables.has(t.table_name))

  return (
    <div ref={ref} className="relative">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setOpen(!open)}
        className="gap-1"
        aria-label="Mostrar / ocultar mesas"
        aria-expanded={open}
      >
        <Eye className="h-3.5 w-3.5" aria-hidden="true" />
        Mesas
        <ChevronDown className={cn("h-3 w-3 ml-0.5 transition-transform", open && "rotate-180")} aria-hidden="true" />
      </Button>

      {open && (
        <div className="absolute right-0 top-full mt-1 w-56 rounded-sm border border-border bg-bg-card shadow-xl z-50">
          <div className="flex items-center justify-between border-b border-border px-3 py-2">
            <span className="text-[10px] uppercase tracking-wider text-text-muted">Mesas visibles</span>
            <button
              onClick={showAllTables}
              className="text-[10px] text-accent hover:text-accent-hover transition-colors"
            >
              Mostrar todas
            </button>
          </div>
          <div className="max-h-[300px] overflow-auto py-1">
            {tables.map((t) => {
              const hidden = hiddenTables.has(t.table_name)
              return (
                <label
                  key={t.table_name}
                  className="flex cursor-pointer items-center gap-2 px-3 py-1.5 hover:bg-bg-card-hover transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={!hidden}
                    onChange={() => toggleTable(t.table_name)}
                    className="h-3.5 w-3.5 rounded-sm border-border bg-bg-card text-accent accent-accent"
                  />
                  <span className={cn("text-xs truncate", hidden ? "text-text-muted" : "text-text")}>
                    {t.name}
                  </span>
                </label>
              )
            })}
          </div>
          {allHidden && (
            <div className="border-t border-border px-3 py-2 text-center text-[10px] text-text-muted">
              Todas las mesas están ocultas
            </div>
          )}
        </div>
      )}
    </div>
  )
}

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
            <TableFilterDropdown />
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