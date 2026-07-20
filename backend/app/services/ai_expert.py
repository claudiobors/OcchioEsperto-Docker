"""
OcchioEsperto.it — AI Expert Service
Answers questions about Vespa models using the knowledge base.
Available for Avanzato plan users.
"""
import re
from typing import Optional

from .knowledge_base import knowledge_base, KnowledgeBase


class AIExpert:
    """
    AI Expert that answers questions about Vespa models.
    Uses keyword matching on the knowledge base to provide
    contextual answers about colors, prices, issues, and specs.
    """

    def __init__(self, kb: Optional[KnowledgeBase] = None):
        self.kb = kb or knowledge_base

    def answer_question(self, question: str, model_id: int) -> dict:
        """Answer a question about a specific Vespa model."""
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return {
                "question": question,
                "answer": "Modello non trovato. Verifica l'ID del modello.",
                "sources": [],
                "disclaimer": "Risposta generata dall'esperto AI basata su database storico. Verifica sempre con un esperto qualificato.",
            }

        question_lower = question.lower()
        answer_parts = []
        sources = []

        # Keyword matching per domande comuni
        if any(w in question_lower for w in ["colore", "color", "vernice", "tinta", "colori", "colorato"]):
            colors = self.kb.get_colors_for_model(model_id)
            if colors:
                answer_parts.append(
                    f"Per la {model['name']} sono disponibili {len(colors)} colori storici:"
                )
                for c in colors:
                    years = f"{c['year_start']}-{c.get('year_end', 'oggi')}"
                    answer_parts.append(f"  • {c['color_name']} ({c['color_hex']}) — {years}")
                sources.append("Database colori storici")
            else:
                answer_parts.append(f"Non ci sono dati sui colori per la {model['name']} nel database.")

        elif any(w in question_lower for w in ["prezzo", "valore", "costo", "quotazione", "quanto", "mercato"]):
            prices = self.kb.get_prices_for_model(model_id)
            if prices:
                answer_parts.append(f"Ecco le stime di mercato per la {model['name']}:")
                for p in prices:
                    cond = p.get('condition', p.get('condition_type', 'N/A'))
                    answer_parts.append(f"  • {cond}: €{p['price_min_eur']} - €{p['price_max_eur']}")
                sources.append("Database prezzi di mercato")
            else:
                answer_parts.append(f"Non ci sono dati sui prezzi per la {model['name']}.")

        elif any(w in question_lower for w in ["problema", "difetto", "guasto", "rotta", "rottura", "difetti"]):
            issues = self.kb.get_issues_for_model(model_id)
            if issues:
                answer_parts.append(f"Problemi noti per la {model['name']}:")
                for i in issues:
                    severity = i.get('severity', 'info')
                    title = i.get('issue_title', i.get('issue', 'Sconosciuto'))
                    desc = i.get('description', '')
                    answer_parts.append(f"  • [{severity.upper()}] {title}: {desc}")
                sources.append("Database problemi noti")
            else:
                answer_parts.append(f"Non ci sono problemi noti registrati per la {model['name']}.")

        elif any(w in question_lower for w in ["anno", "produzione", "quando", "serie", "modello"]):
            start = model.get('production_start', '?')
            end = model.get('production_end', 'oggi') if model.get('production_end') else 'oggi'
            answer_parts.append(
                f"La {model['name']} è stata prodotta dal {start} al {end}. "
                f"Cilindrata: {model.get('engine_cc', 'N/D')}."
            )
            sources.append("Database modelli")

        elif any(w in question_lower for w in ["telaio", "numero", "seriale", "chassis"]):
            answer_parts.append(
                f"Per identificare la {model['name']}, controlla i numeri di telaio e motore. "
                "Usa la funzione 'Identifica' per un matching automatico."
            )
            sources.append("Database modelli")

        elif any(w in question_lower for w in ["originale", "originalità", "autentico"]):
            result = self.kb.check_originality(model_id)
            if result.get("is_original"):
                answer_parts.append(f"La configurazione della {model['name']} appare originale.")
            else:
                answer_parts.append(f"La {model['name']} presenta alcune anomalie:")
                for issue in result.get("issues", []):
                    answer_parts.append(f"  • {issue}")
            sources.append("Database modelli")

        else:
            # Risposta generica
            start = model.get('production_start', '?')
            end = model.get('production_end', 'oggi') if model.get('production_end') else 'oggi'
            answer_parts.append(
                f"La {model['name']} (cilindrata {model.get('engine_cc', 'N/D')}) "
                f"è stata prodotta dal {start} al {end}."
            )
            desc = model.get('description', '')
            if desc:
                answer_parts.append(f"\n{desc[:200]}...")
            answer_parts.append(
                "\nPer informazioni più specifiche, prova a chiedere:\n"
                "  • Colori disponibili\n"
                "  • Prezzi di mercato\n"
                "  • Problemi noti\n"
                "  • Anni di produzione\n"
                "  • Originalità"
            )
            sources.append("Database modelli")

        return {
            "question": question,
            "answer": "\n".join(answer_parts),
            "sources": sources,
            "model_name": model["name"],
            "disclaimer": "Risposta generata dall'esperto AI basata su database storico. Verifica sempre con un esperto qualificato.",
        }


# Singleton
ai_expert = AIExpert()