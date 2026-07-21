import { useCallback, useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import GarageGrid from '../components/GarageGrid'
import LeadForm from '../components/LeadForm'
import { StatsCardSkeleton, GarageGridSkeleton } from '../components/Skeletons'
import { Bike, Clock, Award, TrendingUp, X, FileText, Sparkles, Upload, Save, ShoppingBag } from 'lucide-react'

export default function Dashboard() {
  const { user, api } = useAuth()
  const [analyses, setAnalyses] = useState([])
  const [selected, setSelected] = useState(null)
  const [nameDraft, setNameDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)

  const refreshGarage = useCallback(() => api.get('/vespa/garage').then((res) => {
    const items = res.data.vespe || []
    setAnalyses(items)
    if (selected) setSelected(items.find((item) => item.id === selected.id) || null)
  }), [api, selected])

  useEffect(() => {
    if (user) {
      refreshGarage().catch(() => {}).finally(() => setLoading(false))
    }
  }, [user, refreshGarage])

  const openVehicle = async (item) => {
    const res = await api.get(`/vespa/garage/${item.id}`)
    setSelected(res.data)
    setNameDraft(res.data.display_name || res.data.model_name || '')
  }

  const saveName = async () => {
    if (!selected) return
    setBusy(true)
    try {
      const res = await api.patch(`/vespa/garage/${selected.id}`, { display_name: nameDraft })
      setSelected(res.data)
      await refreshGarage()
    } finally {
      setBusy(false)
    }
  }

  const uploadPhoto = async (file) => {
    if (!selected || !file) return
    const payload = new FormData()
    payload.append('photo', file)
    setBusy(true)
    try {
      const res = await api.post(`/vespa/garage/${selected.id}/photo`, payload, { headers: { 'Content-Type': 'multipart/form-data' } })
      setSelected(res.data)
      await refreshGarage()
    } finally {
      setBusy(false)
    }
  }

  const buyFullReport = async () => {
    const res = await api.post('/payments/create-checkout', {
      plan: 'avanzato',
      success_url: `${window.location.origin}/dashboard`,
      cancel_url: `${window.location.origin}/dashboard`,
    })
    window.location.href = res.data.session_url
  }

  const runPro = async () => {
    if (!selected) return
    setBusy(true)
    try {
      const res = await api.post(`/vespa/garage/${selected.id}/pro-analysis`)
      setSelected(res.data)
      await refreshGarage()
    } finally {
      setBusy(false)
    }
  }

  if (!user) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="text-center animate-fade-in-up">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-vespa-cream-dark flex items-center justify-center">
            <Bike className="w-10 h-10 text-vespa-gray-light" />
          </div>
          <h2 className="font-heading text-2xl font-bold text-vespa-black mb-4">Accedi per vedere il tuo garage</h2>
          <p className="text-vespa-gray">Effettua il login per visualizzare le tue Vespe salvate.</p>
        </div>
      </div>
    )
  }

  const lastAnalysis = analyses.length > 0
    ? analyses.reduce((latest, a) => !latest || new Date(a.created_at) > new Date(latest.created_at) ? a : latest, null)
    : null

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="mb-8 animate-fade-in-up">
        <h1 className="font-heading text-3xl font-bold text-vespa-black">Il mio garage</h1>
        <p className="text-vespa-gray text-sm mt-1">Benvenuto, {user.name}</p>
      </div>

      {!loading && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8 animate-fade-in-up-delay-1">
          {[
            [Bike, 'Vespe salvate', analyses.length],
            [Award, 'Piano attivo', user.plan || 'Free'],
            [TrendingUp, 'Analisi totali', analyses.length],
            [Clock, 'Ultima analisi', lastAnalysis ? new Date(lastAnalysis.created_at).toLocaleDateString('it-IT') : '—'],
          ].map(([Icon, label, value]) => (
            <div key={label} className="bg-white rounded-xl border border-vespa-cream-dark p-5 transition-all duration-300 hover:shadow-md hover:border-vespa-green/30">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-vespa-green/10 flex items-center justify-center">
                  <Icon className="w-5 h-5 text-vespa-green" />
                </div>
                <div>
                  <p className="text-xs text-vespa-gray font-medium">{label}</p>
                  <p className="text-lg font-bold text-vespa-black font-heading capitalize">{value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {loading && <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">{[1, 2, 3, 4].map((i) => <StatsCardSkeleton key={i} />)}</div>}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          {loading ? <GarageGridSkeleton /> : <GarageGrid analyses={analyses} onSelect={openVehicle} />}
        </div>

        <div className="space-y-6">
          <div className="rounded-[2rem] bg-vespa-black p-6 text-white shadow-xl">
            <ShoppingBag className="h-7 w-7 text-vespa-gold" />
            <h3 className="mt-4 font-heading text-2xl font-bold">Completa la storia</h3>
            <p className="mt-2 text-sm leading-6 text-vespa-cream/70">Report Pro, matching colore, verifica originalità e supporto vendita: tutto collegato al mezzo giusto.</p>
          </div>
          <LeadForm garage={analyses} />
        </div>
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-vespa-black/60 p-4 backdrop-blur-sm">
          <div className="mx-auto my-8 max-w-4xl overflow-hidden rounded-[2rem] bg-white shadow-2xl">
            <div className="relative h-64 bg-vespa-cream">
              <img src={selected.photo_path ? `/${selected.photo_path}` : '/hero-vespa.svg'} alt={selected.display_name} className="h-full w-full object-cover" />
              <button type="button" onClick={() => setSelected(null)} className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-vespa-black shadow">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="grid gap-6 p-6 lg:grid-cols-[1.2fr_0.8fr]">
              <div>
                <label className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Nome nel garage</label>
                <div className="mt-2 flex gap-2">
                  <input value={nameDraft} onChange={(e) => setNameDraft(e.target.value)} className="flex-1 rounded-2xl border border-vespa-black/10 px-4 py-3 text-sm outline-none focus:border-vespa-green" />
                  <button type="button" onClick={saveName} disabled={busy} className="rounded-2xl bg-vespa-black px-4 py-3 text-white"><Save className="h-4 w-4" /></button>
                </div>

                <div className="mt-6 grid grid-cols-2 gap-3 text-sm">
                  {[
                    ['Modello', selected.model_name],
                    ['Anno', selected.year || '—'],
                    ['Telaio', selected.frame_number || '—'],
                    ['Motore', selected.engine_number || '—'],
                    ['Livello analisi', selected.analysis_level === 'basic' ? 'Base' : 'Pro'],
                    ['Garage ID', selected.id],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-2xl bg-vespa-cream p-4">
                      <p className="text-xs font-black uppercase tracking-[0.12em] text-vespa-gray">{label}</p>
                      <p className="mt-1 font-bold text-vespa-black">{value}</p>
                    </div>
                  ))}
                </div>

                {selected.analysis?.expert_analysis && (
                  <div className="mt-6 rounded-2xl border border-vespa-green/15 bg-vespa-green/5 p-4">
                    <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Vecchia analisi</p>
                    <p className="mt-2 text-sm leading-6 text-vespa-gray">{selected.analysis.expert_analysis.expert_summary}</p>
                  </div>
                )}
              </div>

              <div className="space-y-4">
                <label className="flex cursor-pointer items-center justify-center gap-2 rounded-2xl border border-dashed border-vespa-black/20 bg-vespa-cream p-4 text-sm font-black text-vespa-black">
                  <Upload className="h-4 w-4" />
                  Scegli immagine
                  <input type="file" accept="image/*" className="sr-only" onChange={(e) => uploadPhoto(e.target.files?.[0])} />
                </label>

                {selected.analysis_level === 'basic' ? (
                  <button type="button" onClick={user.plan === 'free' ? buyFullReport : runPro} disabled={busy} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-vespa-gold px-5 py-4 font-black text-vespa-black">
                    <Sparkles className="h-5 w-5" />
                    {user.plan === 'free' ? 'Sblocca analisi Pro' : 'Approfondisci questo veicolo'}
                  </button>
                ) : (
                  <a href={`/api/vespa/garage/${selected.id}/report.pdf`} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-vespa-black px-5 py-4 font-black text-white">
                    <FileText className="h-5 w-5" />
                    Scarica report Pro PDF
                  </a>
                )}

                <div className="rounded-2xl bg-vespa-black p-5 text-white">
                  <p className="font-heading text-xl font-bold">Ti serve di più?</p>
                  <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-vespa-cream/75">
                    <li>Matching colore originale</li>
                    <li>Range telaio e motore</li>
                    <li>Valutazione vendita assistita</li>
                    <li>Check originalità e dettagli storici</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
