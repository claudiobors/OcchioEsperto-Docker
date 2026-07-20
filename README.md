# OcchioEsperto Docker

Applicazione full-stack pronta per VPS per identificare, analizzare e valorizzare Vespa storiche/moderne.

## Cosa include

- Frontend React/Vite con UI premium heritage orientata al mondo Vespa.
- Backend FastAPI con database SQLite persistente.
- Upload immagini con validazione formato/dimensione ed estrazione colore dominante.
- Knowledge base locale: modelli, sigle telaio/motore, colori, problemi noti, prezzi indicativi.
- AI via OpenRouter con fallback automatico multi-modello; Grok/xAI resta ultimo nella catena.
- Endpoint admin per arricchire la conoscenza: modelli, colori, problemi noti.
- Garage utente, lead vendita, piani Stripe.
- Disclaimer legali su perizie, autenticità, uso marchi e non affiliazione Piaggio.

## Avvio locale / VPS

```bash
cd occhioesperto
cp .env.example .env
# modifica .env: SECRET_KEY, PUBLIC_SITE_URL, OPENROUTER_API_KEY, Stripe se serve

docker compose build --no-cache
docker compose up -d
curl http://localhost:3000/api/health
```

L'app risponde su:

```text
http://localhost:3000
```

## Variabili importanti

```env
SECRET_KEY=...
PUBLIC_SITE_URL=https://occhioesperto.it
OPENROUTER_API_KEY=...
AI_MODEL_FALLBACKS=openai/gpt-4.1-mini,anthropic/claude-3.5-sonnet,google/gemini-2.0-flash-001,x-ai/grok-3-mini
MAX_UPLOAD_MB=10
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
STRIPE_PRICE_4_99=...
STRIPE_PRICE_9_99=...
```

## Deploy dietro reverse proxy

Esempio Nginx:

```nginx
server {
    server_name occhioesperto.it www.occhioesperto.it;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Poi abilita HTTPS con Certbot.

## Verifiche eseguite

- `npm run build`: OK.
- Import backend FastAPI: OK.
- `/api/health`: OK.
- `/api/vespa/identify` con `VMB1T12345`: OK.
- Browser homepage e pagina analisi: OK, nessun errore console.

Nota: la build Docker reale richiede Docker daemon attivo. Se Docker Desktop/VPS Docker non è avviato, `docker compose build` fallisce prima di iniziare.
