import { useState, useEffect, useCallback, useRef } from "react"
import { playAlertSound } from "@/lib/utils"

export function useAlertSound(totalAlerts: number, enabled = true) {
  const previousCount = useRef(0)
  const lastPlayTime = useRef(0)

  useEffect(() => {
    if (!enabled) return
    if (totalAlerts > previousCount.current && previousCount.current >= 0) {
      const now = Date.now()
      if (now - lastPlayTime.current > 3000) {
        playAlertSound()
        lastPlayTime.current = now
      }
    }
    previousCount.current = totalAlerts
  }, [totalAlerts, enabled])
}

export function useLocalStorage<T>(key: string, initial: T): [T, (v: T | ((prev: T) => T)) => void] {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key)
      return item ? (JSON.parse(item) as T) : initial
    } catch {
      return initial
    }
  })

  const set = useCallback(
    (v: T | ((prev: T) => T)) => {
      setValue((prev) => {
        const next = v instanceof Function ? v(prev) : v
        localStorage.setItem(key, JSON.stringify(next))
        return next
      })
    },
    [key]
  )

  return [value, set]
}