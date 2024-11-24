import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db_url: str = (
        f"postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}"
        f":{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    secret: str = "VERY_SECRET_SECRET"
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )


settings = Settings()
