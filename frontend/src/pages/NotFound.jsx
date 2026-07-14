import { Link } from 'react-router-dom'
import { Home, ArrowLeft } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        {/* Vespa silhouette 404 */}
        <div className="relative mb-8">
          <svg viewBox="0 0 200 200" className="w-40 h-40 mx-auto" fill="none">
            <circle cx="100" cy="100" r="90" className="fill-vespa-cream-dark/50" />
            <text x="100" y="110" textAnchor="middle" className="fill-vespa-green font-heading" fontSize="72" fontWeight="bold">404</text>
            <path d="M100 30 C120 30 138 45 145 65 L150 80 L160 75 L165 85 L150 92 L148 105 C145 130 125 150 100 150 C75 150 55 130 52 105 L50 92 L35 85 L40 75 L50 80 L55 65 C62 45 80 30 100 30 Z" className="fill-vespa-green/10" />
          </svg>
        </div>

        <h1 className="font-heading text-3xl font-bold text-vespa-black mb-3">
          Pagina non trovata
        </h1>
        <p className="text-vespa-gray text-sm mb-8 leading-relaxed">
          Questa Vespa non è nei nostri archivi! La pagina che cerchi non esiste o è stata spostata.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white font-medium px-6 py-3 rounded-xl transition-colors"
          >
            <Home className="w-4 h-4" />
            Torna alla Home
          </Link>
          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center gap-2 text-vespa-gray hover:text-vespa-black font-medium px-6 py-3 rounded-xl transition-colors border border-vespa-cream-dark"
          >
            <ArrowLeft className="w-4 h-4" />
            Indietro
          </button>
        </div>
      </div>
    </div>
  )
}