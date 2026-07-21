import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import { Camera, Hash, Calendar, Loader2, AlertCircle } from 'lucide-react'

export default function VespaForm({ onResult }) {
  const { user, api } = useAuth()
  const { addToast } = useToast()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [errors, setErrors] = useState({})
  const [formData, setFormData] = useState({
    telaio: '',
    motore: '',
    immatricolazione: '',
    note: '',
  })
  const [photos, setPhotos] = useState([])
  const [photoPreviews, setPhotoPreviews] = useState([])

  const validateField = (name, value) => {
    if (name === 'telaio' && value && value.length < 3) {
      return 'Il numero telaio è troppo corto'
    }
    if (name === 'motore' && value && value.length < 3) {
      return 'Il numero motore è troppo corto'
    }
    return ''
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    // Clear error on change
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }))
    }
    // Inline validation
    const fieldError = validateField(name, value)
    if (fieldError) {
      setErrors((prev) => ({ ...prev, [name]: fieldError }))
    }
  }

  const handlePhoto = (e) => {
    const selected = Array.from(e.target.files || [])
    if (selected.length) {
      if (photos.length + selected.length > 10) {
        setErrors((prev) => ({ ...prev, photo: 'Puoi caricare fino a 10 fotografie' }))
        return
      }
      for (const file of selected) {
      if (file.size > 10 * 1024 * 1024) {
        setErrors((prev) => ({ ...prev, photo: 'La foto non può superare i 10MB' }))
        return
      }
      if (!file.type.startsWith('image/')) {
        setErrors((prev) => ({ ...prev, photo: 'Il file deve essere un\'immagine' }))
        return
      }
      }
      setPhotos((prev) => [...prev, ...selected])
      setErrors((prev) => ({ ...prev, photo: '' }))
      selected.forEach((file) => {
        const reader = new FileReader()
        reader.onloadend = () => setPhotoPreviews((prev) => [...prev, reader.result])
        reader.readAsDataURL(file)
      })
    }
  }

  const removePhoto = (index) => {
    setPhotos((prev) => prev.filter((_, i) => i !== index))
    setPhotoPreviews((prev) => prev.filter((_, i) => i !== index))
    setErrors((prev) => ({ ...prev, photo: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!user) {
      setError('Accedi o crea il tuo account gratuito per avviare l’identificazione e ritrovare la scheda nel garage.')
      return
    }

    // Validate all fields
    const newErrors = {}
    if (formData.telaio) {
      const err = validateField('telaio', formData.telaio)
      if (err) newErrors.telaio = err
    }
    if (formData.motore) {
      const err = validateField('motore', formData.motore)
      if (err) newErrors.motore = err
    }
    setErrors(newErrors)

    if (Object.keys(newErrors).length > 0) {
      addToast('Correggi gli errori nel form prima di continuare', 'error')
      return
    }

    setLoading(true)

    try {
      const formPayload = new FormData()
      photos.forEach((file) => formPayload.append('photos', file))
      if (formData.telaio) formPayload.append('frame_number', formData.telaio)
      if (formData.motore) formPayload.append('engine_number', formData.motore)
      if (formData.note) formPayload.append('notes', formData.note)
      if (formData.immatricolazione) {
        formPayload.append('year', new Date(formData.immatricolazione).getFullYear().toString())
      }

      const res = await api.post('/vespa/identify', formPayload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      onResult?.(res.data)
      addToast('Identificazione completata con successo!', 'success')
    } catch (err) {
      const detail = err.response?.data?.detail
      const msg = Array.isArray(detail)
        ? detail.map((item) => item.msg).join(', ')
        : detail || 'Errore durante l\'identificazione. Riprova.'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }

  const inputClass = (fieldName) => `
    w-full px-4 py-3.5 rounded-2xl border bg-white/80 outline-none transition-all duration-200 text-sm shadow-inner shadow-vespa-black/5
    ${errors[fieldName] ? 'border-vespa-red focus:border-vespa-red focus:ring-4 focus:ring-vespa-red/10' : 'border-vespa-black/10 focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10'}
  `

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Photo Upload */}
      <div>
        <label className="block text-sm font-black uppercase tracking-[0.16em] text-vespa-black mb-3">
          <Camera className="w-4 h-4 inline mr-1 text-vespa-green" />
          Foto della Vespa <span className="text-vespa-gray">({photos.length}/10)</span>
        </label>
        <div className={`mt-1 flex justify-center px-6 pt-6 pb-7 border-2 border-dashed rounded-[1.75rem] cursor-pointer bg-white/70 transition-all duration-200 hover:bg-white ${
          errors.photo ? 'border-vespa-red' : 'border-vespa-black/10 hover:border-vespa-green/70'
        }`}>
          <div className="space-y-3 text-center">
            {photoPreviews.length > 0 ? (
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                {photoPreviews.map((preview, index) => (
                  <div key={`${preview}-${index}`} className="relative rounded-2xl bg-white p-2 shadow-sm">
                    <img src={preview} alt={`Anteprima ${index + 1}`} className="h-28 w-full rounded-xl object-cover" />
                    <button
                      type="button"
                      onClick={() => removePhoto(index)}
                      className="mt-2 text-xs font-bold text-vespa-red hover:underline"
                    >
                      Rimuovi
                    </button>
                  </div>
                ))}
                {photos.length < 10 && (
                  <label htmlFor="photo-upload" className="flex min-h-32 cursor-pointer items-center justify-center rounded-2xl border border-dashed border-vespa-black/15 text-sm font-bold text-vespa-green">
                    Aggiungi foto
                  </label>
                )}
              </div>
            ) : (
              <>
                <Camera className="mx-auto h-10 w-10 text-vespa-gray-light" />
                <div className="text-sm text-vespa-gray-light">
                  <label htmlFor="photo-upload" className="relative cursor-pointer text-vespa-green hover:text-vespa-green-dark font-medium">
                    <span>Carica una foto</span>
                    <input id="photo-upload" type="file" accept="image/*" multiple className="sr-only" onChange={handlePhoto} />
                  </label>
                  <p className="text-xs">PNG, JPG fino a 10MB ciascuna · massimo 10 foto</p>
                </div>
              </>
            )}
            {photoPreviews.length > 0 && (
              <input id="photo-upload" type="file" accept="image/*" multiple className="sr-only" onChange={handlePhoto} />
            )}
          </div>
        </div>
        {errors.photo && (
          <p className="flex items-center gap-1 text-xs text-vespa-red mt-1">
            <AlertCircle className="w-3 h-3" />
            {errors.photo}
          </p>
        )}
      </div>

      {/* Frame Number */}
      <div>
        <label htmlFor="telaio" className="block text-sm font-black uppercase tracking-[0.16em] text-vespa-black mb-2">
          <Hash className="w-4 h-4 inline mr-1 text-vespa-green" />
          Numero Telaio
        </label>
        <input
          type="text"
          name="telaio"
          id="telaio"
          value={formData.telaio}
          onChange={handleChange}
          placeholder="es. VN1T123456"
          className={inputClass('telaio')}
        />
        {errors.telaio && (
          <p className="flex items-center gap-1 text-xs text-vespa-red mt-1">
            <AlertCircle className="w-3 h-3" />
            {errors.telaio}
          </p>
        )}
      </div>

      {/* Engine Number */}
      <div>
        <label htmlFor="motore" className="block text-sm font-black uppercase tracking-[0.16em] text-vespa-black mb-2">
          <Hash className="w-4 h-4 inline mr-1 text-vespa-green" />
          Numero Motore
        </label>
        <input
          type="text"
          name="motore"
          id="motore"
          value={formData.motore}
          onChange={handleChange}
          placeholder="es. VNM1T123456"
          className={inputClass('motore')}
        />
        {errors.motore && (
          <p className="flex items-center gap-1 text-xs text-vespa-red mt-1">
            <AlertCircle className="w-3 h-3" />
            {errors.motore}
          </p>
        )}
      </div>

      {/* Registration Date */}
      <div>
        <label htmlFor="immatricolazione" className="block text-sm font-black uppercase tracking-[0.16em] text-vespa-black mb-2">
          <Calendar className="w-4 h-4 inline mr-1 text-vespa-green" />
          Data Immatricolazione
        </label>
        <input
          type="date"
          name="immatricolazione"
          id="immatricolazione"
          value={formData.immatricolazione}
          onChange={handleChange}
          className="w-full px-4 py-3.5 rounded-2xl border border-vespa-black/10 bg-white/80 focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10 outline-none transition-colors text-sm shadow-inner shadow-vespa-black/5"
        />
      </div>

      {/* Notes */}
      <div>
        <label htmlFor="note" className="block text-sm font-black uppercase tracking-[0.16em] text-vespa-black mb-2">
          Note aggiuntive
        </label>
        <textarea
          name="note"
          id="note"
          rows={3}
          value={formData.note}
          onChange={handleChange}
          placeholder="Eventuali dettagli aggiuntivi..."
          className="w-full px-4 py-3.5 rounded-2xl border border-vespa-black/10 bg-white/80 focus:border-vespa-green focus:ring-4 focus:ring-vespa-green/10 outline-none transition-colors text-sm resize-none shadow-inner shadow-vespa-black/5"
        />
      </div>

      {/* Error */}
      {error && (
        <div className="bg-vespa-red/10 text-vespa-red text-sm p-3 rounded-xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={loading || !user}
        className="cta-primary w-full rounded-2xl py-4 px-6 font-black transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:-translate-y-0.5"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Analisi in corso...
          </>
        ) : (
          user ? 'Identifica la mia Vespa' : 'Accedi per identificare la tua Vespa'
        )}
      </button>

      {!user && (
        <div className="rounded-3xl border border-vespa-gold/30 bg-vespa-gold/10 p-4 text-center">
          <p className="text-sm font-bold text-vespa-black">Il tuo garage digitale ti aspetta.</p>
          <p className="mt-1 text-xs leading-5 text-vespa-gray">
            Accedi o crea l’account gratuito per iniziare l’identificazione e ritrovare ogni analisi sempre ordinata.
          </p>
          <div className="mt-3 flex justify-center gap-2">
            <Link to="/login" className="rounded-full bg-white px-4 py-2 text-xs font-black text-vespa-black shadow-sm">Accedi</Link>
            <Link to="/register" className="rounded-full bg-vespa-black px-4 py-2 text-xs font-black text-white shadow-sm">Crea account</Link>
          </div>
        </div>
      )}
    </form>
  )
}