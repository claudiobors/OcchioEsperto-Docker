import PricingCards from '../components/PricingCards'
import { Sparkles, HelpCircle } from 'lucide-react'

const faqs = [
  ['Come funziona il pagamento?', 'Per le schede complete prima crei un account, poi vai al pagamento sicuro Stripe. Così credenziali, consenso e scheda restano collegati al tuo garage.'],
  ['Posso salvare le analisi?', 'Sì. Le schede complete richiedono registrazione: potrai conservarle nel garage digitale e consultarle quando vuoi.'],
  ['Sostituisce un certificato ufficiale?', 'No. È un supporto basato su dati storici e AI: utile per orientarti, non un certificato di origine Piaggio.'],
  ['Come funziona la vendita?', 'La richiesta “Vendi la tua Vespa” raccoglie i dettagli e ti mette in contatto con potenziali acquirenti o supporto dedicato.'],
]

export default function Pricing() {
  return (
    <div>
      <section className="dark-panel relative overflow-hidden px-4 py-16 text-center sm:px-6 sm:py-20 lg:px-8">
        <div className="absolute inset-0 vespa-pattern opacity-25" />
        <div className="relative mx-auto max-w-4xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-black text-vespa-gold-light">
            <Sparkles className="h-4 w-4" />
            Piani e prezzi
          </div>
          <h1 className="mt-7 font-heading text-5xl font-bold leading-[0.95] tracking-[-0.06em] text-white sm:text-6xl">
            Scegli quanto in profondità vuoi andare.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-vespa-cream/72">
            Gratis per iniziare. Per la scheda completa ti registri prima, poi paghi in modo sicuro: flusso chiaro, GDPR e dati sotto controllo.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 pb-20 pt-12 sm:px-6 lg:px-8">
        <PricingCards />
      </section>

      <section className="bg-white/55 py-20">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <HelpCircle className="mx-auto h-9 w-9 text-vespa-green" />
            <h2 className="mt-4 font-heading text-4xl font-bold text-vespa-black">Domande frequenti</h2>
          </div>
          <div className="mt-10 grid gap-4 sm:grid-cols-2">
            {faqs.map(([question, answer]) => (
              <div key={question} className="luxury-card rounded-3xl p-6">
                <h3 className="font-bold text-vespa-black">{question}</h3>
                <p className="mt-3 text-sm leading-7 text-vespa-gray">{answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
