#!/bin/bash
# OcchioEsperto.it — Entrypoint script
# Initializes the database on first run, then starts the application

set -e

echo "🚀 OcchioEsperto.it — Starting..."

# Initialize app database (create tables if not exist)
echo "📦 Initializing database..."
python3 -c "from app.database import init_db; init_db(); print('✅ Database tables ready')"

# Create knowledge base database if it doesn't exist
if [ ! -f "data/vespa_knowledge.db" ]; then
    echo "🌱 Seeding knowledge base (first run)..."
    python3 seed_database.py
    echo "✅ Knowledge base seeded"
fi

# Create required directories
mkdir -p uploads static

# Run the main command
echo "✅ Starting uvicorn on port 3000..."
exec "$@"