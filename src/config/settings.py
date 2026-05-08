from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH : Path = Path(__file__).resolve().parent.parent.parent

    HOST: str = "localhost"
    PORT: int = 8080

    DEBUG: bool = True

    DB_USERNAME: str
    DB_NAME : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : int

    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore"

    )

    @property
    def async_postgresql_url(self):
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings():
    return Settings()
