import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_orders():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    count = await db["orders"].count_documents({})
    print(f"Total orders in DB: {count}")
    
    orders = await db["orders"].find().limit(5).to_list(None)
    for ord in orders:
        print(f"Order ID: {ord.get('_id')}, UserID: {ord.get('user_id')}, Total: {ord.get('total_amount')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_orders())
