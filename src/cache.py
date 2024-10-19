import redis.asyncio as redis

from config import get_cache_settings

cache_settings = get_cache_settings()


def get_cache() -> redis.Redis:
    """Получение клиента Redis."""
    pool = redis.ConnectionPool().from_url(cache_settings.url)
    client = redis.Redis(connection_pool=pool)
    return client
