import { Check, Minus, ArrowUpRight } from 'lucide-react'
import { Link } from 'react-router-dom'

const plans = [
  { name: 'Base', price: '0', description: 'Il primo incontro con la sua storia.', cta: 'Identifica gratis', href: '/analisi', features: [['Identificazione modello e anno', true], ['Garage digitale', true], ['Range telaio e motore', false], ['Scheda tecnica sintetica', false], ['Colori e indicazioni di mercato', false]] },
  { name: 'Intermedio', price: '4,99', description: 'I dati per conoscerla meglio.', cta: 'Scegli Intermedio', href: '/register?plan=intermedio', features: [['Identificazione modello e anno', true], ['Garage digitale', true], ['Range telaio e motore', true], ['Scheda tecnica sintetica', true], ['Colori e indicazioni di mercato', false]] },
  { name: 'Premium', price: '9,99', description: 'Uno sguardo più approfondito.', cta: 'Scegli Premium', href: '/register?plan=avanzato', featured: true, features: [['Identificazione e scheda tecnica', true], ['Range telaio e motore', true], ['Colori storici', true], ['Checklist originalità e problemi', true], ['Stima indicativa di mercato', true]] },
]

export default function PricingCards() {
  return <div className="plan-grid">{plans.map(plan => <article className={`plan-card ${plan.featured ? 'plan-featured' : ''}`} key={plan.name}><div className="plan-title"><h3>{plan.name}</h3>{plan.featured && <span>Analisi completa</span>}</div><p className="plan-description">{plan.description}</p><div className="plan-price"><span>{plan.price}</span><span>€<small>{plan.price === '0' ? 'per iniziare' : 'per analisi'}</small></span></div><Link className={`button ${plan.featured ? 'button-ivory' : 'button-outline'}`} to={plan.href}>{plan.cta}<ArrowUpRight size={17} /></Link><ul>{plan.features.map(([label, included]) => <li key={label} className={included ? '' : 'not-included'}>{included ? <Check size={16} /> : <Minus size={16} />}<span>{label}{!included && <span className="sr-only"> — non incluso</span>}</span></li>)}</ul><p className="plan-note">{plan.price === '0' ? 'Registrazione gratuita richiesta' : 'Registrazione prima del pagamento'}</p></article>)}</div>
}
