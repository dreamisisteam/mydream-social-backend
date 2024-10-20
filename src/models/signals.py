from tortoise.signals import post_save

from config import get_settings
from models import User
from tasks.process_recommendations import process_recommendations

settings = get_settings()


@post_save(User)
async def process_recommendation(*args, **kwargs) -> None:
    """Запуск процесса формирования рекомендаций."""
    users_interests: dict[int, dict[str, int]] = dict(
        await User.all().order_by('id').values_list('id', 'interests')
    )

    if len(users_interests) == 1:
        return

    interests_arrays_by_user_id_map: dict[int, list[int]] = {}

    for user_id, user_interest in users_interests.items():
        interests_arrays_by_user_id_map[user_id] = [
            user_interest.get(interest_key)
            for interest_key in settings.INTERESTS_KEYS
        ]

    await process_recommendations.kiq(interests_arrays_by_user_id_map)
