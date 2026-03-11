import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def test_list_all():
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    print("Testing internal 'list_all' logic manually...")
    try:
        cursor = db["users"].find()
        async for user in cursor:
            user_id_str = str(user["_id"])
            print(f"Checking user: {user.get('email')}")
            
            # This is line 86 - 100 in auth.py
            # 86: Calculate Stats for this user
            order_count = await db["orders"].count_documents({"user_id": user_id_str})
            
            total_spent = 0
            user_orders = db["orders"].find({"user_id": user_id_str})
            async for ord in user_orders:
                try:
                    amount_str = "".join(filter(str.isdigit, ord.get("total_amount", "0")))
                    total_spent += int(amount_str) if amount_str else 0
                except:
                    pass
            
            joining_date = user.get("created_at")
            if not joining_date:
                joining_date = datetime.utcnow()
            
            # This is line 100 in auth.py: strftime
            joining_str = joining_date.strftime("%d %b %Y")
            print(f"  - Orders: {order_count}, Spent: {total_spent}, Joined: {joining_str}")
        
        print("\nInternal logic passed for all users in DB.")
        
    except Exception as e:
        print(f"\nCRASHED with error: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()

    client.close()

if __name__ == "__main__":
    asyncio.run(test_list_all())
