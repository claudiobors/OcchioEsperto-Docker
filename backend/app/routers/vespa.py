"""
OcchioEsperto.it — Vespa analysis router.
Endpoints for identifying, analyzing, and managing Vespa scooters.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db, User, UserVespa, UserPlan
from ..auth import get_current_user, get_optional_user
from ..services.knowledge_base import knowledge_base
from ..services.ai_expert import ai_expert
from ..utils import save_upload_file, sanitize_string
from ..services.email_service import send_lead_notification
from ..config import DISCLAIMER, PLANS

router = APIRouter(prefix="/api/vespa", tags=["vespa"])


# --- Pydantic schemas ---

class ModelResponse(BaseModel):
    id: int
    name: str
    slug: str
    production_start: int
    production_end: Optional[int] = None
    engine_cc: str
    description: Optional[str] = None


class IdentifyRequest(BaseModel):
    frame_number: Optional[str] = None
    engine_number: Optional[str] = None
    color_hex: Optional[str] = None
    year: Optional[int] = None


class IdentifyResponse(BaseModel):
    model: Optional[dict] = None
    identification: Optional[dict] = None
    expert_analysis: Optional[dict] = None
    confidence: str = "low"
    match_type: str = "none"
    plan: str = "free"
    requires_registration_for_full_report: bool = True
    disclaimer: str = DISCLAIMER


class AnalysisResponse(BaseModel):
    model: dict
    identification: dict
    frame_ranges: Optional[list] = None
    engine_ranges: Optional[list] = None
    tech_specs: Optional[list] = None
    colors: Optional[list] = None
    known_issues: Optional[list] = None
    market_prices: Optional[list] = None
    originality: Optional[dict] = None
    color_matches: Optional[list] = None
    disclaimer: str = DISCLAIMER


class SaveVespaRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_name: str
    year: Optional[int] = None
    frame_number: Optional[str] = None
    engine_number: Optional[str] = None
    color_name: Optional[str] = None
    notes: Optional[str] = None


class SaveVespaResponse(BaseModel):
    id: int
    message: str
    disclaimer: str = DISCLAIMER


class LeadRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_name: str
    year: Optional[int] = None
    condition: Optional[str] = None
    price_asked: Optional[float] = None
    description: Optional[str] = None
    contact_email: str
    contact_phone: Optional[str] = None


class LeadResponse(BaseModel):
    id: int
    message: str
    disclaimer: str = DISCLAIMER


# --- Endpoints ---

@router.get("/models", response_model=list[ModelResponse])
def list_models():
    """Get list of all Vespa models in the knowledge base."""
    models = knowledge_base.get_all_models()
    return [ModelResponse(**m) for m in models]


@router.get("/models/{model_id}", response_model=ModelResponse)
def get_model(model_id: int):
    """Get a specific Vespa model by ID."""
    model = knowledge_base.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modello non trovato")
    return ModelResponse(**model)


@router.post("/identify", response_model=IdentifyResponse)
async def identify_vespa(
    frame_number: Optional[str] = Form(None),
    engine_number: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Identify a Vespa model from frame number, engine number, or photo."""
    plan = current_user.plan.value if current_user else UserPlan.FREE.value
    result = {
        "disclaimer": DISCLAIMER,
        "confidence": "low",
        "match_type": "none",
        "plan": plan,
        "requires_registration_for_full_report": current_user is None,
    }

    # Sanitize inputs
    if frame_number:
        frame_number = sanitize_string(frame_number, max_length=100).upper()
    if engine_number:
        engine_number = sanitize_string(engine_number, max_length=100).upper()
    if notes:
        notes = sanitize_string(notes, max_length=600)

    matched_model = None
    match = None

    # Try frame number matching first
    if frame_number:
        match = knowledge_base.identify_by_frame_number(frame_number, year=year)
        if match:
            matched_model = {
                "id": match["model_id"],
                "name": match["model_name"],
                "slug": match["model_slug"],
                "production_start": match["production_start"],
                "production_end": match["production_end"],
                "engine_cc": match["engine_cc"],
            }
            result["confidence"] = match.get("confidence", "medium")
            result["match_type"] = "frame_number"
            result["model"] = matched_model

    # Try engine number if frame didn't match
    if not matched_model and engine_number:
        match = knowledge_base.identify_by_engine_number(engine_number, year=year)
        if match:
            matched_model = {
                "id": match["model_id"],
                "name": match["model_name"],
                "slug": match["model_slug"],
                "production_start": match["production_start"],
                "production_end": match["production_end"],
                "engine_cc": match["engine_cc"],
            }
            result["confidence"] = match.get("confidence", "medium")
            result["match_type"] = "engine_number"
            result["model"] = matched_model

    # Save photo if uploaded
    photo_path = None
    if photo and photo.filename:
        photo_path = await save_upload_file(photo, subdir="identifications")

    # If matched, provide basic identification
    if matched_model:
        result["identification"] = {
            "model_name": matched_model["name"],
            "years": f"{matched_model['production_start']} - {matched_model['production_end'] or 'oggi'}",
            "engine_cc": matched_model["engine_cc"],
        }

    should_use_ai = bool(photo_path or notes or not matched_model or result["confidence"] != "high")
    if should_use_ai:
        expert = ai_expert.enrich_identification(
            frame_number=frame_number,
            engine_number=engine_number,
            year=year,
            notes=notes,
            deterministic_match=match if matched_model else None,
            photo_uploaded=bool(photo_path),
        )
        result["expert_analysis"] = expert
        result["confidence"] = expert.get("confidence", result["confidence"])
    elif matched_model:
        result["expert_analysis"] = ai_expert.enrich_identification(
            frame_number=frame_number,
            engine_number=engine_number,
            year=year,
            deterministic_match=match,
            photo_uploaded=False,
        )

    return IdentifyResponse(**result)


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_vespa(
    model_id: int = Query(..., description="ID del modello Vespa"),
    color_hex: Optional[str] = Query(None, description="Codice HEX del colore da analizzare"),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Get full analysis of a Vespa model based on user's plan."""
    plan = current_user.plan.value if current_user else UserPlan.FREE

    model = knowledge_base.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modello non trovato")

    analysis = knowledge_base.get_full_analysis(model_id, plan)

    # Add color matching if hex provided and user is on avanzato
    color_matches = None
    if color_hex and plan == "avanzato":
        color_matches = knowledge_base.analyze_color_match(color_hex, model_id)

    return AnalysisResponse(
        model=analysis["model"],
        identification=analysis["identification"],
        frame_ranges=analysis.get("frame_ranges"),
        engine_ranges=analysis.get("engine_ranges"),
        tech_specs=analysis.get("tech_specs"),
        colors=analysis.get("colors"),
        known_issues=analysis.get("known_issues"),
        market_prices=analysis.get("market_prices"),
        originality=analysis.get("originality"),
        color_matches=color_matches,
    )


@router.post("/ask")
def ask_ai_expert(
    question: str = Query(..., description="Domanda sulla Vespa (es. 'colori disponibili', 'prezzi di mercato')"),
    model_id: int = Query(..., description="ID del modello Vespa"),
    current_user: User = Depends(get_current_user),
):
    """Ask the AI Expert a question about a Vespa model (Avanzato plan only)."""
    if current_user.plan != UserPlan.AVANZATO:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="La funzione 'Esperto AI' è disponibile solo per il piano Avanzato (€9.99). "
                   "Vai su /pricing per aggiornare il tuo piano.",
        )

    model = knowledge_base.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modello non trovato")

    # Sanitize question
    from ..utils import sanitize_string
    clean_question = sanitize_string(question, max_length=500)

    result = ai_expert.answer_question(clean_question, model_id)

    return result


