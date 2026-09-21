import { useCallback, useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import GarageGrid from '../components/GarageGrid'
import LeadForm from '../components/LeadForm'
import { StatsCardSkeleton, GarageGridSkeleton } from '../components/Skeletons'
import { Bike, Clock, Award, TrendingUp, X, FileText, ScanLine, Upload, Save, ShoppingBag, ArrowUpRight, Camera } from 'lucide-react'

export default function Dashboard() {
  const { user, api } = useAuth()
  const [analyses, setAnalyses] = useState([])
  const [selected, setSelected] = useState(null)
  const [nameDraft, setNameDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const dialogRef = useRef(null)
  const selectedId = selected?.id

  useEffect(() => {
    const dialog = dialogRef.current
    if (!selectedId || !dialog) return
    const previousFocus = document.activeElement
    if (!dialog.open) dialog.showModal()
    return () => {
      if (dialog.open) dialog.close()
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus()
    }
  }, [selectedId])

  const keepDialogFocus = (event) => {
    if (event.key !== 'Tab') return
    const controls = [...event.currentTarget.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex="0"]')]
      .filter((element) => element.getClientRects().length > 0)
    const first = controls[0]
    const last = controls[controls.length - 1]
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault()
      last?.focus()
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault()
      first?.focus()
    }
  }

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
      <section className="content-width garage-gate">
        <div><h1>Le tue Vespa.<br /><em>Le loro storie.</em><br />Il tuo garage.</h1><p>Un luogo per custodire fotografie, identificazioni e approfondimenti. Accedi per ritrovare le tue schede o crea il tuo garage gratuito.</p><Link to="/login" className="button button-green">Accedi al garage <ArrowUpRight size={18} /></Link><Link to="/register" className="text-link">Crea account</Link></div>
        <figure><img src={`${import.meta.env.BASE_URL}images/collector-studio.webp`} alt="Scooter storico in atelier, immagine illustrativa generata con AI" width="1536" height="1024" /><figcaption>La tua collezione comincia da una scoperta. Immagine AI illustrativa.</figcaption></figure>
      </section>
    )
  }

  const lastAnalysis = analyses.length > 0
    ? analyses.reduce((latest, a) => !latest || new Date(a.created_at) > new Date(latest.created_at) ? a : latest, null)
    : null

  return (
    <div className="content-width garage-page">
      <div className="garage-heading">
        <div><h1>Il mio garage.</h1><p className="text-vespa-gray text-sm mt-3">Benvenuto, {user.name}. Ogni scoperta trova il suo posto.</p></div>
        <Link to="/analisi" className="button button-green">Aggiungi una Vespa <ArrowUpRight size={18} /></Link>
      </div>

      {!loading && (
        <div className="garage-stats">
          {[
            [Bike, 'Vespe salvate', analyses.length],
            [Award, 'Piano attivo', user.plan || 'Free'],
            [TrendingUp, 'Analisi totali', analyses.length],
            [Clock, 'Ultima analisi', lastAnalysis ? new Date(lastAnalysis.created_at).toLocaleDateString('it-IT') : '—'],
          ].map(([Icon, label, value]) => (
            <div key={label} className="garage-stat">
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
            <ShoppingBag className="h-7 w-7 text-vespa-gold-light" />
            <h3 className="mt-4 font-heading text-2xl font-bold">Completa la storia</h3>
            <p className="mt-2 text-sm leading-6 text-vespa-cream/70">Report Pro, matching colore, verifica originalità e supporto vendita: tutto collegato al mezzo giusto.</p>
          </div>
          <LeadForm garage={analyses} />
        </div>
      </div>

      {selected && (
        <dialog ref={dialogRef} aria-labelledby="vehicle-dialog-title" className="vehicle-dialog" onKeyDown={keepDialogFocus} onCancel={(event) => { event.preventDefault(); setSelected(null) }}>
          <div className="bg-white">
            <h2 id="vehicle-dialog-title" className="sr-only">Scheda di {selected.display_name || selected.model_name || 'Vespa'}</h2>
            <div className="relative h-64 bg-vespa-cream">
              {selected.photo_path ? <img src={`/${selected.photo_path}`} alt={selected.display_name || selected.model_name || 'Il tuo mezzo'} className="h-full w-full object-cover" /> : <div className="vehicle-placeholder"><Camera size={32} strokeWidth={1.3} /><span>Aggiungi una fotografia del tuo mezzo</span></div>}
              <button type="button" aria-label="Chiudi scheda del mezzo" onClick={() => setSelected(null)} className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-vespa-black shadow">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="grid gap-6 p-6 lg:grid-cols-[1.2fr_0.8fr]">
              <div>
                <label htmlFor="garage-name" className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Nome nel garage</label>
                <div className="mt-2 flex gap-2">
                  <input id="garage-name" value={nameDraft} onChange={(e) => setNameDraft(e.target.value)} className="min-w-0 flex-1 rounded-2xl border border-vespa-black/10 px-4 py-3 text-sm outline-none focus:border-vespa-green" />
                  <button type="button" aria-label="Salva nome del mezzo" onClick={saveName} disabled={busy} className="rounded-2xl bg-vespa-black px-4 py-3 text-white"><Save className="h-4 w-4" /></button>
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
                  <button type="button" onClick={user.plan === 'free' ? buyFullReport : runPro} disabled={busy} className="flex w-full items-center justify-center gap-2 rounded-2xl bg-vespa-gold-light px-5 py-4 font-black text-vespa-black">
                    <ScanLine className="h-5 w-5" />
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
        </dialog>
      )}
    </div>
  )
}
