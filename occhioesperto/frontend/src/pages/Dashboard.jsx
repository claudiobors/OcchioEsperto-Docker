import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import GarageGrid from '../components/GarageGrid'
import LeadForm from '../components/LeadForm'
import { ArrowRight, Gauge, Loader2, Plus, ShieldCheck, Warehouse } from 'lucide-react'

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
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-vespa-cream px-4">
        <div className="text-center bg-white rounded-[2rem] border border-vespa-cream-dark p-10 max-w-md shadow-xl">
          <Warehouse className="w-12 h-12 text-vespa-green mx-auto mb-4" />
          <h2 className="font-heading text-3xl font-bold text-vespa-black mb-4">Accedi al tuo garage</h2>
          <p className="text-vespa-gray mb-6">Salva analisi, confronta Vespe e conserva le verifiche fatte prima dell'acquisto.</p>
          <Link to="/login" className="inline-flex items-center gap-2 bg-vespa-green text-white px-6 py-3 rounded-xl font-bold">Accedi <ArrowRight className="w-4 h-4" /></Link>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-[linear-gradient(180deg,#1a1a1a_0%,#1a1a1a_260px,#f5f0e8_260px,#fff_100%)] min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12">
        <div className="text-white mb-10 flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
          <div>
            <p className="text-vespa-gold uppercase tracking-[0.25em] text-xs font-bold mb-3">Area personale</p>
            <h1 className="font-heading text-4xl sm:text-5xl font-bold">Il mio garage</h1>
            <p className="text-vespa-gray-light text-sm mt-3">Benvenuto, {user.name}. Hai {analyses.length} Vespa{analyses.length !== 1 ? 'e' : ''} salvata{analyses.length !== 1 ? 'e' : ''}.</p>
          </div>
          <Link to="/analisi" className="inline-flex items-center gap-2 bg-vespa-green hover:bg-vespa-green-light text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-vespa-green/20">
            <Plus className="w-5 h-5" /> Nuova analisi
          </Link>
        </div>

        <div className="grid sm:grid-cols-3 gap-4 mb-8">
          <Stat icon={Warehouse} value={analyses.length} label="Vespe salvate" />
          <Stat icon={Gauge} value={user.plan || 'free'} label="Piano attivo" />
          <Stat icon={ShieldCheck} value="GDPR" label="Dati sotto controllo" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          <div className="lg:col-span-2 bg-white rounded-[2rem] border border-vespa-cream-dark p-5 sm:p-7 shadow-xl shadow-vespa-green/5">
            {loading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-vespa-green" />
              </div>
            ) : analyses.length ? (
              <GarageGrid analyses={analyses} />
            ) : (
              <div className="text-center py-16">
                <Warehouse className="w-14 h-14 text-vespa-green mx-auto mb-4" />
                <h2 className="font-heading text-2xl font-bold text-vespa-black mb-2">Garage vuoto</h2>
                <p className="text-vespa-gray mb-6">Fai la prima analisi e salvala qui per ritrovarla quando vuoi.</p>
                <Link to="/analisi" className="inline-flex items-center gap-2 bg-vespa-green text-white px-6 py-3 rounded-xl font-bold">Analizza una Vespa <ArrowRight className="w-4 h-4" /></Link>
              </div>
            )}
          </div>

          <div className="space-y-6 lg:sticky lg:top-24">
            <LeadForm />
          </div>
        </div>
      </div>
    </div>
  )
}

function Stat({ icon: Icon, value, label }) {
  return (
    <div className="bg-white rounded-2xl border border-vespa-cream-dark p-5 shadow-lg shadow-vespa-green/5">
      <Icon className="w-5 h-5 text-vespa-green mb-3" />
      <div className="font-heading text-3xl font-bold text-vespa-black capitalize">{String(value)}</div>
      <div className="text-sm text-vespa-gray mt-1">{label}</div>
    </div>
  )
}
