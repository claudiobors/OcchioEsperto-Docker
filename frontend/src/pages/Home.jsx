import { Link } from 'react-router-dom'
import { ArrowRight, Search, Shield, Camera, DollarSign, CheckCircle, Sparkles } from 'lucide-react'
import PricingCards from '../components/PricingCards'

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background pattern */}
        <div className="absolute inset-0 vespa-pattern opacity-30" />
        <div className="absolute inset-0 bg-gradient-to-b from-vespa-cream via-vespa-cream to-white" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
          <div className="text-center max-w-3xl mx-auto">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 bg-vespa-green/10 text-vespa-green text-sm font-medium px-4 py-2 rounded-full mb-8 animate-fade-in-up">
              <Sparkles className="w-4 h-4" />
              AI Specializzata per Appassionati Vespa
            </div>

            <h1 className="font-heading text-4xl sm:text-5xl lg:text-6xl font-bold text-vespa-black leading-tight mb-6 animate-fade-in-up-delay-1">
              Identifica, Valuta e
              <span className="text-vespa-green"> Scopri</span> la
              Storia della tua Vespa
            </h1>

            <p className="text-lg sm:text-xl text-vespa-gray leading-relaxed mb-10 max-w-2xl mx-auto animate-fade-in-up-delay-2">
              Carica una foto o inserisci i numeri di telaio e motore.
              Il nostro AI riconosce modello, anno, colori originali e ti dà una stima del valore di mercato.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up-delay-3">
              <Link
                to="/analisi"
                className="bg-vespa-green hover:bg-vespa-green-light text-white font-medium px-8 py-4 rounded-xl transition-colors flex items-center gap-2 text-lg shadow-lg shadow-vespa-green/20"
              >
                Inizia l'analisi
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/pricing"
                className="bg-white hover:bg-vespa-cream text-vespa-black font-medium px-8 py-4 rounded-xl transition-colors border border-vespa-cream-dark text-lg"
              >
                Vedi i piani
              </Link>
            </div>
          </div>

          {/* Mockup illustration */}
          <div className="mt-16 max-w-4xl mx-auto animate-fade-in-up-delay-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-vespa-green/20 to-vespa-green/5 rounded-3xl blur-3xl" />
              <div className="relative bg-white rounded-2xl shadow-2xl border border-vespa-cream-dark overflow-hidden p-4 sm:p-8">
                <div className="flex flex-col lg:flex-row items-center gap-8">
                  {/* Left: Vespa silhouette */}
                  <div className="flex-1">
                    <svg viewBox="0 0 200 200" className="w-full max-w-xs mx-auto" fill="none">
                      <circle cx="100" cy="100" r="90" className="fill-vespa-cream/50" />
                      <path d="M100 20 C120 20 138 35 145 55 L150 70 L160 65 L165 75 L150 82 L148 95 C145 120 125 140 100 140 C75 140 55 120 52 95 L50 82 L35 75 L40 65 L50 70 L55 55 C62 35 80 20 100 20 Z" className="fill-vespa-green/20" />
                      <circle cx="100" cy="100" r="8" className="fill-vespa-green/40" />
                      <rect x="95" y="55" width="10" height="30" rx="3" className="fill-vespa-green/30" />
                      <circle cx="70" cy="135" r="15" className="fill-vespa-black/10" stroke="vespa-green/30" strokeWidth="2" />
                      <circle cx="130" cy="135" r="15" className="fill-vespa-black/10" stroke="vespa-green/30" strokeWidth="2" />
                    </svg>
                  </div>
                  {/* Right: Mock interface */}
                  <div className="flex-1 w-full">
                    <div className="bg-vespa-cream rounded-xl p-4 space-y-3">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-vespa-green" />
                        <span className="text-xs font-medium text-vespa-black">Vespa 125 Primavera ET3</span>
                      </div>
                      <div className="h-2 bg-vespa-cream-dark rounded w-3/4" />
                      <div className="h-2 bg-vespa-cream-dark rounded w-1/2" />
                      <div className="flex gap-2 mt-2">
                        <span className="text-xs bg-vespa-green/10 text-vespa-green px-2 py-1 rounded">Anno: 1976</span>
                        <span className="text-xs bg-vespa-gold/10 text-vespa-gold px-2 py-1 rounded">€ 4.500</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-4">
              Come funziona
            </h2>
            <p className="text-vespa-gray text-lg max-w-2xl mx-auto">
              Tre semplici passi per conoscere tutto sulla tua Vespa
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-vespa-green/10 flex items-center justify-center">
                <Camera className="w-7 h-7 text-vespa-green" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-vespa-black mb-3">
                1. Carica e inserisci
              </h3>
              <p className="text-vespa-gray text-sm leading-relaxed">
                Carica una foto della tua Vespa o inserisci i numeri di telaio e motore. Aggiungi la data di immatricolazione.
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-vespa-green/10 flex items-center justify-center">
                <Search className="w-7 h-7 text-vespa-green" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-vespa-black mb-3">
                2. Analisi AI
              </h3>
              <p className="text-vespa-gray text-sm leading-relaxed">
                Il nostro AI confronta i dati con il database storico Piaggio per identificare modello, anno e varianti.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-vespa-green/10 flex items-center justify-center">
                <CheckCircle className="w-7 h-7 text-vespa-green" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-vespa-black mb-3">
                3. Risultati e valore
              </h3>
              <p className="text-vespa-gray text-sm leading-relaxed">
                Ricevi una scheda dettagliata con modello, anno, colori storici, check originalità e stima del valore.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20 bg-vespa-cream/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-6">
                Perché scegliere <span className="text-vespa-green">OcchioEsperto</span>
              </h2>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <Shield className="w-6 h-6 text-vespa-green shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-vespa-black">Database storico completo</h4>
                    <p className="text-sm text-vespa-gray">Oltre 70 anni di modelli Vespa Piaggio dal 1946 a oggi.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <DollarSign className="w-6 h-6 text-vespa-green shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-vespa-black">Stima del valore di mercato</h4>
                    <p className="text-sm text-vespa-gray">Basata su dati di vendita reali e condizioni del veicolo.</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <Camera className="w-6 h-6 text-vespa-green shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-vespa-black">Analisi colore AI</h4>
                    <p className="text-sm text-vespa-gray">Riconoscimento automatico del colore dalla foto e confronto con i colori storici.</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-vespa-green rounded-3xl p-8 text-white">
              <h3 className="font-heading text-2xl font-bold mb-4">Inizia gratuitamente</h3>
              <p className="text-vespa-cream/80 text-sm mb-6">
                Registrati e ottieni l'identificazione base del modello e anno della tua Vespa. Nessuna carta di credito richiesta.
              </p>
              <Link
                to="/register"
                className="inline-flex items-center gap-2 bg-white text-vespa-green font-medium px-6 py-3 rounded-xl hover:bg-vespa-cream transition-colors"
              >
                Registrati gratis
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-white" id="pricing">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-4">
              Scegli il tuo piano
            </h2>
            <p className="text-vespa-gray text-lg max-w-2xl mx-auto">
              Dall'identificazione base all'analisi completa con esperto AI
            </p>
          </div>
          <PricingCards />
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-vespa-black">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-heading text-3xl sm:text-4xl font-bold text-white mb-4">
            Pronto a scoprire la storia della tua Vespa?
          </h2>
          <p className="text-vespa-gray-light text-lg mb-8 max-w-2xl mx-auto">
            Migliaia di appassionati usano OcchioEsperto per identificare, valutare e preservare le loro Vespe.
          </p>
          <Link
            to="/analisi"
            className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white font-medium px-8 py-4 rounded-xl transition-colors text-lg"
          >
            Inizia ora
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  )
}