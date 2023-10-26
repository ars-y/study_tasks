from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow'
    )


settings = Config()
