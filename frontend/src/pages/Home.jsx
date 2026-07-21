import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Search, ShieldCheck, Camera, Gauge, CheckCircle2, Sparkles, Gem, Wrench, BadgeEuro, ClipboardCheck } from 'lucide-react'
import PricingCards from '../components/PricingCards'

function ScrollRevealSection({ children, className = '' }) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.unobserve(entry.target) } },
      { threshold: 0.12 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref} className={`scroll-reveal ${visible ? 'visible' : ''} ${className}`}>
      {children}
    </div>
  )
}

const stats = [
  { value: '47+', label: 'modelli storici' },
  { value: '70 anni', label: 'di archivio Piaggio' },
  { value: 'AI + dati', label: 'non solo opinioni' },
]

const steps = [
  {
    icon: Camera,
    title: 'Carica foto o numeri',
    text: 'Telaio, motore, anno e dettagli visivi: più indizi dai, più l’identificazione diventa precisa.',
  },
  {
    icon: Search,
    title: 'Incrocio storico',
    text: 'Il motore confronta range di produzione, sigle, cilindrate, colori e schede modello.',
  },
  {
    icon: ClipboardCheck,
    title: 'Scheda chiara',
    text: 'Ricevi modello probabile, anni, cilindrata, confidenza e percorso per analisi premium.',
  },
]

const benefits = [
  { icon: ShieldCheck, title: 'Più fiducia prima di comprare', text: 'Eviti Vespe raccontate male, restauri incoerenti e stime gonfiate.' },
  { icon: Wrench, title: 'Pensato per restauratori', text: 'Colori storici, range telaio/motore e checklist originalità quando ti serve il dettaglio.' },
  { icon: BadgeEuro, title: 'Prezzo più difendibile', text: 'La stima di mercato rende più facile trattare, vendere o assicurare il mezzo.' },
]

