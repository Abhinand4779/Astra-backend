
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    email = "admin@astra.in"
    password = "admin" # USER'S PASSWORD FROM PREVIOUS ATTEMPTS WAS LIKELY THIS OR admin123
    
    # Check if exists
    user = db['users'].find_one({"email": email})
    
    hashed_password = pwd_context.hash(password)
    
    if user:
        print(f"Updating existing user {email}...")
        db['users'].update_one(
            {"email": email},
            {"$set": {"password": hashed_password, "is_admin": True, "name": "ASTRA Admin"}}
        )
        print("Updated successfully.")
    else:
        print(f"Creating new admin {email}...")
        db['users'].insert_one({
            "email": email,
            "password": hashed_password,
            "is_admin": True,
            "name": "ASTRA Admin",
            "created_at": None,
            "status": "Active"
        })
        print("Created successfully.")

if __name__ == "__main__":
    create_admin()
