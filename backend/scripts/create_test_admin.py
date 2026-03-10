import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from app.auth import get_password_hash

load_dotenv()

async def create_test_admin():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    email = "test@astra.in"
    pwd = "password123"
    
    user = {
        "name": "Test Admin",
        "email": email,
        "password": get_password_hash(pwd),
        "is_admin": True
    }
    
    await db["users"].delete_many({"email": email})
    await db["users"].insert_one(user)
    print(f"Created test user {email} with password {pwd}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_admin())
