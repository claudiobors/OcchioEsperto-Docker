import { Link } from 'react-router-dom'
import { Calendar, ArrowRight, Eye, Bike } from 'lucide-react'

export default function GarageGrid({ analyses }) {
  if (!analyses || analyses.length === 0) {
    return (
      <div className="text-center py-16 animate-fade-in-up">
        <div className="relative mb-8">
          <svg viewBox="0 0 120 120" className="w-28 h-28 mx-auto" fill="none">
            <circle cx="60" cy="60" r="55" className="fill-vespa-cream-dark/50" />
            <path d="M60 15 C78 15 92 28 98 48 L102 60 L110 56 L113 64 L102 70 L100 80 C97 100 80 110 60 110 C40 110 23 100 20 80 L18 70 L7 64 L10 56 L18 60 L22 48 C28 28 42 15 60 15 Z" className="fill-vespa-green/15" />
            <circle cx="40" cy="95" r="12" className="fill-vespa-black/5" stroke="vespa-green/20" strokeWidth="1.5" />
            <circle cx="80" cy="95" r="12" className="fill-vespa-black/5" stroke="vespa-green/20" strokeWidth="1.5" />
            <text x="60" y="68" textAnchor="middle" className="fill-vespa-green font-heading" fontSize="14" fontWeight="bold">?</text>
          </svg>
        </div>
        <h3 className="font-heading text-xl font-semibold text-vespa-black mb-2">
          Nessuna Vespa nel garage
        </h3>
        <p className="text-vespa-gray text-sm mb-6 max-w-md mx-auto leading-relaxed">
          Il tuo garage digitale è vuoto! Inizia subito analizzando la tua prima Vespa per scoprire modello, anno, colori originali e valore di mercato.
        </p>
        <Link
          to="/analisi"
          className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white px-6 py-3 rounded-xl font-medium transition-all hover:shadow-lg hover:shadow-vespa-green/20"
        >
          <ArrowRight className="w-4 h-4" />
          Analizza una Vespa
        </Link>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {analyses.map((item, index) => (
        <Link
          key={item.id}
          to="#"
          className="group bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden hover:shadow-lg hover:border-vespa-green/30 transition-all duration-300 hover:-translate-y-1"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          {/* Image */}
          <div className="h-40 bg-gradient-to-br from-vespa-cream to-vespa-cream-dark flex items-center justify-center overflow-hidden">
            {item.photo_path ? (
              <img src={'/' + item.photo_path} alt={item.model_name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
            ) : (
              <div className="text-center transition-transform duration-300 group-hover:scale-105">
                <svg className="w-16 h-16 mx-auto text-vespa-gray-light/50" viewBox="0 0 60 60" fill="currentColor">
                  <path d="M30 5 C35 5 40 10 40 15 L40 20 L45 18 L48 22 L40 25 L40 30 C40 35 35 40 30 40 C25 40 20 35 20 30 L20 25 L12 22 L15 18 L20 20 L20 15 C20 10 25 5 30 5 Z" />
                </svg>
                <p className="text-xs text-vespa-gray-light mt-2">Nessuna foto</p>
              </div>
            )}
          </div>

          {/* Info */}
          <div className="p-4">
            <h4 className="font-heading font-semibold text-vespa-black group-hover:text-vespa-green transition-colors">
              {item.model_name || 'Vespa'}
            </h4>
            {item.year && (
              <p className="text-xs text-vespa-gray mt-1 flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                {item.year}
              </p>
            )}
            {item.color_name && (
              <p className="text-xs text-vespa-gray mt-1 flex items-center gap-1">
                <span className="w-3 h-3 rounded-full inline-block border border-vespa-cream-dark shrink-0" style={{backgroundColor: item.color_hex || '#ccc'}} />
                {item.color_name}
              </p>
            )}
            <div className="mt-3 flex items-center justify-between">
              <span className="text-xs text-vespa-gray">
                {item.created_at ? new Date(item.created_at).toLocaleDateString('it-IT') : ''}
              </span>
              <Eye className="w-4 h-4 text-vespa-gray-light group-hover:text-vespa-green transition-colors" />
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}