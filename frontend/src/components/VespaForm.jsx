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
      if (formData.telaio) formPayload.append('frame_number', formData.telaio)
      if (formData.motore) formPayload.append('engine_number', formData.motore)
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
          Foto della Vespa
        </label>
        <div className={`mt-1 flex justify-center px-6 pt-6 pb-7 border-2 border-dashed rounded-[1.75rem] cursor-pointer bg-white/70 transition-all duration-200 hover:bg-white ${
          errors.photo ? 'border-vespa-red' : 'border-vespa-black/10 hover:border-vespa-green/70'
        }`}>
          <div className="space-y-3 text-center">
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
        disabled={loading}
        className="cta-primary w-full rounded-2xl py-4 px-6 font-black transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:-translate-y-0.5"
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