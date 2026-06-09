import { useState, useEffect } from "react"

interface LoadingOverlayProps {
  isFresh: boolean
  onBypass: () => void
}

export function LoadingOverlay({ isFresh, onBypass }: LoadingOverlayProps) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    if (isFresh) {
      setVisible(false)
    }
  }, [isFresh])

  if (!visible) return null

  return (
    <div
      className={`fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-bg/98 backdrop-blur-xl transition-[opacity,visibility] duration-700 ${
        !visible ? "pointer-events-none opacity-0" : ""
      }`}
    >
      <div className="relative h-20 w-20">
        <div className="absolute inset-0 animate-spin rounded-full border-[3px] border-transparent border-t-accent border-r-safe" />
        <div className="absolute left-1/2 top-1/2 h-2/5 w-2/5 -translate-x-1/2 -translate-y-1/2 animate-pulse rounded-full bg-accent shadow-[0_0_20px_var(--color-accent)]" />
      </div>
      <h2 className="mt-8 text-lg font-semibold tracking-wide">Conectando al Bot...</h2>
      <p className="mt-2 text-sm text-text-secondary">
        {isFresh ? "Datos disponibles" : "Esperando datos frescos de la ruleta"}
      </p>
      <button
        onClick={onBypass}
        className="mt-6 rounded-lg border border-border px-4 py-2 text-sm text-text-secondary transition-colors hover:border-border-hover hover:text-text"
      >
        Ver datos guardados localmente
      </button>
    </div>
  )
}