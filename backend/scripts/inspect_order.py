import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def check_last_order():
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    print("Checking 'orders' collection...")
    cursor = db["orders"].find().sort('_id', -1).limit(1)
    found = False
    async for order in cursor:
        found = True
        print("\n--- LATEST ORDER ---")
        for k, v in order.items():
            print(f"{k}: {v}")
    
    if not found:
        print("No orders found in 'orders' collection.")

    client.close()

if __name__ == "__main__":
    asyncio.run(check_last_order())
