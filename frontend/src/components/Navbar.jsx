import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Menu, X, LogOut, User, Sparkles } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target) && isOpen) setIsOpen(false)
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  useEffect(() => {
    const handleEsc = (e) => { if (e.key === 'Escape') setIsOpen(false) }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [])

  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/analisi', label: 'Analisi' },
    { to: '/pricing', label: 'Piani' },
    ...(user ? [{ to: '/dashboard', label: 'Garage' }] : []),
  ]

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-vespa-black/90 text-white shadow-2xl shadow-black/10 backdrop-blur-2xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-18 items-center justify-between">
          <Link to="/" className="group flex items-center gap-3" onClick={() => setIsOpen(false)}>
            <div className="relative flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-vespa-gold to-vespa-green shadow-lg shadow-vespa-gold/20 transition-transform group-hover:-rotate-3 group-hover:scale-105">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div className="leading-none">
              <span className="block font-heading text-2xl font-bold tracking-[-0.05em]">
                Occhio<span className="gold-text">Esperto</span>
              </span>
              <span className="text-[10px] font-black uppercase tracking-[0.28em] text-vespa-cream/48">
                Vespa AI atelier
              </span>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-2">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="rounded-full px-4 py-2 text-sm font-bold text-vespa-cream/70 transition-all hover:bg-white/10 hover:text-white"
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <>
                <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-4 py-2 text-sm font-bold text-vespa-cream/70">
                  <User className="h-4 w-4" />
                  {user.name}
                </span>
                <button
                  onClick={logout}
                  className="inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-bold text-vespa-cream/70 transition-all hover:bg-white/10 hover:text-white"
                >
                  <LogOut className="h-4 w-4" />
                  Esci
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="rounded-full px-4 py-2 text-sm font-bold text-vespa-cream/70 transition-colors hover:text-white">
                  Accedi
                </Link>
                <Link to="/analisi" className="cta-primary rounded-full px-5 py-2.5 text-sm font-black transition-transform hover:-translate-y-0.5">
                  Prova gratis
                </Link>
              </>
            )}
          </div>

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden rounded-2xl border border-white/10 bg-white/10 p-2.5 text-vespa-cream/80 transition-colors hover:bg-white/15 hover:text-white"
            aria-label="Menu"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      <div
        ref={menuRef}
        className={`md:hidden overflow-hidden border-t border-white/10 bg-vespa-black-light/95 transition-all duration-300 ${isOpen ? 'max-h-[34rem] opacity-100' : 'max-h-0 opacity-0'}`}
      >
        <div className="px-4 py-4 space-y-2">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setIsOpen(false)}
              className="block rounded-2xl px-4 py-3 text-sm font-bold text-vespa-cream/70 transition-all hover:bg-white/10 hover:text-white"
            >
              {link.label}
            </Link>
          ))}
          <div className="grid grid-cols-2 gap-3 pt-3">
            {user ? (
              <button
                onClick={() => { logout(); setIsOpen(false) }}
                className="col-span-2 rounded-2xl border border-white/10 px-4 py-3 text-sm font-bold text-vespa-cream/72"
              >
                Esci
              </button>
            ) : (
              <>
                <Link to="/login" onClick={() => setIsOpen(false)} className="rounded-2xl border border-white/10 px-4 py-3 text-center text-sm font-bold text-vespa-cream/72">
                  Accedi
                </Link>
                <Link to="/analisi" onClick={() => setIsOpen(false)} className="cta-primary rounded-2xl px-4 py-3 text-center text-sm font-black">
                  Prova gratis
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
