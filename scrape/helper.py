from pymongo import UpdateMany
from pymongo.errors import BulkWriteError
from app import mongo_db_client
import logging
from common.db_manager import BaseCacheManager
from common.db_manager import BaseDBManager
from scrape.serializer import ScrapeDBItemSchema

logger = logging.getLogger(__name__)


class RedisCacheManager(BaseCacheManager):
    def __init__(self, client):
        super().__init__(client)
        self.client = client

    def create_entry(self, payload):
        transformed_payload = dict()
        for each_entry in payload:
            key = f"product|{each_entry['id']}"
            value = each_entry['price']
            transformed_payload.update({key: value})
        return transformed_payload

    def get_entries(self, **kwargs):
        keys = kwargs['keys']
        return self.client.mget(keys)

    def set_entry(self, **kwargs):
        entries = kwargs['entries']
        mapping = self.create_entry(entries)
        raise self.client.mset(mapping)


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

    def transform_payload(self, payload):
        transformed_payload = list()
        for each_item in payload:
            transformed_item = ScrapeDBItemSchema().load(each_item)
            transformed_payload.append(transformed_item)
        return transformed_payload


    async def bulk_update_entries(self, **kwargs) -> str:
        entries = kwargs['entries']
        entries = self.transform_payload(entries)
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


class ScrapeStorage:
    def __init__(self, db_client, cache_client):
        self.db_manager = MongoDBManager(db_client)
        self.cache_manager = RedisCacheManager(cache_client)

    async def preprocess_data(self, payload):
        pass

    async def trigger_storage_pipeline(self, payload):
        await self.db_manager.bulk_update_entries(entries=payload)
        self.cache_manager.set_entry(entries=payload)
