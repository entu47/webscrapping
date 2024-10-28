from fastapi import FastAPI
from redis import Redis

from scrape.router import scrape_router
from motor.motor_asyncio import AsyncIOMotorClient
import redis

app = FastAPI()
app.include_router(scrape_router)

mongo_db_client: AsyncIOMotorClient = None
redis_db_client: Redis = None


@app.on_event("startup")
async def startup_db():
    global mongo_db_client
    mongo_db_client = AsyncIOMotorClient("mongodb://localhost:27017")
    redis_db_client = redis.Redis.from_url('redis://localhost:6379')


@app.on_event("shutdown")
async def shutdown_db():
    global mongo_db_client
    global redis_db_client
    mongo_db_client.close()
    redis_db_client.close()
