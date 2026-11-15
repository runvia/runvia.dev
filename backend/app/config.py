from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True)
    database_url: str
    database_echo: bool = False
    secret_key: SecretStr = Field(min_length=32)
    session_secret_key: SecretStr = Field(min_length=32)
    admin_username: str | None = None
    admin_password: SecretStr | None = None


@lru_cache
def get_settings():
    return Settings()
