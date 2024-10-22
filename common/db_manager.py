from abc import ABC, abstractmethod


class BaseCacheManager(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def create_entry(self, payload) -> object:
        raise NotImplementedError

    @abstractmethod
    def get_entry(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_entry(self, **kwargs) -> str:
        raise NotImplementedError


class BaseDBManager(ABC):
    def __init__(self, client):
        self.db_client = client

    @abstractmethod
    async def create_entry(self, payload) -> object:
        raise NotImplementedError

    @abstractmethod
    async def find_entry(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    async def find_entries(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    async def bulk_update_entries(self, **kwargs) -> str:
        raise NotImplementedError
