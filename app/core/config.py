import secrets
import tomllib

import toml
from pydantic import computed_field, PostgresDsn, AnyHttpUrl, field_validator, AnyUrl, BeforeValidator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional, Annotated

from app.utils.api_utils import parse_cors


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    # API config
    APP: Optional[str] = None
    VERSION: Optional[str] = None
    DESCRIPTION: Optional[str] = None
    DOMAIN: str = "localhost"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_DIR: str = "runtime/logs"
    CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ]

    # Database
    DATABASE_SERVER: str
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_DBNAME: str = ""

    # IAM
    IAM_HOSTNAME: AnyHttpUrl
    IAM_CLIENT_ID: str
    IAM_CLIENT_SECRET: str
    IAM_REDIRECT_URI: AnyHttpUrl
    IAM_ORGANIZATION_ID: str
    IAM_APPLICATION_ID: str

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

    @field_validator("APP", mode="before")
    @classmethod
    def assert_app_name(cls, v):
        if isinstance(v, str):
            return v
        config = toml.load('pyproject.toml')
        return config['tool']['poetry']['name']

    @field_validator("VERSION", mode="before")
    @classmethod
    def assert_version(cls, v):
        if isinstance(v, str):
            return v
        config = toml.load('pyproject.toml')
        return config['tool']['poetry']['version']

    @field_validator("DESCRIPTION", mode="before")
    @classmethod
    def assert_description(cls, v):
        if isinstance(v, str):
            return v
        config = toml.load('pyproject.toml')
        return config['tool']['poetry']['description']


settings = Settings()  # type: ignore
