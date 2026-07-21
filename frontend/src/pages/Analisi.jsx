import { useState } from 'react'
import VespaForm from '../components/VespaForm'
import ResultsCard from '../components/ResultsCard'
import LeadForm from '../components/LeadForm'
import { Search, Sparkles, ShieldCheck, Camera, Gauge } from 'lucide-react'

export default function Analisi() {
  const [result, setResult] = useState(null)
  const [plan, setPlan] = useState('free')

  const handleResult = (data) => {
    setResult(data)
    setPlan(data.plan || 'free')
  }

  return (
    <div className="relative overflow-hidden">
      <section className="dark-panel px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
        <div className="absolute inset-0 vespa-pattern opacity-25" />
        <div className="relative mx-auto max-w-7xl">
          <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-black text-vespa-gold-light">
                <Sparkles className="h-4 w-4" />
                Analisi AI Vespa
              </div>
              <h1 className="mt-7 font-heading text-5xl font-bold leading-[0.95] tracking-[-0.06em] text-white sm:text-6xl">
                Identifica la Vespa. Capisci cosa hai davanti.
              </h1>
              <p className="mt-6 max-w-2xl text-lg leading-8 text-vespa-cream/72">
                Accedi, inserisci telaio, motore, anno e fino a 10 fotografie. Ti restituiamo una scheda pulita con modello probabile,
                anni di produzione, cilindrata e livello di confidenza, salvata nel tuo garage digitale.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-3">
              {[
                [Camera, 'Foto', 'opzionale'],
                [Search, 'Telaio', 'consigliato'],
                [Gauge, 'Output', 'immediato'],
              ].map(([Icon, title, text]) => (
                <div key={title} className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
                  <Icon className="h-6 w-6 text-vespa-gold-light" />
                  <p className="mt-4 font-black text-white">{title}</p>
                  <p className="text-xs uppercase tracking-[0.16em] text-vespa-cream/45">{text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="luxury-card rounded-[2.25rem] p-6 sm:p-8">
            <div className="mb-8 flex items-start gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-vespa-black text-white shadow-xl shadow-vespa-black/15">
                <Search className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-heading text-3xl font-bold text-vespa-black">Dati della Vespa</h2>
                <p className="mt-1 text-sm leading-6 text-vespa-gray">
                  L’identificazione parte dal tuo account: così ogni risultato resta ordinato nel garage digitale.
                </p>
              </div>
            </div>
            <VespaForm onResult={handleResult} />
          </div>

          <div className="space-y-8">
            {result ? (
              <ResultsCard result={result} plan={plan} />
            ) : (
              <div className="dark-panel rounded-[2.25rem] p-8 shadow-[0_32px_90px_rgba(9,13,18,0.22)]">
                <ShieldCheck className="h-10 w-10 text-vespa-gold-light" />
                <h3 className="mt-6 font-heading text-3xl font-bold text-white">Il risultato comparirà qui.</h3>
                <p className="mt-4 text-sm leading-7 text-vespa-cream/68">
                  Visualizzerai modello, anni, cilindrata, confidenza e disclaimer. L’obiettivo è darti un primo responso chiaro,
                  non un certificato ufficiale.
                </p>
              </div>
            )}
            <LeadForm />
          </div>
        </div>
      </section>
    </div>
  )
}
