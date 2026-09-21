import { Link, NavLink, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Menu, X, ArrowUpRight, LogOut } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import Brand from './Brand'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef(null)
  const triggerRef = useRef(null)
  const { pathname } = useLocation()
  useEffect(() => { setIsOpen(false) }, [pathname])
  useEffect(() => {
    const close = (event) => {
      if (event.type === 'keydown' && event.key === 'Escape') {
        setIsOpen(false)
        triggerRef.current?.focus()
      } else if (event.type === 'mousedown' && !menuRef.current?.contains(event.target)) setIsOpen(false)
    }
    document.addEventListener('mousedown', close)
    document.addEventListener('keydown', close)
    return () => { document.removeEventListener('mousedown', close); document.removeEventListener('keydown', close) }
  }, [])
  const links = [['/', 'Il progetto'], ['/analisi', 'Identifica'], ['/pricing', 'Piani e prezzi'], ['/dashboard', 'Il mio garage']]
  return (
    <header className="site-header" ref={menuRef}>
      <a className="skip-link" href="#main-content">Vai al contenuto</a>
      <div className="site-nav content-width">
        <Link to="/" aria-label="OcchioEsperto, homepage"><Brand /></Link>
        <nav className="desktop-nav" aria-label="Navigazione principale">
          {links.map(([to, label]) => <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>)}
        </nav>
        <div className="nav-account">
          {user ? <button className="text-link" onClick={logout}><LogOut size={16} /> Esci</button> : <Link className="text-link" to="/login">Accedi</Link>}
          <Link to="/analisi" className="button button-green button-small">Inizia l’analisi <ArrowUpRight size={16} /></Link>
        </div>
        <button ref={triggerRef} className="menu-toggle" aria-label={isOpen ? 'Chiudi menu' : 'Apri menu'} aria-expanded={isOpen} aria-controls="mobile-navigation" onClick={() => setIsOpen(!isOpen)}>{isOpen ? <X /> : <Menu />}</button>
      </div>
      <nav id="mobile-navigation" className="mobile-nav" aria-label="Navigazione mobile" hidden={!isOpen}>
        {links.map(([to, label]) => <NavLink key={to} to={to} end={to === '/'}>{label}<ArrowUpRight size={17} /></NavLink>)}
        {user ? <button onClick={() => { logout(); setIsOpen(false) }}>Esci dall’account</button> : <Link to="/login">Accedi al tuo account <ArrowUpRight size={17} /></Link>}
      </nav>
    </header>
  )
}
