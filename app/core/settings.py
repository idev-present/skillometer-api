from pydantic import computed_field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    # API config
    DOMAIN: str = "localhost"
    API_PREFIX: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str

    # Database
    DATABASE_SERVER: str
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_DBNAME: str = ""

    @computed_field
    @property
    def DATABASE_DSN(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_DBNAME
        )


settings = Settings()  # type: ignore
