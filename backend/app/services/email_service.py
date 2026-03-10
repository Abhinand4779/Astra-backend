import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# FREE EMAIL SETTINGS (Gmail is best for small stores)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER") # Your Email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") # Your App Password

def send_email(to_email, subject, html_content):
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"SKIPPING EMAIL: SMTP credentials not set. To: {to_email}")
        return False

    msg = MIMEMultipart()
    msg['From'] = f"ASTRA by Ash <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"EMAIL ERROR: {e}")
        return False

def send_order_confirmation(order_data, customer_email):
    subject = "Thank you for your Order! - ASTRA by Ash"
    items_html = "".join([f"<li>{item['name']} - {item['price']} (x{item['quantity']})</li>" for item in order_data['items']])
    
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #9c844a;">Thank you for choosing ASTRA!</h2>
        <p>Dear Customer,</p>
        <p>Your order <strong>#{order_data.get('_id', 'N/A')}</strong> has been successfully placed. We are preparing it with care.</p>
        
        <h3>Order Summary:</h3>
        <ul>{items_html}</ul>
        <p><strong>Total: {order_data['total_amount']}</strong></p>
        
        <p>We'll notify you as soon as your items are shipped!</p>
        <hr>
        <p style="font-size: 12px; color: #999;">ASTRA by Ash - Elegance in Every Detail.</p>
    </div>
    """
    return send_email(customer_email, subject, html)

def send_shipping_notification(order_id, customer_email, tracking_id, tracking_url):
    subject = "Your ASTRA Order is on its way! 🚀"
    
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
        <h2 style="color: #9c844a;">Your Order is Shipped!</h2>
        <p>Great news! Your order <strong>#{order_id}</strong> is now on its way to you.</p>
        
        <p><strong>Tracking ID:</strong> {tracking_id}</p>
        <p><a href="{tracking_url}" style="background: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Track Shipment</a></p>
        
        <p>We hope you love your new ASTRA pieces!</p>
        <hr>
        <p style="font-size: 12px; color: #999;">ASTRA by Ash</p>
    </div>
    """
    return send_email(customer_email, subject, html)
