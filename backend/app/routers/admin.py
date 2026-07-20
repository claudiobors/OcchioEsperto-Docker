"""
OcchioEsperto.it — Admin router.
Administrative endpoints for managing leads and users.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db, User, Lead, Payment, UserVespa
from ..auth import get_admin_user
from ..config import DISCLAIMER, KNOWLEDGE_DB_PATH

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/leads")
def list_leads(
    status_filter: Optional[str] = Query(None, description="Filtra per stato (new, contacted, completed, archived)"),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get all sell leads (admin only)."""
    query = db.query(Lead).order_by(Lead.created_at.desc())

    if status_filter:
        query = query.filter(Lead.status == status_filter)

    total = query.count()
    leads = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "leads": [
            {
                "id": l.id,
                "user_id": l.user_id,
                "model_name": l.model_name,
                "year": l.year,
                "condition": l.condition,
                "price_asked": l.price_asked,
                "description": l.description,
                "contact_email": l.contact_email,
                "contact_phone": l.contact_phone,
                "status": l.status,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in leads
        ],
        "disclaimer": DISCLAIMER,
    }


@router.put("/leads/{lead_id}/status")
def update_lead_status(
    lead_id: int,
    status_value: str = Query(..., description="Nuovo stato (new, contacted, completed, archived)"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Update lead status (admin only)."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"error": "Lead non trovato", "disclaimer": DISCLAIMER}

    valid_statuses = ["new", "contacted", "completed", "archived"]
    if status_value not in valid_statuses:
        return {"error": f"Stato non valido. Usa: {', '.join(valid_statuses)}", "disclaimer": DISCLAIMER}

    lead.status = status_value
    db.commit()

    return {
        "message": f"Lead {lead_id} aggiornato a '{status_value}'",
        "id": lead_id,
        "status": status_value,
        "disclaimer": DISCLAIMER,
    }


@router.get("/stats")
def get_stats(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get admin statistics."""
    total_users = db.query(User).count()
    total_leads = db.query(Lead).count()
    total_payments = db.query(Payment).filter(Payment.status == "completed").count()
    total_vespe = db.query(UserVespa).count()

    plan_counts = db.query(User.plan).all()
    plan_distribution = {}
    for p in plan_counts:
        val = p[0].value if hasattr(p[0], 'value') else str(p[0])
        plan_distribution[val] = plan_distribution.get(val, 0) + 1

    return {
        "total_users": total_users,
        "total_leads": total_leads,
        "completed_payments": total_payments,
        "total_vespe_saved": total_vespe,
        "plan_distribution": plan_distribution,
        "disclaimer": DISCLAIMER,
    }


@router.post("/scrape")
def run_scrape(
    source_url: Optional[str] = Query(None, description="URL specifico da cui fare scraping"),
    admin: User = Depends(get_admin_user),
):
    """Run web scraping to enrich the knowledge base (admin only)."""
    from ..services.web_scraper import WebScraper

    scraper = WebScraper()
    try:
        if source_url:
            result = scraper.scrape_source(source_url)
        else:
            results = scraper.scrape_all()
            report_path = scraper.save_results()

            total_points = sum(len(r.data_points) for r in results if r.success)
            ok = sum(1 for r in results if r.success)
            failed = sum(1 for r in results if not r.success)

            return {
                "message": "Scraping completato",
                "sources_ok": ok,
                "sources_failed": failed,
                "total_data_points": total_points,
                "report_saved": report_path,
                "details": [
                    {
                        "source": r.source_url,
                        "success": r.success,
                        "data_points": len(r.data_points),
                        "error": r.error,
                    }
                    for r in results
                ],
                "disclaimer": DISCLAIMER,
            }
        return {
            "message": "Scraping completato",
            "source": source_url,
            "data_points": len(result.data_points),
            "success": result.success,
            "error": result.error,
            "disclaimer": DISCLAIMER,
        }
    finally:
        scraper.close()


@router.get("/verify")
def verify_knowledge_base(
    admin: User = Depends(get_admin_user),
):
    """Verify KB consistency and show discrepancies (admin only)."""
    from ..services.data_verifier import DataVerifier

    verifier = DataVerifier()
    try:
        summary = verifier.verify_all_models()
        report_path = verifier.save_report()

        discrepancies = [
            {
                "model": d.model_name,
                "field": d.field,
                "kb_value": d.kb_value,
                "expected": d.external_value,
                "severity": d.severity,
            }
            for d in summary.get("discrepancies", [])
        ]

        missing_info = [
            {
                "model": m.model_name,
                "field": m.field,
                "suggestion": m.suggested_value,
                "confidence": m.confidence,
            }
            for m in summary.get("missing_info", [])
        ]

        return {
            "total_models": summary.get("total_models", 0),
            "total_checks": summary.get("total_checks", 0),
            "discrepancies": discrepancies,
            "warnings_count": len(summary.get("warnings", [])),
            "missing_info": missing_info,
            "report_path": report_path,
            "disclaimer": DISCLAIMER,
        }
    finally:
        pass  # verifier has no cleanup needed


@router.post("/verify/model/{model_slug}")
def verify_single_model(
    model_slug: str,
    admin: User = Depends(get_admin_user),
):
    """Verify a specific model (admin only)."""
    from ..services.data_verifier import DataVerifier
    from ..services.knowledge_base import knowledge_base

    model = knowledge_base.get_model_by_slug(model_slug)
    if not model:
        return {"error": f"Modello '{model_slug}' non trovato", "disclaimer": DISCLAIMER}

    verifier = DataVerifier()
    results = verifier.verify_model(model_slug)

    return {
        "model": model["name"],
        "checks": [
            {
                "field": r.field,
                "status": "ok" if r.match else "warning",
                "severity": r.severity,
                "current_value": r.kb_value,
                "expected": r.external_value,
            }
            for r in results
        ],
        "disclaimer": DISCLAIMER,
    }