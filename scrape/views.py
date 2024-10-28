import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from marshmallow import ValidationError
from scrape.action import SrapeDataHunter
from scrape.serializer import ScrapeRequestSchema, FailureResponseSchema

logger = logging.getLogger(__name__)


class ScrapeView:
    @classmethod
    async def post(cls, request: Request):
        response_data = {}
        request_body = await request.json()
        try:
            request_data = ScrapeRequestSchema().load(request_body)
            response = await SrapeDataHunter().scrape_contents(request_data)
        except ValidationError as e:
            # Preparing failure response for validation error
            logger.info({"message": "ValidationError", "exception": e})
            response_data["success"] = False
            response_data = FailureResponseSchema().dump(response_data)
            return JSONResponse(response_data, status_code=400)

        return JSONResponse({"success": True}, status_code=200)
