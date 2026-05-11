import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импортируем твои настройки и метаданные
from src.models.base import BaseModel
from src.config.settings import get_settings

# Инициализируем настройки
settings = get_settings()

# Объект конфигурации Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные моделей для автогенерации
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    # Для оффлайн режима SQLAlchemy просит чистый sqlite:// драйвер
    url = settings.database_url.replace("sqlite+aiosqlite", "sqlite")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True  # Важно для SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Синхронный запуск миграций внутри асинхронного соединения."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True  # Позволяет пересоздавать таблицы в SQLite (Drop/Alter)
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Создание асинхронного движка и запуск миграций."""
    configuration = config.get_section(config.config_ini_section) or {}
    # Подставляем асинхронный URL напрямую
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Переходим в синхронный контекст для выполнения миграций
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
