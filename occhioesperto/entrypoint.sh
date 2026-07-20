#!/bin/bash
# OcchioEsperto.it — Entrypoint script
# Initializes persistent data on first run, then starts the application.

set -euo pipefail

echo "🚀 OcchioEsperto.it — Starting..."

# Create required directories before SQLite connects (volumes may be empty)
mkdir -p data uploads static

# Initialize app database (create tables if not exist)
echo "📦 Initializing application database..."
python3 -c "from app.database import init_db; init_db(); print('✅ Database tables ready')"

# Create knowledge base database if it doesn't exist in the mounted data volume
if [ ! -f "data/vespa_knowledge.db" ]; then
    echo "🌱 Seeding knowledge base (first run)..."
    python3 seed_database.py <<<'s' || python3 create_knowledge_db.py <<<'s'
    echo "✅ Knowledge base seeded"
fi

echo "✅ Starting uvicorn on port 3000..."
exec "$@"
