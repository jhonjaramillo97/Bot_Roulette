import { Link, useLocation } from "react-router-dom"
import { Activity, BarChart3, LayoutGrid } from "lucide-react"
import { Button } from "@/components/ui/shadcn"
import { useOverview } from "@/hooks/useApi"

export function AppHeader() {
  const location = useLocation()
  const { data } = useOverview()
  const tunnelUrl = ""

  const links = [
    { to: "/", label: "Overview", icon: LayoutGrid },
    { to: "/analisis", label: "Analisis Global", icon: BarChart3 },
  ]

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between border-b border-border bg-bg/80 px-4 py-2 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <img src="/logo.png" alt="Roulette Sniper" className="h-8" />
        <div className="flex items-center gap-1.5">
          <Activity className="h-2.5 w-2.5 text-safe" />
          <span className="text-xs text-text-secondary">
            {data?.tables ? `${data.tables.length} mesas` : "Conectando..."}
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
                <Icon className="h-3.5 w-3.5" />
                {link.label}
              </Button>
            </Link>
          )
        })}
      </nav>

      <div className="flex items-center gap-2 text-xs text-text-secondary">
        {tunnelUrl && (
          <a href={tunnelUrl} target="_blank" rel="noopener noreferrer" className="hover:text-text">
            Tunnel activo
          </a>
        )}
      </div>
    </header>
  )
}