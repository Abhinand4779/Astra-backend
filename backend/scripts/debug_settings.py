import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_settings():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    settings = await db["settings"].find_one({"id": "site_config"})
    config = settings.get("config", {}) if settings else {}
    
    print("KEYS IN DB:", config.keys())
    if "products" in config:
        print(f"Number of Products in DB: {len(config['products'])}")
        for p in config['products'][:2]:
            print(f"Product ID: {p.get('id')} Name: {p.get('name')} Images: {len(p.get('images', []))}")
    else:
        print("No products key in DB")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_settings())
