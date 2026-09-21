import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, ArrowUpRight, Camera, Fingerprint, FolderOpen, ScanLine, Check } from 'lucide-react'
import PricingCards from '../components/PricingCards'

const imageRoot = `${import.meta.env.BASE_URL}images/`
const details = [
  { title: 'La sua identità.', text: 'Una sigla sul telaio, una forma, un dettaglio. Incrociamo i tuoi indizi con i dati disponibili per individuare il modello e il periodo di produzione più probabili.', note: 'Modello · Anni di produzione · Cilindrata', icon: Fingerprint },
  { title: 'I dettagli che contano.', text: 'Colori, componenti e coerenza del restauro aiutano a leggere la storia di un mezzo. L’analisi completa offre indicazioni e una checklist da approfondire con un esperto.', note: 'Colori · Coerenza · Controlli di originalità', icon: ScanLine },
  { title: 'Una prospettiva sul valore.', text: 'Comprendere il mezzo è il primo passo per orientarsi nel mercato. La scheda Premium include una stima indicativa, da valutare insieme alle condizioni reali della Vespa.', note: 'Condizioni · Indicazioni di mercato · Approfondimenti', icon: FolderOpen },
]

export default function Home() {
  const [active, setActive] = useState(0)
  const detail = details[active]
  const DetailIcon = detail.icon
  return <div className="home-page">
    <section className="collector-hero" aria-labelledby="hero-title">
      <img className="hero-photo" src={`${imageRoot}collector-studio.webp`} alt="Scooter d’epoca verde salvia in un atelier, immagine illustrativa generata con AI" width="1536" height="1024" fetchPriority="high" />
      <div className="hero-shade" />
      <div className="content-width hero-layout">
        <div className="hero-copy">
          <h1 id="hero-title">Ogni Vespa<br />ha una storia.<br /><em>Scopri la tua.</em></h1>
          <p>Modello, dettagli e valore indicativo.<br className="desktop-break" /> Uno sguardo esperto sulla tua passione,<br className="desktop-break" /> con l’aiuto dei dati e dell’intelligenza artificiale.</p>
          <Link to="/analisi" className="button button-ivory">Identifica la tua Vespa <ArrowUpRight size={19} /></Link>
          <span className="hero-reassurance">Prima identificazione gratuita · Account richiesto</span>
        </div>
        <div className="hero-caption"><span>Il fascino resta.<br />La conoscenza cresce.</span><small>Scena illustrativa · Generata con AI</small></div>
      </div>
      <div className="hero-footer content-width"><span>Un progetto indipendente, dedicato agli appassionati.</span><a href="#metodo">Esplora il metodo <ArrowRight size={15} /></a></div>
    </section>
    <div className="service-strip"><div className="content-width"><span><Camera size={18} /> Foto e sigle del tuo mezzo</span><span><ScanLine size={18} /> Dati storici e analisi AI</span><span><FolderOpen size={18} /> Tutto nel tuo garage</span></div></div>
    <section id="metodo" className="content-width method-section">
      <div className="section-heading"><h2>La passione è tua.<br /><em>Gli indizi li leggiamo insieme.</em></h2><p>Da una curiosità a una scheda da conservare. Un percorso semplice, pensato per conoscere meglio ciò che hai davanti.</p></div>
      <ol className="method-list">
        <li><span className="step-number">01</span><div><h3>Parti dai dettagli</h3><p>Inserisci telaio, motore e anno. Aggiungi le fotografie per raccontare meglio il tuo mezzo.</p></div><Camera aria-hidden="true" size={25} /></li>
        <li><span className="step-number">02</span><div><h3>Metti a fuoco la storia</h3><p>Il sistema confronta le informazioni disponibili e restituisce un’identificazione con il relativo livello di confidenza.</p></div><ScanLine aria-hidden="true" size={25} /></li>
        <li><span className="step-number">03</span><div><h3>Conserva ciò che scopri</h3><p>Ritrova la scheda nel garage. Quando vuoi, approfondisci dati tecnici, originalità e valore indicativo.</p></div><FolderOpen aria-hidden="true" size={25} /></li>
      </ol>
    </section>
    <section className="detail-section" aria-labelledby="detail-title">
      <figure className="detail-image"><img src={`${imageRoot}workshop-detail.webp`} alt="Dettaglio del faro e del manubrio di uno scooter d’epoca in officina, generato con AI" loading="lazy" width="1536" height="1024" /><figcaption>La cura comincia dai dettagli. Immagine AI illustrativa.</figcaption></figure>
      <div className="detail-copy"><h2 id="detail-title">Guarda oltre<br /><em>il primo sguardo.</em></h2><div className="detail-tabs" role="group" aria-label="Esplora gli approfondimenti">{['Identità', 'Originalità', 'Valore'].map((label, index) => <button key={label} aria-pressed={active === index} onClick={() => setActive(index)}>{label}</button>)}</div><div className="detail-panel" aria-live="polite"><DetailIcon size={25} strokeWidth={1.4} /><h3>{detail.title}</h3><p>{detail.text}</p><small>{detail.note}</small></div><Link to="/analisi" className="text-link">Comincia a conoscerla <ArrowUpRight size={18} /></Link></div>
    </section>
    <section className="content-width garage-story"><div><h2>Un posto per ogni Vespa.<br /><em>E per ogni sua storia.</em></h2><p>Il tuo garage digitale raccoglie fotografie e analisi. Dai un nome ai tuoi mezzi, riapri le schede e aggiungi nuovi dettagli nel tempo.</p><Link to="/dashboard" className="button button-green">Entra nel tuo garage <ArrowUpRight size={18} /></Link></div><div className="report-preview" aria-label="Esempio illustrativo di una scheda garage"><div className="report-top"><span>OCCHIOESPERTO / GARAGE</span><span>Esempio illustrativo</span></div><h3>La tua prossima scoperta.</h3><dl><div><dt>Identificazione</dt><dd>Modello e periodo</dd></div><div><dt>Documentazione</dt><dd>Foto e dati del mezzo</dd></div><div><dt>Approfondimenti</dt><dd>Una storia da completare</dd></div></dl><p><Check size={16} /> Le schede reali si creano con la tua analisi.</p></div></section>
    <section className="plans-section"><div className="content-width"><div className="section-heading"><h2>La curiosità è un inizio.<br /><em>Scegli quanto scoprire.</em></h2><p>Inizia gratuitamente. Gli approfondimenti si acquistano per singola analisi, senza abbonamento.</p></div><PricingCards /></div></section>
    <section className="closing-section content-width"><h2>La prossima storia<br /><em>potrebbe essere la tua.</em></h2><Link to="/analisi" className="button button-green">Inizia gratuitamente <ArrowUpRight size={20} /></Link></section>
  </div>
}
