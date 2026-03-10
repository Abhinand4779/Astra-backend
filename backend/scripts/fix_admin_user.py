"""
This script checks if the admin user exists and has is_admin=True.
If not, it creates or updates the admin user.
Run: python scripts/fix_admin_user.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os, bcrypt
from dotenv import load_dotenv

load_dotenv()

async def fix_admin():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    admin_email = os.getenv("ADMIN_EMAIL", "admin@astra.in")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    print(f"\n--- ASTRA Admin Fix Script ---")
    print(f"Checking for admin user: {admin_email}")
    
    # Check if user exists
    existing = await db["users"].find_one({"email": admin_email})
    
    if existing:
        print(f"✅ Admin user found in database.")
        print(f"   is_admin flag: {existing.get('is_admin', False)}")
        
        if not existing.get("is_admin"):
            # Fix: Set is_admin to True
            await db["users"].update_one(
                {"email": admin_email},
                {"$set": {"is_admin": True}}
            )
            print(f"🔧 FIXED: Set is_admin=True for {admin_email}")
        else:
            print(f"✅ Admin privileges are correctly set. No fix needed.")
    else:
        # Create admin user
        print(f"❌ Admin user NOT found. Creating one...")
        hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        await db["users"].insert_one({
            "email": admin_email,
            "name": "Admin",
            "password": hashed_pw,
            "is_admin": True
        })
        print(f"✅ Admin user created: {admin_email} / {admin_password}")
    
    # Final verification
    admin = await db["users"].find_one({"email": admin_email})
    print(f"\n--- Final State ---")
    print(f"   Email:    {admin['email']}")
    print(f"   Name:     {admin.get('name', 'N/A')}")
    print(f"   is_admin: {admin.get('is_admin', False)}")
    print(f"\n✅ Done! You can now log in with: {admin_email} / {admin_password}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_admin())
