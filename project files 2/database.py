import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "auracart_db"

client = None
db = None
use_mock_db = False

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    db = client[DB_NAME]
    # We'll check actual connection in main.py startup
except Exception:
    use_mock_db = True

async def get_db():
    return db