@router.post("/save", response_model=SaveVespaResponse)
def save_vespa(
    req: SaveVespaRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save a Vespa to user's digital garage."""
    if current_user.plan == UserPlan.FREE:
        # Free users can save up to 3 vespe
        count = db.query(UserVespa).filter(UserVespa.user_id == current_user.id).count()
        if count >= 3:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Limite gratuito raggiunto (3 vespe). Passa a un piano a pagamento per salvare più vespe.",
            )

    vespa = UserVespa(
        user_id=current_user.id,
        model_name=req.model_name,
        year=req.year,
        frame_number=req.frame_number,
        engine_number=req.engine_number,
        color_name=req.color_name,
        notes=req.notes,
    )
    db.add(vespa)
    db.commit()
    db.refresh(vespa)

    return SaveVespaResponse(id=vespa.id, message="Vespa salvata nel garage digitale!")


@router.get("/garage")
def get_garage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's saved Vespe (digital garage)."""
    vespe = db.query(UserVespa).filter(UserVespa.user_id == current_user.id).all()
    return {
        "vespe": [
            {
                "id": v.id,
                "model_name": v.model_name,
                "year": v.year,
                "frame_number": v.frame_number,
                "engine_number": v.engine_number,
                "color_name": v.color_name,
                "notes": v.notes,
                "created_at": v.created_at.isoformat() if v.created_at else None,
            }
            for v in vespe
        ],
        "disclaimer": DISCLAIMER,
    }


@router.delete("/garage/{vespa_id}")
def delete_vespa(
    vespa_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a Vespa from user's garage."""
    vespa = db.query(UserVespa).filter(
        UserVespa.id == vespa_id,
        UserVespa.user_id == current_user.id,
    ).first()
    if not vespa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vespa non trovata nel garage")

    db.delete(vespa)
    db.commit()
    return {"message": "Vespa rimossa dal garage", "disclaimer": DISCLAIMER}


@router.post("/lead", response_model=LeadResponse)
def create_lead(
    req: LeadRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """Create a sell lead (from 'Vendi' button)."""
    from ..database import Lead

    lead = Lead(
        user_id=current_user.id if current_user else None,
        model_name=req.model_name,
        year=req.year,
        condition=req.condition,
        price_asked=req.price_asked,
        description=req.description,
        contact_email=req.contact_email,
        contact_phone=req.contact_phone,
        status="new",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Send lead notification
    send_lead_notification({
        "model_name": req.model_name,
        "year": req.year,
        "condition": req.condition,
        "price_asked": req.price_asked,
        "contact_email": req.contact_email,
        "contact_phone": req.contact_phone,
        "description": req.description,
    })

    return LeadResponse(id=lead.id, message="Grazie! La tua richiesta di vendita è stata ricevuta.")