from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
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

    def get_entry(self, **kwargs) -> str:
        pass

    def get_entries(self, **kwargs):
        keys = kwargs['keys']
        return self.client.mget(keys)

    def set_entry(self, **kwargs):
        entries = kwargs['entries']
        mapping = self.create_entry(entries)
        self.client.mset(mapping)


class MongoDBManager(BaseDBManager):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.db_client = client.scrape
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

    async def bulk_update_entries(self, **kwargs):
        entries = kwargs['entries']
        entries = self.transform_payload(entries)
        bulk_operations = list()
        for entry in entries:
            bulk_operation = UpdateOne({"id": entry["id"]}, {"$set": entry}, upsert=True)
            bulk_operations.append(bulk_operation)

        try:
            result = await self.collection.bulk_write(bulk_operations)
        except BulkWriteError as bwe:
            logger.exception(bwe)


class ScrapeStorage:
    def __init__(self, db_client, cache_client):
        self.db_manager = MongoDBManager(db_client)
        self.cache_manager = RedisCacheManager(cache_client)
        self.payload = []
        self.products_updated = 0

    def preprocess_data(self, payload):
        payload_dict = {product["id"]: product for product in payload}
        keys = list(payload_dict.keys())
        products_already_in_db = self.cache_manager.get_entries(keys=keys)
        products_already_in_db_dict = {keys[index]: products_already_in_db[index] for index in range(len(keys))}
        for product_id in products_already_in_db_dict:
            product_in_db = products_already_in_db_dict.get(product_id, None)
            if product_in_db is not None:
                if product_in_db['price'] == payload_dict[product_id]['price']:
                    payload_dict.pop(product_id)
                else:
                    self.products_updated += 1
        self.payload = payload_dict.values()

    async def trigger_storage_pipeline(self):
        self.cache_manager.set_entry(entries=self.payload)
        await self.db_manager.bulk_update_entries(entries=self.payload)
