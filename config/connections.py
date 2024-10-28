from config.settings import settings


class DockerConfig:
    mongo_url = settings.database_url
    redis_url = settings.cache_url
    app_id = settings.app_id
    app_token = settings.app_token
