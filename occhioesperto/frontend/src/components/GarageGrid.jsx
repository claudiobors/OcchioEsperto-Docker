import { Link } from 'react-router-dom'
import { Clock, Calendar, ArrowRight, Eye } from 'lucide-react'

export default function GarageGrid({ analyses }) {
  if (!analyses || analyses.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-vespa-cream-dark flex items-center justify-center">
          <Clock className="w-10 h-10 text-vespa-gray-light" />
        </div>
        <h3 className="font-heading text-xl font-semibold text-vespa-black mb-2">
          Nessuna Vespa nel garage
        </h3>
        <p className="text-vespa-gray text-sm mb-6 max-w-md mx-auto">
          Le tue analisi salvate appariranno qui. Inizia analizzando la tua prima Vespa!
        </p>
        <Link
          to="/analisi"
          className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white px-6 py-3 rounded-xl font-medium transition-colors"
        >
          <ArrowRight className="w-4 h-4" />
          Analizza una Vespa
        </Link>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {analyses.map((item) => (
        <Link
          key={item.id}
          to="#"
          className="group bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden hover:shadow-lg hover:border-vespa-green/30 transition-all duration-300"
        >
          {/* Image */}
          <div className="h-40 bg-gradient-to-br from-vespa-cream to-vespa-cream-dark flex items-center justify-center overflow-hidden">
            {item.photo_path ? (
              <img src={'/' + item.photo_path} alt={item.model_name} className="w-full h-full object-cover" />
            ) : (
              <div className="text-center">
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
                <span className="w-3 h-3 rounded-full inline-block border border-vespa-cream-dark" style={{backgroundColor: item.color_hex || '#ccc'}} />
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