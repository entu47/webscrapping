from pydantic_settings import BaseSettings
import os


class BaseConfig(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    cache_url: str
    app_id: str
    app_token: str

    class Config:
        env_file = None


class DevelopmentConfig(BaseConfig):
    debug_mode: bool = True

    class Config(BaseConfig.Config):
        env_file = ".env"


class ProductionConfig(BaseConfig):
    debug_mode: bool = False


env = os.getenv("ENV", "development")
if env == "production":
    settings = ProductionConfig()
else:
    from dotenv import load_dotenv
    load_dotenv()
    settings = DevelopmentConfig()
