from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from config import get_cache_settings

cache_settings = get_cache_settings()

taskiq_broker = ListQueueBroker(
    url=cache_settings.url,
)


class TaskIQBroker:
    """Брокер TaskIQ."""

    broker = taskiq_broker

    async def __aenter__(self):
        """Действия при старте воркера."""
        if not self.broker.is_worker_process:
            await self.broker.startup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Действия при завершении работы приложения."""
        if not self.broker.is_worker_process:
            await self.broker.shutdown()


init_broker = TaskIQBroker
