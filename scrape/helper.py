from pymongo import UpdateMany
from pymongo.errors import BulkWriteError
from app import mongo_db_client
import logging
from common.db_manager import BaseCacheManager
from common.db_manager import BaseDBManager

logger = logging.getLogger(__name__)


class RedisCacheManager(BaseCacheManager):
    def __init__(self, client):
        super().__init__(client)
        self.client = client

    def create_entry(self, payload):
        key = f"product|{payload['id']}"
        value = payload['price']
        entry = {key: value}
        return entry

    def get_entry(self, **kwargs):
        key = kwargs['key']
        return self.client.get(key)

    def set_entry(self, **kwargs):
        key = kwargs['key']
        value = kwargs['value']
        raise self.client.set(key, value)


class MongoDBManager(BaseDBManager):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.db_client = mongo_db_client.scrape
        self.collection = self.db_client.products

    def create_entry(self, payload) -> object:
        pass

    def find_entry(self, **kwargs) -> str:
        pass

    def find_entries(self, **kwargs) -> str:
        pass

    async def bulk_update_entries(self, **kwargs) -> str:
        entries = kwargs['entries']
        bulk_operations = list()
        for entry in entries:
            query = entry["filter"]
            update = {"$set": entry["update"]}

            bulk_operation = UpdateMany(query, update, upsert=True)
            bulk_operations.append(bulk_operation)

        try:
            result = await self.collection.bulk_write(bulk_operations)
        except BulkWriteError as bwe:
            logger.exception(bwe)


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

