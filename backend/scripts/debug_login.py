import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from passlib.hash import bcrypt

load_dotenv()

async def debug_user():
    print("Connecting to DB...")
    client = AsyncIOMotorClient(
        os.getenv("DATABASE_URL"), 
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    db = client[os.getenv("DATABASE_NAME")]
    
    email = "abhinand@gmail.com"
    print(f"Finding user: {email}...")
    user = await db["users"].find_one({"email": email})
    
    if user:
        print("User Found!")
        print(f"Name: {user.get('name')}")
        print(f"Stored Hash: {user.get('password')}")
        
        # Test password against stored hash using passlib
        test_pass = "password"
        try:
            is_valid = bcrypt.verify(test_pass, user.get('password'))
            print(f"Passlib check for '{test_pass}': {is_valid}")
        except Exception as e:
            print(f"Passlib check failed with error: {e}")
            
    else:
        print("User NOT found in database.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_user())
