import stripe
from typing import Optional
import os

# Initialize Stripe (use test keys for development)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_stripe_secret_key")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_your_stripe_publishable_key")

stripe.api_key = STRIPE_SECRET_KEY

def create_payment_intent(amount: float, currency: str = "INR", metadata: dict = None):
    """Create a Stripe payment intent"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents/paisa
            currency=currency.lower(),
            metadata=metadata or {},
            payment_method_types=["card"],
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "status": intent.status
        }
    except Exception as e:
        raise Exception(f"Payment intent creation failed: {str(e)}")

def confirm_payment(payment_intent_id: str):
    """Confirm a payment"""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            "status": intent.status,
            "amount": intent.amount / 100,
            "currency": intent.currency.upper()
        }
    except Exception as e:
        raise Exception(f"Payment confirmation failed: {str(e)}")

def create_refund(payment_intent_id: str, amount: Optional[float] = None):
    """Create a refund"""
    try:
        refund_data = {"payment_intent": payment_intent_id}
        if amount:
            refund_data["amount"] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_data)
        return {
            "refund_id": refund.id,
            "amount": refund.amount / 100,
            "status": refund.status
        }
    except Exception as e:
        raise Exception(f"Refund failed: {str(e)}")

# Mock payment processor for development (when Stripe keys are not set)
def mock_payment(amount: float, payment_method: str):
    """Mock payment processor for development"""
    return {
        "transaction_id": f"mock_txn_{hash(str(amount) + payment_method)}",
        "status": "completed",
        "amount": amount
    }

