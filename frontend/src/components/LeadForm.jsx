import { useMemo, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { DollarSign, Loader2, Check, Send } from 'lucide-react'

export default function LeadForm({ garage = [], currentVehicle = null }) {
  const { user, api } = useAuth()
  const [selectedId, setSelectedId] = useState(currentVehicle?.garage_id ? String(currentVehicle.garage_id) : '')
  const [email, setEmail] = useState('')
  const [descrizione, setDescrizione] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const selectedVehicle = useMemo(
    () => garage.find((item) => String(item.id) === selectedId),
    [garage, selectedId]
  )

  const source = selectedVehicle || currentVehicle
  const modelName = source?.model_name || source?.model?.name || ''
  const year = source?.year || source?.model?.production_start || null
  const frameNumber = source?.frame_number || source?.analysis?.frame_number || ''
  const engineNumber = source?.engine_number || source?.analysis?.engine_number || ''

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await api.post('/vespa/lead', {
        contact_email: email || user?.email,
        description: [
          descrizione,
          modelName ? `Modello: ${modelName}` : '',
          year ? `Anno: ${year}` : '',
          frameNumber ? `Telaio: ${frameNumber}` : '',
          engineNumber ? `Motore: ${engineNumber}` : '',
        ].filter(Boolean).join('\n'),
        model_name: modelName || 'Vespa da garage',
        year,
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
      <div className="luxury-card rounded-[2.25rem] p-8 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl bg-vespa-green/10">
          <Check className="h-8 w-8 text-vespa-green" />
        </div>
        <h3 className="mt-5 font-heading text-2xl font-bold text-vespa-black">Richiesta inviata</h3>
        <p className="mt-2 text-sm leading-6 text-vespa-gray">Ti contatteremo per aiutarti a valorizzare la Vespa giusta, con dati già ordinati e pronti.</p>
      </div>
    )
  }

  return (
    <div className="luxury-card rounded-[2.25rem] p-6 sm:p-8">
      <div className="flex items-start gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-vespa-gold text-vespa-black">
          <DollarSign className="h-5 w-5" />
        </div>
        <div>
          <h3 className="font-heading text-2xl font-bold text-vespa-black">Vendi la tua Vespa</h3>
          <p className="mt-1 text-sm leading-6 text-vespa-gray">Usa l’analisi appena fatta o scegli un mezzo dal garage: meno dati da riscrivere, più qualità nella valutazione.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        {garage.length > 0 && (
          <div>
            <label className="mb-2 block text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Prendi dati dal garage</label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="w-full rounded-2xl border border-vespa-black/10 bg-white/80 px-4 py-3.5 text-sm outline-none transition-all focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10"
            >
              <option value="">Usa analisi accanto o inserisci a mano</option>
              {garage.map((item) => (
                <option key={item.id} value={item.id}>{item.display_name || item.model_name}</option>
              ))}
            </select>
          </div>
        )}

        {source && (
          <div className="rounded-2xl bg-vespa-cream p-4 text-sm text-vespa-gray">
            <p className="font-bold text-vespa-black">Dati pronti: {modelName || 'Vespa identificata'}</p>
            <p>{[year, frameNumber, engineNumber].filter(Boolean).join(' · ')}</p>
          </div>
        )}

        {!user && (
          <div>
            <label className="mb-2 block text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">La tua email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tua@email.it"
              required
              className="w-full rounded-2xl border border-vespa-black/10 bg-white/80 px-4 py-3.5 text-sm outline-none transition-all focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10"
            />
          </div>
        )}
        <div>
          <label className="mb-2 block text-xs font-black uppercase tracking-[0.16em] text-vespa-gray">Descrivi la vendita</label>
          <textarea
            value={descrizione}
            onChange={(e) => setDescrizione(e.target.value)}
            rows={4}
            placeholder="Stato, lavori fatti, prezzo desiderato, urgenza, documenti disponibili..."
            required
            className="w-full resize-none rounded-2xl border border-vespa-black/10 bg-white/80 px-4 py-3.5 text-sm outline-none transition-all focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10"
          />
        </div>
        {error && <p className="rounded-2xl bg-vespa-red/10 p-3 text-sm text-vespa-red">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-2xl bg-vespa-black px-6 py-4 font-black text-white transition-all hover:-translate-y-0.5 hover:bg-vespa-black-light disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? <Loader2 className="mx-auto h-5 w-5 animate-spin" /> : <span className="inline-flex items-center gap-2">Richiedi valutazione <Send className="h-4 w-4" /></span>}
        </button>
      </form>
    </div>
  )
}
