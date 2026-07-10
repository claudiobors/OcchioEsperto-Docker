"""
OcchioEsperto.it — Payments router.
Stripe checkout, webhooks, and plan management.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import stripe

from ..database import get_db, User, UserPlan, Payment
from ..auth import get_current_user
from ..services.stripe_service import create_checkout_session, verify_webhook_signature
from ..config import DISCLAIMER

router = APIRouter(prefix="/api/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    plan: str  # "intermedio" or "avanzato"
    success_url: str = "https://occhioesperto.it/payments/success"
    cancel_url: str = "https://occhioesperto.it/payments/cancel"


class CheckoutResponse(BaseModel):
    session_url: str
    session_id: str
    disclaimer: str = DISCLAIMER


@router.post("/create-checkout", response_model=CheckoutResponse)
def create_checkout(
    req: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe Checkout session for the selected plan."""
    if req.plan not in ("intermedio", "avanzato"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Piano non valido. Scegli: intermedio o avanzato.")

    session = create_checkout_session(
        user_email=current_user.email,
        user_id=current_user.id,
        plan=req.plan,
        success_url=req.success_url,
        cancel_url=req.cancel_url,
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore nella creazione della sessione di pagamento. Riprova più tardi.",
        )

    # Save payment record
    payment = Payment(
        user_id=current_user.id,
        stripe_session_id=session.id,
        amount=4.99 if req.plan == "intermedio" else 9.99,
        currency="EUR",
        plan=req.plan,
        status="pending",
    )
    db.add(payment)
    db.commit()

    return CheckoutResponse(
        session_url=session.url,
        session_id=session.id,
    )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    event = verify_webhook_signature(payload, sig_header)
    if not event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")

    # Handle the event
    event_type = event.get("type", "")
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        user_id = int(metadata.get("user_id", 0))
        plan = metadata.get("plan", "intermedio")

        # Update user plan
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.plan = UserPlan(plan)

            # Update payment record
            payment = db.query(Payment).filter(
                Payment.stripe_session_id == session.id
            ).first()
            if payment:
                payment.status = "completed"
                payment.stripe_payment_intent = session.get("payment_intent")

            db.commit()

    return {"status": "ok"}


@router.get("/plans")
def get_plans():
    """Get available plans and features."""
    from ..config import PLANS
    return {
        "plans": {
            key: {
                "name": val["name"],
                "price": val["price"],
                "features": val["features"],
            }
            for key, val in PLANS.items()
        },
        "disclaimer": DISCLAIMER,
    }


@router.post("/verify")
def verify_payment(
    session_id: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if a payment session was completed successfully."""
    payment = db.query(Payment).filter(
        Payment.stripe_session_id == session_id,
        Payment.user_id == current_user.id,
    ).first()

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento non trovato")

    return {
        "status": payment.status,
        "plan": payment.plan,
        "amount": payment.amount,
        "user_plan": current_user.plan.value,
        "disclaimer": DISCLAIMER,
    }