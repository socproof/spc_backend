# sim_post_cap_backend/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator, ValidationInfo
from typing import Optional, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "SimPostCap Backend API"
    API_V1_STR: str = "/api/v1"
    DEBUG_MODE: bool = True

    DB_USER: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_PORT: str = "5432"
    DB_NAME: str

    DB_DRIVER: str = "postgresql"
    DB_ASYNC_DRIVER_SUFFIX: str = "+asyncpg"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    ASYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        required_keys = {"DB_DRIVER", "DB_USER", "DB_PASSWORD", "DB_SERVER", "DB_PORT", "DB_NAME"}
        if not required_keys.issubset(info.data.keys()):
            raise ValueError(f"Missing one or more required fields for DB connection: {required_keys - info.data.keys()}")

        return str(PostgresDsn.build(
            scheme=info.data.get("DB_DRIVER"),
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_SERVER"),
            port=int(info.data.get("DB_PORT")),
            path=info.data.get("DB_NAME"),
        ))

    @field_validator("ASYNC_SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_async_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        required_keys = {"DB_DRIVER", "DB_ASYNC_DRIVER_SUFFIX", "DB_USER", "DB_PASSWORD", "DB_SERVER", "DB_PORT", "DB_NAME"}
        if not required_keys.issubset(info.data.keys()):
            raise ValueError(f"Missing one or more required fields for async DB connection: {required_keys - info.data.keys()}")

        return str(PostgresDsn.build(
            scheme=f"{info.data.get('DB_DRIVER')}{info.data.get('DB_ASYNC_DRIVER_SUFFIX')}",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_SERVER"),
            port=int(info.data.get("DB_PORT")),
            path=info.data.get("DB_NAME"),
        ))

settings = Settings()