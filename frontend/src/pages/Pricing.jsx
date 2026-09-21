import PricingCards from '../components/PricingCards'
import { Plus } from 'lucide-react'

const faqs = [
  ['È un abbonamento?', 'No. Gli approfondimenti sono acquistati per singola analisi. L’identificazione Base è gratuita.'],
  ['Come funziona il pagamento?', 'Crea un account e completa il pagamento tramite Stripe. La scheda rimane collegata al tuo account e al tuo garage digitale.'],
  ['Posso salvare le analisi?', 'Sì. Con un account puoi conservare le identificazioni nel garage, aggiungere fotografie e consultare i tuoi mezzi.'],
  ['L’analisi è un certificato ufficiale?', 'No. È un supporto informativo indipendente basato sui dati disponibili e sull’AI. Non sostituisce una perizia, una verifica fisica o un certificato ufficiale.'],
  ['Come funziona la richiesta di vendita?', 'Il modulo “Vendi la tua Vespa” raccoglie i dettagli e i tuoi contatti per una richiesta di supporto. Non garantisce la vendita del mezzo.'],
]
export default function Pricing() {
  return <div className="pricing-page"><section className="page-intro content-width"><div><h1>Quanto vuoi sapere<br /><em>della tua Vespa?</em></h1><p>Una prima risposta gratuita. Oppure uno sguardo più approfondito, con un acquisto per singola analisi.</p></div><div className="intro-note"><p>Nessun abbonamento.<br />Scegli tu, una scoperta alla volta.</p></div></section><section className="content-width pricing-content" aria-label="Confronta i piani"><PricingCards /><p className="pricing-footnote">Account richiesto. Analisi e stime indicative, senza valore di certificazione ufficiale.</p></section><section className="content-width faq-section"><h2>Prima di cominciare.</h2><div>{faqs.map(([question, answer]) => <details key={question}><summary>{question}<Plus size={18} /></summary><p>{answer}</p></details>)}</div></section></div>
}
