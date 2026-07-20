import { CheckCircle, AlertTriangle, XCircle, Sparkles, Camera, ShieldCheck } from 'lucide-react'

const confidenceValue = (confidence, score) => {
  if (score) return score
  if (confidence === 'high') return 90
  if (confidence === 'medium') return 65
  return 35
}

export default function ResultsCard({ result }) {
  if (!result) return null

  const model = result.model || result.analysis?.model
  const identification = result.identification || result.analysis?.identification
  const analysis = result.analysis || result
  const score = confidenceValue(result.confidence, result.confidence_score)
  const prices = analysis.market_prices || []
  const colors = analysis.colors || []
  const issues = analysis.known_issues || []
  const colorMatches = analysis.color_matches || result.color_matches || []

  return (
    <div className="animate-fade-in-up bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden shadow-xl shadow-vespa-green/5">
      <div className="p-6 bg-gradient-to-br from-vespa-green to-vespa-green-dark text-white">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-vespa-cream/80">Risultato OcchioEsperto</p>
            <h3 className="font-heading text-2xl font-bold mt-1">
              {model?.name || 'Analisi Vespa'}
            </h3>
            {identification?.years && <p className="text-sm text-vespa-cream/85 mt-1">Produzione: {identification.years}</p>}
          </div>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white/15 border border-white/20">
            {result.match_type === 'none' ? 'Da verificare' : 'Match dati'}
          </span>
        </div>

        <div className="bg-white/10 rounded-xl p-3 flex items-center gap-3">
          {score >= 80 ? <CheckCircle className="w-5 h-5" /> : score >= 55 ? <AlertTriangle className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
          <div className="flex-1">
            <div className="flex justify-between text-sm font-medium"><span>Attendibilità</span><span>{score}%</span></div>
            <div className="h-2 bg-white/15 rounded-full mt-2 overflow-hidden"><div className="h-full bg-vespa-gold-light" style={{ width: `${Math.min(score, 100)}%` }} /></div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-5">
        {result.photo && (
          <div className="rounded-xl bg-vespa-cream/50 p-4 flex items-center gap-4">
            {result.photo.path ? <img src={result.photo.path} alt="Foto caricata" className="w-20 h-20 object-cover rounded-lg border border-vespa-cream-dark" /> : <Camera className="w-8 h-8 text-vespa-green" />}
            <div className="text-sm text-vespa-gray">
              <p className="font-semibold text-vespa-black">Foto caricata correttamente</p>
              {result.photo.dominant_color_hex && <p>Colore stimato: <span className="inline-block w-3 h-3 rounded-full border align-middle" style={{ background: result.photo.dominant_color_hex }} /> {result.photo.dominant_color_hex}</p>}
            </div>
          </div>
        )}

        {model && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-xl bg-vespa-cream/40 p-3"><span className="block text-vespa-gray">Cilindrata</span><strong>{model.engine_cc}</strong></div>
            <div className="rounded-xl bg-vespa-cream/40 p-3"><span className="block text-vespa-gray">Periodo</span><strong>{model.production_start}-{model.production_end || 'oggi'}</strong></div>
          </div>
        )}

        {analysis.frame_ranges?.length > 0 && (
          <InfoList title="Range telaio" items={analysis.frame_ranges.map((r) => `${r.frame_number_start} → ${r.frame_number_end} (${r.year_start}-${r.year_end})`)} />
        )}
        {analysis.engine_ranges?.length > 0 && (
          <InfoList title="Range motore" items={analysis.engine_ranges.map((r) => `${r.engine_number_start} → ${r.engine_number_end} (${r.year_start}-${r.year_end})`)} />
        )}

        {colorMatches.length > 0 && (
          <div>
            <h4 className="font-semibold text-vespa-black mb-2">Colori storici più vicini</h4>
            <div className="space-y-2">
              {colorMatches.slice(0, 3).map((c, i) => (
                <div key={i} className="flex items-center justify-between text-sm rounded-lg border border-vespa-cream-dark p-2">
                  <span><span className="inline-block w-4 h-4 rounded-full border align-middle mr-2" style={{ background: c.color_hex }} />{c.color_name}</span>
                  <strong className="text-vespa-green">{c.similarity_percent}%</strong>
                </div>
              ))}
            </div>
          </div>
        )}

        {colors.length > 0 && <InfoList title="Colori originali noti" items={colors.slice(0, 6).map((c) => `${c.color_name} (${c.year_start}-${c.year_end || 'oggi'})`)} />}
        {issues.length > 0 && <InfoList title="Controlli consigliati" items={issues.slice(0, 5).map((i) => `${i.issue_title}: ${i.description}`)} danger />}
        {prices.length > 0 && <InfoList title="Valori indicativi" items={prices.map((p) => `${p.condition}: €${p.price_min_eur}–€${p.price_max_eur}`)} />}

        {result.ai_summary && (
          <div className="rounded-xl bg-vespa-green/10 border border-vespa-green/20 p-4">
            <div className="flex items-center gap-2 text-vespa-green font-semibold mb-2"><Sparkles className="w-4 h-4" /> Sintesi esperta AI</div>
            <p className="text-sm text-vespa-black whitespace-pre-line leading-relaxed">{result.ai_summary}</p>
            {result.ai_model && <p className="text-xs text-vespa-gray mt-2">Modello usato: {result.ai_model}</p>}
          </div>
        )}

        <div className="rounded-xl bg-vespa-cream/40 p-4 text-xs text-vespa-gray leading-relaxed flex gap-2">
          <ShieldCheck className="w-5 h-5 text-vespa-green shrink-0" />
          <span>{result.disclaimer}</span>
        </div>
      </div>
    </div>
  )
}

function InfoList({ title, items, danger = false }) {
  return (
    <div>
      <h4 className="font-semibold text-vespa-black mb-2">{title}</h4>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className="text-sm text-vespa-gray flex gap-2">
            {danger ? <AlertTriangle className="w-4 h-4 text-vespa-gold shrink-0 mt-0.5" /> : <CheckCircle className="w-4 h-4 text-vespa-green shrink-0 mt-0.5" />}
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
