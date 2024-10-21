from fastapi import FastAPI
from serializer import ScrapeRequest
from simple_scrapping import scrape_contents

app = FastAPI()


@app.post("/scrape-url")
async def get_details(request_body: ScrapeRequest):
    request_url = request_body.url
    limit = request_body.limit
    scrape_contents(request_url, limit)
    return {"success": True}
