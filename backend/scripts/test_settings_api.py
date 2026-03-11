
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_settings_post():
    API_URL = "http://localhost:8000/api"
    
    async with httpx.AsyncClient() as client:
        # 1. Login
        login_res = await client.post(f"{API_URL}/auth/login", data={
            "username": "testadmin@astra.in",
            "password": "password123"
        })
        if login_res.status_code != 200:
            print(f"Login failed: {login_res.text}")
            return
            
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get current config
        res = await client.get(f"{API_URL}/settings/")
        config = res.json().get("config", {})
        
        # 3. Add a dummy product
        if "products" not in config: config["products"] = []
        
        dummy_product = {
            "id": 9999,
            "name": "TEST PRODUCT",
            "price": "₹1,000",
            "section": "Women",
            "category": "Bangles",
            "images": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="]
        }
        
        config["products"].append(dummy_product)
        
        # 4. Try to save
        print("Saving config...")
        save_res = await client.post(f"{API_URL}/settings/", json=config, headers=headers)
        print(f"SAVE Status: {save_res.status_code}")
        print(f"Response: {save_res.text}")


if __name__ == "__main__":
    asyncio.run(test_settings_post())
