import redis
from motor.motor_asyncio import AsyncIOMotorClient
from config import current_config
from config.settings import settings


async def connect_to_db():
    current_config.mongo_db_client = AsyncIOMotorClient(settings.database_url)
    current_config.redis_db_client = redis.Redis.from_url(settings.cache_url)
    print("Database connection established")


async def close_db_connection():
    if current_config.mongo_db_client:
        current_config.mongo_db_client.close()
        print("Database connection closed")
    if current_config.redis_db_client:
        current_config.redis_db_client.close()
        print("Database connection closed")
