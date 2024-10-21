from fastapi import FastAPI
from scrape.router import scrape_router
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
app = FastAPI()
app.include_router(scrape_router)

mongo_db_client: AsyncIOMotorClient = None


@app.on_event("startup")
async def startup_db():
    global mongo_db_client
    mongo_db_client = AsyncIOMotorClient("mongodb://localhost:27017")


@app.on_event("shutdown")
async def shutdown_db():
    global mongo_db_client
    mongo_db_client.close()
