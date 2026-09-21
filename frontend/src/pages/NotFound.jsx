import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'
export default function NotFound() {
  return <section className="content-width not-found"><span>404 / Pagina non trovata</span><h1>Una piccola deviazione.</h1><p>La pagina che cerchi non esiste o è stata spostata. Riparti dalla homepage per ritrovare la tua strada.</p><Link to="/" className="button button-green">Torna alla homepage <ArrowUpRight size={18} /></Link></section>
}
