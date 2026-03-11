import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_api_auth_all():
    # Use the admin credentials from .env
    admin_email = os.getenv("ADMIN_EMAIL", "admin@astra.in")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    base_url = "http://localhost:8000/api"
    
    print(f"Logging in as {admin_email}...")
    login_res = requests.post(
        f"{base_url}/auth/login", 
        data={"username": admin_email, "password": admin_password}
    )
    
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.status_code} - {login_res.text}")
        return
        
    token = login_res.json().get("access_token")
    print("Login successful.")
    
    print("Fetching /api/auth/all...")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{base_url}/auth/all", headers=headers)
    
    if res.status_code == 200:
        data = res.json()
        print(f"Success! Found {len(data)} customers.")
        for u in data:
            print(f"- {u.get('email')} ({u.get('name')}) | Stats: {u.get('orders')} orders, {u.get('spent')} spent")
    else:
        print(f"FAILED: {res.status_code}")
        print(res.text)

if __name__ == "__main__":
    test_api_auth_all()
