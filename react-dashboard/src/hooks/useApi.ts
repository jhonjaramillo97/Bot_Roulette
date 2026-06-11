import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

const POLL_INTERVAL = 1000
const BACKTEST_INTERVAL = 5000

export function useOverview() {
  return useQuery({
    queryKey: ["overview"],
    queryFn: api.overview,
    refetchInterval: POLL_INTERVAL,
    staleTime: POLL_INTERVAL,
  })
}

export function useMesas() {
  return useQuery({
    queryKey: ["mesas"],
    queryFn: api.mesas,
    staleTime: 60_000,
  })
}

export function useMesaData(table: string) {
  return useQuery({
    queryKey: ["mesa", table],
    queryFn: () => api.mesaData(table),
    refetchInterval: POLL_INTERVAL,
    staleTime: POLL_INTERVAL,
    enabled: !!table,
  })
}

export function useBacktest(table: string) {
  return useQuery({
    queryKey: ["backtest", table],
    queryFn: () => api.backtest(table),
    refetchInterval: BACKTEST_INTERVAL,
    staleTime: BACKTEST_INTERVAL,
    enabled: !!table,
  })
}

export function useBacktestColor(table: string) {
  return useQuery({
    queryKey: ["backtest-color", table],
    queryFn: () => api.backtestColor(table),
    refetchInterval: BACKTEST_INTERVAL,
    staleTime: BACKTEST_INTERVAL,
    enabled: !!table,
  })
}

export function useBacktestNumber(table: string) {
  return useQuery({
    queryKey: ["backtest-number", table],
    queryFn: () => api.backtestNumber(table),
    refetchInterval: BACKTEST_INTERVAL,
    staleTime: BACKTEST_INTERVAL,
    enabled: !!table,
  })
}

export function useAnalisisGlobal() {
  return useQuery({
    queryKey: ["analisis-global"],
    queryFn: api.analisisGlobal,
    staleTime: 30_000,
  })
}

export function useSignalDetail(table: string, start: string, end: string, pico: number) {
  return useQuery({
    queryKey: ["signal-detail", table, start, end, pico],
    queryFn: () => api.signalDetail(table, start, end, pico),
    enabled: !!table && pico > 0,
  })
}

export function useTunnel() {
  return useQuery({
    queryKey: ["tunnel"],
    queryFn: api.tunnel,
    refetchInterval: 10_000,
    staleTime: 5_000,
  })
}