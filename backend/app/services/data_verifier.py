"""
OcchioEsperto.it — Data Verifier Service
Compares scraped data against the knowledge base to find discrepancies
and enrich missing information.
"""
import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from .knowledge_base import knowledge_base
from .web_scraper import WebScraper, ScrapedDataPoint


@dataclass
class VerificationResult:
    """Result of comparing external data with the knowledge base."""
    model_slug: str
    model_name: str
    field: str
    kb_value: Optional[str]
    external_value: Optional[str]
    external_source: Optional[str]
    match: bool  # True if consistent, False if discrepancy
    severity: str = "info"  # info, warning, critical
    confidence: str = "medium"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class MissingInfo:
    """Information present in external sources but missing from KB."""
    model_slug: str
    model_name: str
    field: str
    suggested_value: str
    source: str
    confidence: str


class DataVerifier:
    """
    Verifies the knowledge base data by comparing with external sources.
    Identifies discrepancies and missing information.
    """

    def __init__(self):
        self.kb = knowledge_base
        self.verification_log: List[VerificationResult] = []
        self.missing_info: List[MissingInfo] = []
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

    def verify_all_models(self) -> Dict[str, Any]:
        """Verify all models in the knowledge base against known data patterns."""
        models = self.kb.get_all_models()
        results = []

        for model in models:
            model_result = self.verify_model(model["slug"])
            results.extend(model_result)

        self.verification_log = results

        summary = {
            "total_models": len(models),
            "total_checks": len(results),
            "discrepancies": [r for r in results if not r.match],
            "warnings": [r for r in results if r.severity == "warning"],
            "missing_info": self.missing_info,
        }
        return summary

    def verify_model(self, model_slug: str) -> List[VerificationResult]:
        """Verify a single model against logical consistency rules."""
        model = self.kb.get_model_by_slug(model_slug)
        if not model:
            return []

        results = []
        model_id = model["id"]

        # 1. Verify production years make sense
        results.extend(self._verify_years(model))

        # 2. Verify frame numbers exist
        results.extend(self._verify_frame_numbers(model_id, model_slug))

        # 3. Verify engine numbers exist
        results.extend(self._verify_engine_numbers(model_id, model_slug))

        # 4. Verify colors exist
        results.extend(self._verify_colors(model_id, model_slug))

        # 5. Verify issues exist
        results.extend(self._verify_issues(model_id, model_slug))

        # 6. Verify prices exist
        results.extend(self._verify_prices(model_id, model_slug))

        # 7. Check for missing data
        self._check_missing_data(model_id, model)

        return results

    def _verify_years(self, model: dict) -> List[VerificationResult]:
        """Verify production years are logical."""
        results = []
        start = model.get("production_start")
        end = model.get("production_end")

        if start and start < 1946:
            results.append(VerificationResult(
                model_slug=model["slug"],
                model_name=model["name"],
                field="production_start",
                kb_value=str(start),
                external_value="1946+",
                external_source="historical data",
                match=False,
                severity="critical",
                confidence="high",
            ))

        if start and end and end < start:
            results.append(VerificationResult(
                model_slug=model["slug"],
                model_name=model["name"],
                field="production_years",
                kb_value=f"{start}-{end}",
                external_value="end >= start",
                external_source="logic",
                match=False,
                severity="critical",
                confidence="high",
            ))

        if start and end and (end - start) > 40:
            results.append(VerificationResult(
                model_slug=model["slug"],
                model_name=model["name"],
                field="production_span",
                kb_value=f"{start}-{end} ({end - start} years)",
                external_value="< 40 years",
                external_source="logic",
                match=False,
                severity="warning",
                confidence="medium",
            ))

        return results

    def _verify_frame_numbers(self, model_id: int, slug: str) -> List[VerificationResult]:
        """Verify frame number ranges exist for the model."""
        results = []
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return results

        # Check if any frame ranges exist via direct query
        has_frame_data = self._has_data("vespa_chassis_numbers", model_id)
        if not has_frame_data:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="frame_number_ranges",
                kb_value="missing",
                external_value="expected",
                external_source="KB consistency",
                match=True,  # Not a discrepancy, just missing
                severity="info",
                confidence="medium",
            ))
            self.missing_info.append(MissingInfo(
                model_slug=slug,
                model_name=model["name"],
                field="frame_number_ranges",
                suggested_value=f"Range numeri telaio per {model['name']}",
                source="KB auto-check",
                confidence="medium",
            ))

        return results

    def _verify_engine_numbers(self, model_id: int, slug: str) -> List[VerificationResult]:
        """Verify engine number ranges exist."""
        results = []
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return results

        has_engine_data = self._has_data("vespa_engine_numbers", model_id)
        if not has_engine_data:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="engine_number_ranges",
                kb_value="missing",
                external_value="expected",
                external_source="KB consistency",
                match=True,
                severity="info",
                confidence="medium",
            ))

        return results

    def _verify_colors(self, model_id: int, slug: str) -> List[VerificationResult]:
        """Verify colors exist for the model."""
        results = []
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return results

        colors = self.kb.get_colors_for_model(model_id)
        if not colors:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="colors",
                kb_value="missing",
                external_value="expected",
                external_source="KB consistency",
                match=True,
                severity="info",
                confidence="medium",
            ))
        elif len(colors) <= 1:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="colors_count",
                kb_value=str(len(colors)),
                external_value="> 1",
                external_source="typical (2-6 colors per model)",
                match=False,
                severity="warning",
                confidence="low",
            ))

        return results

    def _verify_issues(self, model_id: int, slug: str) -> List[VerificationResult]:
        """Verify known issues exist."""
        results = []
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return results

        issues = self.kb.get_issues_for_model(model_id)
        if not issues:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="known_issues",
                kb_value="none",
                external_value="expected",
                external_source="KB consistency",
                match=True,
                severity="info",
                confidence="medium",
            ))

        return results

    def _verify_prices(self, model_id: int, slug: str) -> List[VerificationResult]:
        """Verify market prices exist."""
        results = []
        model = self.kb.get_model_by_id(model_id)
        if not model:
            return results

        prices = self.kb.get_prices_for_model(model_id)
        if not prices:
            results.append(VerificationResult(
                model_slug=slug,
                model_name=model["name"],
                field="market_prices",
                kb_value="missing",
                external_value="expected",
                external_source="KB consistency",
                match=True,
                severity="info",
                confidence="medium",
            ))
        else:
            # Verify price ranges make sense
            for price in prices:
                if price.get("price_min_eur", 0) <= 0:
                    results.append(VerificationResult(
                        model_slug=slug,
                        model_name=model["name"],
                        field=f"price_{price.get('condition', 'unknown')}",
                        kb_value=str(price.get("price_min_eur", 0)),
                        external_value="> 0",
                        external_source="logic",
                        match=False,
                        severity="warning",
                        confidence="high",
                    ))

        return results

    def _check_missing_data(self, model_id: int, model: dict):
        """Identify data that should exist but doesn't."""
        name = model["name"]
        slug = model["slug"]

        # Modern models (after 2000) should have more data points
        if model.get("production_start", 2000) >= 2000:
            colors = self.kb.get_colors_for_model(model_id)
            if len(colors) < 3:
                self.missing_info.append(MissingInfo(
                    model_slug=slug,
                    model_name=name,
                    field="colors",
                    suggested_value="Aggiungere più colori (min 3 per modelli moderni)",
                    source="KB auto-check",
                    confidence="high",
                ))

    def _has_data(self, table: str, model_id: int) -> bool:
        """Check if a table has data for a given model_id."""
        import sqlite3
        from ..config import KNOWLEDGE_DB_PATH

        conn = sqlite3.connect(KNOWLEDGE_DB_PATH)
        cursor = conn.cursor()

        # Map table names to their FK column
        fk_map = {
            "vespa_chassis_numbers": "model_id",
            "vespa_engine_numbers": "model_id",
            "vespa_colors": "model_id",
            "vespa_known_issues": "model_id",
            "vespa_market_prices": "model_id",
        }

        fk = fk_map.get(table, "model_id")
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {fk} = ?", (model_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def run_with_scraper(self) -> Dict[str, Any]:
        """Run verification enhanced with web scraping."""
        # First do internal consistency checks
        summary = self.verify_all_models()

        # Then run web scraper on key sources for enrichment
        print("\n🌐 Running web scraping for external verification...")
        scraper = WebScraper()
        try:
            scrape_results = scraper.scrape_all()
            scraper.save_results()
            summary["scrape_results_count"] = sum(len(r.data_points) for r in scrape_results if r.success)
            summary["scrape_sources_ok"] = sum(1 for r in scrape_results if r.success)
            summary["scrape_sources_failed"] = sum(1 for r in scrape_results if not r.success)
        finally:
            scraper.close()

        return summary

    def save_report(self, filename: str = "verification_report.json") -> str:
        """Save comprehensive verification report."""
        filepath = os.path.join(self.data_dir, filename)
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "verifications": [asdict(v) for v in self.verification_log],
            "missing_info": [asdict(m) for m in self.missing_info],
            "summary": {
                "total_verifications": len(self.verification_log),
                "discrepancies": len([v for v in self.verification_log if not v.match and v.severity == "critical"]),
                "warnings": len([v for v in self.verification_log if v.severity == "warning"]),
                "missing_fields": len(self.missing_info),
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filepath


# CLI usage
if __name__ == "__main__":
    import sys
    print("🔍 OcchioEsperto.it — Data Verifier\n")

    verifier = DataVerifier()
    summary = verifier.run_with_scraper()

    print(f"\n📊 Summary:")
    print(f"   Models checked: {summary['total_models']}")
    print(f"   Total checks: {summary['total_checks']}")
    print(f"   Discrepancies: {len(summary['discrepancies'])}")
    print(f"   Warnings: {len(summary['warnings'])}")
    print(f"   Missing info: {len(summary['missing_info'])}")

    if summary.get("scrape_sources_ok"):
        print(f"\n🌐 Web scraping:")
        print(f"   Sources OK: {summary['scrape_sources_ok']}")
        print(f"   Sources failed: {summary['scrape_sources_failed']}")
        print(f"   Data points: {summary['scrape_results_count']}")

    report_path = verifier.save_report()
    print(f"\n📄 Report saved: {report_path}")