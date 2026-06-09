import { BrowserRouter, Routes, Route } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { AppHeader } from "@/components/layout/AppHeader"
import { DashboardProvider } from "@/lib/DashboardContext"
import OverviewPage from "@/pages/Overview"
import MesaDetailPage from "@/pages/MesaDetail"
import AnalisisGlobalPage from "@/pages/AnalisisGlobal"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 2,
      retryDelay: 1000,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <DashboardProvider>
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
        </DashboardProvider>
      </BrowserRouter>
    </QueryClientProvider>
  )
}