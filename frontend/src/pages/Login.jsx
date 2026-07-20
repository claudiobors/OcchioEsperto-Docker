import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import { Loader2, LogIn, AlertCircle, Eye, EyeOff } from 'lucide-react'

export default function Login() {
  const { login } = useAuth()
  const { addToast } = useToast()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const newErrors = {}
    if (!email) newErrors.email = 'Inserisci la tua email'
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Email non valida'
    if (!password) newErrors.password = 'Inserisci la password'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!validate()) return
    setLoading(true)
    try {
      await login(email, password)
      addToast('Bentornato! Accesso effettuato.', 'success')
      navigate('/dashboard')
    } catch (err) {
      const msg = err.response?.data?.detail || 'Credenziali non valide. Riprova.'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }

  const inputClass = (field) => `
    w-full px-4 py-3 rounded-xl border bg-white outline-none transition-all duration-200 text-sm
    ${errors[field] ? 'border-vespa-red focus:border-vespa-red focus:ring-1 focus:ring-vespa-red' : 'border-vespa-cream-dark focus:border-vespa-green focus:ring-1 focus:ring-vespa-green'}
  `

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md animate-fade-in-up">
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
              onChange={(e) => { setEmail(e.target.value); setErrors((p) => ({...p, email: ''})) }}
              onBlur={() => {
                if (email && !/\S+@\S+\.\S+/.test(email)) setErrors((p) => ({...p, email: 'Email non valida'}))
              }}
              required
              placeholder="tua@email.it"
              className={inputClass('email')}
            />
            {errors.email && (
              <p className="flex items-center gap-1 text-xs text-vespa-red mt-1">
                <AlertCircle className="w-3 h-3" />
                {errors.email}
              </p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-vespa-black mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => { setPassword(e.target.value); setErrors((p) => ({...p, password: ''})) }}
                required
                placeholder="••••••••"
                className={inputClass('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-vespa-gray-light hover:text-vespa-gray"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {errors.password && (
              <p className="flex items-center gap-1 text-xs text-vespa-red mt-1">
                <AlertCircle className="w-3 h-3" />
                {errors.password}
              </p>
            )}
          </div>

          {error && (
            <div className="bg-vespa-red/10 text-vespa-red text-sm p-3 rounded-xl flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-vespa-green hover:bg-vespa-green-light text-white font-medium py-3 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-vespa-green/20"
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