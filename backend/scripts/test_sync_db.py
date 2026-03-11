import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def test_sync():
    uri = os.getenv('DATABASE_URL')
    print("Testing SYNC pymongo connection...")
    try:
        # Try both with and without certifi
        print("URI:", uri)
        client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("SYNC Connection Successful!")
    except Exception as e:
        print(f"SYNC Connection Failed: {e}")

if __name__ == "__main__":
    test_sync()
