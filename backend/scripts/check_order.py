
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    print("--- FIRST ORDER IN DB ---")
    order = db['orders'].find_one()
    if order:
        import json
        from bson import json_util
        print(json.dumps(order, indent=2, default=json_util.default))
    else:
        print("No orders found.")

if __name__ == "__main__":
    check()
