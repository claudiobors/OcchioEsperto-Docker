"""
OcchioEsperto.it — Vespa analysis router.
Endpoints for identifying, analyzing, enriching and managing Vespa scooters.
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db, User, UserVespa, UserPlan
from ..auth import get_current_user, get_optional_user, get_admin_user
from ..services.ai_service import ai_service
from ..services.knowledge_base import knowledge_base
from ..utils import absolute_upload_path, extract_dominant_hex, save_upload_file
from ..config import DISCLAIMER

router = APIRouter(prefix="/api/vespa", tags=["vespa"])
legacy_router = APIRouter(tags=["legacy-vespa"])


class ModelResponse(BaseModel):
    id: int
    name: str
    slug: str
    production_start: int
    production_end: Optional[int] = None
    engine_cc: str
    description: Optional[str] = None


class IdentifyResponse(BaseModel):
    model: Optional[dict] = None
    identification: Optional[dict] = None
    analysis: Optional[dict] = None
    ai_summary: Optional[str] = None
    ai_model: Optional[str] = None
    photo: Optional[dict] = None
    confidence: str = "low"
    confidence_score: int = 0
    match_type: str = "none"
    recommendations: list[str] = []
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
    ai_summary: Optional[str] = None
    ai_model: Optional[str] = None
    disclaimer: str = DISCLAIMER


class SaveVespaRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: Optional[int] = None
    model_name: str
    year: Optional[int] = None
    frame_number: Optional[str] = None
    engine_number: Optional[str] = None
    color_name: Optional[str] = None
    color_hex: Optional[str] = None
    notes: Optional[str] = None
    analysis_json: Optional[str] = None


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


class ExpertRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: int
    question: str = Field(..., min_length=3, max_length=1500)
    context: Optional[dict] = None


class EnrichModelRequest(BaseModel):
    name: str
    slug: str
    production_start: int
    production_end: Optional[int] = None
    engine_cc: str
    description: Optional[str] = ""


class EnrichIssueRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: int
    issue: str
    severity: str = Field("info", pattern="^(info|warning|critical)$")
    description: str


class EnrichColorRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: int
    color_name: str
    color_hex: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    notes: Optional[str] = None


@router.get("/models", response_model=list[ModelResponse])
def list_models(q: Optional[str] = Query(None, description="Cerca modello, cilindrata o descrizione")):
    models = knowledge_base.search_models(q) if q else knowledge_base.get_all_models()
    return [ModelResponse(**m) for m in models]


@router.get("/models/{model_id}", response_model=ModelResponse)
def get_model(model_id: int):
    model = knowledge_base.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modello non trovato")
    return ModelResponse(**model)


def _model_from_match(match: dict) -> dict:
    return {
        "id": match["model_id"],
        "name": match["model_name"],
        "slug": match["model_slug"],
        "production_start": match["production_start"],
        "production_end": match["production_end"],
        "engine_cc": match["engine_cc"],
    }


def _recommendations(result: dict) -> list[str]:
    recs = []
    if result.get("match_type") == "none":
        recs.append("Aggiungi numero telaio o motore leggibile: aumenta molto l'attendibilità.")
    if result.get("photo", {}).get("dominant_color_hex"):
        recs.append("Confronta il colore estratto dalla foto con i codici originali: luce e restauro possono alterare il risultato.")
    recs.append("Verifica sempre punzonature, libretto e conservazione del telaio prima di acquistare o vendere.")
    return recs


@router.post("/identify", response_model=IdentifyResponse)
async def identify_vespa(
    frame_number: Optional[str] = Form(None),
    engine_number: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Identify a Vespa from frame number, engine number, year and/or photo. Returns immediate rich analysis."""
    result: dict = {"disclaimer": DISCLAIMER, "confidence": "low", "confidence_score": 0, "match_type": "none"}
    matched_model = None

    if frame_number:
        match = knowledge_base.identify_by_frame_number(frame_number, year=year)
        if match:
            matched_model = _model_from_match(match)
            result.update({
                "confidence": match.get("confidence", "medium"),
                "confidence_score": match.get("confidence_score", 80),
                "match_type": "frame_number",
                "match_reasons": match.get("match_reasons", []),
                "model": matched_model,
            })

    if not matched_model and engine_number:
        match = knowledge_base.identify_by_engine_number(engine_number, year=year)
        if match:
            matched_model = _model_from_match(match)
            result.update({
                "confidence": match.get("confidence", "medium"),
                "confidence_score": match.get("confidence_score", 75),
                "match_type": "engine_number",
                "match_reasons": match.get("match_reasons", []),
                "model": matched_model,
            })

    photo_info = None
    color_hex = None
    if photo and photo.filename:
        rel_path = await save_upload_file(photo, subdir="identifications")
        abs_path = absolute_upload_path(rel_path)
        color_hex = extract_dominant_hex(abs_path)
        photo_info = {"path": "/" + rel_path.replace("\\", "/"), "dominant_color_hex": color_hex}
        result["photo"] = photo_info

    if matched_model:
        result["identification"] = {
            "model_name": matched_model["name"],
            "years": f"{matched_model['production_start']} - {matched_model['production_end'] or 'oggi'}",
            "engine_cc": matched_model["engine_cc"],
            "year_input": year,
        }
        plan = current_user.plan.value if current_user else UserPlan.FREE.value
        analysis = knowledge_base.get_full_analysis(matched_model["id"], plan)
        if year:
            analysis["originality"] = knowledge_base.check_originality(matched_model["id"], year=year)
        if color_hex:
            analysis["color_matches"] = knowledge_base.analyze_color_match(color_hex, matched_model["id"])
        result["analysis"] = analysis
        ai = await ai_service.expert_summary(analysis, notes)
        if ai.get("ok"):
            result["ai_summary"] = ai["text"]
            result["ai_model"] = ai["model"]
    elif year:
        # Helpful fallback when only year/photo is available.
        candidates = [m for m in knowledge_base.get_all_models() if m["production_start"] <= year <= (m["production_end"] or 2100)]
        result["identification"] = {"possible_models": candidates[:8], "year_input": year}
        result["confidence_score"] = 25 if candidates else 0

    result["recommendations"] = _recommendations(result)
    return IdentifyResponse(**result)


