from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH : Path = Path(__file__).resolve().parent.parent.parent

    HOST: str = "localhost"
    PORT: int = 8080

    DEBUG: bool = True

    DB : str = "sqlite"

    DB_USERNAME: str | None = None
    DB_NAME : str | None = None
    DB_PASSWORD : str | None = None
    DB_HOST : str | None = None
    DB_PORT : int | None = None

    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:

        if self.DB == "sqlite":
            db_path = self.BASE_PATH / "sql_database.db"
            return f"sqlite+aiosqlite:///{db_path}"

        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings():
    return Settings()
