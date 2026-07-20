import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import VespaForm from '../components/VespaForm'
import ResultsCard from '../components/ResultsCard'
import LeadForm from '../components/LeadForm'
import ExpertPanel from '../components/ExpertPanel'
import { Camera, CheckCircle, Clock, FileText, Lock, Save, Search, ShieldCheck, Sparkles } from 'lucide-react'

export default function Analisi() {
  const { user, api } = useAuth()
  const [result, setResult] = useState(null)
  const [saveState, setSaveState] = useState({ loading: false, message: '', error: '' })

  const handleResult = (data) => {
    setResult(data)
    setSaveState({ loading: false, message: '', error: '' })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const saveResult = async () => {
    if (!result?.model) return
    setSaveState({ loading: true, message: '', error: '' })
    try {
      const res = await api.post('/vespa/save', {
        model_id: result.model.id,
        model_name: result.model.name,
        year: result.identification?.year_input || null,
        color_hex: result.photo?.dominant_color_hex || null,
        notes: result.recommendations?.join('\n') || '',
        analysis_json: JSON.stringify(result),
      })
      setSaveState({ loading: false, message: res.data.message, error: '' })
    } catch (err) {
      setSaveState({ loading: false, message: '', error: err.response?.data?.detail || 'Impossibile salvare nel garage.' })
    }
  }

  return (
    <div className="bg-[linear-gradient(180deg,#f5f0e8_0%,#fff_42%,#f7f3eb_100%)]">
      <section className="relative overflow-hidden bg-vespa-black text-white">
        <div className="absolute inset-0 opacity-30 bg-[radial-gradient(circle_at_20%_20%,rgba(123,163,90,.45),transparent_30%),radial-gradient(circle_at_80%_0%,rgba(198,164,74,.35),transparent_28%)]" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14">
          <div className="grid lg:grid-cols-[1.1fr_.9fr] gap-10 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-white/10 border border-white/10 text-vespa-cream text-sm font-medium px-4 py-2 rounded-full mb-5">
                <Sparkles className="w-4 h-4 text-vespa-gold" /> Analisi assistita da knowledge base + AI
              </div>
              <h1 className="font-heading text-4xl sm:text-5xl font-bold leading-tight">
                Carica i dati. Ricevi una scheda chiara, utile e prudente.
              </h1>
              <p className="text-vespa-gray-light text-lg mt-5 max-w-2xl leading-relaxed">
                OcchioEsperto combina numeri telaio/motore, anno, foto, colori storici, problemi noti e prezzi indicativi per aiutarti a capire se una Vespa merita attenzione.
              </p>
              <div className="grid sm:grid-cols-3 gap-3 mt-8">
                {[
                  ['1', 'Carica foto e dati'],
                  ['2', 'Controllo storico'],
                  ['3', 'Decisione più sicura'],
                ].map(([n, text]) => (
                  <div key={n} className="rounded-2xl bg-white/10 border border-white/10 p-4">
                    <span className="text-vespa-gold font-bold text-sm">STEP {n}</span>
                    <p className="text-sm mt-1 text-white">{text}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-[2rem] border border-white/10 bg-white/10 p-5 backdrop-blur shadow-2xl">
              <div className="grid grid-cols-2 gap-3 text-sm">
                <TrustItem icon={Camera} title="Foto validata" text="JPG, PNG, WEBP" />
                <TrustItem icon={ShieldCheck} title="Disclaimer chiari" text="Nessuna falsa certezza" />
                <TrustItem icon={FileText} title="Dati storici" text="Modelli, colori, prezzi" />
                <TrustItem icon={Clock} title="Risultato rapido" text="Subito utilizzabile" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.05fr)_minmax(360px,.95fr)] gap-8 items-start">
          <div className="space-y-6">
            <div className="bg-white rounded-[2rem] border border-vespa-cream-dark p-6 sm:p-8 shadow-xl shadow-vespa-green/5">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-2xl bg-vespa-green/10 flex items-center justify-center">
                  <Search className="w-6 h-6 text-vespa-green" />
                </div>
                <div>
                  <h2 className="font-heading font-bold text-vespa-black text-2xl">Analisi veicolo</h2>
                  <p className="text-sm text-vespa-gray">Più informazioni inserisci, più il risultato diventa affidabile.</p>
                </div>
              </div>
              <VespaForm onResult={handleResult} />
            </div>

            <div className="rounded-[2rem] bg-vespa-cream/70 border border-vespa-cream-dark p-6">
              <h3 className="font-heading text-xl font-bold text-vespa-black mb-3">Checklist prima di inviare</h3>
              <div className="grid sm:grid-cols-2 gap-3">
                {['Punzonatura telaio leggibile', 'Numero motore se disponibile', 'Foto laterale ben illuminata', 'Anno libretto o immatricolazione'].map((item) => (
                  <div key={item} className="flex items-center gap-2 text-sm text-vespa-gray"><CheckCircle className="w-4 h-4 text-vespa-green" /> {item}</div>
                ))}
              </div>
            </div>
          </div>

          <aside className="space-y-6 lg:sticky lg:top-24">
            {result ? (
              <>
                <ResultsCard result={result} />
                <div className="bg-white rounded-[2rem] border border-vespa-cream-dark p-5 shadow-lg">
                  {user ? (
                    <button onClick={saveResult} disabled={!result.model || saveState.loading} className="w-full rounded-xl bg-vespa-green hover:bg-vespa-green-light text-white font-semibold py-3 flex items-center justify-center gap-2 disabled:opacity-50">
                      <Save className="w-5 h-5" /> {saveState.loading ? 'Salvataggio...' : 'Salva nel mio garage'}
                    </button>
                  ) : (
                    <Link to="/login" className="w-full rounded-xl bg-vespa-black hover:bg-vespa-black-light text-white font-semibold py-3 flex items-center justify-center gap-2">
                      <Lock className="w-5 h-5" /> Accedi per salvare nel garage
                    </Link>
                  )}
                  {saveState.message && <p className="text-sm text-vespa-green mt-3 text-center">{saveState.message}</p>}
                  {saveState.error && <p className="text-sm text-vespa-red mt-3 text-center">{saveState.error}</p>}
                </div>
                <ExpertPanel result={result} />
              </>
            ) : (
              <div className="bg-white rounded-[2rem] border border-vespa-cream-dark p-7 shadow-xl shadow-vespa-green/5">
                <h3 className="font-heading text-2xl font-bold text-vespa-black mb-3">Qui apparirà la tua scheda</h3>
                <p className="text-sm text-vespa-gray leading-relaxed">Dopo l'invio vedrai modello, attendibilità, colore stimato, possibili problemi, valore indicativo e prossimi passi.</p>
              </div>
            )}
            <LeadForm />
          </aside>
        </div>
      </section>
    </div>
  )
}

function TrustItem({ icon: Icon, title, text }) {
  return (
    <div className="rounded-2xl bg-white text-vespa-black p-4">
      <Icon className="w-5 h-5 text-vespa-green mb-3" />
      <p className="font-semibold">{title}</p>
      <p className="text-xs text-vespa-gray mt-1">{text}</p>
    </div>
  )
}