export default function Home() {
  return (
    <div>
      <section className="relative overflow-hidden dark-panel">
        <div className="absolute inset-0 vespa-pattern opacity-30" />
        <div className="absolute left-1/2 top-0 h-[38rem] w-[38rem] -translate-x-1/2 rounded-full bg-vespa-gold/15 blur-3xl" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28 lg:py-32">
          <div className="grid lg:grid-cols-[0.92fr_1.08fr] gap-12 lg:gap-16 items-center">
            <div className="max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-sm font-bold text-vespa-gold-light shadow-2xl shadow-black/20 animate-fade-in-up">
                <Sparkles className="w-4 h-4" />
                Identificazione Vespa d’autore
              </div>

              <h1 className="mt-8 font-heading text-5xl sm:text-6xl lg:text-7xl font-bold leading-[0.95] tracking-[-0.06em] text-white animate-fade-in-up-delay-1">
                La tua Vespa merita una diagnosi bella quanto la sua storia.
              </h1>

              <p className="mt-7 text-lg sm:text-xl leading-8 text-vespa-cream/78 animate-fade-in-up-delay-2">
                OcchioEsperto unisce archivio storico, AI e occhio da collezionista per riconoscere modello,
                anno, dettagli originali e valore indicativo. Semplice, elegante, utile.
              </p>

              <div className="mt-10 flex flex-col sm:flex-row gap-4 animate-fade-in-up-delay-3">
                <Link
                  to="/analisi"
                  className="cta-primary inline-flex items-center justify-center gap-2 rounded-2xl px-7 py-4 text-base font-bold transition-transform hover:-translate-y-0.5"
                >
                  Identifica la mia Vespa
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <Link
                  to="/pricing"
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-7 py-4 text-base font-bold text-white backdrop-blur transition-all hover:-translate-y-0.5 hover:bg-white/15"
                >
                  Vedi i piani
                </Link>
              </div>

              <div className="mt-12 grid grid-cols-3 gap-3 animate-fade-in-up-delay-3">
                {stats.map((item) => (
                  <div key={item.label} className="rounded-2xl border border-white/12 bg-white/[0.06] p-4 backdrop-blur">
                    <p className="text-2xl font-black text-white">{item.value}</p>
                    <p className="mt-1 text-xs font-medium uppercase tracking-[0.18em] text-vespa-cream/55">{item.label}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative animate-fade-in-up-delay-2">
              <div className="absolute -inset-8 rounded-[3rem] bg-vespa-green/20 blur-3xl" />
              <img
                src="/static/hero-vespa.svg"
                alt="Illustrazione premium di una Vespa classica analizzata da OcchioEsperto"
                className="relative w-full rounded-[2.5rem] border border-white/12 shadow-[0_40px_120px_rgba(0,0,0,0.45)]"
              />
              <div className="absolute -bottom-6 left-6 right-6 rounded-3xl border border-white/12 bg-white/90 p-5 text-vespa-black shadow-2xl backdrop-blur md:left-auto md:w-80">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-black uppercase tracking-[0.2em] text-vespa-green">Risultato demo</p>
                    <p className="mt-1 font-heading text-2xl font-bold">Vespa 150 GS</p>
                  </div>
                  <Gauge className="h-9 w-9 text-vespa-gold" />
                </div>
                <div className="mt-4 h-2 rounded-full bg-vespa-cream-dark">
                  <div className="h-full w-[88%] rounded-full bg-gradient-to-r from-vespa-green to-vespa-gold" />
                </div>
                <p className="mt-3 text-sm text-vespa-gray">Confidenza alta · 1955—1961 · 150 cc</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <ScrollRevealSection>
        <section className="py-20 sm:py-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <p className="text-sm font-black uppercase tracking-[0.24em] text-vespa-green">Metodo</p>
              <h2 className="mt-3 font-heading text-4xl sm:text-5xl font-bold text-vespa-black">
                Tre passaggi, zero confusione.
              </h2>
              <p className="mt-4 text-lg text-vespa-gray">
                Un’esperienza da officina boutique: pochi campi, risultato chiaro, dettagli sbloccabili quando vuoi.
              </p>
            </div>

            <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6">
              {steps.map((step, index) => {
                const Icon = step.icon
                return (
                  <div key={step.title} className="luxury-card group rounded-[2rem] p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_30px_90px_rgba(9,13,18,0.16)]">
                    <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-vespa-black text-white shadow-xl shadow-vespa-black/15 transition-transform group-hover:rotate-3 group-hover:scale-105">
                      <Icon className="h-6 w-6" />
                    </div>
                    <p className="mt-8 text-sm font-black uppercase tracking-[0.22em] text-vespa-gold">0{index + 1}</p>
                    <h3 className="mt-2 font-heading text-2xl font-bold text-vespa-black">{step.title}</h3>
                    <p className="mt-3 text-sm leading-6 text-vespa-gray">{step.text}</p>
                  </div>
                )
              })}
            </div>
          </div>
        </section>
      </ScrollRevealSection>

      <ScrollRevealSection>
        <section className="py-20 sm:py-24 dark-panel overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <p className="text-sm font-black uppercase tracking-[0.24em] text-vespa-gold-light">Valore reale</p>
                <h2 className="mt-3 font-heading text-4xl sm:text-5xl font-bold text-white">
                  Non è solo “che modello è?”. È capire se vale davvero.
                </h2>
                <p className="mt-5 text-lg leading-8 text-vespa-cream/75">
                  Il bello di una Vespa classica sta nei dettagli: sigle, anni, colori, coerenza del restauro,
                  rarità e mercato. OcchioEsperto li mette in ordine in una scheda leggibile.
                </p>

                <div className="mt-9 space-y-4">
                  {benefits.map((benefit) => {
                    const Icon = benefit.icon
                    return (
                      <div key={benefit.title} className="flex gap-4 rounded-3xl border border-white/10 bg-white/[0.06] p-5 backdrop-blur">
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-vespa-gold text-vespa-black">
                          <Icon className="h-5 w-5" />
                        </div>
                        <div>
                          <h3 className="font-bold text-white">{benefit.title}</h3>
                          <p className="mt-1 text-sm leading-6 text-vespa-cream/65">{benefit.text}</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>

              <div className="relative">
                <div className="absolute -inset-8 rounded-[3rem] bg-vespa-gold/10 blur-3xl" />
                <img
                  src="/static/workshop-detail.svg"
                  alt="Scheda tecnica illustrata con dettagli storici Vespa"
                  className="relative w-full rounded-[2.5rem] border border-white/12 shadow-[0_38px_110px_rgba(0,0,0,0.42)]"
                />
              </div>
            </div>
          </div>
        </section>
      </ScrollRevealSection>

      <ScrollRevealSection>
        <section className="py-20 sm:py-24 bg-white/55">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mb-12 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
              <div className="max-w-2xl">
                <p className="text-sm font-black uppercase tracking-[0.24em] text-vespa-green">Prezzi</p>
                <h2 className="mt-3 font-heading text-4xl sm:text-5xl font-bold text-vespa-black">
                  Parti gratis. Paga solo quando vuoi più profondità.
                </h2>
              </div>
              <p className="max-w-md text-vespa-gray">
                Tre livelli puliti: identificazione rapida, scheda tecnica, oppure analisi completa da collezionista.
              </p>
            </div>
            <PricingCards />
          </div>
        </section>
      </ScrollRevealSection>

      <ScrollRevealSection>
        <section className="px-4 py-20 sm:px-6 lg:px-8">
          <div className="relative mx-auto max-w-6xl overflow-hidden rounded-[2.5rem] dark-panel p-8 text-center shadow-[0_40px_120px_rgba(9,13,18,0.28)] sm:p-14">
            <div className="absolute inset-0 vespa-pattern opacity-20" />
            <div className="relative mx-auto max-w-3xl">
              <Gem className="mx-auto h-10 w-10 text-vespa-gold-light" />
              <h2 className="mt-5 font-heading text-4xl sm:text-5xl font-bold text-white">
                Facciamola sembrare una piattaforma seria, non un form qualsiasi.
              </h2>
              <p className="mt-5 text-lg leading-8 text-vespa-cream/75">
                Inizia dall’identificazione gratuita e trasforma ogni Vespa in una scheda ordinata, utile e bella da consultare.
              </p>
              <Link
                to="/analisi"
                className="cta-primary mt-9 inline-flex items-center justify-center gap-2 rounded-2xl px-8 py-4 text-base font-bold transition-transform hover:-translate-y-0.5"
              >
                Prova ora
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </section>
      </ScrollRevealSection>
    </div>
  )
}
