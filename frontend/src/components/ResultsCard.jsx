import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react'

const badges = {
  free: { label: 'Base', class: 'bg-vespa-cream-dark text-vespa-black' },
  premium: { label: 'Premium', class: 'bg-vespa-green text-white' },
}

export default function ResultsCard({ result, plan = 'free' }) {
  if (!result) return null

  const badge = badges[plan] || badges.free
  const modelName = result.model?.name || result.modello
  const productionYears = result.identification?.years || result.anno
  const engineCc = result.identification?.engine_cc || result.model?.engine_cc
  const confidenceLabel = {
    high: 'Alta',
    medium: 'Media',
    low: 'Bassa',
  }[result.confidence] || result.confidence
  const confidencePercent = result.confidenza

  return (
    <div className="animate-scale-in bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden hover:shadow-md transition-all duration-300">
      {/* Header */}
      <div className="p-6 border-b border-vespa-cream-dark">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-heading text-xl font-bold text-vespa-black">
            {modelName || 'Nessuna corrispondenza certa'}
          </h3>
          <span className={`text-xs font-medium px-3 py-1 rounded-full ${badge.class}`}>
            {badge.label}
          </span>
        </div>
        {productionYears && (
          <p className="text-vespa-gray text-sm">
            Anni: <span className="font-semibold text-vespa-black">{productionYears}</span>
          </p>
        )}
        {engineCc && (
          <p className="text-vespa-gray text-sm">
            Motore: <span className="font-semibold text-vespa-black">{engineCc} cc</span>
          </p>
        )}
      </div>

      {/* Body */}
      <div className="p-6 space-y-4">
        {/* Model confidence */}
        {(confidencePercent || confidenceLabel) && (
          <div className="flex items-center gap-2">
            {confidencePercent ? (
              confidencePercent > 80 ? (
                <CheckCircle className="w-5 h-5 text-vespa-green" />
              ) : confidencePercent > 50 ? (
                <AlertTriangle className="w-5 h-5 text-vespa-gold" />
              ) : (
                <XCircle className="w-5 h-5 text-vespa-red" />
              )
            ) : result.confidence === 'high' ? (
              <CheckCircle className="w-5 h-5 text-vespa-green" />
            ) : result.confidence === 'medium' ? (
              <AlertTriangle className="w-5 h-5 text-vespa-gold" />
            ) : (
              <XCircle className="w-5 h-5 text-vespa-red" />
            )}
            <span className="text-sm text-vespa-gray">
              Confidenza:{' '}
              <span className="font-semibold text-vespa-black">
                {confidencePercent ? `${confidencePercent}%` : confidenceLabel}
              </span>
            </span>
          </div>
        )}

        {/* Details */}
        {result.dettagli && (
          <div className="space-y-2">
            {result.dettagli.telaio_range && (
              <p className="text-sm text-vespa-gray">
                <span className="font-medium text-vespa-black">Range telaio:</span> {result.dettagli.telaio_range}
              </p>
            )}
            {result.dettagli.motore_range && (
              <p className="text-sm text-vespa-gray">
                <span className="font-medium text-vespa-black">Range motore:</span> {result.dettagli.motore_range}
              </p>
            )}
            {result.dettagli.colori && (
              <p className="text-sm text-vespa-gray">
                <span className="font-medium text-vespa-black">Colori storici:</span> {result.dettagli.colori}
              </p>
            )}
          </div>
        )}

        {/* Premium-only info */}
        {plan === 'premium' && (
          <div className="bg-vespa-cream/50 rounded-xl p-4 space-y-2">
            {result.prezzo_stimato && (
              <p className="text-sm">
                <span className="font-medium text-vespa-black">Valore stimato:</span>{' '}
                <span className="text-vespa-green font-bold">{result.prezzo_stimato}</span>
              </p>
            )}
            {result.originalita && (
              <div className="flex items-center gap-2">
                {result.originalita === 'originale' ? (
                  <CheckCircle className="w-4 h-4 text-vespa-green" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-vespa-gold" />
                )}
                <span className="text-sm text-vespa-gray">
                  Originalità: <span className="font-semibold text-vespa-black capitalize">{result.originalita}</span>
                </span>
              </div>
            )}
            {result.checklist && result.checklist.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-medium text-vespa-black mb-1">Checklist problemi:</p>
                <ul className="space-y-1">
                  {result.checklist.map((item, i) => (
                    <li key={i} className="text-sm text-vespa-gray flex items-start gap-2">
                      {item.criticita === 'alta' ? (
                        <XCircle className="w-4 h-4 text-vespa-red shrink-0 mt-0.5" />
                      ) : item.criticita === 'media' ? (
                        <AlertTriangle className="w-4 h-4 text-vespa-gold shrink-0 mt-0.5" />
                      ) : (
                        <CheckCircle className="w-4 h-4 text-vespa-green shrink-0 mt-0.5" />
                      )}
                      <span>{item.descrizione}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* CTA for premium upgrade */}
        {plan === 'free' && (
          <div className="bg-vespa-cream/50 rounded-xl p-4 text-center">
            <p className="text-sm text-vespa-gray mb-2">
              Sblocca l'analisi Premium per vedere colori storici, stima del valore e check originalità.
            </p>
            <a
              href="/pricing"
              className="inline-block text-sm font-medium text-vespa-green hover:text-vespa-green-light transition-colors"
            >
              Passa a Premium →
            </a>
          </div>
        )}
      </div>

      {/* Footer */}
      {result.id && (
        <div className="px-6 py-3 bg-vespa-cream/30 border-t border-vespa-cream-dark">
          <p className="text-xs text-vespa-gray">
            ID Analisi: {result.id} | {new Date().toLocaleDateString('it-IT')}
          </p>
        </div>
      )}
    </div>
  )
}