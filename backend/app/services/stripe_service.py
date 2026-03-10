import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

def create_checkout_session(order_id, amount_in_rupees, customer_email):
    """
    Creates a Stripe Checkout Session for the given order.
    """
    try:
        # 1. Check if the key is still the default placeholder
        if not stripe.api_key or "your_secret_key" in stripe.api_key or stripe.api_key == "" or "sk_test_51..." in stripe.api_key:
            print("STRIPE ERROR: Stripe Secret Key is missing or using placeholder in .env")
            return None

        # 2. Check if amount is valid (Stripe requires > 0)
        if amount_in_rupees <= 0:
            print(f"STRIPE ERROR: Invalid amount ₹{amount_in_rupees}. Amount must be greater than zero.")
            return None

        # Stripe expects amount in cents/paisa
        unit_amount = int(amount_in_rupees * 100)
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f'Order #{order_id}',
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{os.getenv('FRONTEND_URL')}/orders?success=true",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/checkout?canceled=true",
            customer_email=customer_email,
            metadata={
                "order_id": str(order_id)
            }
        )
        return session.url
    except Exception as e:
        print(f"STRIPE ERROR: {e}")
        return None
