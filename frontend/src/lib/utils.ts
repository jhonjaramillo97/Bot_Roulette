export function clsx(...args: (string | undefined | null | false | Record<string, boolean>)[]): string {
  let out = ""
  for (const arg of args) {
    if (!arg) continue
    if (typeof arg === "string") {
      out += (out && " ") + arg
    } else {
      for (const k in arg) {
        if (arg[k]) out += (out && " ") + k
      }
    }
  }
  return out
}

export function cn(...inputs: (string | undefined | null | false | Record<string, boolean>)[]) {
  return clsx(...inputs)
}

export function getChipClass(value: number, threshold: number): string {
  if (value >= threshold) return "critical"
  if (value >= threshold - 2) return "danger"
  if (value >= 6) return "warn"
  return "safe"
}

export function formatTimeAgo(seconds: number): string {
  if (seconds >= 999000) return "Sin datos"
  if (seconds < 60) return `${Math.floor(seconds)}s`
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}m ${secs}s`
}

export function getSpinColorClass(color: string): string {
  switch (color) {
    case "Red":
      return "bg-roulette-red"
    case "Black":
      return "bg-roulette-black"
    case "Green":
      return "bg-roulette-green"
    default:
      return "bg-roulette-green"
  }
}

export function getNumberColor(num: number): "red" | "black" | "green" {
  if (num === 0) return "green"
  const reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
  return reds.includes(num) ? "red" : "black"
}

export function getDelaySeverity(
  value: number,
  threshold: number
): "safe" | "warn" | "critical" {
  if (value >= threshold) return "critical"
  if (value >= threshold - 2) return "warn"
  return "safe"
}

export function playAlertSound(): void {
  try {
    const ctx = new AudioContext()
    const t = ctx.currentTime

    const osc1 = ctx.createOscillator()
    const gain1 = ctx.createGain()
    osc1.type = "triangle"
    osc1.frequency.setValueAtTime(520, t)
    gain1.gain.setValueAtTime(0, t)
    gain1.gain.linearRampToValueAtTime(0.04, t + 0.02)
    gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.35)
    osc1.connect(gain1)
    gain1.connect(ctx.destination)
    osc1.start(t)
    osc1.stop(t + 0.35)

    const osc2 = ctx.createOscillator()
    const gain2 = ctx.createGain()
    osc2.type = "triangle"
    osc2.frequency.setValueAtTime(680, t + 0.08)
    gain2.gain.setValueAtTime(0, t + 0.08)
    gain2.gain.linearRampToValueAtTime(0.03, t + 0.1)
    gain2.gain.exponentialRampToValueAtTime(0.001, t + 0.35)
    osc2.connect(gain2)
    gain2.connect(ctx.destination)
    osc2.start(t + 0.08)
    osc2.stop(t + 0.35)
  } catch {
    // Audio not available
  }
}

export function playClickSound(): void {
  try {
    const ctx = new AudioContext()
    const t = ctx.currentTime
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = "sine"
    osc.frequency.setValueAtTime(600, t)
    gain.gain.setValueAtTime(0, t)
    gain.gain.linearRampToValueAtTime(0.02, t + 0.005)
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.035)
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start(t)
    osc.stop(t + 0.035)
  } catch {
    // Audio not available
  }
}

const ZONE_LABELS: Record<string, string> = {
  docena_1: "1ª Doc",
  docena_2: "2ª Doc",
  docena_3: "3ª Doc",
  columna_1: "Col 1",
  columna_2: "Col 2",
  columna_3: "Col 3",
}

export function getZoneLabel(key: string): string {
  return ZONE_LABELS[key] ?? key
}