import { createContext, useContext } from "react"
import { useLocalStorage } from "@/hooks/useAlert"
import { useState } from "react"

interface DashboardState {
  viewMode: "list" | "grid"
  setViewMode: (v: "list" | "grid") => void
  filterSignals: boolean
  setFilterSignals: (v: boolean) => void
}

const DashboardContext = createContext<DashboardState>({
  viewMode: "list",
  setViewMode: () => {},
  filterSignals: false,
  setFilterSignals: () => {},
})

export function useDashboard() {
  return useContext(DashboardContext)
}

export function DashboardProvider({ children }: { children: React.ReactNode }) {
  const [viewMode, setViewMode] = useLocalStorage<"list" | "grid">("dashboardView", "list")
  const [filterSignals, setFilterSignals] = useState(false)

  return (
    <DashboardContext.Provider value={{ viewMode, setViewMode, filterSignals, setFilterSignals }}>
      {children}
    </DashboardContext.Provider>
  )
}