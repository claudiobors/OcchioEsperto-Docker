import { useState } from 'react'
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
  const [photo, setPhoto] = useState(null)
  const [photoPreview, setPhotoPreview] = useState(null)

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
    const file = e.target.files?.[0]
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setErrors((prev) => ({ ...prev, photo: 'La foto non può superare i 10MB' }))
        return
      }
      if (!file.type.startsWith('image/')) {
        setErrors((prev) => ({ ...prev, photo: 'Il file deve essere un\'immagine' }))
        return
      }
      setPhoto(file)
      setErrors((prev) => ({ ...prev, photo: '' }))
      const reader = new FileReader()
      reader.onloadend = () => setPhotoPreview(reader.result)
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

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
      if (photo) formPayload.append('photo', photo)
      formPayload.append('telaio', formData.telaio)
      formPayload.append('motore', formData.motore)
      formPayload.append('immatricolazione', formData.immatricolazione)
      formPayload.append('note', formData.note)

      const res = await api.post('/analyze', formPayload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      onResult?.(res.data)
      addToast('Analisi completata con successo!', 'success')
    } catch (err) {
      const msg = err.response?.data?.detail || 'Errore durante l\'analisi. Riprova.'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }

  const inputClass = (fieldName) => `
    w-full px-4 py-3 rounded-xl border bg-white outline-none transition-all duration-200 text-sm
    ${errors[fieldName] ? 'border-vespa-red focus:border-vespa-red focus:ring-1 focus:ring-vespa-red' : 'border-vespa-cream-dark focus:border-vespa-green focus:ring-1 focus:ring-vespa-green'}
  `

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Photo Upload */}
      <div>
        <label className="block text-sm font-medium text-vespa-black mb-2">
          <Camera className="w-4 h-4 inline mr-1" />
          Foto della Vespa
        </label>
        <div className={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-xl cursor-pointer bg-white transition-all duration-200 ${
          errors.photo ? 'border-vespa-red' : 'border-vespa-cream-dark hover:border-vespa-green'
        }`}>
          <div className="space-y-2 text-center">
            {photoPreview ? (
              <div className="relative">
                <img src={photoPreview} alt="Anteprima" className="mx-auto max-h-48 rounded-lg object-contain" />
                <button
                  type="button"
                  onClick={() => { setPhoto(null); setPhotoPreview(null); setErrors((prev) => ({ ...prev, photo: '' })) }}
                  className="mt-2 text-xs text-vespa-red hover:underline"
                >
                  Rimuovi foto
                </button>
              </div>
            ) : (
              <>
                <Camera className="mx-auto h-10 w-10 text-vespa-gray-light" />
                <div className="text-sm text-vespa-gray-light">
                  <label htmlFor="photo-upload" className="relative cursor-pointer text-vespa-green hover:text-vespa-green-dark font-medium">
                    <span>Carica una foto</span>
                    <input id="photo-upload" type="file" accept="image/*" className="sr-only" onChange={handlePhoto} />
                  </label>
                  <p className="text-xs">PNG, JPG fino a 10MB</p>
                </div>
              </>
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
        <label htmlFor="telaio" className="block text-sm font-medium text-vespa-black mb-1">
          <Hash className="w-4 h-4 inline mr-1" />
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
        <label htmlFor="motore" className="block text-sm font-medium text-vespa-black mb-1">
          <Hash className="w-4 h-4 inline mr-1" />
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
        <label htmlFor="immatricolazione" className="block text-sm font-medium text-vespa-black mb-1">
          <Calendar className="w-4 h-4 inline mr-1" />
          Data Immatricolazione
        </label>
        <input
          type="date"
          name="immatricolazione"
          id="immatricolazione"
          value={formData.immatricolazione}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
        />
      </div>

      {/* Notes */}
      <div>
        <label htmlFor="note" className="block text-sm font-medium text-vespa-black mb-1">
          Note aggiuntive
        </label>
        <textarea
          name="note"
          id="note"
          rows={3}
          value={formData.note}
          onChange={handleChange}
          placeholder="Eventuali dettagli aggiuntivi..."
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm resize-none"
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
        disabled={loading}
        className="w-full bg-vespa-green hover:bg-vespa-green-light text-white font-medium py-3 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-vespa-green/20"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Analisi in corso...
          </>
        ) : (
          'Identifica la mia Vespa'
        )}
      </button>

      {!user && (
        <p className="text-xs text-vespa-gray text-center">
          Effettua il login per salvare i risultati nel tuo garage digitale.
        </p>
      )}
    </form>
  )
}