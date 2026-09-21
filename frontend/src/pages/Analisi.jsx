import { useState } from 'react'
import VespaForm from '../components/VespaForm'
import ResultsCard from '../components/ResultsCard'
import LeadForm from '../components/LeadForm'
import { FileSearch, Camera, Hash, FolderOpen } from 'lucide-react'

export default function Analisi() {
  const [result, setResult] = useState(null)
  const [plan, setPlan] = useState('free')
  const handleResult = (data) => { setResult(data); setPlan(data.plan || 'free') }
  return <div className="analysis-page">
    <section className="page-intro content-width"><div><h1>Ogni dettaglio<br /><em>è un punto di partenza.</em></h1><p>Inserisci ciò che sai della tua Vespa. Mettiamo insieme gli indizi per aiutarti a conoscerla meglio.</p></div><div className="intro-note"><FileSearch size={24} strokeWidth={1.4} /><p>Identificazione indipendente.<br />Risultati indicativi, non certificazioni.</p></div></section>
    <div className="content-width analysis-layout">
      <section className="form-surface"><div className="form-heading"><h2>Raccontaci il tuo mezzo.</h2><p>Foto e sigle ci aiutano a dare un nome alla sua storia.</p></div><VespaForm onResult={handleResult} /></section>
      <aside className="analysis-aside">
        {result ? <div aria-live="polite"><ResultsCard result={result} plan={plan} /></div> : <section className="result-placeholder"><FileSearch size={32} strokeWidth={1.3} /><h2>Qui prende forma<br />la tua scoperta.</h2><p>Dopo l’analisi troverai il modello probabile, il periodo di produzione e il livello di confidenza del risultato.</p><ul><li><Hash size={17} /><span>La sigla del telaio è il punto di partenza più utile.</span></li><li><Camera size={17} /><span>Fotografa entrambi i lati e i dettagli che vuoi approfondire.</span></li><li><FolderOpen size={17} /><span>Accedi per ritrovare la scheda nel tuo garage.</span></li></ul><figure><img src={`${import.meta.env.BASE_URL}images/workshop-detail.webp`} alt="Faro di uno scooter storico, immagine AI illustrativa" width="1536" height="1024" loading="lazy" /><figcaption>Immagine illustrativa generata con AI</figcaption></figure></section>}
        <LeadForm currentVehicle={result} />
      </aside>
    </div>
  </div>
}
