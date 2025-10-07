from typing import Annotated
from pathlib import Path
from annotated_types import Le


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    BaseModel,
    computed_field,
    PostgresDsn,
    NonNegativeInt,
    PositiveInt,
    HttpUrl,
)


BASE_DIR = Path(__file__).resolve().parent


class Database(BaseModel):
    host: str = "localhost"
    port: Annotated[NonNegativeInt, Le(le=65535)] = 5432
    name: str = "wallet"
    username: str = "admin"
    password: str = "admin"
    isolation_level: str = "SERIALIZABLE"
    pool_size: PositiveInt = 10
    max_overflow: PositiveInt = 10
    ssl: str = "disable"  # allow prefer require verify-ca verify-full

    @computed_field
    def postgre_connection_string(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    test_mode: bool = False
    db: Database = Database()
    test_db: Database = Database()
    base_url: HttpUrl = "http://localhost"
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="WALLET__",
    )


settings = Settings()
