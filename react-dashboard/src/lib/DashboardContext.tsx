import { createContext, useContext, useCallback } from "react"
import { useLocalStorage } from "@/hooks/useAlert"
import { useState } from "react"

interface Thresholds {
  delay: number
  colorStreak: number
  numberDelay: number
}

interface DashboardState {
  viewMode: "list" | "grid"
  setViewMode: (v: "list" | "grid") => void
  filterSignals: boolean
  setFilterSignals: (v: boolean) => void
  hiddenTables: Set<string>
  toggleTable: (name: string) => void
  showAllTables: () => void
  customThresholds: Thresholds | null
  setCustomThresholds: (t: Thresholds | null) => void
}

const DashboardContext = createContext<DashboardState>({
  viewMode: "list",
  setViewMode: () => {},
  filterSignals: false,
  setFilterSignals: () => {},
  hiddenTables: new Set(),
  toggleTable: () => {},
  showAllTables: () => {},
  customThresholds: null,
  setCustomThresholds: () => {},
})

export function useDashboard() {
  return useContext(DashboardContext)
}

export function DashboardProvider({ children }: { children: React.ReactNode }) {
  const [viewMode, setViewMode] = useLocalStorage<"list" | "grid">("dashboardView", "list")
  const [filterSignals, setFilterSignals] = useState(false)
  const [hiddenRaw, setHiddenRaw] = useLocalStorage<string[]>("hiddenTables", [])
  const [customRaw, setCustomRaw] = useLocalStorage<Thresholds | null>("customThresholds", null)

  const hiddenTables = new Set(hiddenRaw)

  const toggleTable = useCallback((name: string) => {
    setHiddenRaw((prev) => {
      if (prev.includes(name)) return prev.filter((n) => n !== name)
      return [...prev, name]
    })
  }, [setHiddenRaw])

  const showAllTables = useCallback(() => {
    setHiddenRaw([])
  }, [setHiddenRaw])

  return (
    <DashboardContext.Provider value={{
      viewMode, setViewMode, filterSignals, setFilterSignals,
      hiddenTables, toggleTable, showAllTables,
      customThresholds: customRaw,
      setCustomThresholds: setCustomRaw,
    }}>
      {children}
    </DashboardContext.Provider>
  )
}