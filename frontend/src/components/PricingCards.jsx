import { Check, X } from 'lucide-react'
import { Link } from 'react-router-dom'

const plans = [
  {
    name: 'Base',
    price: 'Gratuito',
    period: '',
    description: 'Identificazione modello e anno',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: false },
      { text: 'Scheda tecnica sintetica', included: false },
      { text: 'Colori storici originali', included: false },
      { text: 'Analisi AI colore da foto', included: false },
      { text: 'Checklist problemi e verifica originalità', included: false },
      { text: 'Stima prezzi di mercato', included: false },
      { text: 'Salvataggio nel garage digitale', included: true },
      { text: 'Domanda all\'esperto AI', included: false },
    ],
    cta: 'Inizia gratis',
    href: '/register',
    featured: false,
  },
  {
    name: 'Intermedio',
    price: '4,99 €',
    period: 'per analisi',
    description: 'Dati tecnici dettagliati',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: true },
      { text: 'Scheda tecnica sintetica', included: true },
      { text: 'Colori storici originali', included: false },
      { text: 'Analisi AI colore da foto', included: false },
      { text: 'Checklist problemi e verifica originalità', included: false },
      { text: 'Stima prezzi di mercato', included: false },
      { text: 'Salvataggio nel garage digitale', included: true },
      { text: 'Domanda all\'esperto AI', included: false },
    ],
    cta: 'Scegli Intermedio',
    href: '/register?plan=intermedio',
    featured: true,
  },
  {
    name: 'Premium',
    price: '9,99 €',
    period: 'per analisi',
    description: 'Analisi completa + esperto AI',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: true },
      { text: 'Scheda tecnica sintetica', included: true },
      { text: 'Colori storici originali', included: true },
      { text: 'Analisi AI colore da foto', included: true },
      { text: 'Checklist problemi e verifica originalità', included: true },
      { text: 'Stima prezzi di mercato', included: true },
      { text: 'Salvataggio nel garage digitale', included: true },
      { text: 'Domanda all\'esperto AI', included: true },
    ],
    cta: 'Scegli Premium',
    href: '/register?plan=premium',
    featured: false,
  },
]

export default function PricingCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-5xl mx-auto">
      {plans.map((plan) => (
        <div
          key={plan.name}
          className={`relative rounded-2xl overflow-hidden transition-all duration-300 hover:scale-[1.02] ${
            plan.featured
              ? 'bg-vespa-green text-white shadow-xl ring-2 ring-vespa-green-light'
              : 'bg-white text-vespa-black border border-vespa-cream-dark'
          }`}
        >
          {/* Featured badge */}
          {plan.featured && (
            <div className="absolute top-0 right-0 bg-vespa-gold text-vespa-black text-xs font-bold px-4 py-1 rounded-bl-xl">
              Più scelto
            </div>
          )}

          <div className="p-8">
            {/* Name */}
            <h3 className={`font-heading text-2xl font-bold mb-1 ${plan.featured ? 'text-white' : 'text-vespa-black'}`}>
              {plan.name}
            </h3>
            <p className={`text-sm mb-6 ${plan.featured ? 'text-vespa-cream/80' : 'text-vespa-gray'}`}>
              {plan.description}
            </p>

            {/* Price */}
            <div className="mb-8">
              <span className={`text-4xl font-bold ${plan.featured ? 'text-white' : 'text-vespa-black'}`}>
                {plan.price}
              </span>
              {plan.period && (
                <span className={`text-sm ml-1 ${plan.featured ? 'text-vespa-cream/80' : 'text-vespa-gray'}`}>
                  {plan.period}
                </span>
              )}
            </div>

            {/* Features */}
            <ul className="space-y-3 mb-8">
              {plan.features.map((feature, i) => (
                <li key={i} className="flex items-start gap-3">
                  {feature.included ? (
                    <Check className={`w-5 h-5 shrink-0 ${plan.featured ? 'text-vespa-gold-light' : 'text-vespa-green'}`} />
                  ) : (
                    <X className={`w-5 h-5 shrink-0 ${plan.featured ? 'text-vespa-cream/40' : 'text-vespa-gray-light'}`} />
                  )}
                  <span className={`text-sm ${plan.featured ? 'text-vespa-cream/90' : 'text-vespa-gray'}`}>
                    {feature.text}
                  </span>
                </li>
              ))}
            </ul>

            {/* CTA */}
            <Link
              to={plan.href}
              className={`block text-center font-medium py-3 px-6 rounded-xl transition-colors ${
                plan.featured
                  ? 'bg-white text-vespa-green hover:bg-vespa-cream'
                  : 'bg-vespa-cream-dark text-vespa-black hover:bg-vespa-cream'
              }`}
            >
              {plan.cta}
            </Link>
          </div>
        </div>
      ))}
    </div>
  )
}