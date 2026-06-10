import { useState, useEffect, useRef, useCallback } from "react"
import type { OverviewData } from "@/lib/types"
import { createSSEConnection } from "@/lib/api"

export function useSSEStream(enabled = true) {
  const [data, setData] = useState<OverviewData | null>(null)
  const [connected, setConnected] = useState(false)
  const disconnectRef = useRef<(() => void) | null>(null)

  const start = useCallback(() => {
    if (!enabled) return
    disconnectRef.current = createSSEConnection(
      (overviewData: OverviewData) => {
        setData(overviewData)
        setConnected(true)
      },
      () => {
        setConnected(false)
      }
    )
  }, [enabled])

  useEffect(() => {
    start()
    return () => {
      disconnectRef.current?.()
    }
  }, [start])

  return { data, connected }
}