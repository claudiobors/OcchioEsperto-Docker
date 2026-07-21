import { Link } from 'react-router-dom'
import { Calendar, Eye } from 'lucide-react'

export default function GarageGrid({ analyses, onSelect }) {
  if (!analyses || analyses.length === 0) {
    return (
      <div className="text-center py-16 animate-fade-in-up">
        <div className="relative mb-8">
          <svg viewBox="0 0 120 120" className="w-28 h-28 mx-auto" fill="none">
            <circle cx="60" cy="60" r="55" className="fill-vespa-cream-dark/50" />
            <path d="M60 15 C78 15 92 28 98 48 L102 60 L110 56 L113 64 L102 70 L100 80 C97 100 80 110 60 110 C40 110 23 100 20 80 L18 70 L7 64 L10 56 L18 60 L22 48 C28 28 42 15 60 15 Z" className="fill-vespa-green/15" />
            <text x="60" y="68" textAnchor="middle" className="fill-vespa-green font-heading" fontSize="14" fontWeight="bold">?</text>
          </svg>
        </div>
        <h3 className="font-heading text-xl font-semibold text-vespa-black mb-2">Nessuna Vespa nel garage</h3>
        <p className="text-vespa-gray text-sm mb-6 max-w-md mx-auto leading-relaxed">
          Il tuo garage digitale è vuoto. Inizia con una prima identificazione, poi potrai arricchirla con report, foto e valutazione.
        </p>
        <Link to="/analisi" className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white px-6 py-3 rounded-xl font-medium transition-all hover:shadow-lg hover:shadow-vespa-green/20">
          Analizza una Vespa
        </Link>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {analyses.map((item, index) => (
        <button
          key={item.id}
          type="button"
          onClick={() => onSelect?.(item)}
          className="group text-left bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden hover:shadow-lg hover:border-vespa-green/30 transition-all duration-300 hover:-translate-y-1"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          <div className="h-40 bg-gradient-to-br from-vespa-cream to-vespa-cream-dark flex items-center justify-center overflow-hidden">
            {item.photo_path ? (
              <img src={'/' + item.photo_path} alt={item.display_name || item.model_name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
            ) : (
              <img src="/hero-vespa.svg" alt={item.model_name || 'Vespa'} className="h-full w-full object-cover opacity-85 transition-transform duration-500 group-hover:scale-105" />
            )}
          </div>

          <div className="p-4">
            <h4 className="font-heading font-semibold text-vespa-black group-hover:text-vespa-green transition-colors">
              {item.display_name || item.model_name || 'Vespa'}
            </h4>
            <p className="mt-1 text-xs font-bold text-vespa-gray">{item.model_name}</p>
            {item.year && (
              <p className="text-xs text-vespa-gray mt-1 flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                {item.year}
              </p>
            )}
            <div className="mt-3 flex items-center justify-between">
              <span className="rounded-full bg-vespa-cream px-2 py-1 text-[11px] font-black uppercase tracking-[0.12em] text-vespa-gray">
                {item.analysis_level === 'basic' ? 'Base' : 'Pro'}
              </span>
              <Eye className="w-4 h-4 text-vespa-gray-light group-hover:text-vespa-green transition-colors" />
            </div>
          </div>
        </button>
      ))}
    </div>
  )
}
