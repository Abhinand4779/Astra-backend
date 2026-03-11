
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def migrate():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    settings = db['settings'].find_one({'id': 'site_config'})
    if not settings or 'config' not in settings:
        print("No settings found.")
        return
        
    products = settings['config'].get('products', [])
    if not products:
        print("No products in config.")
        return
        
    # Clear existing products to avoid duplicates during migration
    db['products'].delete_many({})
    
    # Insert them
    db['products'].insert_many(products)
    print(f"Migrated {len(products)} products to 'products' collection.")

if __name__ == "__main__":
    migrate()
