import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from marshmallow import ValidationError

from config import current_config
from scrape.action import SrapeDataHunter
from scrape.serializer import ScrapeRequestSchema, FailureResponseSchema

logger = logging.getLogger(__name__)

authorized_clients = [(current_config.app_id, current_config.app_token)]


class ScrapeView:
    @classmethod
    async def post(cls, request: Request):
        response_data = {}
        request_body = await request.json()
        request_client_credentials = tuple(
            (request.headers.get("X-Application-ID"), request.headers.get("X-Application-Token")))
        if request_client_credentials not in authorized_clients:
            return JSONResponse({"success": False}, status_code=401)
        try:
            request_data = ScrapeRequestSchema().load(request_body)
            response = await SrapeDataHunter().scrape_contents(request_data['url'], request_data['limit'])
        except ValidationError as e:
            logger.error({"message": "ValidationError", "exception": e})
            response_data["success"] = False
            return JSONResponse(response_data, status_code=400)

        except Exception as e:
            logger.error({"Exception": e})
            response_data["success"] = False
            return JSONResponse({"success": False}, status_code=400)

        return JSONResponse({"success": True}, status_code=200)
