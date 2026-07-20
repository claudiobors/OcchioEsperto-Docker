"""
OcchioEsperto.it — Web Scraper Service
Automated web scraping and data extraction from Vespa knowledge sources.

Extracts only factual data (model names, years, frame/engine numbers,
colors, prices) and cites sources. No copyrighted content is stored.
"""
import json
import os
import re
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


@dataclass
class ScrapedDataPoint:
    """A single data point extracted from a source."""
    source_url: str
    source_name: str
    data_type: str  # model, color, price, issue, frame_range, engine_range, spec
    model_slug: Optional[str] = None
    model_name: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    confidence: str = "medium"  # high, medium, low
    scraped_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ScrapeResult:
    """Result of a scraping operation."""
    source_url: str
    success: bool
    data_points: List[ScrapedDataPoint] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class WebScraper:
    """
    Web scraping engine that searches specialized Vespa websites
    for factual data to enrich and verify the knowledge base.
    """

    # Known reliable sources for factual Vespa data
    SOURCES = {
        "scooterhelp": {
            "url": "https://www.scooterhelp.com/vespa/",
            "name": "ScooterHelp Vespa Database",
            "type": "registry",
        },
        "vespa_paint": {
            "url": "https://www.vespapaintcolors.com/",
            "name": "Vespa Paint Colors Database",
            "type": "colors",
        },
        "motorcyclespecs": {
            "url": "https://www.motorcyclespecs.co.za/",
            "name": "Motorcycle Specs",
            "type": "specs",
        },
        "bikez": {
            "url": "https://bikez.com/motorcycles/vespa.php",
            "name": "Bikez Vespa Models",
            "type": "specs",
        },
        "thisoldvespa": {
            "url": "https://www.thisoldvespa.com/",
            "name": "This Old Vespa",
            "type": "technical",
        },
    }

    def __init__(self, timeout: int = 30):
        self.client = httpx.Client(
            follow_redirects=True,
            timeout=timeout,
            headers={
                "User-Agent": "OcchioEsperto.it/1.0 (knowledge base verifier; contact@occhioesperto.it)",
                "Accept": "text/html,application/xhtml+xml",
            }
        )
        self.results: List[ScrapeResult] = []
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
        os.makedirs(self.data_dir, exist_ok=True)

    def scrape_all(self) -> List[ScrapeResult]:
        """Scrape all known sources for Vespa data."""
        for source_key, source_info in self.SOURCES.items():
            try:
                result = self._scrape_source(source_info)
                self.results.append(result)
                print(f"  ✓ {source_info['name']}: {len(result.data_points)} data points")
            except Exception as e:
                self.results.append(ScrapeResult(
                    source_url=source_info["url"],
                    success=False,
                    error=str(e),
                ))
                print(f"  ✗ {source_info['name']}: {e}")
        return self.results

    def scrape_source(self, url: str, source_name: str = "") -> ScrapeResult:
        """Scrape a specific URL for Vespa data."""
        if not source_name:
            parsed = urlparse(url)
            source_name = parsed.netloc

        try:
            resp = self.client.get(url)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "lxml")

            # Extract data based on content patterns
            data_points = self._extract_from_page(soup, url, source_name)

            result = ScrapeResult(
                source_url=url,
                success=True,
                data_points=data_points,
            )
            self.results.append(result)
            return result

        except Exception as e:
            return ScrapeResult(
                source_url=url,
                success=False,
                error=str(e),
            )

    def search_model(self, model_name: str) -> List[ScrapedDataPoint]:
        """Search for information about a specific model across sources."""
        all_points = []
        search_terms = model_name.lower().replace(" ", "+")

        for source_key, source_info in self.SOURCES.items():
            try:
                url = f"{source_info['url'].rstrip('/')}/?s={search_terms}"
                resp = self.client.get(url, timeout=15)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    points = self._extract_from_page(soup, url, source_info["name"])
                    all_points.extend(points)
            except Exception:
                continue

        return all_points

    def _scrape_source(self, source_info: dict) -> ScrapeResult:
        """Scrape a configured source."""
        url = source_info["url"]
        name = source_info["name"]
        return self.scrape_source(url, name)

    def _extract_from_page(self, soup: BeautifulSoup, url: str, source_name: str) -> List[ScrapedDataPoint]:
        """Extract data points from a parsed HTML page."""
        points = []

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # --- Extract model names and years ---
        model_patterns = [
            r"Vespa\s+(98|125|150|160|180|200|250|300|400|50|90)\s*(?:cc|GT[SL]?|Super|Sprint|Rally|PX|ET\d?|PK|Cosa|Primavera)?",
            r"Vespa\s+(GT[SL]?\s+\d{3}|GTV\s+\d{3}|LX\s+\d{2,3}|S\s+\d{2,3}|Primavera\s+\d{2,3})",
            r"(?:Vespa\s+)?(98|125|150|160|180|200)\s*(?:GS|SS|Super|Sprint|Rally|VL[AB]?|V[LM]A\d?)",
        ]

        for pattern in model_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                points.append(ScrapedDataPoint(
                    source_url=url,
                    source_name=source_name,
                    data_type="model",
                    field_name="model_name",
                    field_value=match.group(0).strip(),
                    confidence="medium",
                ))

        # --- Extract years (4-digit numbers that look like years) ---
        year_pattern = r"(?:19[4-9]\d|20[0-2]\d)\s*(?:-|–|to)\s*(?:19[4-9]\d|20[0-2]\d|oggi|present)"
        for match in re.finditer(year_pattern, text, re.IGNORECASE):
            points.append(ScrapedDataPoint(
                source_url=url,
                source_name=source_name,
                data_type="model",
                field_name="production_years",
                field_value=match.group(0).strip(),
                confidence="medium",
            ))

        # --- Extract frame/engine number patterns ---
        number_patterns = [
            r"(?:telaio|frame|chassis|number)\s*(?:n[°o]|no|#)?\s*:?\s*(\d{3,6})",
            r"(?:motore|engine|motor)\s*(?:n[°o]|no|#)?\s*:?\s*(\d{3,6})",
            r"(?:V[LM]A\d?|V[SL]A\d?|VBC|VSD|VSE|PX\d{3}|T5)\s*\d*",
        ]

        for pattern in number_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                points.append(ScrapedDataPoint(
                    source_url=url,
                    source_name=source_name,
                    data_type="frame_range",
                    field_name="number",
                    field_value=match.group(0).strip(),
                    confidence="low",
                ))

        # --- Extract price patterns ---
        price_pattern = r"(?:€|EUR|Euro|euro)\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)"
        for match in re.finditer(price_pattern, text):
            points.append(ScrapedDataPoint(
                source_url=url,
                source_name=source_name,
                data_type="price",
                field_name="price_eur",
                field_value=match.group(0).strip(),
                confidence="low",
            ))

        # --- Extract color names (near keywords) ---
        color_keywords = ["colore", "color", "vernice", "paint", "rosso", "blu",
                          "verde", "giallo", "nero", "bianco", "grigio", "celeste",
                          "argento", "marrone", "viola", "rosa", "arancio", "beige"]
        for keyword in color_keywords:
            # Find text near color keywords
            idx = text.lower().find(keyword)
            if idx >= 0:
                context = text[max(0, idx-30):idx+50]
                points.append(ScrapedDataPoint(
                    source_url=url,
                    source_name=source_name,
                    data_type="color",
                    field_name=keyword,
                    field_value=context.strip()[:100],
                    confidence="low",
                ))

        # Deduplicate (simple: by field_value)
        seen = set()
        unique_points = []
        for p in points:
            key = f"{p.data_type}:{p.field_value}"
            if key not in seen:
                seen.add(key)
                unique_points.append(p)

        return unique_points

    def save_results(self, filename: str = "scrape_results.json") -> str:
        """Save scraping results to a JSON file."""
        filepath = os.path.join(self.data_dir, filename)
        data = []
        for result in self.results:
            data.append({
                "source_url": result.source_url,
                "success": result.success,
                "error": result.error,
                "data_points_count": len(result.data_points),
                "data_points": [asdict(dp) for dp in result.data_points[:50]],  # limit per source
                "timestamp": result.timestamp,
            })

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()