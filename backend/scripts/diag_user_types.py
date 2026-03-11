import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def diag_user_types():
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    print("Listing user created_at types...")
    cursor = db["users"].find()
    async for user in cursor:
        ca = user.get("created_at")
        print(f"User: {user.get('email')} | created_at: {ca} | type: {type(ca)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(diag_user_types())
