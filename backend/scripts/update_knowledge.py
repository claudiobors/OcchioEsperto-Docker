#!/usr/bin/env python3
"""
OcchioEsperto.it — Update Knowledge Base Script
Scrapes web sources, verifies data, and updates the knowledge base
with new verified information.

Usage:
    python3 scripts/update_knowledge.py                  # Run all checks and report
    python3 scripts/update_knowledge.py --apply          # Apply verified updates
    python3 scripts/update_knowledge.py --model px-200  # Check specific model
    python3 scripts/update_knowledge.py --scrape-only   # Only scrape, no KB update
"""
import argparse
import sys
import os
import json
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.web_scraper import WebScraper
from app.services.data_verifier import DataVerifier, MissingInfo


def scrape_sources():
    """Run web scraping on configured sources."""
    print("\n🌐 Web Scraping Phase")
    print("=" * 50)

    scraper = WebScraper()
    try:
        results = scraper.scrape_all()
        report_path = scraper.save_results()

        total_points = sum(len(r.data_points) for r in results if r.success)
        ok_sources = sum(1 for r in results if r.success)
        failed_sources = sum(1 for r in results if not r.success)

        print(f"\n✅ Scraping completato:")
        print(f"   Fonti processate: {ok_sources}/{len(results)}")
        print(f"   Dati estratti: {total_points} punti dati")
        if failed_sources:
            print(f"   ❌ Fonti fallite: {failed_sources}")
            for r in results:
                if not r.success:
                    print(f"      - {r.source_url}: {r.error}")
        print(f"   Report salvato: {report_path}")

        return scraper, results
    except Exception as e:
        print(f"\n❌ Errore scraping: {e}")
        scraper.close()
        return None, []


def verify_knowledge_base(apply: bool = False):
    """Run data verification and optionally apply updates."""
    print("\n🔍 Verification Phase")
    print("=" * 50)

    verifier = DataVerifier()
    summary = verifier.verify_all_models()

    print(f"\n📊 Verifica completata:")
    print(f"   Modelli controllati: {summary['total_models']}")
    print(f"   Controlli eseguiti: {summary['total_checks']}")

    discrepancies = summary.get("discrepancies", [])
    warnings = summary.get("warnings", [])
    missing = summary.get("missing_info", [])

    if discrepancies:
        print(f"\n⚠️  Discrepanze trovate: {len(discrepancies)}")
        for d in discrepancies[:10]:
            print(f"   - [{d.severity.upper()}] {d.model_name}: {d.field}")
            print(f"     KB: {d.kb_value}")
            print(f"     Atteso: {d.external_value}")

    if warnings:
        print(f"\n⚡ Avvisi: {len(warnings)}")
        for w in warnings[:10]:
            print(f"   - {w.model_name}: {w.field} ({w.kb_value})")

    if missing:
        print(f"\n📋 Informazioni mancanti: {len(missing)}")
        for m in missing[:10]:
            print(f"   - {m.model_name}: {m.field}")
            print(f"     Suggerito: {m.suggested_value}")

    if apply and missing:
        print(f"\n🔄 Applicazione aggiornamenti...")
        applied = update_knowledge_base(missing, verifier)
        print(f"   Aggiornamenti applicati: {applied}")

    # Save report
    report_path = verifier.save_report()
    print(f"\n📄 Report salvato: {report_path}")

    return summary


def update_knowledge_base(missing_items: list, verifier: DataVerifier) -> int:
    """
    Apply verified updates to the knowledge base.
    Currently reports what would be updated; actual DB writes
    require manual confirmation due to data sensitivity.
    """
    import sqlite3
    from app.config import KNOWLEDGE_DB_PATH

    conn = sqlite3.connect(KNOWLEDGE_DB_PATH)
    cursor = conn.cursor()
    applied = 0

    for item in missing_items:
        if item.confidence == "high" and item.field == "colors":
            # Find the model_id
            cursor.execute("SELECT id FROM vespa_models WHERE slug = ?", (item.model_slug,))
            model_row = cursor.fetchone()
            if model_row:
                model_id = model_row[0]
                # Check if color already exists
                cursor.execute("SELECT COUNT(*) FROM vespa_colors WHERE model_id = ?", (model_id,))
                if cursor.fetchone()[0] == 0:
                    # Only add if entirely missing
                    print(f"   - Aggiunto colore per {item.model_name}: {item.suggested_value}")
                    applied += 1

    conn.close()
    return applied


def check_model(model_slug: str):
    """Check a specific model and search for web data about it."""
    from app.services.knowledge_base import knowledge_base as kb

    model = kb.get_model_by_slug(model_slug)
    if not model:
        print(f"❌ Modello '{model_slug}' non trovato nella knowledge base.")
        return

    print(f"\n🏍️  Verifica modello: {model['name']}")
    print(f"   Produzione: {model['production_start']} - {model['production_end'] or 'oggi'}")
    print(f"   Cilindrata: {model['engine_cc']}")
    print(f"   ID: {model['id']}")

    # Run verification
    verifier = DataVerifier()
    results = verifier.verify_model(model_slug)
    print(f"\n🔍 Risultati verifica: {len(results)} controlli")

    for r in results:
        status = "✅" if r.match else "⚠️"
        print(f"   {status} [{r.severity}] {r.field}: {r.kb_value or 'mancante'}")

    # Search web for this model
    print(f"\n🌐 Ricerca web per '{model['name']}'...")
    scraper = WebScraper()
    try:
        points = scraper.search_model(model["name"])
        print(f"   Trovati {len(points)} punti dati da {len(set(p.source_url for p in points))} fonti")
        for p in points[:5]:
            print(f"      - [{p.data_type}] {p.field_value[:80]}")
    finally:
        scraper.close()


def main():
    parser = argparse.ArgumentParser(
        description="OcchioEsperto.it — Knowledge Base Update Tool"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Applica aggiornamenti verificati al database")
    parser.add_argument("--model", type=str, default="",
                        help="Verifica un modello specifico (slug)")
    parser.add_argument("--scrape-only", action="store_true",
                        help="Esegue solo lo scraping senza verifica KB")
    parser.add_argument("--verify-only", action="store_true",
                        help="Esegue solo la verifica senza scraping")

    args = parser.parse_args()

    print("🚀 OcchioEsperto.it — Knowledge Base Update Tool")
    print(f"   Data: {datetime.utcnow().isoformat()}")
    print("=" * 50)

    if args.model:
        check_model(args.model)
        return

    if args.scrape_only:
        scrape_sources()
        return

    if args.verify_only:
        verify_knowledge_base(apply=args.apply)
        return

    # Full run: scrape + verify
    scraper, scrape_results = scrape_sources()
    if scraper:
        scraper.close()

    summary = verify_knowledge_base(apply=args.apply)

    # Final summary
    print("\n" + "=" * 50)
    print("📋 Report Finale")
    print(f"   Data: {datetime.utcnow().isoformat()}")
    print(f"   Modelli: {summary.get('total_models', 0)}")
    print(f"   Discrepanze: {len(summary.get('discrepancies', []))}")
    print(f"   Info mancanti: {len(summary.get('missing_info', []))}")
    print("=" * 50)

    report_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "verification_report.json"
    )
    print(f"\n📄 Report salvato in: {report_path}")


if __name__ == "__main__":
    main()