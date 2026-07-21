"""
OcchioEsperto.it — Configurazione applicazione
"""
import os
import sys

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
_SECRET_KEY = os.environ.get("SECRET_KEY")
if not _SECRET_KEY:
    if os.environ.get("ENV", "development") == "production":
        raise RuntimeError(
            "❌ SECRET_KEY non impostata! "
            "Imposta la variabile d'ambiente SECRET_KEY per la produzione.\n"
            "Genera una chiave con: python3 -c \"import secrets; print(secrets.token_hex(32))\""
        )
    _SECRET_KEY = "occhio-esperto-dev-key-change-in-production-2024"
    print("⚠️  WARNING: SECRET_KEY fallback usata. Imposta SECRET_KEY per produzione!")

SECRET_KEY = _SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 ore (ridotto da 24h per sicurezza)

# Stripe
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_4_99 = os.environ.get("STRIPE_PRICE_4_99", "price_intermedio")
STRIPE_PRICE_9_99 = os.environ.get("STRIPE_PRICE_9_99", "price_avanzato")

# OpenRouter AI — configurable, no API key in code.
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "")
OPENROUTER_MODEL_FREE = os.environ.get("OPENROUTER_MODEL_FREE", "")
OPENROUTER_MODELS_PREMIUM = os.environ.get("OPENROUTER_MODELS_PREMIUM", "")
AI_MODEL_FALLBACKS = [
    m.strip() for m in os.environ.get("AI_MODEL_FALLBACKS", OPENROUTER_MODEL).split(",") if m.strip()
]
AI_MODEL_FREE_FALLBACKS = [
    m.strip() for m in os.environ.get("AI_MODEL_FREE_FALLBACKS", OPENROUTER_MODEL_FREE or OPENROUTER_MODEL).split(",") if m.strip()
]
AI_MODEL_PREMIUM_FALLBACKS = [
    m.strip() for m in os.environ.get("AI_MODEL_PREMIUM_FALLBACKS", OPENROUTER_MODELS_PREMIUM or OPENROUTER_MODEL).split(",") if m.strip()
]
AI_SITE_URL = os.environ.get("AI_SITE_URL", os.environ.get("PUBLIC_SITE_URL", "https://occhioesperto.it"))
AI_APP_NAME = os.environ.get("AI_APP_NAME", "OcchioEsperto.it")

# Plans
PLANS = {
    "free": {"name": "Gratuito", "price": 0, "features": ["Identificazione modello", "Anni produzione"]},
    "intermedio": {"name": "Intermedio", "price": 4.99, "stripe_price_id": STRIPE_PRICE_4_99,
                   "features": ["Range numeri telaio/motore", "Scheda tecnica sintetica"]},
    "avanzato": {"name": "Avanzato", "price": 9.99, "stripe_price_id": STRIPE_PRICE_9_99,
                 "features": ["Colori storici", "Analisi AI colore", "Check-list problemi",
                              "Verifica originalità", "Stima prezzi mercato", "1 domanda all'esperto AI"]},
}

# Rate limiting (generale)
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW_SECONDS = 60

# Rate limiting specifico per auth (login/register)
AUTH_RATE_LIMIT = "10/minute"

# Detect environment
IS_PRODUCTION = os.environ.get("ENV", "development") == "production"

# CORS — dinamico: in sviluppo include localhost, in produzione solo domini reali
if IS_PRODUCTION:
    CORS_ORIGINS = [
        "https://5eb182d861afc0802e1986e9f0250810.ctonew.app",
        "https://occhioesperto.it",
    ]
else:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://5eb182d861afc0802e1986e9f0250810.ctonew.app",
    ]

# Disclaimer
DISCLAIMER = (
    "Questo servizio offre un'analisi basata su dati storici per supportare "
    "appassionati e restauratori. Non costituisce un certificato ufficiale di "
    "origine e non è affiliato in alcun modo al Gruppo Piaggio."
)