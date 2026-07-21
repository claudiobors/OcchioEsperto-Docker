import { Link } from 'react-router-dom'
import { Sparkles, Mail, ShieldCheck } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="dark-panel mt-10 border-t border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-[1.3fr_0.7fr_0.8fr]">
          <div>
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-vespa-gold to-vespa-green">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <span className="block font-heading text-2xl font-bold tracking-[-0.05em] text-white">
                  Occhio<span className="gold-text">Esperto</span>
                </span>
                <span className="text-[10px] font-black uppercase tracking-[0.28em] text-vespa-cream/48">
                  Archivio · AI · Valore
                </span>
              </div>
            </div>
            <p className="mt-5 max-w-md text-sm leading-7 text-vespa-cream/62">
              Una piattaforma italiana per identificare, valutare e raccontare Vespe classiche con un’interfaccia degna di un mezzo iconico.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-black uppercase tracking-[0.24em] text-vespa-gold-light">Naviga</h3>
            <ul className="mt-5 space-y-3">
              {[
                ['Home', '/'],
                ['Analisi Vespa', '/analisi'],
                ['Piani', '/pricing'],
                ['Garage', '/dashboard'],
              ].map(([label, to]) => (
                <li key={to}>
                  <Link to={to} className="text-sm font-bold text-vespa-cream/62 transition-colors hover:text-white">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-black uppercase tracking-[0.24em] text-vespa-gold-light">Fiducia</h3>
            <ul className="mt-5 space-y-3 text-sm text-vespa-cream/62">
              <li className="flex items-center gap-2"><Mail className="h-4 w-4 text-vespa-gold" /> info@occhioesperto.it</li>
              <li className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-vespa-gold" /> Non affiliato al Gruppo Piaggio</li>
              <li>&copy; {new Date().getFullYear()} OcchioEsperto</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 border-t border-white/10 pt-7">
          <p className="text-center text-xs leading-6 text-vespa-cream/45">
            Questo servizio offre un'analisi basata su dati storici per supportare appassionati e restauratori.
            Non costituisce un certificato ufficiale di origine e non è affiliato in alcun modo al Gruppo Piaggio.
          </p>
        </div>
      </div>
    </footer>
  )
}
