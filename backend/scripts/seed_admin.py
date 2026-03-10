import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

async def seed_admin():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    admin_email = "admin@astra.in"
    admin_password = "admin123"
    
    existing_user = await db["users"].find_one({"email": admin_email})
    
    # Hash password directly using bcrypt library
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    admin_user = {
        "name": "ASTRA Admin",
        "email": admin_email,
        "password": hashed_password,
        "is_admin": True,
        "created_at": None 
    }

    if existing_user:
        await db["users"].update_one(
            {"email": admin_email},
            {"$set": admin_user}
        )
        print(f"Admin user {admin_email} updated successfully.")
    else:
        await db["users"].insert_one(admin_user)
        print(f"Admin user {admin_email} created successfully.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_admin())
