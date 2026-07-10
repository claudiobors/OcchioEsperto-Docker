import PricingCards from '../components/PricingCards'
import { Sparkles } from 'lucide-react'

export default function Pricing() {
  return (
    <div className="min-h-[calc(100vh-4rem)]">
      {/* Header */}
      <div className="bg-gradient-to-b from-vespa-cream to-white py-16 sm:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 bg-vespa-green/10 text-vespa-green text-sm font-medium px-4 py-2 rounded-full mb-4">
            <Sparkles className="w-4 h-4" />
            Piani e Prezzi
          </div>
          <h1 className="font-heading text-3xl sm:text-4xl lg:text-5xl font-bold text-vespa-black mb-4">
            Scegli il piano perfetto per te
          </h1>
          <p className="text-vespa-gray text-lg max-w-2xl mx-auto">
            Dall'identificazione base all'analisi completa con assistente AI. Paghi solo quando usi il servizio.
          </p>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20 -mt-8">
        <PricingCards />
      </div>

      {/* FAQ */}
      <div className="bg-white py-20 border-t border-vespa-cream-dark">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="font-heading text-2xl font-bold text-vespa-black text-center mb-12">
            Domande frequenti
          </h2>
          <div className="space-y-6">
            <div className="bg-vespa-cream/30 rounded-xl p-6">
              <h3 className="font-semibold text-vespa-black mb-2">Come funziona il pagamento?</h3>
              <p className="text-sm text-vespa-gray leading-relaxed">
                Paghi solo per ogni analisi effettuata. Scegli il piano Base (gratuito) per l'identificazione modello,
                o passa a Intermedio o Premium per analisi più dettagliate. Nessun abbonamento mensile.
              </p>
            </div>
            <div className="bg-vespa-cream/30 rounded-xl p-6">
              <h3 className="font-semibold text-vespa-black mb-2">Posso salvare le analisi?</h3>
              <p className="text-sm text-vespa-gray leading-relaxed">
                Sì! Una volta registrato, tutte le tue analisi vengono salvate nel tuo "garage digitale" personale,
                accessibile dalla dashboard. Puoi rivedere i risultati in qualsiasi momento.
              </p>
            </div>
            <div className="bg-vespa-cream/30 rounded-xl p-6">
              <h3 className="font-semibold text-vespa-black mb-2">L'analisi sostituisce un certificato ufficiale?</h3>
              <p className="text-sm text-vespa-gray leading-relaxed">
                No. OcchioEsperto offre un'analisi basata su dati storici per supportare appassionati e restauratori.
                Non costituisce un certificato ufficiale di origine e non è affiliato al Gruppo Piaggio.
              </p>
            </div>
            <div className="bg-vespa-cream/30 rounded-xl p-6">
              <h3 className="font-semibold text-vespa-black mb-2">Come funziona la vendita?</h3>
              <p className="text-sm text-vespa-gray leading-relaxed">
                Il pulsante "Vendi la tua Vespa" ti mette in contatto con collezionisti verificati.
                Inserisci una descrizione e ti contatteremo per aiutarti a trovare il miglior acquirente.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}