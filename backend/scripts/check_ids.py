
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    print("--- PRODUCTS IN DB ---")
    for p in db['products'].find():
        print(f"Name: {p.get('name')} | ID: {p.get('id')} | _ID: {p.get('_id')}")

if __name__ == "__main__":
    check()
