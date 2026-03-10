import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_pwd():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    user = await db["users"].find_one({"email": "admin@astra.in"})
    if user:
        pwd = user.get("password")
        print(f"User found. Password type: {type(pwd)}")
        if pwd:
            print(f"Password starts with: {pwd[:10]}")
        else:
            print("Password is EMPTY or NONE")
    else:
        print("User NOT found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_pwd())
