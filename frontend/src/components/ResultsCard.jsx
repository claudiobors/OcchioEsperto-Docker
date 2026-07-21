import { CheckCircle, AlertTriangle, XCircle, Gauge, Brain, ClipboardCheck } from 'lucide-react'

const badges = {
  free: { label: 'Base', class: 'bg-vespa-black text-white' },
  premium: { label: 'Premium', class: 'bg-vespa-gold text-vespa-black' },
}

export default function ResultsCard({ result, plan = 'free' }) {
  if (!result) return null

  const badge = badges[plan] || badges.free
  const modelName = result.model?.name || result.modello
  const productionYears = result.identification?.years || result.expert_analysis?.years || result.anno
  const engineCc = result.identification?.engine_cc || result.model?.engine_cc || result.expert_analysis?.engine_cc
  const confidenceLabel = {
    high: 'Alta',
    medium: 'Media',
    low: 'Bassa',
  }[result.confidence] || result.confidence
  const confidencePercent = result.confidenza
  const confidenceIcon = confidencePercent
    ? confidencePercent > 80 ? CheckCircle : confidencePercent > 50 ? AlertTriangle : XCircle
    : result.confidence === 'high' ? CheckCircle : result.confidence === 'medium' ? AlertTriangle : XCircle
  const ConfidenceIcon = confidenceIcon
  const expert = result.expert_analysis

  return (
    <div className="animate-scale-in overflow-hidden rounded-[2.25rem] bg-white shadow-[0_30px_90px_rgba(9,13,18,0.14)] ring-1 ring-vespa-black/10">
      <div className="dark-panel p-7">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-black uppercase tracking-[0.22em] text-vespa-gold-light">Risultato</p>
            <h3 className="mt-2 font-heading text-3xl font-bold leading-tight text-white">
              {modelName || 'Nessuna corrispondenza certa'}
            </h3>
          </div>
          <span className={`rounded-full px-3 py-1.5 text-xs font-black uppercase tracking-[0.16em] ${badge.class}`}>
            {badge.label}
          </span>
        </div>
      </div>

      <div className="p-7 space-y-5">
        <div className="grid grid-cols-2 gap-3">
          {productionYears && (
            <div className="rounded-2xl bg-vespa-cream p-4">
              <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Anni</p>
              <p className="mt-1 font-bold text-vespa-black">{productionYears}</p>
            </div>
          )}
          {engineCc && (
            <div className="rounded-2xl bg-vespa-cream p-4">
              <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Motore</p>
              <p className="mt-1 font-bold text-vespa-black">{engineCc}</p>
            </div>
          )}
        </div>

        {(confidencePercent || confidenceLabel) && (
          <div className="flex items-center gap-3 rounded-2xl border border-vespa-black/10 bg-white p-4">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-vespa-green/10 text-vespa-green">
              <ConfidenceIcon className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Confidenza</p>
              <p className="font-bold text-vespa-black">{confidencePercent ? `${confidencePercent}%` : confidenceLabel}</p>
            </div>
          </div>
        )}

        {result.dettagli && (
          <div className="space-y-2 rounded-2xl bg-vespa-cream/65 p-4">
            {result.dettagli.telaio_range && <p className="text-sm text-vespa-gray"><span className="font-bold text-vespa-black">Range telaio:</span> {result.dettagli.telaio_range}</p>}
            {result.dettagli.motore_range && <p className="text-sm text-vespa-gray"><span className="font-bold text-vespa-black">Range motore:</span> {result.dettagli.motore_range}</p>}
            {result.dettagli.colori && <p className="text-sm text-vespa-gray"><span className="font-bold text-vespa-black">Colori storici:</span> {result.dettagli.colori}</p>}
          </div>
        )}

        {expert && (
          <div className="rounded-3xl border border-vespa-green/15 bg-vespa-green/5 p-5">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-vespa-green text-white">
                <Brain className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Occhio dell’esperto</p>
                <p className="font-bold text-vespa-black">Analisi ragionata</p>
              </div>
            </div>
            {expert.expert_summary && <p className="mt-4 text-sm leading-7 text-vespa-gray">{expert.expert_summary}</p>}
            {expert.evidence?.length > 0 && (
              <ul className="mt-4 space-y-2 text-sm text-vespa-gray">
                {expert.evidence.slice(0, 4).map((item) => (
                  <li key={item} className="flex gap-2">
                    <ClipboardCheck className="mt-0.5 h-4 w-4 shrink-0 text-vespa-green" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            )}
            {expert.recommended_checks?.length > 0 && (
              <div className="mt-4 rounded-2xl bg-white/70 p-4">
                <p className="text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Controlli consigliati</p>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-xs leading-5 text-vespa-gray">
                  {expert.recommended_checks.slice(0, 3).map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>
            )}
          </div>
        )}

        {plan === 'free' && (
          <div className="rounded-3xl bg-vespa-black p-5 text-white">
            <div className="flex items-center gap-3">
              <Gauge className="h-5 w-5 text-vespa-gold" />
              <p className="font-bold">Vuoi la scheda completa?</p>
            </div>
            <p className="mt-2 text-sm leading-6 text-vespa-cream/70">
              per avere maggiori informazioni, registrati. La scheda completa apre il confronto colore,
              i range dei numeri telaio e motore, i dettagli storici e altri dati utili per capire meglio la tua Vespa.
            </p>
            <a href="/register?plan=avanzato" className="mt-4 inline-flex rounded-full bg-white px-4 py-2 text-sm font-black text-vespa-black transition-transform hover:-translate-y-0.5">
              Scopri la scheda completa →
            </a>
          </div>
        )}
      </div>

      {result.id && (
        <div className="border-t border-vespa-black/10 bg-vespa-cream/60 px-7 py-4">
          <p className="text-xs text-vespa-gray">ID Analisi: {result.id} · {new Date().toLocaleDateString('it-IT')}</p>
        </div>
      )}
    </div>
  )
}
