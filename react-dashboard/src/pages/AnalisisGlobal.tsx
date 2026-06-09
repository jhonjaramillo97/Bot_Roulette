import { useState } from "react"
import { useAnalisisGlobal, useSignalDetail } from "@/hooks/useApi"
import { Card, CardHeader, CardTitle, CardContent, Badge } from "@/components/ui/shadcn"
import { Tabs, TabsTrigger, TabsContent } from "@/components/ui/Tabs"
import { Link } from "react-router-dom"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import { cn } from "@/lib/utils"

const TABLE_NAMES: Record<string, string> = {
  ruleta_latina: "Ruleta Latina",
  mega_roulette: "Mega Roulette",
  brazilian_roulette: "Brazilian Roulette",
  roulette_1: "Roulette 1",
  roulette_3: "Roulette 3",
  roulette_macao: "Roulette Macao",
  roulette_2_extra_time: "Roulette 2 ET",
  brazilian_mega_roulette: "Brazilian Mega",
  lucky_6_roulette: "Lucky 6",
  auto_roulette: "Auto Roulette",
  stake_roulette: "Stake Roulette",
  turkish_roulette: "Turkish Roulette",
  german_roulette: "German Roulette",
  romanian_roulette: "Romanian Roulette",
  roulette_italia_tricolore: "Italia Tricolore",
  russian_roulette: "Russian Roulette",
  gates_of_olympus_roulette: "Gates of Olympus",
  turkish_mega_roulette: "Turkish Mega",
  mega_roulette_3000: "Mega 3000",
}

function formatShortDate(dateStr: string) {
  if (!dateStr) return "—"
  return dateStr.slice(5, 16).replace(" ", " ")
}

