import asyncio
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_db():
    print("Testing with default URI...")
    uri = os.getenv('DATABASE_URL')
    print("URI:", uri)
    try:
        client1 = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        res = await client1.admin.command('ping')
        print("Success without certifi!", res)
    except Exception as e:
        print("Failed without certifi:", type(e).__name__)

    print("\nTesting with certifi...")
    try:
        client2 = AsyncIOMotorClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        res = await client2.admin.command('ping')
        print("Success with certifi!", res)
    except Exception as e:
        print("Failed with certifi:", type(e).__name__)

    print("\nTesting with tlsAllowInvalidCertificates=True in kwargs...")
    try:
        client3 = AsyncIOMotorClient(uri, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
        res = await client3.admin.command('ping')
        print("Success with tlsAllowInvalidCertificates kwargs!", res)
    except Exception as e:
        print("Failed with kwargs:", type(e).__name__)

asyncio.run(test_db())
