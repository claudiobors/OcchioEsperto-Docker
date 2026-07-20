import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-vespa-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-full bg-vespa-green flex items-center justify-center">
                <span className="text-white font-bold text-sm">OE</span>
              </div>
              <span className="font-heading text-xl font-bold">
                Occhio<span className="text-vespa-green">Esperto</span>
              </span>
            </div>
            <p className="text-vespa-gray-light text-sm leading-relaxed">
              L'assistente AI specializzato per appassionati e restauratori di Vespa Piaggio.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-heading text-lg font-semibold mb-4">Link</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-vespa-gray-light hover:text-vespa-green transition-colors text-sm">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/analisi" className="text-vespa-gray-light hover:text-vespa-green transition-colors text-sm">
                  Analisi Vespa
                </Link>
              </li>
              <li>
                <Link to="/pricing" className="text-vespa-gray-light hover:text-vespa-green transition-colors text-sm">
                  Piani
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-vespa-gray-light hover:text-vespa-green transition-colors text-sm">
                  Il mio garage
                </Link>
              </li>
            </ul>
          </div>

          {/* Info */}
          <div>
            <h3 className="font-heading text-lg font-semibold mb-4">Info</h3>
            <ul className="space-y-2">
              <li className="text-vespa-gray-light text-sm">
                &copy; {new Date().getFullYear()} OcchioEsperto
              </li>
              <li className="text-vespa-gray-light text-sm">
                Supporto: info@occhioesperto.it
              </li>
            </ul>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 pt-8 border-t border-vespa-black-light/50">
          <p className="text-xs text-vespa-gray leading-relaxed text-center">
            Questo servizio offre un'analisi basata su dati storici per supportare appassionati e restauratori.
            Non costituisce un certificato ufficiale di origine e non è affiliato in alcun modo al Gruppo Piaggio.
          </p>
        </div>
      </div>
    </footer>
  )
}