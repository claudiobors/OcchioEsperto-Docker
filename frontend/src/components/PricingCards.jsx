import { Check, X, Crown } from 'lucide-react'
import { Link } from 'react-router-dom'

const plans = [
  {
    name: 'Base',
    price: 'Gratis',
    period: '',
    description: 'Per capire subito da dove partire.',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: false },
      { text: 'Scheda tecnica sintetica', included: false },
      { text: 'Colori storici originali', included: false },
      { text: 'Stima prezzi di mercato', included: false },
      { text: 'Garage digitale', included: true },
    ],
    cta: 'Inizia gratis',
    href: '/analisi',
    featured: false,
  },
  {
    name: 'Intermedio',
    price: '4,99 €',
    period: 'per analisi',
    description: 'La scheda tecnica che serve davvero.',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: true },
      { text: 'Scheda tecnica sintetica', included: true },
      { text: 'Colori storici originali', included: false },
      { text: 'Stima prezzi di mercato', included: false },
      { text: 'Garage digitale', included: true },
    ],
    cta: 'Scegli Intermedio',
    href: '/register?plan=intermedio',
    featured: true,
  },
  {
    name: 'Premium',
    price: '9,99 €',
    period: 'per analisi',
    description: 'Per comprare, vendere o restaurare meglio.',
    features: [
      { text: 'Identificazione modello + anno', included: true },
      { text: 'Range numeri telaio/motore', included: true },
      { text: 'Scheda tecnica sintetica', included: true },
      { text: 'Colori storici originali', included: true },
      { text: 'Checklist originalità + problemi', included: true },
      { text: 'Stima prezzi di mercato', included: true },
    ],
    cta: 'Scegli Premium',
    href: '/register?plan=premium',
    featured: false,
  },
]

export default function PricingCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
      {plans.map((plan) => (
        <div
          key={plan.name}
          className={`relative overflow-hidden rounded-[2rem] p-[1px] transition-all duration-300 hover:-translate-y-2 ${
            plan.featured
              ? 'bg-gradient-to-br from-vespa-gold via-white/20 to-vespa-green shadow-[0_32px_100px_rgba(47,111,173,0.26)]'
              : 'bg-vespa-black/10 shadow-[0_22px_70px_rgba(9,13,18,0.08)]'
          }`}
        >
          <div className={`h-full rounded-[calc(2rem-1px)] p-8 ${plan.featured ? 'pricing-card-premium text-white' : 'pricing-card-gradient text-vespa-black'}`}>
            {plan.featured && (
              <div className="mb-7 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-xs font-black uppercase tracking-[0.18em] text-vespa-gold-light">
                <Crown className="h-3.5 w-3.5" />
                Più scelto
              </div>
            )}

            <h3 className={`font-heading text-3xl font-bold ${plan.featured ? 'text-white' : 'text-vespa-black'}`}>
              {plan.name}
            </h3>
            <p className={`mt-2 text-sm leading-6 ${plan.featured ? 'text-vespa-cream/68' : 'text-vespa-gray'}`}>
              {plan.description}
            </p>

            <div className="mt-8 flex items-end gap-2">
              <span className={`text-5xl font-black tracking-[-0.06em] ${plan.featured ? 'text-white' : 'text-vespa-black'}`}>
                {plan.price}
              </span>
              {plan.period && <span className={`pb-2 text-sm ${plan.featured ? 'text-vespa-cream/58' : 'text-vespa-gray'}`}>{plan.period}</span>}
            </div>

            <ul className="mt-8 space-y-3.5">
              {plan.features.map((feature) => (
                <li key={feature.text} className="flex items-start gap-3">
                  {feature.included ? (
                    <Check className={`mt-0.5 h-5 w-5 shrink-0 ${plan.featured ? 'text-vespa-gold-light' : 'text-vespa-green'}`} />
                  ) : (
                    <X className={`mt-0.5 h-5 w-5 shrink-0 ${plan.featured ? 'text-vespa-cream/30' : 'text-vespa-gray-light'}`} />
                  )}
                  <span className={`text-sm leading-6 ${feature.included ? (plan.featured ? 'text-vespa-cream/88' : 'text-vespa-black-light') : (plan.featured ? 'text-vespa-cream/38' : 'text-vespa-gray')}`}>
                    {feature.text}
                  </span>
                </li>
              ))}
            </ul>

            <Link
              to={plan.href}
              className={`mt-9 block rounded-2xl px-6 py-3.5 text-center text-sm font-black transition-all ${
                plan.featured
                  ? 'bg-white text-vespa-black shadow-xl shadow-black/15 hover:-translate-y-0.5 hover:bg-vespa-gold-light'
                  : 'bg-vespa-black text-white hover:-translate-y-0.5 hover:bg-vespa-black-light'
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
