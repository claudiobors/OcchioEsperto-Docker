"""
OcchioEsperto.it — Configurazione applicazione
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Database
KNOWLEDGE_DB_PATH = os.path.join(DATA_DIR, "vespa_knowledge.db")
APP_DB_PATH = os.path.join(DATA_DIR, "occhioesperto.db")
DATABASE_URL = f"sqlite:///{APP_DB_PATH}"

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "occhio-esperto-dev-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Stripe
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_4_99 = os.environ.get("STRIPE_PRICE_4_99", "price_intermedio")
STRIPE_PRICE_9_99 = os.environ.get("STRIPE_PRICE_9_99", "price_avanzato")

# AI / OpenRouter. Order matters: Grok/xAI should stay last as requested.
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
AI_MODEL_FALLBACKS = [
    m.strip() for m in os.environ.get(
        "AI_MODEL_FALLBACKS",
        "openai/gpt-4.1-mini,anthropic/claude-3.5-sonnet,google/gemini-2.0-flash-001,x-ai/grok-3-mini"
    ).split(",")
]
AI_REQUEST_TIMEOUT_SECONDS = int(os.environ.get("AI_REQUEST_TIMEOUT_SECONDS", "45"))
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "10"))
PUBLIC_SITE_URL = os.environ.get("PUBLIC_SITE_URL", "https://occhioesperto.it")

# Plans
PLANS = {
    "free": {"name": "Gratuito", "price": 0, "features": ["Identificazione modello", "Anni produzione"]},
    "intermedio": {"name": "Intermedio", "price": 4.99, "stripe_price_id": STRIPE_PRICE_4_99,
                   "features": ["Range numeri telaio/motore", "Scheda tecnica sintetica"]},
    "avanzato": {"name": "Avanzato", "price": 9.99, "stripe_price_id": STRIPE_PRICE_9_99,
                 "features": ["Colori storici", "Analisi AI colore", "Check-list problemi",
                              "Verifica originalità", "Stima prezzi mercato", "1 domanda all'esperto AI"]},
}

# Rate limiting
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW_SECONDS = 60

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://5eb182d861afc0802e1986e9f0250810.ctonew.app",
    "https://occhioesperto.it",
]

# Disclaimer
DISCLAIMER = (
    "OcchioEsperto.it fornisce analisi probabilistiche e orientative basate su dati storici, "
    "foto e informazioni inserite dall'utente. Non costituisce certificato di origine, perizia, "
    "valutazione assicurativa o garanzia di autenticità. Per decisioni economiche rilevanti "
    "verifica sempre documenti, punzonature e stato del veicolo con un professionista o registro "
    "riconosciuto. OcchioEsperto.it non è affiliato, sponsorizzato o approvato dal Gruppo Piaggio; "
    "Vespa e Piaggio sono marchi dei rispettivi titolari."
)