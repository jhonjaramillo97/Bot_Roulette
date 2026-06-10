import { useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, useSearchParams } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { AppHeader } from "@/components/layout/AppHeader"
import { DashboardProvider } from "@/lib/DashboardContext"
import { LoginPage } from "@/features/auth/Login"
import OverviewPage from "@/features/overview/Overview"
import MesaDetailPage from "@/features/mesa-detail/MesaDetail"
import AnalisisGlobalPage from "@/features/analytics/AnalisisGlobal"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 2,
      retryDelay: 1000,
    },
  },
})

function AppContent() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [token, setToken] = useState<string | null>(null)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    const urlToken = searchParams.get("token")
    const storedToken = localStorage.getItem("dashboardToken")

    if (urlToken) {
      localStorage.setItem("dashboardToken", urlToken)
      setToken(urlToken)
      if (urlToken === searchParams.get("token")) {
        searchParams.delete("token")
        setSearchParams(searchParams, { replace: true })
      }
    } else if (storedToken) {
      setToken(storedToken)
    }
    setChecking(false)
  }, [])

  const handleLogin = (t: string) => {
    localStorage.setItem("dashboardToken", t)
    setToken(t)
    searchParams.delete("token")
    setSearchParams(searchParams, { replace: true })
  }

  if (checking) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg" />
    )
  }

  if (!token) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <div className="flex min-h-screen flex-col bg-bg text-text">
      <AppHeader />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/mesa" element={<MesaDetailPage />} />
          <Route path="/analisis" element={<AnalisisGlobalPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <DashboardProvider>
          <AppContent />
        </DashboardProvider>
      </BrowserRouter>
    </QueryClientProvider>
  )
}