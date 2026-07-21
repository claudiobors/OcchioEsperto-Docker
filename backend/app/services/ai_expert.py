"""
OcchioEsperto.it — AI Expert Service.

Uses the local knowledge base first and OpenRouter when configured. No API keys
are stored in code; set OPENROUTER_API_KEY and AI_MODEL_FALLBACKS in the env.
"""
import json
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from .knowledge_base import knowledge_base, KnowledgeBase
from ..config import (
    AI_APP_NAME,
    AI_MODEL_FALLBACKS,
    AI_SITE_URL,
    DISCLAIMER,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)


class AIExpert:
    """Vespa expert backed by local factual data plus optional OpenRouter LLM."""

    def __init__(self, kb: Optional[KnowledgeBase] = None):
        self.kb = kb or knowledge_base

    @property
    def enabled(self) -> bool:
        return bool(OPENROUTER_API_KEY and AI_MODEL_FALLBACKS)

    def enrich_identification(
        self,
        *,
        frame_number: Optional[str] = None,
        engine_number: Optional[str] = None,
        year: Optional[int] = None,
        notes: Optional[str] = None,
        deterministic_match: Optional[Dict[str, Any]] = None,
        candidates: Optional[List[Dict[str, Any]]] = None,
        photo_uploaded: bool = False,
    ) -> Dict[str, Any]:
        """Return an expert-style identification note, using OpenRouter when available."""
        context = {
            "frame_number": frame_number,
            "engine_number": engine_number,
            "year": year,
            "notes": notes,
            "photo_uploaded": photo_uploaded,
            "deterministic_match": deterministic_match,
            "candidates": candidates or [],
        }

        if self.enabled:
            ai_result = self._ask_openrouter(context)
            if ai_result:
                return ai_result

        return self._fallback_identification(context)

    def answer_question(self, question: str, model_id: int) -> dict:
        """Answer a question about a specific Vespa model."""
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return {
                "question": question,
                "answer": "Modello non trovato. Verifica l'ID del modello.",
                "sources": [],
                "disclaimer": DISCLAIMER,
            }

        if self.enabled:
            prompt = {
                "task": "Rispondi come un restauratore Vespa senior, in italiano, con tono chiaro e prudente.",
                "question": question,
                "model": model,
                "colors": self.kb.get_colors_for_model(model_id),
                "issues": self.kb.get_issues_for_model(model_id),
                "prices": self.kb.get_prices_for_model(model_id),
                "rules": [
                    "Non inventare certificazioni ufficiali.",
                    "Distingui dati certi da ipotesi.",
                    "Suggerisci sempre verifiche fisiche quando utile.",
                ],
            }
            ai_result = self._chat_json(prompt)
            if ai_result:
                return {
                    "question": question,
                    "answer": ai_result.get("expert_summary") or ai_result.get("answer") or "Risposta AI non disponibile.",
                    "sources": ai_result.get("sources", ["Knowledge base OcchioEsperto", "OpenRouter AI"]),
                    "model_name": model["name"],
                    "ai_provider": "openrouter",
                    "ai_model": ai_result.get("model_used"),
                    "disclaimer": DISCLAIMER,
                }

        return self._fallback_question(question, model_id, model)

    def _ask_openrouter(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        prompt = {
            "task": "Identifica una Vespa come farebbe un perito/restauratore esperto.",
            "language": "it",
            "context": context,
            "output_schema": {
                "expert_summary": "spiegazione esperta in italiano",
                "confidence": "high|medium|low",
                "model_name": "nome modello più probabile oppure null",
                "evidence": ["indizi usati"],
                "alternatives": ["modelli alternativi plausibili"],
                "recommended_checks": ["controlli fisici suggeriti"],
                "sources": ["Knowledge base OcchioEsperto", "OpenRouter AI"],
            },
            "rules": [
                "Non forzare un modello se prefisso/telaio/motore non sono compatibili.",
                "Se i dati sono insufficienti, dichiaralo chiaramente.",
                "Non presentare mai il risultato come certificato ufficiale Piaggio.",
                "Rispondi con JSON valido e nessun markdown fuori dal JSON.",
            ],
        }
        return self._chat_json(prompt)

    def _chat_json(self, prompt: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for model in AI_MODEL_FALLBACKS:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Sei un esperto italiano di Vespa storiche, restauri, numeri telaio/motore e colori originali. Rispondi solo con JSON valido.",
                    },
                    {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            }
            req = urllib.request.Request(
                f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                method="POST",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": AI_SITE_URL,
                    "X-Title": AI_APP_NAME,
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=35) as res:
                    data = json.loads(res.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                parsed["model_used"] = model
                return parsed
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError, TimeoutError):
                continue
        return None

    def _fallback_identification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        match = context.get("deterministic_match") or {}
        model_name = match.get("model_name") or match.get("name")
        if model_name:
            summary = (
                f"Dai dati inseriti il candidato più coerente è {model_name}. "
                "Ho usato il confronto con il database locale di numeri telaio/motore; "
                "per conferma controlla punzonatura, prefisso completo, libretto e dettagli costruttivi."
            )
        else:
            summary = (
                "Non forzo un'identificazione: i dati inseriti non bastano per una corrispondenza affidabile nel database locale. "
                "Aggiungi prefisso completo del telaio, numero motore, anno e foto nitida delle punzonature."
            )
        return {
            "expert_summary": summary,
            "confidence": match.get("confidence", "low"),
            "model_name": model_name,
            "evidence": self._evidence_from_context(context),
            "alternatives": [],
            "recommended_checks": [
                "Fotografa punzonatura telaio e motore in modo leggibile.",
                "Verifica che prefisso telaio e prefisso motore appartengano alla stessa famiglia.",
                "Confronta anno di immatricolazione con il periodo di produzione del modello.",
            ],
            "sources": ["Knowledge base OcchioEsperto"],
            "ai_provider": "local_fallback",
        }

    def _fallback_question(self, question: str, model_id: int, model: Dict[str, Any]) -> dict:
        question_lower = question.lower()
        if any(w in question_lower for w in ["colore", "color", "vernice", "tinta", "colori"]):
            colors = self.kb.get_colors_for_model(model_id)
            answer = f"Per la {model['name']} risultano {len(colors)} colori nel database locale."
            if colors:
                answer += "\n" + "\n".join(f"• {c['color_name']} ({c['color_hex']})" for c in colors[:8])
        elif any(w in question_lower for w in ["prezzo", "valore", "quotazione", "mercato"]):
            prices = self.kb.get_prices_for_model(model_id)
            answer = f"Stime indicative per {model['name']}:"
            if prices:
                answer += "\n" + "\n".join(f"• {p['condition']}: €{p['price_min_eur']} - €{p['price_max_eur']}" for p in prices)
            else:
                answer += " dati insufficienti nel database locale."
        else:
            end = model.get("production_end") or "oggi"
            answer = f"La {model['name']} è registrata nel database come modello {model.get('engine_cc', 'N/D')} prodotto dal {model.get('production_start')} al {end}."
        return {
            "question": question,
            "answer": answer,
            "sources": ["Knowledge base OcchioEsperto"],
            "model_name": model["name"],
            "ai_provider": "local_fallback",
            "disclaimer": DISCLAIMER,
        }

    @staticmethod
    def _evidence_from_context(context: Dict[str, Any]) -> List[str]:
        evidence = []
        if context.get("frame_number"):
            evidence.append(f"Telaio inserito: {context['frame_number']}")
        if context.get("engine_number"):
            evidence.append(f"Motore inserito: {context['engine_number']}")
        if context.get("year"):
            evidence.append(f"Anno indicato: {context['year']}")
        if context.get("photo_uploaded"):
            evidence.append("Foto caricata: utile per verifica manuale/AI vision se il modello scelto lo supporta")
        return evidence


ai_expert = AIExpert()
