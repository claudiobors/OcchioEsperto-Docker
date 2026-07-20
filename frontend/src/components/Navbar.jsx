import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Menu, X, LogOut, User } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef(null)

  // Close menu on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target) && isOpen) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  // Close menu on route change (esc key)
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') setIsOpen(false)
    }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [])

  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/analisi', label: 'Analisi' },
    { to: '/pricing', label: 'Piani' },
    ...(user ? [{ to: '/dashboard', label: 'Il mio garage' }] : []),
  ]

  return (
    <nav className="bg-vespa-black text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group" onClick={() => setIsOpen(false)}>
            <div className="w-8 h-8 rounded-full bg-vespa-green flex items-center justify-center transition-transform group-hover:scale-110 duration-200">
              <span className="text-white font-bold text-sm">OE</span>
            </div>
            <span className="font-heading text-xl font-bold tracking-tight">
              Occhio<span className="text-vespa-green">Esperto</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="text-vespa-gray-light hover:text-white transition-colors text-sm font-medium relative after:absolute after:bottom-[-4px] after:left-0 after:w-0 after:h-0.5 after:bg-vespa-green after:transition-all after:duration-300 hover:after:w-full"
              >
                {link.label}
              </Link>
            ))}
            {user ? (
              <div className="flex items-center gap-3 ml-2 pl-3 border-l border-vespa-black-light/50">
                <span className="text-sm text-vespa-gray-light flex items-center gap-1.5">
                  <User className="w-4 h-4" />
                  {user.name}
                </span>
                <button
                  onClick={logout}
                  className="flex items-center gap-1 text-sm text-vespa-gray-light hover:text-white transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Esci
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3 ml-2 pl-3 border-l border-vespa-black-light/50">
                <Link
                  to="/login"
                  className="text-sm text-vespa-gray-light hover:text-white transition-colors"
                >
                  Accedi
                </Link>
                <Link
                  to="/register"
                  className="bg-vespa-green hover:bg-vespa-green-light text-white px-4 py-2 rounded-lg text-sm font-medium transition-all hover:shadow-lg hover:shadow-vespa-green/20"
                >
                  Registrati
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-vespa-gray-light hover:text-white p-2 rounded-lg hover:bg-vespa-black-light/50 transition-colors"
            aria-label="Menu"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu with smooth transition */}
      <div
        ref={menuRef}
        className={`md:hidden overflow-hidden transition-all duration-300 ease-in-out ${
          isOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="bg-vespa-black-light border-t border-vespa-black-light/50 px-4 py-4 space-y-1">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setIsOpen(false)}
              className="block text-vespa-gray-light hover:text-white hover:bg-vespa-black/50 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
            >
              {link.label}
            </Link>
          ))}
          <div className="border-t border-vespa-black-light/50 my-2 pt-3">
            {user ? (
              <div className="space-y-2">
                <span className="block text-vespa-gray-light text-sm px-3">
                  <User className="w-4 h-4 inline mr-2" />
                  {user.name}
                </span>
                <button
                  onClick={() => { logout(); setIsOpen(false) }}
                  className="w-full text-left text-vespa-gray-light hover:text-white hover:bg-vespa-black/50 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
                >
                  <LogOut className="w-4 h-4 inline mr-2" />
                  Esci
                </button>
              </div>
            ) : (
              <div className="flex gap-3 px-3">
                <Link
                  to="/login"
                  onClick={() => setIsOpen(false)}
                  className="flex-1 text-center text-vespa-gray-light hover:text-white border border-vespa-black-light/50 hover:bg-vespa-black/50 px-4 py-2.5 rounded-lg text-sm transition-all duration-200"
                >
                  Accedi
                </Link>
                <Link
                  to="/register"
                  onClick={() => setIsOpen(false)}
                  className="flex-1 text-center bg-vespa-green hover:bg-vespa-green-light text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
                >
                  Registrati
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}