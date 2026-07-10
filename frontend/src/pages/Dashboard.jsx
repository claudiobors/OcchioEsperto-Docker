import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import GarageGrid from '../components/GarageGrid'
import LeadForm from '../components/LeadForm'
import { Loader2 } from 'lucide-react'

export default function Dashboard() {
  const { user, api } = useAuth()
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      api.get('/vespa/garage')
        .then((res) => setAnalyses(res.data.vespe || []))
        .catch(() => {})
        .finally(() => setLoading(false))
    }
  }, [user])

  if (!user) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="text-center">
          <h2 className="font-heading text-2xl font-bold text-vespa-black mb-4">Accedi per vedere il tuo garage</h2>
          <p className="text-vespa-gray">Effettua il login per visualizzare le tue Vespe salvate.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-vespa-black">
            Il mio garage
          </h1>
          <p className="text-vespa-gray text-sm mt-1">
            Benvenuto, {user.name} — {analyses.length} Vespa{analyses.length !== 1 ? 'e' : ''} salvata{analyses.length !== 1 ? 'e' : ''}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content */}
        <div className="lg:col-span-2">
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-8 h-8 animate-spin text-vespa-green" />
            </div>
          ) : (
            <GarageGrid analyses={analyses} />
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <LeadForm />
        </div>
      </div>
    </div>
  )
}