from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    await db.client.server_info()  # Test connection

async def close_mongo_connection():
    db.client.close()

def get_database():
    return db.client[settings.MONGODB_DB_NAME]