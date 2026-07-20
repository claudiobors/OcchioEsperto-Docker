import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Loader2, LogIn } from 'lucide-react'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenziali non valide. Riprova.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-vespa-green/10 flex items-center justify-center">
            <LogIn className="w-7 h-7 text-vespa-green" />
          </div>
          <h1 className="font-heading text-3xl font-bold text-vespa-black">Accedi</h1>
          <p className="text-vespa-gray text-sm mt-2">Bentornato! Accedi al tuo garage digitale.</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-vespa-cream-dark p-8 space-y-5">
          <div>
            <label className="block text-sm font-medium text-vespa-black mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="tua@email.it"
              className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-vespa-black mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
            />
          </div>

          {error && (
            <div className="bg-vespa-red/10 text-vespa-red text-sm p-3 rounded-xl">{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-vespa-green hover:bg-vespa-green-light text-white font-medium py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Accedi'}
          </button>

          <p className="text-center text-sm text-vespa-gray">
            Non hai un account?{' '}
            <Link to="/register" className="text-vespa-green hover:underline font-medium">
              Registrati
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}