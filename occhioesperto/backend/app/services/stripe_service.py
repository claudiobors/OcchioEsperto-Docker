"""
OcchioEsperto.it — Stripe payment integration service.
"""
import stripe
from typing import Optional

from ..config import (
    STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
    STRIPE_PRICE_4_99, STRIPE_PRICE_9_99,
)

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(
    user_email: str,
    user_id: int,
    plan: str,
    success_url: str,
    cancel_url: str,
) -> Optional[dict]:
    """
    Create a Stripe Checkout Session for the given plan.
    
    Returns the session data or None on error.
    """
    price_map = {
        "intermedio": STRIPE_PRICE_4_99,
        "avanzato": STRIPE_PRICE_9_99,
    }

    price_id = price_map.get(plan)
    if not price_id or price_id.startswith("price_"):
        # If using real Stripe price IDs, use them.
        # Otherwise create a one-time price inline.
        amount_map = {
            "intermedio": 499,   # €4.99 in cents
            "avanzato": 999,     # €9.99 in cents
        }
        amount = amount_map.get(plan)
        if not amount:
            return None

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"Piano {plan.capitalize()} - OcchioEsperto.it",
                            "description": f"Accesso al piano {plan} per identificazione Vespa",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user_email,
                metadata={
                    "user_id": str(user_id),
                    "plan": plan,
                },
            )
            return session
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return None
    else:
        # Use predefined price IDs
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user_email,
                metadata={
                    "user_id": str(user_id),
                    "plan": plan,
                },
            )
            return session
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return None


def verify_webhook_signature(payload: bytes, sig_header: str) -> Optional[dict]:
    """
    Verify Stripe webhook signature and return the event.
    """
    if not STRIPE_WEBHOOK_SECRET:
        # Dev mode: accept without verification
        import json
        return json.loads(payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        print(f"Webhook signature verification failed: {e}")
        return None