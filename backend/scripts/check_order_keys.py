
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
        # Print keys to see structure
        print("Keys:", list(order.keys()))
        if 'shipping_address' in order:
            print("Shipping Address Keys:", list(order['shipping_address'].keys()))
            print("Email in Shipping Address:", order['shipping_address'].get('email'))
        if 'email' in order:
            print("Top-level Email:", order.get('email'))
    else:
        print("No orders found.")

if __name__ == "__main__":
    check()
