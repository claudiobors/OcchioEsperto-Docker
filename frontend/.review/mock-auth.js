const analysis = {
  id: 'DEMO-01', garage_id: 1, plan: 'premium', confidence: 'high',
  model: { name: 'Vespa 125 — esempio sintetico', engine_cc: 125 },
  identification: { years: '1960–1965 (esempio)', engine_cc: 125 },
  expert_analysis: {
    expert_summary: 'Dati dimostrativi: le informazioni inserite sono coerenti con il profilo del modello usato per questa prova. Questo contenuto serve esclusivamente a verificare il layout del report.',
    evidence: ['Sigla telaio dimostrativa: DEMO-125', 'Cilindrata sintetica: 125 cc', 'Fotografie non caricate in questa verifica'],
    recommended_checks: ['Confrontare le sigle reali sul mezzo.', 'Verificare i documenti con un esperto qualificato.']
  }
}
const vehicle = { id: 1, display_name: 'La prima Vespa — esempio', model_name: 'Vespa 125 (dati sintetici)', year: 1962, frame_number: 'DEMO-TELAIO-123456', engine_number: 'DEMO-MOTORE-654321', analysis_level: 'basic', created_at: '2026-09-21T10:00:00Z', analysis }
const items = [vehicle]
const user = { name: 'Collezionista Demo', email: 'demo@example.invalid', plan: 'free' }
const api = {
  get: async (path) => ({data: path === '/vespa/garage' ? {vespe:items} : vehicle}),
  post: async (path) => {
    if (path === '/vespa/identify') return {data: analysis}
    throw new Error('Azione disabilitata nella fixture: nessuna transazione reale.')
  },
  patch: async (_path, data) => { Object.assign(vehicle,data); return {data:vehicle} }
}
export function useAuth() { return {user,api,loading:false,logout:()=>{}} }
export function AuthProvider({children}) { return children }

