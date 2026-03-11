import asyncio
import os
import certifi
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_auth_all_directly():
    # Use motor to check database content
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    # Check users collection
    print("Checking database users directly...")
    users_list = await db["users"].find().to_list(100)
    print(f"Total Users in DB: {len(users_list)}")
    for u in users_list:
        print(f"  - {u.get('email')} | is_admin: {u.get('is_admin')}")

    # Simulate list_all_users endpoint logic
    print("\nSimulating /auth/all logic internally...")
    try:
        results = []
        for user in users_list:
            user_id_str = str(user["_id"])
            user["_id"] = user_id_str
            # Calculate stats...
            results.append(user)
        print(f"Simulated result has {len(results)} items.")
    except Exception as e:
        print(f"Internal Logic Simulation Failed: {e}")

    # Now make an actual request to the running server!
    print("\nMaking HTTP request to running server on localhost:8000...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            # Login first
            login_data = {
                "username": os.getenv("ADMIN_EMAIL"),
                "password": os.getenv("ADMIN_PASSWORD")
            }
            login_res = await http_client.post("http://localhost:8000/api/auth/login", data=login_data)
            
            if login_res.status_code == 200:
                token = login_res.json()["access_token"]
                print("Login successful.")
                
                # Fetch all users
                auth_res = await http_client.get(
                    "http://localhost:8000/api/auth/all", 
                    headers={"Authorization": f"Bearer {token}"}
                )
                print(f"API /auth/all status: {auth_res.status_code}")
                if auth_res.status_code == 200:
                    data = auth_res.json()
                    print(f"API returned {len(data)} customers.")
                    if len(data) > 0:
                        print(f"First customer: {data[0].get('email')}")
                else:
                    print(f"API Error Content: {auth_res.text}")
            else:
                print(f"Login failed: {login_res.status_code} - {login_res.text}")
    except Exception as e:
        print(f"HTTP Request failed: {e}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(test_auth_all_directly())
