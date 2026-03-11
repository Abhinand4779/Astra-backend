
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check_admin():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    print("--- SEARCHING FOR ADMIN USER ---")
    user = db['users'].find_one({"email": "admin@astra.in"})
    if user:
        print(f"Found User: {user.get('email')}")
        print(f"Is Admin: {user.get('is_admin')}")
        print(f"Has Password Hash: {bool(user.get('password'))}")
    else:
        print("User admin@astra.in NOT FOUND in database.")
        
    print("\n--- ALL USERS WITH is_admin=True ---")
    admins = list(db['users'].find({"is_admin": True}))
    for a in admins:
        print(f"Admin: {a.get('email')}")

if __name__ == "__main__":
    check_admin()
