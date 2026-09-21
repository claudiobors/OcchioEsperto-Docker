import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'
import Brand from './Brand'

export default function Footer() {
  return <footer className="site-footer">
    <div className="content-width">
      <div className="footer-main">
        <div><Link to="/" aria-label="OcchioEsperto, homepage"><Brand /></Link><p>Per chi vede una storia,<br />prima ancora di uno scooter.</p></div>
        <nav aria-label="Esplora"><h2>Esplora</h2><Link to="/analisi">Identifica la tua Vespa</Link><Link to="/dashboard">Il mio garage</Link><Link to="/pricing">Piani e prezzi</Link></nav>
        <nav aria-label="Informazioni"><h2>Informazioni</h2><Link to="/terms">Termini di servizio</Link><Link to="/privacy">Privacy</Link><a href="mailto:info@occhioesperto.it">Scrivici <ArrowUpRight size={14} /></a></nav>
      </div>
      <div className="footer-disclaimer"><strong>Uno sguardo indipendente.</strong><p>OcchioEsperto non è affiliato, approvato o sponsorizzato dal Gruppo Piaggio. Vespa, Piaggio e i relativi marchi appartengono ai rispettivi titolari e sono citati a scopo descrittivo. Le analisi e le stime sono indicative: non costituiscono perizie o certificati ufficiali.</p></div>
      <div className="footer-bottom"><span>© {new Date().getFullYear()} OcchioEsperto</span><span>Le immagini editoriali sono generate con AI e hanno finalità illustrative.</span></div>
    </div>
  </footer>
}
