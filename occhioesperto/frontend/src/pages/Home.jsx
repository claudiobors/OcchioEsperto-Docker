import { Link } from 'react-router-dom'
import { ArrowRight, BadgeEuro, Camera, CheckCircle, FileSearch, Gauge, Shield, Sparkles, Star, Wrench } from 'lucide-react'
import PricingCards from '../components/PricingCards'
import heroImage from '../assets/hero.png'

const stats = [
  ['1946–oggi', 'modelli storici e moderni'],
  ['3 minuti', 'per una prima lettura utile'],
  ['AI fallback', 'più modelli, Grok per ultimo'],
]

const features = [
  { icon: Camera, title: 'Foto + numeri', text: 'Carichi immagine, telaio, motore e anno. Il sistema combina gli indizi invece di affidarsi a un solo dato.' },
  { icon: FileSearch, title: 'Knowledge base Vespa', text: 'Modelli, sigle telaio/motore, colori, problemi ricorrenti e prezzi indicativi consultabili e arricchibili.' },
  { icon: Shield, title: 'Risposte prudenti', text: 'Disclaimer chiari, punteggio di attendibilità e controlli consigliati prima di comprare o vendere.' },
]

export default function Home() {
  return (
    <div className="overflow-hidden bg-vespa-cream">
      <section className="relative min-h-[calc(100vh-4rem)] bg-vespa-black text-white flex items-center">
        <div className="absolute inset-0 opacity-50">
          <img src={heroImage} alt="Vespa vintage" className="w-full h-full object-cover" />
        </div>
        <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(26,26,26,.98)_0%,rgba(26,26,26,.82)_42%,rgba(26,26,26,.35)_100%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_75%_20%,rgba(198,164,74,.28),transparent_30%)]" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 w-full">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 bg-white/10 border border-white/15 text-vespa-cream text-sm font-semibold px-4 py-2 rounded-full mb-8 backdrop-blur">
              <Sparkles className="w-4 h-4 text-vespa-gold" /> OcchioEsperto per Vespa: utile, rapido, prudente
            </div>
            <h1 className="font-heading text-5xl sm:text-6xl lg:text-7xl font-bold leading-[0.95] tracking-tight">
              Capisci se quella Vespa è davvero un affare.
            </h1>
            <p className="mt-7 text-lg sm:text-xl text-vespa-gray-light leading-relaxed max-w-2xl">
              Identifica modello e anno, confronta colori e punzonature, scopri rischi tecnici e ottieni una stima indicativa prima di acquistare, vendere o restaurare.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 mt-10">
              <Link to="/analisi" className="group bg-vespa-green hover:bg-vespa-green-light text-white font-bold px-8 py-4 rounded-xl transition-all flex items-center justify-center gap-2 text-lg shadow-2xl shadow-vespa-green/30">
                Analizza la tua Vespa <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/pricing" className="bg-white/10 hover:bg-white/15 text-white font-semibold px-8 py-4 rounded-xl transition-colors border border-white/15 text-lg backdrop-blur text-center">
                Vedi perché conviene
              </Link>
            </div>

            <div className="grid sm:grid-cols-3 gap-3 mt-12 max-w-3xl">
              {stats.map(([value, label]) => (
                <div key={value} className="bg-white/10 border border-white/10 rounded-2xl p-4 backdrop-blur">
                  <div className="font-heading text-2xl font-bold text-vespa-gold">{value}</div>
                  <div className="text-xs text-vespa-gray-light mt-1">{label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-[.8fr_1.2fr] gap-12 items-start">
            <div>
              <p className="text-vespa-green font-bold uppercase tracking-[0.25em] text-xs mb-4">Metodo chiaro</p>
              <h2 className="font-heading text-4xl sm:text-5xl font-bold text-vespa-black leading-tight">Non solo AI: una scheda decisionale.</h2>
              <p className="text-vespa-gray mt-5 leading-relaxed">Il risultato è progettato per aiutarti a decidere: cosa torna, cosa non torna, quanto fidarti e cosa verificare dal vivo.</p>
            </div>
            <div className="grid md:grid-cols-3 gap-5">
              {features.map((f) => (
                <div key={f.title} className="rounded-[2rem] bg-vespa-cream/70 border border-vespa-cream-dark p-6 hover:-translate-y-1 transition-transform">
                  <div className="w-12 h-12 rounded-2xl bg-vespa-green text-white flex items-center justify-center mb-5"><f.icon className="w-6 h-6" /></div>
                  <h3 className="font-heading text-xl font-bold text-vespa-black mb-3">{f.title}</h3>
                  <p className="text-sm text-vespa-gray leading-relaxed">{f.text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-vespa-black text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="rounded-[2rem] bg-white text-vespa-black p-6 sm:p-8 shadow-2xl">
              <div className="flex items-center justify-between border-b border-vespa-cream-dark pb-5 mb-5">
                <div>
                  <p className="text-xs uppercase tracking-[0.25em] text-vespa-gray">Esempio report</p>
                  <h3 className="font-heading text-3xl font-bold">Primavera ET3</h3>
                </div>
                <div className="text-right"><div className="text-3xl font-bold text-vespa-green">99%</div><div className="text-xs text-vespa-gray">attendibilità</div></div>
              </div>
              <div className="space-y-3">
                <ReportRow icon={Gauge} title="Match telaio" text="Sigla VMB1T compatibile con ET3, anno coerente." />
                <ReportRow icon={Wrench} title="Controlli" text="Verifica accensione elettronica, carter, numero motore VMB1M." />
                <ReportRow icon={BadgeEuro} title="Valore" text="Stima indicativa per condizione: progetto, buona, restaurata." />
                <ReportRow icon={Star} title="Affare?" text="L'AI spiega rischi e prossimi passi, non vende false certezze." />
              </div>
            </div>
            <div>
              <p className="text-vespa-gold font-bold uppercase tracking-[0.25em] text-xs mb-4">Perché sembra un affare</p>
              <h2 className="font-heading text-4xl sm:text-5xl font-bold leading-tight">Costa meno di una perizia sbagliata e ti prepara meglio.</h2>
              <p className="text-vespa-gray-light mt-5 leading-relaxed text-lg">Anche quando poi serve un esperto fisico, arrivi con domande migliori: sigle, colori, problemi noti, range prezzi e documenti da controllare.</p>
              <Link to="/analisi" className="inline-flex items-center gap-2 mt-8 bg-white text-vespa-black hover:bg-vespa-cream font-bold px-7 py-4 rounded-xl">
                Prova ora <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white" id="pricing">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-14">
            <p className="text-vespa-green font-bold uppercase tracking-[0.25em] text-xs mb-4">Piani semplici</p>
            <h2 className="font-heading text-4xl sm:text-5xl font-bold text-vespa-black mb-4">Scegli quanto vuoi approfondire</h2>
            <p className="text-vespa-gray text-lg max-w-2xl mx-auto">Gratis per iniziare, completo quando vuoi valutare seriamente un acquisto, restauro o vendita.</p>
          </div>
          <PricingCards />
        </div>
      </section>

      <section className="py-20 bg-vespa-green text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <CheckCircle className="w-12 h-12 mx-auto mb-5 text-vespa-gold-light" />
          <h2 className="font-heading text-4xl sm:text-5xl font-bold mb-5">Pronto a guardarla con occhio esperto?</h2>
          <p className="text-vespa-cream/85 text-lg mb-8">Carica foto e dati. In pochi passaggi ottieni una scheda utile, leggibile e con i giusti limiti legali.</p>
          <Link to="/analisi" className="inline-flex items-center gap-2 bg-white hover:bg-vespa-cream text-vespa-green font-bold px-8 py-4 rounded-xl text-lg">
            Inizia l'analisi <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  )
}

function ReportRow({ icon: Icon, title, text }) {
  return (
    <div className="flex gap-4 rounded-2xl bg-vespa-cream/70 p-4">
      <Icon className="w-5 h-5 text-vespa-green shrink-0 mt-1" />
      <div><p className="font-semibold">{title}</p><p className="text-sm text-vespa-gray">{text}</p></div>
    </div>
  )
}
