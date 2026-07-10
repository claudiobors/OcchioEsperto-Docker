import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Menu, X, Search, LogOut, User } from 'lucide-react'
import { useState } from 'react'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-vespa-black text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-full bg-vespa-green flex items-center justify-center">
              <span className="text-white font-bold text-sm">OE</span>
            </div>
            <span className="font-heading text-xl font-bold tracking-tight">
              Occhio<span className="text-vespa-green">Esperto</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            <Link to="/" className="text-vespa-gray-light hover:text-white transition-colors text-sm font-medium">
              Home
            </Link>
            <Link to="/analisi" className="text-vespa-gray-light hover:text-white transition-colors text-sm font-medium">
              Analisi
            </Link>
            <Link to="/pricing" className="text-vespa-gray-light hover:text-white transition-colors text-sm font-medium">
              Piani
            </Link>
            {user && (
              <Link to="/dashboard" className="text-vespa-gray-light hover:text-white transition-colors text-sm font-medium">
                Il mio garage
              </Link>
            )}
            {user ? (
              <div className="flex items-center gap-3">
                <span className="text-sm text-vespa-gray-light">
                  <User className="w-4 h-4 inline mr-1" />
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
              <div className="flex items-center gap-3">
                <Link
                  to="/login"
                  className="text-sm text-vespa-gray-light hover:text-white transition-colors"
                >
                  Accedi
                </Link>
                <Link
                  to="/register"
                  className="bg-vespa-green hover:bg-vespa-green-light text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Registrati
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-vespa-gray-light hover:text-white"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-vespa-black-light border-t border-vespa-black-light/50">
          <div className="px-4 py-4 space-y-3">
            <Link to="/" onClick={() => setIsOpen(false)} className="block text-vespa-gray-light hover:text-white text-sm font-medium">
              Home
            </Link>
            <Link to="/analisi" onClick={() => setIsOpen(false)} className="block text-vespa-gray-light hover:text-white text-sm font-medium">
              Analisi
            </Link>
            <Link to="/pricing" onClick={() => setIsOpen(false)} className="block text-vespa-gray-light hover:text-white text-sm font-medium">
              Piani
            </Link>
            {user && (
              <Link to="/dashboard" onClick={() => setIsOpen(false)} className="block text-vespa-gray-light hover:text-white text-sm font-medium">
                Il mio garage
              </Link>
            )}
            {user ? (
              <button onClick={() => { logout(); setIsOpen(false) }} className="block text-vespa-gray-light hover:text-white text-sm font-medium">
                Esci
              </button>
            ) : (
              <div className="flex gap-3 pt-2">
                <Link to="/login" onClick={() => setIsOpen(false)} className="text-vespa-gray-light hover:text-white text-sm">
                  Accedi
                </Link>
                <Link to="/register" onClick={() => setIsOpen(false)} className="bg-vespa-green text-white px-4 py-2 rounded-lg text-sm">
                  Registrati
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}