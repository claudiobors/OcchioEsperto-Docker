"""
OcchioEsperto.it — Knowledge base service.
Matches frame/engine numbers to Vespa models and retrieves historical data.
"""
import sqlite3
import re
from typing import Optional, Dict, Any, List

from ..config import KNOWLEDGE_DB_PATH, DISCLAIMER


class KnowledgeBase:
    """Service for querying the Vespa knowledge database."""

    def __init__(self, db_path: str = KNOWLEDGE_DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_models(self) -> List[Dict[str, Any]]:
        """Get list of all models."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, slug, production_start, production_end,
                   displacement_cc as engine_cc, description
            FROM vespa_models
            ORDER BY production_start
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_model_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get model details by slug."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, slug, production_start, production_end,
                   displacement_cc as engine_cc, description
            FROM vespa_models WHERE slug = ?
        """, (slug,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_model_by_id(self, model_id: int) -> Optional[Dict[str, Any]]:
        """Get model details by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, slug, production_start, production_end,
                   displacement_cc as engine_cc, description
            FROM vespa_models WHERE id = ?
        """, (model_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def identify_by_frame_number(self, frame_number: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Match frame number to model using prefix, number ranges and year hints."""
        normalized = self._normalize_code(frame_number)
        numeric_part = self._extract_numeric(normalized)
        alpha_prefix = self._extract_alpha_prefix(normalized)
        candidates: list[dict[str, Any]] = []

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.model_id, c.number_start, c.number_end, c.year_start, c.year_end, c.notes,
                   m.name as model_name, m.slug as model_slug, m.production_start, m.production_end,
                   m.displacement_cc as engine_cc
            FROM vespa_chassis_numbers c
            JOIN vespa_models m ON c.model_id = m.id
        """)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            r = dict(row)
            start = self._normalize_code(r.get("number_start", ""))
            end = self._normalize_code(r.get("number_end", "") or start)
            score = 0
            reasons = []

            start_prefix = self._extract_alpha_prefix(start)
            notes_norm = self._normalize_code(r.get("notes", ""))
            if start and len(start) >= 4 and (normalized.startswith(start) or start in normalized):
                score += 55
                reasons.append("prefisso/range telaio coerente")
            if alpha_prefix and (alpha_prefix in notes_norm or notes_norm.startswith(alpha_prefix[:3])):
                score += 70
                reasons.append("sigla telaio presente nei dati storici")
            elif alpha_prefix and start_prefix and (alpha_prefix.startswith(start_prefix) or start_prefix.startswith(alpha_prefix[:3])):
                score += 35
                reasons.append("sigla telaio compatibile")

            n_start = self._extract_numeric(start)
            n_end = self._extract_numeric(end)
            if numeric_part is not None and n_start is not None and n_end is not None:
                if min(n_start, n_end) <= numeric_part <= max(n_start, n_end):
                    if alpha_prefix and not (alpha_prefix in notes_norm or start_prefix):
                        score += 8
                        reasons.append("numero nel range, sigla da verificare")
                    else:
                        score += 45
                        reasons.append("numero nel range storico")

            if year is not None:
                y_start, y_end = r.get("year_start"), r.get("year_end")
                if y_start and (y_end or y_start) and int(y_start) <= year <= int(y_end or y_start):
                    score += 30
                    reasons.append("anno compatibile con il range")
                elif y_start:
                    score -= 40
                    reasons.append("anno fuori range: verificare dati")

            if score > 0:
                r["confidence_score"] = min(score, 99)
                r["confidence"] = "high" if score >= 80 else "medium"
                r["match_type"] = "frame_number"
                r["match_reasons"] = reasons
                candidates.append(r)

        if candidates:
            return sorted(candidates, key=lambda x: x["confidence_score"], reverse=True)[0]
        return None

    def identify_by_engine_number(self, engine_number: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Match engine number to model using engine prefixes and numeric ranges."""
        normalized = self._normalize_code(engine_number)
        numeric_part = self._extract_numeric(normalized)
        alpha_prefix = self._extract_alpha_prefix(normalized)
        candidates: list[dict[str, Any]] = []

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.model_id, e.number_start, e.number_end, e.year_start, e.year_end, e.notes,
                   m.name as model_name, m.slug as model_slug, m.production_start, m.production_end,
                   m.displacement_cc as engine_cc
            FROM vespa_engine_numbers e
            JOIN vespa_models m ON e.model_id = m.id
        """)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            r = dict(row)
            start = self._normalize_code(r.get("number_start", ""))
            end = self._normalize_code(r.get("number_end", "") or start)
            score = 0
            reasons = []
            start_prefix = self._extract_alpha_prefix(start)
            notes_norm = self._normalize_code(r.get("notes", ""))
            if start and len(start) >= 4 and (normalized.startswith(start) or start in normalized):
                score += 60
                reasons.append("sigla motore compatibile")
            if alpha_prefix and (alpha_prefix in notes_norm or notes_norm.startswith(alpha_prefix[:3])):
                score += 50
                reasons.append("sigla motore presente nei dati storici")
            elif alpha_prefix and start_prefix and (alpha_prefix.startswith(start_prefix) or start_prefix.startswith(alpha_prefix[:3])):
                score += 25
                reasons.append("prefisso motore coerente")
            n_start = self._extract_numeric(start)
            n_end = self._extract_numeric(end)
            if numeric_part is not None and n_start is not None and n_end is not None:
                if min(n_start, n_end) <= numeric_part <= max(n_start, n_end):
                    if alpha_prefix and not (alpha_prefix in notes_norm or start_prefix):
                        score += 5
                        reasons.append("numero motore nel range, sigla da verificare")
                    else:
                        score += 35
                        reasons.append("numero motore nel range")

            if year is not None:
                y_start, y_end = r.get("year_start"), r.get("year_end")
                if y_start and (y_end or y_start) and int(y_start) <= year <= int(y_end or y_start):
                    score += 25
                    reasons.append("anno compatibile con il range motore")
                elif y_start:
                    score -= 35
                    reasons.append("anno fuori range motore")

            if score > 0:
                r["confidence_score"] = min(score, 99)
                r["confidence"] = "high" if score >= 80 else "medium"
                r["match_type"] = "engine_number"
                r["match_reasons"] = reasons
                candidates.append(r)

        if candidates:
            return sorted(candidates, key=lambda x: x["confidence_score"], reverse=True)[0]
        return None

    def get_colors_for_model(self, model_id: int) -> List[Dict[str, Any]]:
        """Get historical colors for a model."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, color_name, color_hex, year_start, year_end, notes
            FROM vespa_colors
            WHERE model_id = ?
            ORDER BY year_start
        """, (model_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_issues_for_model(self, model_id: int) -> List[Dict[str, Any]]:
        """Get known issues for a model."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, issue as issue_title, severity, description
            FROM vespa_known_issues
            WHERE model_id = ?
            ORDER BY
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'warning' THEN 2
                    WHEN 'info' THEN 3
                END
        """, (model_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_prices_for_model(self, model_id: int) -> List[Dict[str, Any]]:
        """Get market prices for a model."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, condition_type as condition, price_min as price_min_eur,
                   price_max as price_max_eur, currency, last_updated
            FROM vespa_market_prices
            WHERE model_id = ?
            ORDER BY
                CASE condition_type
                    WHEN 'restored' THEN 1
                    WHEN 'good' THEN 2
                    WHEN 'fair' THEN 3
                    WHEN 'project' THEN 4
                END
        """, (model_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_tech_specs_for_model(self, model_id: int) -> List[Dict[str, Any]]:
        """Get tech specs - derived from the model data."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, displacement_cc as engine_cc, production_start, production_end,
                   description
            FROM vespa_models
            WHERE id = ?
        """, (model_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return []

        model = dict(row)
        specs = [
            {"spec_name": "Cilindrata", "spec_value": model.get("engine_cc", ""), "unit": "cc"},
            {"spec_name": "Inizio produzione", "spec_value": str(model.get("production_start", "")), "unit": ""},
        ]
        if model.get("production_end"):
            specs.append({"spec_name": "Fine produzione", "spec_value": str(model["production_end"]), "unit": ""})
        return specs

    def analyze_color_match(self, color_hex: str, model_id: int) -> List[Dict[str, Any]]:
        """Find closest matching historical color for a given hex code."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT color_name, color_hex, year_start, year_end
            FROM vespa_colors
            WHERE model_id = ?
        """, (model_id,))
        colors = cursor.fetchall()
        conn.close()

        matches = []
        for color in colors:
            hist_hex = color["color_hex"].lstrip("#")
            input_hex = color_hex.lstrip("#")

            # Simple RGB distance matching
            if len(hist_hex) == 6 and len(input_hex) == 6:
                r1, g1, b1 = int(hist_hex[0:2], 16), int(hist_hex[2:4], 16), int(hist_hex[4:6], 16)
                r2, g2, b2 = int(input_hex[0:2], 16), int(input_hex[2:4], 16), int(input_hex[4:6], 16)
                distance = ((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2) ** 0.5

                # Normalize: 0 = perfect, ~441 = max (black to white)
                similarity = max(0, 100 - (distance / 441) * 100)

                matches.append({
                    "color_name": color["color_name"],
                    "color_hex": color["color_hex"],
                    "year_start": color["year_start"],
                    "year_end": color["year_end"],
                    "similarity_percent": round(similarity, 1),
                })

        # Sort by similarity (best match first)
        matches.sort(key=lambda x: x["similarity_percent"], reverse=True)
        return matches[:5]  # Top 5 matches

    def check_originality(self, model_id: int, year: Optional[int] = None,
                          color_name: Optional[str] = None) -> Dict[str, Any]:
        """Check if the configuration looks original."""
        issues = []
        original = True

        colors = self.get_colors_for_model(model_id)
        if color_name and colors:
            color_names = [c["color_name"].lower() for c in colors]
            if color_name.lower() not in color_names:
                issues.append(f"Il colore '{color_name}' non è presente nei registri storici per questo modello.")
                original = False

        if year:
            model = self.get_model_by_id(model_id)
            if model:
                if year < model["production_start"] or (model["production_end"] and year > model["production_end"]):
                    issues.append(f"L'anno {year} non è compreso nel periodo di produzione di questo modello.")
                    original = False

        return {
            "is_original": original,
            "issues": issues,
            "confidence": "medium" if issues else "high"
        }

    def get_full_analysis(self, model_id: int, plan: str = "free") -> Dict[str, Any]:
        """Get comprehensive analysis based on plan level."""
        model = self.get_model_by_id(model_id)
        if not model:
            return {"error": "Modello non trovato"}

        analysis = {
            "model": model,
            "disclaimer": DISCLAIMER,
        }

        # Free: basic model identification
        analysis["identification"] = {
            "model_name": model["name"],
            "years": f"{model['production_start']} - {model['production_end'] or 'oggi'}",
            "engine_cc": model["engine_cc"],
        }

        if plan in ("intermedio", "avanzato"):
            frame_ranges = self._get_frame_ranges(model_id)
            engine_ranges = self._get_engine_ranges(model_id)
            tech_specs = self.get_tech_specs_for_model(model_id)
            analysis["frame_ranges"] = frame_ranges
            analysis["engine_ranges"] = engine_ranges
            analysis["tech_specs"] = tech_specs

        if plan == "avanzato":
            colors = self.get_colors_for_model(model_id)
            issues = self.get_issues_for_model(model_id)
            prices = self.get_prices_for_model(model_id)
            analysis["colors"] = colors
            analysis["known_issues"] = issues
            analysis["market_prices"] = prices
            analysis["originality"] = self.check_originality(model_id)

        return analysis

    def _get_frame_ranges(self, model_id: int) -> List[Dict[str, Any]]:
        """Get frame number ranges for a model."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, number_start as frame_number_start, number_end as frame_number_end,
                   year_start, year_end, notes
            FROM vespa_chassis_numbers
            WHERE model_id = ?
            ORDER BY year_start
        """, (model_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _get_engine_ranges(self, model_id: int) -> List[Dict[str, Any]]:
        """Get engine number ranges for a model."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, number_start as engine_number_start, number_end as engine_number_end,
                   year_start, year_end, notes
            FROM vespa_engine_numbers
            WHERE model_id = ?
            ORDER BY year_start
        """, (model_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


    def search_models(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """Search models by name, slug, displacement or description."""
        q = f"%{query.strip()}%"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, slug, production_start, production_end,
                   displacement_cc as engine_cc, description
            FROM vespa_models
            WHERE name LIKE ? OR slug LIKE ? OR displacement_cc LIKE ? OR description LIKE ?
            ORDER BY production_start
            LIMIT ?
        """, (q, q, q, q, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def upsert_model(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Add or update a Vespa model in the local knowledge base."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vespa_models (name, slug, production_start, production_end, displacement_cc, description)
            VALUES (:name, :slug, :production_start, :production_end, :engine_cc, :description)
            ON CONFLICT(slug) DO UPDATE SET
                name=excluded.name, production_start=excluded.production_start,
                production_end=excluded.production_end, displacement_cc=excluded.displacement_cc,
                description=excluded.description
        """, payload)
        conn.commit()
        model = self.get_model_by_slug(payload["slug"])
        conn.close()
        return model or {}

    def add_known_issue(self, model_id: int, issue: str, severity: str, description: str) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vespa_known_issues (model_id, issue, severity, description)
            VALUES (?, ?, ?, ?)
        """, (model_id, issue, severity, description))
        conn.commit()
        new_id = int(cursor.lastrowid)
        conn.close()
        return new_id

    def add_color(self, model_id: int, color_name: str, color_hex: str, year_start: int | None = None, year_end: int | None = None, notes: str | None = None) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vespa_colors (model_id, color_name, color_hex, year_start, year_end, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (model_id, color_name, color_hex, year_start, year_end, notes))
        conn.commit()
        new_id = int(cursor.lastrowid)
        conn.close()
        return new_id

    @staticmethod
    def _extract_numeric(s: str) -> Optional[int]:
        """Extract numeric value from a string like 'VLA12345'."""
        numbers = re.findall(r'\d+', s or "")
        return int(numbers[-1]) if numbers else None

    @staticmethod
    def _extract_alpha_prefix(s: str) -> str:
        """Extract alpha prefix from a string like 'VLA12345'."""
        match = re.match(r'^([A-Za-z]+)', s or "")
        return match.group(1) if match else ""

    @staticmethod
    def _normalize_code(s: str) -> str:
        """Normalize user-entered frame/engine numbers for matching."""
        return re.sub(r'[^A-Z0-9]', '', (s or '').upper())


# Singleton
knowledge_base = KnowledgeBase()