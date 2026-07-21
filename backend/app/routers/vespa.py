"""
OcchioEsperto.it — Vespa analysis router.
Endpoints for identifying, analyzing, and managing Vespa scooters.
"""
import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status, UploadFile, File, Form
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
    requires_registration_for_full_report: bool = False
    garage_id: Optional[int] = None
    photo_count: int = 0
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


class UpdateGarageVespaRequest(BaseModel):
    display_name: Optional[str] = None
    notes: Optional[str] = None
    color_name: Optional[str] = None
    color_hex: Optional[str] = None


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
    photos: list[UploadFile] = File(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Identify a Vespa model from frame number, engine number, or photo."""
    plan = current_user.plan.value if current_user else UserPlan.FREE.value
    result = {
        "disclaimer": DISCLAIMER,
        "confidence": "low",
        "match_type": "none",
        "plan": plan,
        "requires_registration_for_full_report": False,
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
    frame_match = None
    engine_match = None

    # Try frame number matching first
    if frame_number:
        frame_match = knowledge_base.identify_by_frame_number(frame_number, year=year)
        if frame_match:
            match = frame_match
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
        engine_match = knowledge_base.identify_by_engine_number(engine_number, year=year)
        if engine_match:
            match = engine_match
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

    if frame_number and not engine_number and frame_match:
        ranges = knowledge_base._get_engine_ranges(frame_match["model_id"])
        if ranges:
            result["engine_prefix_suggestion"] = ranges[0].get("notes") or ranges[0].get("engine_number_start")
    if engine_number and not frame_number and engine_match:
        ranges = knowledge_base._get_frame_ranges(engine_match["model_id"])
        if ranges:
            result["frame_prefix_suggestion"] = ranges[0].get("notes") or ranges[0].get("frame_number_start")
    if frame_number and engine_number:
        if not engine_match:
            engine_match = knowledge_base.identify_by_engine_number(engine_number, year=year)
        result["number_correspondence"] = {
            "status": "coherent" if frame_match and engine_match and frame_match["model_id"] == engine_match["model_id"] else "to_review",
            "message": "Telaio e motore risultano coerenti per lo stesso modello." if frame_match and engine_match and frame_match["model_id"] == engine_match["model_id"] else "Telaio e motore meritano un controllo più attento nella scheda completa.",
        }

    # Save up to 10 photos for this account-backed identification.
    uploaded_photos = [p for p in ([photo] if photo and photo.filename else []) + list(photos or []) if p and p.filename]
    if len(uploaded_photos) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Puoi caricare al massimo 10 fotografie per identificazione.",
        )
    photo_paths = []
    for uploaded_photo in uploaded_photos:
        photo_paths.append(await save_upload_file(uploaded_photo, subdir=f"identifications/user-{current_user.id}"))

    # If matched, provide basic identification
    if matched_model:
        result["identification"] = {
            "model_name": matched_model["name"],
            "years": f"{matched_model['production_start']} - {matched_model['production_end'] or 'oggi'}",
            "engine_cc": matched_model["engine_cc"],
        }

    should_use_ai = bool(photo_paths or notes or not matched_model or result["confidence"] != "high")
    if should_use_ai:
        expert = ai_expert.enrich_identification(
            frame_number=frame_number,
            engine_number=engine_number,
            year=year,
            notes=notes,
            deterministic_match=match if matched_model else None,
            photo_uploaded=bool(photo_paths),
            plan=plan,
            analysis_depth="basic" if plan == UserPlan.FREE.value else "premium",
        )
        result["expert_analysis"] = expert
        result["confidence"] = expert.get("confidence", result["confidence"])
        if not matched_model and expert.get("model_name"):
            years = expert.get("years") or ""
            start, end = None, None
            if " - " in years:
                parts = years.split(" - ", 1)
                start = int(parts[0]) if parts[0].isdigit() else None
                end = int(parts[1]) if parts[1].isdigit() else None
            matched_model = {
                "id": None,
                "name": expert["model_name"],
                "slug": None,
                "production_start": start,
                "production_end": end,
                "engine_cc": expert.get("engine_cc") or "",
            }
            result["model"] = matched_model
            result["identification"] = {
                "model_name": matched_model["name"],
                "years": years or "Da confermare",
                "engine_cc": matched_model["engine_cc"] or "Da confermare",
            }
    elif matched_model:
        result["expert_analysis"] = ai_expert.enrich_identification(
            frame_number=frame_number,
            engine_number=engine_number,
            year=year,
            deterministic_match=match,
            photo_uploaded=False,
            plan=plan,
            analysis_depth="basic" if plan == UserPlan.FREE.value else "premium",
        )

    result["photo_count"] = len(photo_paths)
    vespa = UserVespa(
        user_id=current_user.id,
        display_name=(matched_model.get("name") if matched_model else result.get("expert_analysis", {}).get("model_name")) or "La mia Vespa",
        model_id=matched_model.get("id") if matched_model else None,
        model_name=(matched_model.get("name") if matched_model else result.get("expert_analysis", {}).get("model_name")) or "Identificazione da completare",
        model_slug=matched_model.get("slug") if matched_model else None,
        year=year,
        frame_number=frame_number,
        engine_number=engine_number,
        notes=notes,
        photo_path=photo_paths[0] if photo_paths else None,
        analysis_json=json.dumps({**result, "photo_paths": photo_paths}, ensure_ascii=False),
    )
    db.add(vespa)
    db.commit()
    db.refresh(vespa)
    result["garage_id"] = vespa.id

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
        display_name=req.model_name,
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
        "vespe": [_serialize_vespa(v) for v in vespe],
        "disclaimer": DISCLAIMER,
    }


@router.get("/garage/{vespa_id}")
def get_garage_vespa(
    vespa_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Open one saved Vespa with its stored analysis."""
    return _serialize_vespa(_get_user_vespa(db, current_user.id, vespa_id))


@router.patch("/garage/{vespa_id}")
def update_garage_vespa(
    vespa_id: int,
    req: UpdateGarageVespaRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Rename a saved Vespa and update editable garage fields."""
    vespa = _get_user_vespa(db, current_user.id, vespa_id)
    if req.display_name is not None:
        vespa.display_name = sanitize_string(req.display_name, max_length=255) or vespa.model_name
    if req.notes is not None:
        vespa.notes = sanitize_string(req.notes, max_length=1000)
    if req.color_name is not None:
        vespa.color_name = sanitize_string(req.color_name, max_length=100)
    if req.color_hex is not None:
        vespa.color_hex = sanitize_string(req.color_hex, max_length=7)
    db.commit()
    db.refresh(vespa)
    return _serialize_vespa(vespa)


@router.post("/garage/{vespa_id}/photo")
async def update_garage_photo(
    vespa_id: int,
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Choose/upload the primary image for a garage Vespa."""
    vespa = _get_user_vespa(db, current_user.id, vespa_id)
    vespa.photo_path = await save_upload_file(photo, subdir=f"garage/user-{current_user.id}")
    db.commit()
    db.refresh(vespa)
    return _serialize_vespa(vespa)


@router.post("/garage/{vespa_id}/pro-analysis")
def run_pro_analysis(
    vespa_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Use an active paid token/plan to enrich one saved vehicle analysis."""
    if current_user.plan not in (UserPlan.INTERMEDIO, UserPlan.AVANZATO):
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Sblocca una scheda completa per approfondire questo veicolo.")
    vespa = _get_user_vespa(db, current_user.id, vespa_id)
    stored = json.loads(vespa.analysis_json) if vespa.analysis_json else {}
    if vespa.model_id:
        stored["pro_analysis"] = knowledge_base.get_full_analysis(vespa.model_id, current_user.plan.value)
    stored["expert_deep_dive"] = ai_expert.enrich_identification(
        frame_number=vespa.frame_number,
        engine_number=vespa.engine_number,
        year=vespa.year,
        notes=vespa.notes,
        plan=current_user.plan.value,
        analysis_depth="pro",
        photo_uploaded=bool(vespa.photo_path),
    )
    vespa.analysis_level = current_user.plan.value
    vespa.analysis_json = json.dumps(stored, ensure_ascii=False)
    db.commit()
    db.refresh(vespa)
    return _serialize_vespa(vespa)


@router.get("/garage/{vespa_id}/report.pdf")
def download_pro_report(
    vespa_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download a compact PDF report for paid, enriched vehicles."""
    vespa = _get_user_vespa(db, current_user.id, vespa_id)
    if current_user.plan not in (UserPlan.INTERMEDIO, UserPlan.AVANZATO) or vespa.analysis_level == "basic":
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Report Pro disponibile dopo aver sbloccato la scheda completa.")
    pdf = _build_simple_pdf([
        "OcchioEsperto.it - Report Pro",
        f"Veicolo: {vespa.display_name or vespa.model_name}",
        f"Modello: {vespa.model_name}",
        f"Anno: {vespa.year or 'N/D'}",
        f"Telaio: {vespa.frame_number or 'N/D'}",
        f"Motore: {vespa.engine_number or 'N/D'}",
        "Include dati storici, range telaio/motore, controlli colore e analisi esperta disponibili per il piano attivo.",
        DISCLAIMER,
    ])
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="occhioesperto-vespa-{vespa.id}.pdf"'})


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


def _get_user_vespa(db: Session, user_id: int, vespa_id: int) -> UserVespa:
    vespa = db.query(UserVespa).filter(UserVespa.id == vespa_id, UserVespa.user_id == user_id).first()
    if not vespa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vespa non trovata nel garage")
    return vespa


def _serialize_vespa(v: UserVespa) -> dict:
    return {
        "id": v.id,
        "display_name": v.display_name or v.model_name,
        "model_name": v.model_name,
        "model_id": v.model_id,
        "model_slug": v.model_slug,
        "year": v.year,
        "frame_number": v.frame_number,
        "engine_number": v.engine_number,
        "color_name": v.color_name,
        "color_hex": v.color_hex,
        "notes": v.notes,
        "photo_path": v.photo_path,
        "analysis_level": v.analysis_level or "basic",
        "pro_report_path": v.pro_report_path,
        "analysis": json.loads(v.analysis_json) if v.analysis_json else None,
        "created_at": v.created_at.isoformat() if v.created_at else None,
    }


def _build_simple_pdf(lines: list[str]) -> bytes:
    """Tiny dependency-free text PDF generator for the downloadable Pro report."""
    safe_lines = [line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")[:100] for line in lines]
    text_ops = ["BT", "/F1 12 Tf", "50 790 Td"]
    for i, line in enumerate(safe_lines):
        if i:
            text_ops.append("0 -18 Td")
        text_ops.append(f"({line}) Tj")
    text_ops.append("ET")
    stream = "\n".join(text_ops).encode("latin-1", "replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return bytes(pdf)