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
    AI_MODEL_FREE_FALLBACKS,
    AI_MODEL_PREMIUM_FALLBACKS,
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
        plan: str = "free",
        analysis_depth: str = "basic",
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
            "plan": plan,
            "analysis_depth": analysis_depth,
            "local_prefix_hint": self._prefix_hint(frame_number),
        }

        if self.enabled:
            ai_result = self._ask_openrouter(context, plan=plan)
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

    def _ask_openrouter(self, context: Dict[str, Any], plan: str = "free") -> Optional[Dict[str, Any]]:
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
                "Se i dati sono parziali, dai comunque il miglior inquadramento tecnico possibile: modello/famiglia, cilindrata, periodo e verifiche consigliate.",
                "Non presentare mai il risultato come certificato ufficiale Piaggio.",
                "Non spiegare logiche interne, costi, credenziali, provider o flussi di pagamento.",
                "Rispondi con JSON valido e nessun markdown fuori dal JSON.",
            ],
        }
        return self._chat_json(prompt, plan=plan)

    def _chat_json(self, prompt: Dict[str, Any], plan: str = "free") -> Optional[Dict[str, Any]]:
        for model in self._models_for_plan(plan):
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

    @staticmethod
    def _models_for_plan(plan: str) -> List[str]:
        if plan in {"intermedio", "avanzato"}:
            return AI_MODEL_PREMIUM_FALLBACKS or AI_MODEL_FALLBACKS
        return AI_MODEL_FREE_FALLBACKS or AI_MODEL_FALLBACKS

    def _fallback_identification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        match = context.get("deterministic_match") or {}
        model_name = match.get("model_name") or match.get("name")
        prefix_hint = self._prefix_hint(context.get("frame_number"))
        if model_name:
            summary = (
                f"Il telaio è coerente con {model_name}. La prima lettura indica una Vespa da "
                f"{match.get('engine_cc', 'cilindrata da confermare')}, prodotta nel periodo "
                f"{match.get('production_start', '')}-{match.get('production_end') or 'oggi'}. "
                "La conferma più solida arriva confrontando punzonature, libretto, motore e dettagli costruttivi."
            )
        elif prefix_hint:
            model_name = prefix_hint["model_name"]
            match = {"confidence": "medium"}
            summary = (
                f"Il prefisso telaio {prefix_hint['prefix']} indirizza verso {prefix_hint['model_name']}, "
                f"una Vespa {prefix_hint['engine_cc']} del periodo {prefix_hint['years']}. "
                "Per una lettura completa conviene verificare numero progressivo, motore abbinato, colore e dettagli di allestimento."
            )
        else:
            summary = (
                "La prima lettura ha bisogno di qualche indizio in più per essere davvero precisa. "
                "Le foto delle punzonature, il numero motore e l’anno aiutano a distinguere varianti molto simili."
            )
        return {
            "expert_summary": summary,
            "confidence": match.get("confidence", "low"),
            "model_name": model_name,
            "engine_cc": prefix_hint.get("engine_cc") if prefix_hint and not context.get("deterministic_match") else match.get("engine_cc"),
            "years": prefix_hint.get("years") if prefix_hint and not context.get("deterministic_match") else None,
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

    @staticmethod
    def _prefix_hint(frame_number: Optional[str]) -> Optional[Dict[str, str]]:
        normalized = KnowledgeBase._normalize_number(frame_number or "")
        prefix = KnowledgeBase._extract_code_prefix(normalized)
        hints = {
            "VN2T": {
                "prefix": "VN2T",
                "model_name": "Vespa 125 VN2T",
                "engine_cc": "125 cc",
                "years": "1956 - 1957",
            },
        }
        return hints.get(prefix)

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
