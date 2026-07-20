import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Camera, Hash, Calendar, Loader2 } from 'lucide-react'

export default function VespaForm({ onResult }) {
  const { user, api } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    frame_number: '',
    engine_number: '',
    registration_date: '',
    notes: '',
  })
  const [photo, setPhoto] = useState(null)
  const [photoPreview, setPhotoPreview] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handlePhoto = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setPhoto(file)
      const reader = new FileReader()
      reader.onloadend = () => setPhotoPreview(reader.result)
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const formPayload = new FormData()
      if (photo) formPayload.append('photo', photo)
      formPayload.append('frame_number', formData.frame_number)
      formPayload.append('engine_number', formData.engine_number)
      if (formData.registration_date) {
        formPayload.append('year', parseInt(formData.registration_date.split('-')[0]))
      }
      if (formData.notes) formPayload.append('notes', formData.notes)

      const res = await api.post('/vespa/identify', formPayload)
      onResult?.(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Errore durante l\'analisi. Riprova.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      action="/api/vespa/identify"
      method="post"
      encType="multipart/form-data"
      className="space-y-6"
    >
      {/* Photo Upload */}
      <div>
        <label className="block text-sm font-medium text-vespa-black mb-2">
          <Camera className="w-4 h-4 inline mr-1" />
          Foto della Vespa
        </label>
        <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed border-vespa-cream-dark rounded-xl hover:border-vespa-green transition-colors cursor-pointer bg-white">
          <div className="space-y-2 text-center">
            {photoPreview ? (
              <div className="relative">
                <img src={photoPreview} alt="Anteprima" className="mx-auto max-h-48 rounded-lg object-contain" />
                <button
                  type="button"
                  onClick={() => { setPhoto(null); setPhotoPreview(null) }}
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
      </div>

      {/* Frame Number */}
      <div>
        <label htmlFor="telaio" className="block text-sm font-medium text-vespa-black mb-1">
          <Hash className="w-4 h-4 inline mr-1" />
          Numero Telaio
        </label>
        <input
          type="text"
          name="frame_number"
          id="telaio"
          value={formData.frame_number}
          onChange={handleChange}
          placeholder="es. VN1T123456"
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
        />
      </div>

      {/* Engine Number */}
      <div>
        <label htmlFor="motore" className="block text-sm font-medium text-vespa-black mb-1">
          <Hash className="w-4 h-4 inline mr-1" />
          Numero Motore
        </label>
        <input
          type="text"
          name="engine_number"
          id="motore"
          value={formData.engine_number}
          onChange={handleChange}
          placeholder="es. VNM1T123456"
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
        />
      </div>

      {/* Registration Date */}
      <div>
        <label htmlFor="immatricolazione" className="block text-sm font-medium text-vespa-black mb-1">
          <Calendar className="w-4 h-4 inline mr-1" />
          Data Immatricolazione
        </label>
        <input
          type="date"
          name="registration_date"
          id="immatricolazione"
          value={formData.registration_date}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm"
        />
        <input
          type="hidden"
          name="year"
          value={formData.registration_date ? formData.registration_date.split('-')[0] : ''}
        />
      </div>
      <div>
        <label htmlFor="note" className="block text-sm font-medium text-vespa-black mb-1">
          Note aggiuntive
        </label>
        <textarea
          name="notes"
          id="note"
          rows={3}
          value={formData.notes}
          onChange={handleChange}
          placeholder="Eventuali dettagli aggiuntivi..."
          className="w-full px-4 py-3 rounded-xl border border-vespa-cream-dark bg-white focus:border-vespa-green focus:ring-1 focus:ring-vespa-green outline-none transition-colors text-sm resize-none"
        />
      </div>

      {/* Error */}
      {error && (
        <div className="bg-vespa-red/10 text-vespa-red text-sm p-3 rounded-xl">
          {error}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-vespa-green hover:bg-vespa-green-light text-white font-medium py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Analisi in corso...
          </>
        ) : (
          'Analizza la tua Vespa'
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