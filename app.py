from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import connect_to_db, close_db_connection
from scrape.router import scrape_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    print("Database connection established")

    yield

    await close_db_connection()
    print("Database connection closed")

app = FastAPI(lifespan=lifespan)
app.include_router(scrape_router)

