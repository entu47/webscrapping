from fastapi import APIRouter
from scrape.views import ScrapeView

scrape_router = APIRouter(prefix='/v1.0')

scrape_router.add_api_route("/scrape", methods=["POST"], endpoint=ScrapeView.post)