@legacy_router.post("/vespa/identify", response_model=IdentifyResponse)
@legacy_router.post("/analisi", response_model=IdentifyResponse)
async def identify_vespa_legacy_form(
    frame_number: Optional[str] = Form(None),
    engine_number: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    telaio: Optional[str] = Form(None),
    motore: Optional[str] = Form(None),
    immatricolazione: Optional[str] = Form(None),
    note: Optional[str] = Form(None),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Compatibility endpoint for old frontend builds/native form submits.

    Older bundles posted to /analisi or /vespa/identify and used Italian field names.
    Keep these routes POST-capable so stale browser caches/VPS builds do not surface 405.
    """
    parsed_year = year
    if parsed_year is None and immatricolazione:
        try:
            parsed_year = int(str(immatricolazione).split("-")[0])
        except (TypeError, ValueError):
            parsed_year = None

    return await identify_vespa(
        frame_number=frame_number or telaio,
        engine_number=engine_number or motore,
        year=parsed_year,
        notes=notes or note,
        photo=photo,
        current_user=current_user,
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_vespa(
    model_id: int = Query(..., description="ID del modello Vespa"),
    color_hex: Optional[str] = Query(None, description="Codice HEX del colore da analizzare"),
    year: Optional[int] = Query(None, description="Anno da verificare"),
    with_ai: bool = Query(True, description="Genera sintesi esperta AI se configurata"),
    current_user: Optional[User] = Depends(get_optional_user),
):
    plan = current_user.plan.value if current_user else UserPlan.FREE.value
    model = knowledge_base.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modello non trovato")

    analysis = knowledge_base.get_full_analysis(model_id, plan)
    color_matches = knowledge_base.analyze_color_match(color_hex, model_id) if color_hex else None
    originality = knowledge_base.check_originality(model_id, year=year) if year else analysis.get("originality")
    ai_summary = ai_model = None
    if with_ai:
        ai = await ai_service.expert_summary({**analysis, "color_matches": color_matches, "originality": originality})
        if ai.get("ok"):
            ai_summary = ai["text"]
            ai_model = ai["model"]

    return AnalysisResponse(
        model=analysis["model"],
        identification=analysis["identification"],
        frame_ranges=analysis.get("frame_ranges"),
        engine_ranges=analysis.get("engine_ranges"),
        tech_specs=analysis.get("tech_specs"),
        colors=analysis.get("colors"),
        known_issues=analysis.get("known_issues"),
        market_prices=analysis.get("market_prices"),
        originality=originality,
        color_matches=color_matches,
        ai_summary=ai_summary,
        ai_model=ai_model,
    )


@router.post("/expert")
async def ask_expert(req: ExpertRequest, current_user: Optional[User] = Depends(get_optional_user)):
    model = knowledge_base.get_model_by_id(req.model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Modello non trovato")
    analysis = knowledge_base.get_full_analysis(req.model_id, current_user.plan.value if current_user else UserPlan.FREE.value)
    ai = await ai_service.complete([
        {"role": "user", "content": f"Domanda utente: {req.question}\nContesto modello e dati: {analysis}\nContesto extra: {req.context}"}
    ])
    return {"answer": ai["text"], "model": ai.get("model"), "fallback_used": ai.get("fallback_used"), "disclaimer": DISCLAIMER}


@router.post("/save", response_model=SaveVespaResponse)
def save_vespa(req: SaveVespaRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.plan == UserPlan.FREE:
        count = db.query(UserVespa).filter(UserVespa.user_id == current_user.id).count()
        if count >= 3:
            raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Limite gratuito raggiunto (3 vespe). Passa a un piano a pagamento per salvarne altre.")
    vespa = UserVespa(
        user_id=current_user.id,
        model_id=req.model_id,
        model_name=req.model_name,
        year=req.year,
        frame_number=req.frame_number,
        engine_number=req.engine_number,
        color_name=req.color_name,
        color_hex=req.color_hex,
        notes=req.notes,
        analysis_json=req.analysis_json,
    )
    db.add(vespa)
    db.commit()
    db.refresh(vespa)
    return SaveVespaResponse(id=vespa.id, message="Vespa salvata nel garage digitale!")


@router.get("/garage")
def get_garage(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    vespe = db.query(UserVespa).filter(UserVespa.user_id == current_user.id).all()
    return {"vespe": [{"id": v.id, "model_id": v.model_id, "model_name": v.model_name, "year": v.year, "frame_number": v.frame_number, "engine_number": v.engine_number, "color_name": v.color_name, "color_hex": v.color_hex, "notes": v.notes, "created_at": v.created_at.isoformat() if v.created_at else None} for v in vespe], "disclaimer": DISCLAIMER}


@router.delete("/garage/{vespa_id}")
def delete_vespa(vespa_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    vespa = db.query(UserVespa).filter(UserVespa.id == vespa_id, UserVespa.user_id == current_user.id).first()
    if not vespa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vespa non trovata nel garage")
    db.delete(vespa)
    db.commit()
    return {"message": "Vespa rimossa dal garage", "disclaimer": DISCLAIMER}


@router.post("/lead", response_model=LeadResponse)
def create_lead(req: LeadRequest, current_user: Optional[User] = Depends(get_optional_user), db: Session = Depends(get_db)):
    from ..database import Lead
    lead = Lead(user_id=current_user.id if current_user else None, model_name=req.model_name, year=req.year, condition=req.condition, price_asked=req.price_asked, description=req.description, contact_email=req.contact_email, contact_phone=req.contact_phone, status="new")
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return LeadResponse(id=lead.id, message="Grazie! La tua richiesta di vendita è stata ricevuta.")


@router.post("/knowledge/models")
def enrich_model(req: EnrichModelRequest, admin: User = Depends(get_admin_user)):
    model = knowledge_base.upsert_model(req.model_dump())
    return {"message": "Knowledge base aggiornata", "model": model, "disclaimer": DISCLAIMER}


@router.post("/knowledge/issues")
def enrich_issue(req: EnrichIssueRequest, admin: User = Depends(get_admin_user)):
    new_id = knowledge_base.add_known_issue(req.model_id, req.issue, req.severity, req.description)
    return {"message": "Problema noto aggiunto", "id": new_id, "disclaimer": DISCLAIMER}


@router.post("/knowledge/colors")
def enrich_color(req: EnrichColorRequest, admin: User = Depends(get_admin_user)):
    new_id = knowledge_base.add_color(req.model_id, req.color_name, req.color_hex, req.year_start, req.year_end, req.notes)
    return {"message": "Colore storico aggiunto", "id": new_id, "disclaimer": DISCLAIMER}
