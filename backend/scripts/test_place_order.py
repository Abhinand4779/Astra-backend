import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_place_order():
    # 1. Login to get token
    login_data = {
        "username": "admin@astra.in",
        "password": "admin123"
    }
    login_res = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
    
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Place Order
    order_data = {
        "items": [
            {
                "product_id": "1",
                "name": "Test Item",
                "price": "₹1,000",
                "quantity": 1,
                "image": None
            }
        ],
        "total_amount": "₹1,000",
        "shipping_address": {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "123 Street",
            "city": "Test City",
            "state": "Test State",
            "zipCode": "123456",
            "country": "India"
        }
    }
    
    print("Placing order...")
    res = requests.post(f"{BASE_URL}/orders/", headers=headers, json=order_data)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}")

if __name__ == "__main__":
    test_place_order()
