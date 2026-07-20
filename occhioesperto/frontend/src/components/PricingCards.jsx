import { Check, Crown, ShieldCheck, X } from 'lucide-react'
import { Link } from 'react-router-dom'

const plans = [
  {
    name: 'Base',
    price: 'Gratis',
    period: 'per iniziare',
    description: 'Perfetto per capire se vale la pena approfondire.',
    promise: 'Identificazione orientativa senza carta di credito.',
    features: [
      ['Identificazione modello e periodo', true],
      ['Risultato con attendibilità', true],
      ['Upload foto e colore stimato', true],
      ['Garage digitale fino a 3 Vespe', true],
      ['Range telaio/motore completi', false],
      ['Prezzi e problemi noti', false],
      ['Domanda all’esperto AI', false],
    ],
    cta: 'Inizia gratis', href: '/analisi', featured: false,
  },
  {
    name: 'Intermedio',
    price: '4,99 €',
    period: 'per analisi',
    description: 'Per controllare meglio sigle e dati tecnici.',
    promise: 'Il miglior rapporto costo/utilità per pre-acquisto.',
    features: [
      ['Tutto del piano Base', true],
      ['Range telaio e motore', true],
      ['Scheda tecnica sintetica', true],
      ['Controlli documentali consigliati', true],
      ['Colori storici completi', false],
      ['Stima prezzi di mercato', false],
      ['Domanda all’esperto AI', false],
    ],
    cta: 'Scegli Intermedio', href: '/register?plan=intermedio', featured: true,
  },
  {
    name: 'Avanzato',
    price: '9,99 €',
    period: 'per analisi',
    description: 'Per decidere con più sicurezza su acquisto, vendita o restauro.',
    promise: 'Costa poco rispetto a un errore su una Vespa sbagliata.',
    features: [
      ['Tutto del piano Intermedio', true],
      ['Colori storici e match colore', true],
      ['Checklist problemi noti', true],
      ['Verifica originalità orientativa', true],
      ['Stima prezzi per condizione', true],
      ['Domanda all’esperto AI', true],
      ['Report più completo', true],
    ],
    cta: 'Scegli Avanzato', href: '/register?plan=avanzato', featured: false, premium: true,
  },
]

export default function PricingCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-6xl mx-auto">
      {plans.map((plan) => (
        <div key={plan.name} className={`relative rounded-[2rem] overflow-hidden transition-all duration-300 hover:-translate-y-2 ${plan.featured ? 'bg-vespa-green text-white shadow-2xl shadow-vespa-green/25 ring-4 ring-vespa-green/20' : 'bg-white text-vespa-black border border-vespa-cream-dark shadow-xl shadow-vespa-green/5'}`}>
          {plan.featured && (
            <div className="absolute top-4 right-4 bg-vespa-gold text-vespa-black text-xs font-black px-3 py-1 rounded-full flex items-center gap-1">
              <Crown className="w-3 h-3" /> Più conveniente
            </div>
          )}
          <div className="p-8 flex flex-col min-h-full">
            <div className="mb-7">
              <p className={`text-xs uppercase tracking-[0.25em] font-bold mb-3 ${plan.featured ? 'text-vespa-cream/80' : 'text-vespa-green'}`}>{plan.promise}</p>
              <h3 className={`font-heading text-3xl font-bold mb-2 ${plan.featured ? 'text-white' : 'text-vespa-black'}`}>{plan.name}</h3>
              <p className={`text-sm leading-relaxed ${plan.featured ? 'text-vespa-cream/85' : 'text-vespa-gray'}`}>{plan.description}</p>
            </div>

            <div className="mb-8">
              <span className="text-5xl font-black tracking-tight">{plan.price}</span>
              <span className={`text-sm ml-2 ${plan.featured ? 'text-vespa-cream/80' : 'text-vespa-gray'}`}>{plan.period}</span>
            </div>

            <ul className="space-y-3 mb-8 flex-1">
              {plan.features.map(([text, included]) => (
                <li key={text} className="flex items-start gap-3">
                  {included ? <Check className={`w-5 h-5 shrink-0 ${plan.featured ? 'text-vespa-gold-light' : 'text-vespa-green'}`} /> : <X className="w-5 h-5 shrink-0 text-vespa-gray-light" />}
                  <span className={`text-sm ${plan.featured ? 'text-vespa-cream/95' : included ? 'text-vespa-black' : 'text-vespa-gray'}`}>{text}</span>
                </li>
              ))}
            </ul>

            <Link to={plan.href} className={`block text-center font-bold py-4 px-6 rounded-xl transition-colors ${plan.featured ? 'bg-white text-vespa-green hover:bg-vespa-cream' : plan.premium ? 'bg-vespa-black text-white hover:bg-vespa-black-light' : 'bg-vespa-cream-dark text-vespa-black hover:bg-vespa-cream'}`}>
              {plan.cta}
            </Link>
            <p className={`text-[11px] mt-4 leading-relaxed ${plan.featured ? 'text-vespa-cream/70' : 'text-vespa-gray'}`}>
              <ShieldCheck className="w-3 h-3 inline mr-1" /> Analisi orientativa: non sostituisce perizia o certificato ufficiale.
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}
