import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import VespaForm from '../components/VespaForm'
import ResultsCard from '../components/ResultsCard'
import LeadForm from '../components/LeadForm'
import { FormSkeleton } from '../components/Skeletons'
import { Search, Sparkles } from 'lucide-react'

export default function Analisi() {
  const { user } = useAuth()
  const [result, setResult] = useState(null)
  const [plan, setPlan] = useState('free')
  const [loading, setLoading] = useState(false)

  const handleResult = (data) => {
    setResult(data)
    setPlan(data.plan || 'free')
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header */}
      <div className="text-center mb-10 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 bg-vespa-green/10 text-vespa-green text-sm font-medium px-4 py-2 rounded-full mb-4">
          <Sparkles className="w-4 h-4" />
          Analisi AI
        </div>
        <h1 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-4">
          Analizza la tua Vespa
        </h1>
        <p className="text-vespa-gray text-lg max-w-2xl mx-auto">
          Inserisci i dati della tua Vespa o carica una foto per ricevere un'analisi dettagliata.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-2 animate-fade-in-up-delay-1">
          {loading ? (
            <FormSkeleton />
          ) : (
            <div className="bg-white rounded-2xl border border-vespa-cream-dark p-6 sm:p-8 transition-all duration-300 hover:shadow-md">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-vespa-green/10 flex items-center justify-center">
                  <Search className="w-5 h-5 text-vespa-green" />
                </div>
                <div>
                  <h2 className="font-heading font-semibold text-vespa-black text-lg">
                    Inserisci i dati
                  </h2>
                  <p className="text-xs text-vespa-gray">
                    Tutti i campi sono opzionali — più dati inserisci, più precisa sarà l'analisi.
                  </p>
                </div>
              </div>
              <VespaForm onResult={handleResult} />
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Results (if any) */}
          {result && (
            <div className="animate-scale-in">
              <ResultsCard result={result} plan={plan} />
            </div>
          )}

          {/* Lead Form */}
          <LeadForm />
        </div>
      </div>
    </div>
  )
}