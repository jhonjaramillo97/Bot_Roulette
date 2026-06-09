import type {
  OverviewData,
  MesaData,
  BacktestSignal,
  ColorStreakSignal,
  NumberDelaySignal,
  GlobalAnalysisData,
  SignalDetail,
} from "./types"

const API_BASE = "/api"

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`API Error: ${res.status}`)
  return res.json()
}

export const api = {
  overview: () => fetchJSON<OverviewData>(`${API_BASE}/overview`),

  mesas: () => fetchJSON<string[]>(`${API_BASE}/mesas`).then(data => {
    if (Array.isArray(data)) return data.map((d: any) => d.value ?? d)
    return data as unknown as string[]
  }),

  mesaData: (table: string) =>
    fetchJSON<MesaData>(`${API_BASE}/data?mesa=${encodeURIComponent(table)}`),

  backtest: (table: string) =>
    fetchJSON<BacktestSignal[]>(`${API_BASE}/backtest?mesa=${encodeURIComponent(table)}`),

  backtestColor: (table: string) =>
    fetchJSON<ColorStreakSignal[]>(`${API_BASE}/backtest_color?mesa=${encodeURIComponent(table)}`),

  backtestNumber: (table: string) =>
    fetchJSON<{
      history: NumberDelaySignal[]
      active: { table_name: string; number: number; max_delay: number }[]
    }>(`${API_BASE}/backtest_number?mesa=${encodeURIComponent(table)}`),

  analisisGlobal: () =>
    fetchJSON<GlobalAnalysisData>(`${API_BASE}/analisis_global`),

  signalDetail: (table: string, start: string, end: string, pico: number) =>
    fetchJSON<SignalDetail>(
      `${API_BASE}/signal_detail?mesa=${encodeURIComponent(table)}&start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}&pico=${pico}`
    ),

  tunnel: () => fetchJSON<{ url: string }>(`${API_BASE}/tunnel`),
}

export function createSSEConnection(
  onData: (data: OverviewData) => void,
  onError?: (err: Event) => void
): () => void {
  let reconnectTimer: ReturnType<typeof setTimeout>

  function connect() {
    const source = new EventSource(`${API_BASE}/stream`)
    source.addEventListener("overview", (e) => {
      try {
        onData(JSON.parse(e.data))
      } catch {
        // ignore parse errors
      }
    })
    source.onerror = (e) => {
      onError?.(e)
      source.close()
      reconnectTimer = setTimeout(connect, 3000)
    }
    return () => {
      source.close()
      clearTimeout(reconnectTimer)
    }
  }

  const disconnect = connect()
  return disconnect
}