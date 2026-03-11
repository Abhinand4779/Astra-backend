
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def update_db_config():
    client = MongoClient(os.getenv('DATABASE_URL'))
    db = client[os.getenv('DATABASE_NAME')]
    
    # Define the full set of categories
    women_cats = [
        { "name": "Anklets", "count": 42 },
        { "name": "Adjustable Bangle", "count": 25 },
        { "name": "Diamond Replica", "count": 18 },
        { "name": "Bracelet", "count": 64 },
        { "name": "Earrings", "count": 210 },
        { "name": "Hindu God Chains", "count": 12 },
        { "name": "Rings", "count": 56 },
        { "name": "Traditional", "count": 42 },
        { "name": "Hip Chain", "count": 15 },
        { "name": "Jumkhas", "count": 32 },
        { "name": "Bangles", "count": 85 },
        { "name": "Chains", "count": 120 },
        { "name": "Neckpiece", "count": 124 },
        { "name": "Hindu Thali chains", "count": 8 },
        { "name": "Toe Ring", "count": 14 }
    ]
    
    # Get current config
    settings = db['settings'].find_one({'id': 'site_config'})
    if not settings:
        print("Settings not found.")
        return
        
    config = settings.get('config', {})
    
    # Update sectionCategories
    config['sectionCategories'] = config.get('sectionCategories', {})
    config['sectionCategories']['women'] = women_cats
    
    # Clear navCategories dropdowns to ensure they use sectionCategories
    if 'navCategories' in config:
        for cat in config['navCategories']:
            cat['dropdown'] = []
            
    # Save back
    db['settings'].update_one({'id': 'site_config'}, {'$set': {'config': config}})
    print("Database config updated with full category list.")

if __name__ == "__main__":
    update_db_config()
