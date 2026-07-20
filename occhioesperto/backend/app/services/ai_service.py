"""
OcchioEsperto.it — AI service with automatic model fallback.
Uses OpenRouter's OpenAI-compatible API when OPENROUTER_API_KEY is configured.
Grok/xAI models are intentionally placed last by default.
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

import httpx

from ..config import AI_MODEL_FALLBACKS, AI_REQUEST_TIMEOUT_SECONDS, OPENROUTER_API_KEY, OPENROUTER_BASE_URL


SYSTEM_PROMPT = """Sei OcchioEsperto, assistente tecnico per Vespa Piaggio storiche e moderne.
Rispondi in italiano, in modo pratico, prudente e utile. Non inventare certificazioni:
se i dati non bastano, indica il livello di confidenza e cosa verificare fisicamente.
Non sei affiliato a Piaggio e non sostituisci registri storici, FMI/ASI o perizie ufficiali.
"""


class AIService:
    def __init__(self) -> None:
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL.rstrip("/")
        self.models = [m.strip() for m in AI_MODEL_FALLBACKS if m.strip()]

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.models)

    async def complete(self, messages: list[dict[str, Any]], *, max_tokens: int = 900) -> dict[str, Any]:
        """Call configured LLMs in order. If a model errors or exhausts context, try the next one."""
        if not self.configured:
            return {
                "text": "AI non configurata: imposta OPENROUTER_API_KEY e AI_MODEL_FALLBACKS nel file .env.",
                "model": "local-rule-based",
                "fallback_used": False,
                "ok": False,
            }

        last_error = ""
        payload_messages = [{"role": "system", "content": SYSTEM_PROMPT}, *messages]
        async with httpx.AsyncClient(timeout=AI_REQUEST_TIMEOUT_SECONDS) as client:
            for idx, model in enumerate(self.models):
                try:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": os.getenv("PUBLIC_SITE_URL", "https://occhioesperto.it"),
                            "X-Title": "OcchioEsperto.it",
                        },
                        json={
                            "model": model,
                            "messages": payload_messages,
                            "temperature": 0.25,
                            "max_tokens": max_tokens,
                        },
                    )
                    if response.status_code in {400, 402, 408, 409, 413, 429, 500, 502, 503, 504}:
                        last_error = f"{model}: HTTP {response.status_code} {response.text[:300]}"
                        continue
                    response.raise_for_status()
                    data = response.json()
                    text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    if text:
                        return {"text": text, "model": model, "fallback_used": idx > 0, "ok": True}
                    last_error = f"{model}: risposta vuota"
                except Exception as exc:  # pragma: no cover - defensive fallback
                    last_error = f"{model}: {type(exc).__name__}: {exc}"
                    continue

        return {
            "text": "Al momento l'assistente AI non è raggiungibile. Ho comunque preparato l'analisi con la knowledge base locale.",
            "model": "fallback-unavailable",
            "fallback_used": True,
            "ok": False,
            "error": last_error,
        }

    @staticmethod
    def image_to_data_url(path: str) -> str | None:
        try:
            p = Path(path)
            mime = "image/jpeg"
            if p.suffix.lower() == ".png":
                mime = "image/png"
            elif p.suffix.lower() == ".webp":
                mime = "image/webp"
            return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")
        except Exception:
            return None

    async def expert_summary(self, analysis: dict[str, Any], user_notes: str | None = None) -> dict[str, Any]:
        compact = json.dumps(analysis, ensure_ascii=False, default=str)[:7000]
        prompt = (
            "Crea una scheda esperta per l'utente: 1) identificazione, 2) attendibilità, "
            "3) controlli da fare, 4) valore indicativo, 5) prossimi passi. "
            "Sii concreto e commerciale ma non promettere certezze.\n\n"
            f"Dati analisi: {compact}\nNote utente: {user_notes or 'nessuna'}"
        )
        return await self.complete([{"role": "user", "content": prompt}], max_tokens=1000)


ai_service = AIService()
