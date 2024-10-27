from tortoise.signals import post_save

from config import get_settings
from models import User
from tasks.process_recommendations import process_users_info

settings = get_settings()


@post_save(User)
async def process_recommendation(
    sender: type[User],
    instance: User,
    created: bool,
    *args,
    **kwargs,
) -> None:
    """Запуск процесса формирования рекомендаций."""
    if created:
        await process_users_info.kiq()
