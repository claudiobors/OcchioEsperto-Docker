import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { DollarSign, Loader2, Check } from 'lucide-react'

export default function LeadForm() {
  const { user, api } = useAuth()
  const [email, setEmail] = useState('')
  const [descrizione, setDescrizione] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await api.post('/vespa/lead', {
        contact_email: email || user?.email,
        description: descrizione,
        model_name: '',
      })
      setSuccess(true)
      setEmail('')
      setDescrizione('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Errore durante l\'invio. Riprova.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="bg-white rounded-2xl border border-vespa-green/30 p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-vespa-green/10 flex items-center justify-center">
          <Check className="w-8 h-8 text-vespa-green" />
        </div>
        <h3 className="font-heading text-xl font-semibold text-vespa-black mb-2">
          Richiesta Inviata!
        </h3>
        <p className="text-vespa-gray text-sm">
          Ti contatteremo per aiutarti a vendere la tua Vespa al miglior prezzo.
        </p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl border border-vespa-cream-dark p-6 sm:p-8">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-vespa-green/10 flex items-center justify-center">
          <DollarSign className="w-5 h-5 text-vespa-green" />
        </div>
        <div>
          <h3 className="font-heading font-semibold text-vespa-black">
            Vendi la tua Vespa
          </h3>
          <p className="text-xs text-vespa-gray">
            Ricevi offerte da collezionisti verificati
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {!user && (
          <div>
            <label className="block text-sm text-vespa-gray mb-1">La tua email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tua@email.it"
              required
              className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
            />
          </div>
        )}
        <div>
          <label className="block text-sm text-vespa-gray mb-1">Descrivi la tua Vespa</label>
          <textarea
            value={descrizione}
            onChange={(e) => setDescrizione(e.target.value)}
            rows={3}
            placeholder="Modello, anno, stato di conservazione, prezzo desiderato..."
            required
            className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm resize-none"
          />
        </div>
        {error && (
          <p className="text-vespa-red text-sm">{error}</p>
        )}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-vespa-green hover:bg-vespa-green-light text-white font-medium py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            'Vendi'
          )}
        </button>
      </form>
    </div>
  )
}