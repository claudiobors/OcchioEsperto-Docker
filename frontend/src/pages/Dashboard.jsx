import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import GarageGrid from '../components/GarageGrid'
import LeadForm from '../components/LeadForm'
import { StatsCardSkeleton, GarageGridSkeleton } from '../components/Skeletons'
import { Bike, Clock, Award, TrendingUp, Loader2 } from 'lucide-react'

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
        <div className="text-center animate-fade-in-up">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-vespa-cream-dark flex items-center justify-center">
            <Bike className="w-10 h-10 text-vespa-gray-light" />
          </div>
          <h2 className="font-heading text-2xl font-bold text-vespa-black mb-4">Accedi per vedere il tuo garage</h2>
          <p className="text-vespa-gray">Effettua il login per visualizzare le tue Vespe salvate.</p>
        </div>
      </div>
    )
  }

  const lastAnalysis = analyses.length > 0
    ? analyses.reduce((latest, a) => !latest || new Date(a.created_at) > new Date(latest.created_at) ? a : latest, null)
    : null

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header */}
      <div className="mb-8 animate-fade-in-up">
        <h1 className="font-heading text-3xl font-bold text-vespa-black">
          Il mio garage
        </h1>
        <p className="text-vespa-gray text-sm mt-1">
          Benvenuto, {user.name}
        </p>
      </div>

      {/* Stats Cards */}
      {!loading && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8 animate-fade-in-up-delay-1">
          <div className="bg-white rounded-xl border border-vespa-cream-dark p-5 transition-all duration-300 hover:shadow-md hover:border-vespa-green/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-vespa-green/10 flex items-center justify-center">
                <Bike className="w-5 h-5 text-vespa-green" />
              </div>
              <div>
                <p className="text-xs text-vespa-gray font-medium">Vespe salvate</p>
                <p className="text-2xl font-bold text-vespa-black font-heading">{analyses.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-vespa-cream-dark p-5 transition-all duration-300 hover:shadow-md hover:border-vespa-green/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-vespa-gold/10 flex items-center justify-center">
                <Award className="w-5 h-5 text-vespa-gold" />
              </div>
              <div>
                <p className="text-xs text-vespa-gray font-medium">Piano attivo</p>
                <p className="text-lg font-bold text-vespa-black font-heading capitalize">{user.plan || 'Free'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-vespa-cream-dark p-5 transition-all duration-300 hover:shadow-md hover:border-vespa-green/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-vespa-green/10 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-vespa-green" />
              </div>
              <div>
                <p className="text-xs text-vespa-gray font-medium">Analisi totali</p>
                <p className="text-2xl font-bold text-vespa-black font-heading">{analyses.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-vespa-cream-dark p-5 transition-all duration-300 hover:shadow-md hover:border-vespa-green/30">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-vespa-black-light/10 flex items-center justify-center">
                <Clock className="w-5 h-5 text-vespa-gray" />
              </div>
              <div>
                <p className="text-xs text-vespa-gray font-medium">Ultima analisi</p>
                <p className="text-sm font-semibold text-vespa-black">
                  {lastAnalysis
                    ? new Date(lastAnalysis.created_at).toLocaleDateString('it-IT')
                    : '—'
                  }
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[1, 2, 3, 4].map((i) => <StatsCardSkeleton key={i} />)}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content */}
        <div className="lg:col-span-2">
          {loading ? (
            <GarageGridSkeleton />
          ) : (
            <div className="animate-fade-in-up">
              <GarageGrid analyses={analyses} />
            </div>
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