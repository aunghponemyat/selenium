from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    target_url: str = ""
    chat_name: str = ""
    chat_id: str = ""
    message: str = ""
    pin: str = ""
    username: str = ""
    password: str = ""


@lru_cache
def get_settings() -> Settings:
    settings = Settings(_env_file=".env")
    return settings
