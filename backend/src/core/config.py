from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class SpimexSettings(BaseSettings):

    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'


settings = SpimexSettings()
