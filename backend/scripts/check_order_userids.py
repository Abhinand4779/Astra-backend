
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    print("--- RECENT ORDERS ---")
    cursor = db['orders'].find().limit(5)
    for order in cursor:
        print(f"ID: {order.get('_id')} | UserID: {order.get('user_id')} | Email: {order.get('email')}")
        if 'shipping_address' in order:
            print(f"  Shipping Email: {order['shipping_address'].get('email')}")

if __name__ == "__main__":
    check()
