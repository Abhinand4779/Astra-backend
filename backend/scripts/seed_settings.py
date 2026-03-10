import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def seed_settings():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    # Check if settings already exist
    if await db["settings"].find_one({"id": "site_config"}):
        print("Site configuration already exists.")
    else:
        # Initial default config matching the frontend's defaultConfig
        default_config = {
            "id": "site_config",
            "config": {
                "hero": {
                    "title": "Elegance in Every Detail",
                    "subtitle": "Explore the exclusive collection from Astra by Ash.",
                    "btnText": "Shop Collection",
                    "btnLink": "/shop"
                },
                "footer": {
                    "storeName": "Our Store",
                    "description": "Astra by Ash was started in 2022 to bring elegance and tradition to your everyday style."
                }
                # Add more fields if necessary, but the frontend will handle merging
            }
        }
        await db["settings"].insert_one(default_config)
        print("Initial site configuration seeded.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_settings())
