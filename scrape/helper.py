from pymongo import UpdateMany
from pymongo.errors import BulkWriteError
from app import mongo_db_client
import logging
logger = logging.getLogger(__name__)


async def update_scrape_details_in_db(products):
    bulk_operations = []
    db_client = mongo_db_client.firebolt
    collection = db_client.products
    for entry in products:
        query = entry["filter"]
        update = {"$set": entry["update"]}

        bulk_operation = UpdateMany(query, update, upsert=True)
        bulk_operations.append(bulk_operation)

    try:
        result = await collection.bulk_write(bulk_operations)
    except BulkWriteError as bwe:
        logger.exception(bwe)
