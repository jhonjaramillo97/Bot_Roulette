import { useState, useEffect, useRef } from "react"
import { Link, useLocation } from "react-router-dom"
import { Activity, BarChart3, LayoutGrid, List, Filter, Eye, ChevronDown, SlidersHorizontal } from "lucide-react"
import { Button } from "@/components/ui/shadcn"
import { useOverview } from "@/hooks/useApi"
import { useDashboard } from "@/lib/DashboardContext"
import { cn, playClickSound } from "@/lib/utils"

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
        onClick={() => { playClickSound(); setOpen(!open) }}
        className="gap-1"
        aria-label="Mostrar / ocultar mesas"
        aria-expanded={open}
      >
        <Eye className="h-3.5 w-3.5" aria-hidden="true" />
        <span className="hidden sm:inline">Mesas</span>
        <ChevronDown className={cn("h-3 w-3 ml-0.5 transition-transform", open && "rotate-180")} aria-hidden="true" />
      </Button>

      {open && (
        <div className="absolute right-0 top-full mt-1 w-56 rounded-sm border border-border bg-bg-card shadow-xl z-50">
          <div className="flex items-center justify-between border-b border-border px-3 py-2">
            <span className="text-[10px] uppercase tracking-wider text-text-muted">Mesas visibles</span>
            <button
              onClick={() => { playClickSound(); showAllTables() }}
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

function ThresholdDropdown() {
  const { data } = useOverview()
  const { customThresholds, setCustomThresholds } = useDashboard()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    if (open) document.addEventListener("mousedown", handler)
    return () => document.removeEventListener("mousedown", handler)
  }, [open])

  const apiThreshold = data?.threshold ?? 15
  const apiColorStreak = data?.color_streak_threshold ?? 8
  const apiNumberDelay = data?.number_delay_threshold ?? 70

  const current = {
    delay: customThresholds?.delay ?? apiThreshold,
    colorStreak: customThresholds?.colorStreak ?? apiColorStreak,
    numberDelay: customThresholds?.numberDelay ?? apiNumberDelay,
  }

  const hasCustom = customThresholds !== null

  const update = (key: keyof typeof current, value: number) => {
    setCustomThresholds({
      delay: key === "delay" ? value : current.delay,
      colorStreak: key === "colorStreak" ? value : current.colorStreak,
      numberDelay: key === "numberDelay" ? value : current.numberDelay,
    })
  }

  const reset = () => { playClickSound(); setCustomThresholds(null) }

  const sliderClass = (hasCustom: boolean) => cn(
    "w-full cursor-pointer appearance-none rounded-full h-1.5",
    "bg-white/10",
    "[&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:cursor-pointer",
    hasCustom
      ? "[&::-webkit-slider-thumb]:bg-accent [&::-webkit-slider-thumb]:shadow-[0_0_8px_var(--color-accent)]"
      : "[&::-webkit-slider-thumb]:bg-text-muted"
  )

  return (
    <div ref={ref} className="relative">
      <Button
        variant={hasCustom ? "default" : "ghost"}
        size="sm"
        onClick={() => { playClickSound(); setOpen(!open) }}
        className="gap-1.5"
        aria-label="Ajustar umbrales de alerta"
        aria-expanded={open}
      >
        <SlidersHorizontal className="h-3.5 w-3.5" aria-hidden="true" />
        <span className="hidden sm:inline">Ajustes</span>
      </Button>

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute right-0 top-full mt-1 w-64 rounded-sm border border-border bg-bg-card shadow-xl z-50">
            <div className="flex items-center justify-between border-b border-border px-3 py-2">
              <span className="text-[10px] uppercase tracking-wider text-text-muted">Umbrales</span>
              <button
                onClick={reset}
                className={cn("text-[10px] transition-colors", hasCustom ? "text-accent hover:text-accent-hover" : "text-text-muted")}
              >
                Restablecer
              </button>
            </div>

            <div className="px-3 py-2 space-y-4">
              {/* Docenas / Columnas */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] text-text-secondary">Docenas / Columnas</span>
                  <span className="font-tabular-nums text-xs font-semibold text-text">{current.delay}</span>
                </div>
                <input
                  type="range"
                  min={5}
                  max={30}
                  step={1}
                  value={current.delay}
                  onChange={(e) => update("delay", Number(e.target.value))}
                  className={sliderClass(current.delay !== apiThreshold)}
                />
                <div className="flex items-center justify-between mt-0.5 text-[8px] text-text-muted">
                  <span>5</span>
                  <span>30</span>
                </div>
              </div>

              {/* Racha Rojo / Negro */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] text-text-secondary">Racha Rojo / Negro</span>
                  <span className="font-tabular-nums text-xs font-semibold text-text">{current.colorStreak}</span>
                </div>
                <input
                  type="range"
                  min={3}
                  max={20}
                  step={1}
                  value={current.colorStreak}
                  onChange={(e) => update("colorStreak", Number(e.target.value))}
                  className={sliderClass(current.colorStreak !== apiColorStreak)}
                />
                <div className="flex items-center justify-between mt-0.5 text-[8px] text-text-muted">
                  <span>3</span>
                  <span>20</span>
                </div>
              </div>

              {/* Números */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] text-text-secondary">Números</span>
                  <span className="font-tabular-nums text-xs font-semibold text-text">{current.numberDelay}</span>
                </div>
                <input
                  type="range"
                  min={50}
                  max={200}
                  step={5}
                  value={current.numberDelay}
                  onChange={(e) => update("numberDelay", Number(e.target.value))}
                  className={sliderClass(current.numberDelay !== apiNumberDelay)}
                />
                <div className="flex items-center justify-between mt-0.5 text-[8px] text-text-muted">
                  <span>50</span>
                  <span>200</span>
                </div>
              </div>

              {!hasCustom && (
                <div className="text-center text-[9px] text-text-muted pt-1">
                  Usando valores por defecto del bot
                </div>
              )}
            </div>
          </div>
        </>
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
    <header className="sticky top-0 z-50 flex items-center justify-between border-b border-border bg-bg/80 px-2 sm:px-4 py-2 backdrop-blur-md">
      <div className="flex items-center gap-2 sm:gap-3">
        <img src="/logo.png" alt="Roulette Sniper" className="h-6 sm:h-7" />
        <div className="hidden sm:flex items-center gap-1.5">
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
                className="gap-1 sm:gap-1.5 px-2 sm:px-3"
                onClick={playClickSound}
              >
                <Icon className="h-3.5 w-3.5" aria-hidden="true" />
                <span className="hidden sm:inline">{link.label}</span>
              </Button>
            </Link>
          )
        })}

        {isOverview && (
          <>
            <div className="mx-1 h-5 w-px bg-border hidden sm:block" aria-hidden="true" />
            <ThresholdDropdown />
            <TableFilterDropdown />
            <Button
              variant={filterSignals ? "danger" : "ghost"}
              size="sm"
              onClick={() => { playClickSound(); setFilterSignals(!filterSignals) }}
              className="gap-1 sm:gap-1.5 px-2 sm:px-3"
              aria-label={filterSignals ? "Mostrar todas las mesas" : "Filtrar solo mesas con señales"}
              aria-pressed={filterSignals}
            >
              <Filter className="h-3.5 w-3.5" aria-hidden="true" />
              <span className="hidden sm:inline">{filterSignals ? "Todas" : "Señales"}</span>
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => { playClickSound(); setViewMode(viewMode === "list" ? "grid" : "list") }}
              className="gap-1 sm:gap-1.5 px-2 sm:px-3"
              aria-label={viewMode === "list" ? "Cambiar a vista de cuadrícula" : "Cambiar a vista de lista"}
            >
              {viewMode === "list" ? <LayoutGrid className="h-3.5 w-3.5" aria-hidden="true" /> : <List className="h-3.5 w-3.5" aria-hidden="true" />}
              <span className="hidden sm:inline">{viewMode === "list" ? "Grid" : "Lista"}</span>
            </Button>
          </>
        )}
      </nav>
    </header>
  )
}