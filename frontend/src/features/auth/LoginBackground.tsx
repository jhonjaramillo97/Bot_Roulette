import { useEffect, useRef } from "react"

interface Particle {
  x: number
  y: number
  r: number
  vx: number
  vy: number
  size: number
  alpha: number
  pulse: number
  pulseSpeed: number
}

export function LoginBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let particles: Particle[] = []
    let frame: number
    let w = 0
    let h = 0

    const resize = () => {
      const parent = canvas.parentElement
      if (!parent) return
      w = parent.clientWidth
      h = parent.clientHeight
      canvas.width = w * devicePixelRatio
      canvas.height = h * devicePixelRatio
      canvas.style.width = `${w}px`
      canvas.style.height = `${h}px`
      ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0)
    }

    const init = () => {
      resize()
      particles = []
      const count = Math.floor((w * h) / 8000)
      const cx = w / 2
      const cy = h / 2

      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2
        const dist = Math.random() * Math.max(w, h) * 0.65 + 40
        const speed = (Math.random() * 0.3 + 0.08) * (Math.random() > 0.5 ? 1 : -1)
        particles.push({
          x: cx + Math.cos(angle) * dist,
          y: cy + Math.sin(angle) * dist,
          r: dist,
          vx: speed,
          vy: speed * (0.8 + Math.random() * 0.4),
          size: Math.random() * 1.8 + 0.4,
          alpha: Math.random() * 0.5 + 0.2,
          pulse: Math.random() * Math.PI * 2,
          pulseSpeed: Math.random() * 0.02 + 0.005,
        })
      }
    }

    const draw = () => {
      ctx.fillStyle = "#1a1a1e"
      ctx.fillRect(0, 0, w, h)

      const cx = w / 2
      const cy = h / 2

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i]
        p.pulse += p.pulseSpeed

        const angle = Math.atan2(p.y - cy, p.x - cx)
        const px = cx + Math.cos(angle) * p.r
        const py = cy + Math.sin(angle) * p.r

        p.x += (px - p.x) * 0.002
        p.y += (py - p.y) * 0.002

        const newAngle = angle + p.vx * 0.01
        p.r += (Math.random() - 0.5) * 0.3
        p.r = Math.max(30, Math.min(Math.max(w, h) * 0.7, p.r))

        p.x = cx + Math.cos(newAngle) * p.r
        p.y = cy + Math.sin(newAngle) * p.r

        const distFromCenter = Math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2) / Math.max(w, h)
        const glow = Math.sin(p.pulse) * 0.3 + 0.7
        const alpha = p.alpha * glow * (1 - distFromCenter * 0.2)

        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(180, 180, 190, ${alpha.toFixed(3)})`
        ctx.fill()
      }

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const a = particles[i]
          const b = particles[j]
          const dx = a.x - b.x
          const dy = a.y - b.y
          const dist = Math.sqrt(dx * dx + dy * dy)

          if (dist < 40 && dist > 0) {
            const lineAlpha = (1 - dist / 40) * 0.04
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.strokeStyle = `rgba(140, 140, 160, ${lineAlpha.toFixed(3)})`
            ctx.lineWidth = 0.5
            ctx.stroke()
          }
        }
      }

      frame = requestAnimationFrame(draw)
    }

    init()
    draw()

    const onResize = () => { init() }
    window.addEventListener("resize", onResize)

    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener("resize", onResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0"
      aria-hidden="true"
    />
  )
}