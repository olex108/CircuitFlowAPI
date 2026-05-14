from taskiq_aio_pika import AioPikaBroker

from src.config.settings import get_settings

settings = get_settings()

broker = AioPikaBroker(
    url=settings.rmq_url,
)
