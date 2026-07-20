#!/usr/bin/env python3
"""
OcchioEsperto.it — Create the Vespa knowledge database.
This script creates and populates data/vespa_knowledge.db.
"""
import sys
import os

# Add backend dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the seed script
from seed_database import main as seed_main

if __name__ == "__main__":
    print("🚀 Creazione database conoscenza Vespa...")
    seed_main()
    print("✅ Database creato in data/vespa_knowledge.db")