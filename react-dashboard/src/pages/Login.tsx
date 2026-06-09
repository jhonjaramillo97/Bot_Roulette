import { useState } from "react"
import { LoginBackground } from "./LoginBackground"
import { playClickSound } from "@/lib/utils"

export function LoginPage({ onLogin }: { onLogin: (token: string) => void }) {
  const [token, setToken] = useState("")
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token.trim()) return
    playClickSound()
    setLoading(true)
    setError(false)

    try {
      const res = await fetch(`/api/overview?token=${encodeURIComponent(token.trim())}`)
      if (res.ok) {
        onLogin(token.trim())
      } else {
        setError(true)
      }
    } catch {
      setError(true)
    } finally {
      setLoading(false)
    }
  }

  const isValid = token.trim().length > 0

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center bg-bg">
      <LoginBackground />
      <div className="relative z-10 w-full max-w-[320px] px-4">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="password"
            value={token}
            onChange={(e) => { setToken(e.target.value); setError(false) }}
            placeholder="Ingresa el token…"
            autoFocus
            spellCheck={false}
            autoComplete="off"
            className="w-full rounded-sm border border-border bg-bg-card px-4 py-2.5 text-sm text-text placeholder:text-text-muted outline-none transition-colors focus:border-accent focus:ring-1 focus:ring-accent"
          />
          <button
            type="submit"
            disabled={!isValid || loading}
            className="w-full rounded-sm border border-border bg-white/5 px-4 py-2.5 text-sm font-medium text-text-secondary transition-colors hover:border-border-hover hover:bg-white/10 hover:text-text disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {loading ? "Verificando…" : "Ingresar"}
          </button>
          {error && (
            <p className="text-center text-xs text-danger animate-in fade-in">
              Token incorrecto
            </p>
          )}
        </form>
      </div>
    </div>
  )
}