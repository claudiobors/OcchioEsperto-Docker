import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Menu, X, LogOut, User, Sparkles } from 'lucide-react'
import { useState } from 'react'

const navClass = ({ isActive }) =>
  `text-sm font-semibold transition-colors ${isActive ? 'text-white' : 'text-vespa-gray-light hover:text-white'}`

export default function Navbar() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-vespa-black/95 text-white sticky top-0 z-50 border-b border-white/10 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-[72px] py-3">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative w-11 h-11 rounded-2xl bg-vespa-cream text-vespa-black flex items-center justify-center shadow-lg">
              <span className="font-heading font-black text-sm">OE</span>
              <span className="absolute -right-1 -bottom-1 w-4 h-4 rounded-full bg-vespa-green border-2 border-vespa-black" />
            </div>
            <div>
              <span className="block font-heading text-xl font-bold tracking-tight leading-none">
                Occhio<span className="text-vespa-green">Esperto</span>
              </span>
              <span className="text-[10px] uppercase tracking-[0.22em] text-vespa-gray-light">Vespa intelligence</span>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-7">
            <NavLink to="/" className={navClass}>Home</NavLink>
            <NavLink to="/analisi" className={navClass}>Analisi</NavLink>
            <NavLink to="/pricing" className={navClass}>Piani</NavLink>
            {user && <NavLink to="/dashboard" className={navClass}>Garage</NavLink>}
          </div>

          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <>
                <div className="flex items-center gap-2 rounded-full bg-white/10 border border-white/10 px-3 py-2">
                  <User className="w-4 h-4 text-vespa-gold" />
                  <span className="text-sm text-vespa-cream max-w-36 truncate">{user.name}</span>
                </div>
                <button onClick={logout} className="flex items-center gap-1 text-sm text-vespa-gray-light hover:text-white transition-colors">
                  <LogOut className="w-4 h-4" /> Esci
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-sm font-semibold text-vespa-gray-light hover:text-white transition-colors">Accedi</Link>
                <Link to="/analisi" className="bg-vespa-green hover:bg-vespa-green-light text-white px-5 py-3 rounded-xl text-sm font-bold transition-colors inline-flex items-center gap-2 shadow-lg shadow-vespa-green/20">
                  <Sparkles className="w-4 h-4" /> Prova gratis
                </Link>
              </>
            )}
          </div>

          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden text-vespa-gray-light hover:text-white p-2">
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-vespa-black-light border-t border-white/10">
          <div className="px-4 py-5 space-y-4">
            {[
              ['/', 'Home'],
              ['/analisi', 'Analisi'],
              ['/pricing', 'Piani'],
              ...(user ? [['/dashboard', 'Garage']] : []),
            ].map(([to, label]) => (
              <Link key={to} to={to} onClick={() => setIsOpen(false)} className="block text-vespa-gray-light hover:text-white text-sm font-semibold">
                {label}
              </Link>
            ))}
            {user ? (
              <button onClick={() => { logout(); setIsOpen(false) }} className="block text-vespa-gray-light hover:text-white text-sm font-semibold">Esci</button>
            ) : (
              <div className="grid grid-cols-2 gap-3 pt-2">
                <Link to="/login" onClick={() => setIsOpen(false)} className="text-center border border-white/10 text-vespa-gray-light px-4 py-3 rounded-xl text-sm font-semibold">Accedi</Link>
                <Link to="/analisi" onClick={() => setIsOpen(false)} className="text-center bg-vespa-green text-white px-4 py-3 rounded-xl text-sm font-bold">Prova gratis</Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
