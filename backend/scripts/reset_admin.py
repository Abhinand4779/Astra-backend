import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from app.auth import get_password_hash

load_dotenv()

async def reset_admin():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    admin_email = "admin@astra.in"
    admin_password = "admin123"
    
    # Update or Insert
    admin_user = {
        "name": "ASTRA Admin",
        "email": admin_email,
        "password": get_password_hash(admin_password),
        "is_admin": True
    }
    
    await db["users"].update_one(
        {"email": admin_email},
        {"$set": admin_user},
        upsert=True
    )
    print(f"Admin user {admin_email} has been reset/created with password: {admin_password}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(reset_admin())
