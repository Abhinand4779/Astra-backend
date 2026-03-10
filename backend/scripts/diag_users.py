import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def list_users():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    users = await db["users"].find().to_list(100)
    print(f"Total users found: {len(users)}")
    for u in users:
        print(f"Email: '{u.get('email')}', IsAdmin: {u.get('is_admin')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_users())
