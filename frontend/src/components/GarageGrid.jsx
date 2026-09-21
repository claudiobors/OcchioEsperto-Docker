import { Link } from 'react-router-dom'
import { Calendar, ArrowUpRight, Camera, FolderOpen } from 'lucide-react'

export default function GarageGrid({ analyses, onSelect }) {
  if (!analyses || analyses.length === 0) {
    return <div className="garage-empty"><FolderOpen size={38} strokeWidth={1.3} /><h3>La prima storia ti aspetta.</h3><p>Il tuo garage è ancora vuoto. Identifica una Vespa per iniziare a raccogliere fotografie, dati e approfondimenti.</p><Link to="/analisi" className="button button-green">Aggiungi la prima Vespa <ArrowUpRight size={17} /></Link></div>
  }
  return <div className="vehicle-grid">{analyses.map(item => <button key={item.id} type="button" onClick={() => onSelect?.(item)} className="vehicle-card"><div className="vehicle-image">{item.photo_path ? <img src={'/' + item.photo_path} alt={item.display_name || item.model_name || 'Il tuo mezzo'} loading="lazy" /> : <div className="vehicle-placeholder"><Camera size={30} strokeWidth={1.3} /><span>Nessuna foto aggiunta</span></div>}</div><div className="vehicle-info"><h3>{item.display_name || item.model_name || 'Vespa'}</h3><p>{item.model_name}</p>{item.year && <span><Calendar size={13} />{item.year}</span>}<div><span>{item.analysis_level === 'basic' ? 'Analisi Base' : 'Analisi Pro'}</span><ArrowUpRight size={19} /></div></div></button>)}</div>
}
