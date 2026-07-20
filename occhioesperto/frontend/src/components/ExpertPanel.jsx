import { useState } from 'react'
import { Bot, Loader2, Send, Sparkles } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const starterQuestions = [
  'Quali controlli devo fare prima di acquistare?',
  'Il prezzo richiesto è realistico?',
  'Cosa può ridurre il valore di questo modello?',
]

export default function ExpertPanel({ result }) {
  const { api } = useAuth()
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const modelId = result?.model?.id || result?.analysis?.model?.id
  if (!modelId) return null

  const ask = async (q = question) => {
    if (!q.trim()) return
    setLoading(true)
    setError('')
    setAnswer('')
    setQuestion(q)
    try {
      const res = await api.post('/vespa/expert', {
        model_id: modelId,
        question: q,
        context: {
          confidence: result.confidence,
          match_type: result.match_type,
          identification: result.identification,
          analysis: result.analysis,
        },
      })
      setAnswer(res.data.answer)
    } catch (err) {
      setError(err.response?.data?.detail || 'Esperto AI non disponibile. Verifica OPENROUTER_API_KEY nel file .env.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-vespa-black text-white rounded-[2rem] overflow-hidden border border-white/10 shadow-2xl">
      <div className="p-6 border-b border-white/10 bg-[radial-gradient(circle_at_top_right,rgba(198,164,74,.22),transparent_35%)]">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-11 h-11 rounded-2xl bg-vespa-green flex items-center justify-center">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-heading text-xl font-bold">Esperto AI</h3>
            <p className="text-xs text-vespa-gray-light">Domande tecniche, valore, originalità, rischi acquisto</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-4">
        <div className="flex flex-wrap gap-2">
          {starterQuestions.map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => ask(q)}
              className="text-xs rounded-full border border-white/10 bg-white/5 hover:bg-white/10 px-3 py-2 text-vespa-cream transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Es. secondo te è un affare a 4.800 €?"
            className="flex-1 rounded-xl bg-white/10 border border-white/10 px-4 py-3 text-sm text-white placeholder:text-vespa-gray-light outline-none focus:border-vespa-gold"
          />
          <button
            onClick={() => ask()}
            disabled={loading || !question.trim()}
            className="rounded-xl bg-vespa-gold hover:bg-vespa-gold-light text-vespa-black px-4 py-3 disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </div>

        {error && <div className="rounded-xl bg-vespa-red/20 border border-vespa-red/30 p-3 text-sm text-red-100">{error}</div>}
        {answer && (
          <div className="rounded-2xl bg-white text-vespa-black p-4 leading-relaxed text-sm whitespace-pre-line">
            <div className="flex items-center gap-2 font-semibold text-vespa-green mb-2">
              <Sparkles className="w-4 h-4" /> Risposta esperta
            </div>
            {answer}
          </div>
        )}
      </div>
    </div>
  )
}
