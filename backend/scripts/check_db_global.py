import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def list_db_data():
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    print("--- COLLECTIONS ---")
    cols = await db.list_collection_names()
    print(cols)
    
    for col_name in ['users', 'orders']:
        print(f"\n--- {col_name.upper()} ---")
        count = await db[col_name].count_documents({})
        print(f"Total entries: {count}")
        
        cursor = db[col_name].find().sort('_id', -1).limit(5)
        async for doc in cursor:
            # Print a summary of each doc
            if col_name == 'users':
                print(f"User: {doc.get('email')} | Name: {doc.get('name')} | Admin: {doc.get('is_admin')}")
            else:
                print(f"Order ID: {doc.get('_id')} | UserID: {doc.get('user_id')} | Amount: {doc.get('total_amount')} | Date: {doc.get('created_at')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(list_db_data())
