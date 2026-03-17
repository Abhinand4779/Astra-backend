import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

client = None
if key_id and key_secret and not key_id.endswith("Here"):
    try:
        client = razorpay.Client(auth=(key_id, key_secret))
    except Exception as e:
        print(f"Failed to initialize Razorpay client: {e}")

def create_checkout_session(order_id, amount_in_rupees, customer_email, customer_name="", customer_phone=""):
    """
    Creates a Razorpay Payment Link for the given order.
    Returns a URL we can redirect the customer to (similar to Stripe Checkout).
    """
    try:
        if not client:
            print("RAZORPAY ERROR: Client not initialized. Check your RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env.")
            return None

        if amount_in_rupees <= 0:
            print(f"RAZORPAY ERROR: Invalid amount ₹{amount_in_rupees}. Amount must be greater than zero.")
            return None

        amount_in_paise = int(amount_in_rupees * 100)
        callback_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/orders?success=true"

        payment_link = client.payment_link.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "accept_partial": False,
            "description": f"Order #{str(order_id)}",
            "customer": {
                "email": customer_email,
                "name": customer_name,
                "contact": customer_phone
            },
            "notify": {
                "sms": False,
                "email": True
            },
            "reminder_enable": True,
            "callback_url": callback_url,
            "callback_method": "get"
        })
        
        return payment_link.get('short_url')

    except Exception as e:
        print(f"RAZORPAY ERROR: {e}")
        return None
