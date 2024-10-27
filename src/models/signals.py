from tortoise.signals import post_save

from config import get_settings
from models import User
from tasks.process_recommendations import process_users_info

settings = get_settings()


@post_save(User)
async def process_recommendation(*args, created: bool, **kwargs) -> None:
    """Запуск процесса формирования рекомендаций."""
    if created:
        await process_users_info.kiq()
