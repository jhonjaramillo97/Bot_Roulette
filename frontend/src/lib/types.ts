export interface OverviewData {
  threshold: number
  color_streak_threshold: number
  number_delay_threshold: number
  tables: TableData[]
}

export interface TableData {
  name: string
  table_name: string
  max_delay: number
  max_zone: string
  delays: Record<string, number>
  alertas: string[]
  ultimo: number | null
  ultimo_color: string | null
  last_10: LastSpin[]
  last_update_seconds: number
  color_streak: ColorStreak | null
  number_delays: Record<string, number>
  number_alert_count: number
  number_alert_numbers: [number, number][]
}

export interface LastSpin {
  val: number
  col: string
}

export interface ColorStreak {
  color: "Red" | "Black" | null
  streak: number
}

export interface MesaData {
  mesa: string
  ultimos: SpinRecord[]
  delays: Record<string, number>
  alertas: string[]
  threshold: number
  color_streak: ColorStreak | null
  color_streak_threshold: number
  number_delays: Record<string, number>
  number_alert_count: number
  number_alert_numbers: [number, number][]
  number_delay_threshold: number
  last_update_seconds: number
}

export interface SpinRecord {
  numero: number
  color: string
  timestamp: string
}

export interface BacktestSignal {
  id?: number
  table_name: string
  zone_name: string
  start_time: string
  end_time: string | null
  max_delay: number
  threshold_used: number
}

export interface ColorStreakSignal {
  id?: number
  table_name: string
  streak_color: string
  streak_count: number
  start_time: string
  end_time: string | null
  threshold_used: number
}

export interface NumberDelaySignal {
  id?: number
  table_name: string
  number: number
  start_time: string
  end_time: string | null
  max_delay: number
  threshold_used: number
  termination: string
}

export interface NumberAlert {
  table_name: string
  number: number
  max_delay: number
}

export interface GlobalAnalysisData {
  history: BacktestSignal[]
  color_history: ColorStreakSignal[]
  number_history: NumberDelaySignal[]
  current_number_delays: Record<string, Record<string, number>>
  active_number_alerts: NumberAlert[]
  threshold: number
  color_streak_threshold: number
  number_delay_threshold: number
}

export interface SignalDetail {
  plays: SpinRecord[]
}

export type ViewMode = "list" | "grid"
export type BacktestTab = "tercios" | "colores" | "numeros"