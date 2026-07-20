"""
OcchioEsperto.it — Admin router.
Administrative endpoints for managing leads and users.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db, User, Lead, Payment, UserVespa
from ..auth import get_admin_user
from ..config import DISCLAIMER

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