export default function AnalisisGlobalPage() {
  const { data, isLoading } = useAnalisisGlobal()
  const [tab, setTab] = useState("tercios")
  const [selectedSignal, setSelectedSignal] = useState<{ mesa: string; start: string; end: string; pico: number } | null>(null)

  const threshold = data?.threshold ?? 12

  if (isLoading || !data) {
    return (
      <div className="flex min-h-screen items-center justify-center text-text-secondary">
        Cargando análisis global...
      </div>
    )
  }

  const topTercios = data.history
    .sort((a, b) => b.max_delay - a.max_delay)
    .slice(0, 10)

  const topColores = data.color_history
    .sort((a, b) => b.streak_count - a.streak_count)
    .slice(0, 10)

  const topNumeros = data.number_history
    .sort((a, b) => b.max_delay - a.max_delay)
    .slice(0, 10)

  return (
    <div className="mx-auto min-h-screen max-w-[1100px] px-4 py-6">
      <div className="mb-6 flex items-center gap-3">
        <Link to="/" className="text-sm font-medium text-accent hover:text-accent-hover">← Volver</Link>
        <h1 className="text-lg font-bold">Análisis Global</h1>
      </div>

      {/* Stats Summary */}
      <div className="mb-6 grid grid-cols-3 gap-3">
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-xs uppercase tracking-wider text-text-muted">Señales Tercios</div>
            <div className="font-tabular-nums text-2xl font-bold text-accent">{data.history.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-xs uppercase tracking-wider text-text-muted">Rachas Color</div>
            <div className="font-tabular-nums text-2xl font-bold text-danger">{data.color_history.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-xs uppercase tracking-wider text-text-muted">Números Retrasados</div>
            <div className="font-tabular-nums text-2xl font-bold text-warn">{data.number_history.length}</div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="mb-6 space-y-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle>Pico de Delay — Tercios</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={topTercios}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="start_time" tickFormatter={formatShortDate} tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <YAxis tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1a1a24", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, fontSize: 12 }}
                    labelFormatter={(v) => `Inicio: ${v}`}
                  />
                  <Line type="monotone" dataKey="max_delay" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} name="Pico" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle>Rachas de Color</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={topColores}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="start_time" tickFormatter={formatShortDate} tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <YAxis tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1a1a24", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, fontSize: 12 }}
                  />
                  <Line type="monotone" dataKey="streak_count" stroke="#dc5a5a" strokeWidth={2} dot={{ r: 3 }} name="Racha" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle>Retraso por Número</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={topNumeros}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="start_time" tickFormatter={formatShortDate} tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <YAxis tick={{ fontSize: 10, fill: "#8a8a9a" }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1a1a24", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, fontSize: 12 }}
                  />
                  <Line type="monotone" dataKey="max_delay" stroke="#d4a853" strokeWidth={2} dot={{ r: 3 }} name="Delay" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Tables */}
      <Tabs value={tab} onValueChange={setTab}>
        <div className="flex gap-0.5 mb-4">
          <TabsTrigger value="tercios">Tercios</TabsTrigger>
          <TabsTrigger value="colores">Rojos / Negros</TabsTrigger>
          <TabsTrigger value="numeros">Números</TabsTrigger>
        </div>

        <TabsContent value="tercios">
          <Card>
            <CardContent className="p-0">
              <div className="max-h-[500px] overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-bg-card">
                    <tr className="border-b border-border">
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Zona</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Inicio</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Pico</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fin</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.history.sort((a, b) => b.max_delay - a.max_delay).map((s, i) => (
                      <tr
                        key={i}
                        className="cursor-pointer border-b border-border/30 hover:bg-bg-card-hover"
                        onClick={() => setSelectedSignal({ mesa: s.table_name, start: s.start_time, end: s.end_time ?? "", pico: s.max_delay })}
                      >
                        <td className="px-3 py-2 text-xs">{TABLE_NAMES[s.table_name] ?? s.table_name}</td>
                        <td className="px-3 py-2 text-xs">{s.zone_name}</td>
                        <td className="px-3 py-2 text-xs">{formatShortDate(s.start_time)}</td>
                        <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= threshold ? "text-danger" : "text-text")}>{s.max_delay}</td>
                        <td className="px-3 py-2 text-xs">{s.end_time ? formatShortDate(s.end_time) : "Activa"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="colores">
          <Card>
            <CardContent className="p-0">
              <div className="max-h-[500px] overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-bg-card">
                    <tr className="border-b border-border">
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Color</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Racha</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Inicio</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Fin</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.color_history.sort((a, b) => b.streak_count - a.streak_count).map((s, i) => (
                      <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover">
                        <td className="px-3 py-2 text-xs">{TABLE_NAMES[s.table_name] ?? s.table_name}</td>
                        <td className="px-3 py-2">
                          <Badge variant={s.streak_color === "Red" ? "red" : "black"} className="text-[10px]">
                            {s.streak_color === "Red" ? "Rojos" : "Negros"}
                          </Badge>
                        </td>
                        <td className="px-3 py-2 font-tabular-nums font-bold">{s.streak_count}</td>
                        <td className="px-3 py-2 text-xs">{formatShortDate(s.start_time)}</td>
                        <td className="px-3 py-2 text-xs">{s.end_time ? formatShortDate(s.end_time) : "Activa"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="numeros">
          <Card>
            <CardContent className="p-0">
              <div className="max-h-[500px] overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-bg-card">
                    <tr className="border-b border-border">
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Mesa</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Número</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Delay Máx</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Inicio</th>
                      <th className="px-3 py-2 text-left text-xs font-semibold text-text-muted">Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.number_history.sort((a, b) => b.max_delay - a.max_delay).map((s, i) => (
                      <tr key={i} className="border-b border-border/30 hover:bg-bg-card-hover">
                        <td className="px-3 py-2 text-xs">{TABLE_NAMES[s.table_name] ?? s.table_name}</td>
                        <td className="px-3 py-2 font-tabular-nums font-bold">{s.number}</td>
                        <td className={cn("px-3 py-2 font-tabular-nums font-bold", s.max_delay >= 50 ? "text-danger" : "text-text")}>{s.max_delay}</td>
                        <td className="px-3 py-2 text-xs">{formatShortDate(s.start_time)}</td>
                        <td className="px-3 py-2">
                          <Badge variant={s.termination === "normal" ? "safe" : "warn"} className="text-[10px]">
                            {s.termination === "normal" ? "Normal" : "Cadena"}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Signal Detail Modal */}
      {selectedSignal && (
        <SignalModal
          mesa={selectedSignal.mesa}
          start={selectedSignal.start}
          end={selectedSignal.end}
          pico={selectedSignal.pico}
          onClose={() => setSelectedSignal(null)}
        />
      )}
    </div>
  )
}

function SignalModal({ mesa, start, end, pico, onClose }: { mesa: string; start: string; end: string; pico: number; onClose: () => void }) {
  const { data, isLoading } = useSignalDetail(mesa, start, end, pico)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="mx-4 max-h-[70vh] w-full max-w-[600px] overflow-auto rounded-lg border border-border bg-bg-card p-4" onClick={(e) => e.stopPropagation()}>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold">Detalle de Señal</h3>
          <button onClick={onClose} className="text-text-muted hover:text-text text-lg">&times;</button>
        </div>
        {isLoading ? (
          <div className="py-8 text-center text-text-secondary">Cargando...</div>
        ) : data?.spins ? (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="px-2 py-1 text-left text-xs text-text-muted">Número</th>
                <th className="px-2 py-1 text-left text-xs text-text-muted">Color</th>
                <th className="px-2 py-1 text-left text-xs text-text-muted">Hora</th>
              </tr>
            </thead>
            <tbody>
              {data.spins.map((s, i) => (
                <tr key={i} className="border-b border-border/30">
                  <td className="px-2 py-1 font-tabular-nums font-bold">{s.numero}</td>
                  <td className="px-2 py-1">
                    <Badge variant={s.color === "Red" ? "red" : s.color === "Black" ? "black" : "safe"} className="text-[10px]">
                      {s.color}
                    </Badge>
                  </td>
                  <td className="px-2 py-1 text-xs text-text-muted">{s.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="py-8 text-center text-text-secondary">Sin datos</div>
        )}
      </div>
    </div>
  )
}