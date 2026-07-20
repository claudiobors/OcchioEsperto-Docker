# OcchioEsperto — Team Workflow

## Code Workflow
- Tutto il codice viene sviluppato in `/home/team/shared/occhioesperto/`
- I membri lavorano in autonomia nel proprio ambiente
- Il repository GitHub collegato: `claudiobors/OcchioEsperto-Docker`
- Quando un task è completato, il membro fa `finish_task` con un riepilogo
- Il lead (agent-lead) revisiona e fa il merge su GitHub

## Branch Strategy
- Il main branch su GitHub rappresenta la versione stabile
- I membri fanno commit direttamente o preparano il codice per il merge

## Requisiti di Codice
- Backend: Python/FastAPI, SQLite, Docker
- Frontend: React + Vite + Tailwind CSS
- Docker: Multi-stage build, singolo container su porta 3000
- Stripe: Integrazione per pagamenti

## Review Process
1. Il membro completa il task e chiama `finish_task`
2. Il lead revisiona il risultato
3. Se OK → approva e fa merge
4. Se NO → respinge con feedback