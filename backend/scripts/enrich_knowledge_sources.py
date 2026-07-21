#!/usr/bin/env python3
"""Collect factual Vespa data candidates from public sources for manual review.

This script is intentionally conservative: it does not copy full articles/pages and
it does not write directly into the production knowledge tables. It extracts short
factual candidates (model names, years, number-like prefixes/ranges, colors) with
source attribution into backend/data/enrichment_candidates.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.web_scraper import WebScraper  # noqa: E402


def main() -> int:
    output = ROOT / "data" / "enrichment_candidates.json"
    with WebScraper(timeout=20) as scraper:
        results = scraper.scrape_all()
        output_path = scraper.save_results(output.name)

    ok = sum(1 for r in results if r.success)
    points = sum(len(r.data_points) for r in results)
    print(f"Scraped sources: {ok}/{len(results)} successful")
    print(f"Candidate factual data points: {points}")
    print(f"Saved manual-review file: {output_path}")
    print("No production DB rows were changed; review candidates before import.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
