import json

import redis.asyncio as redis
import numpy as np

from config import get_recommendations_settings, get_settings
from broker import taskiq_broker
from models import User
from processors.matrix_factorization import RecommendationsProcessor

settings = get_settings()
recommendation_settings = get_recommendations_settings()


@taskiq_broker.task
async def process_recommendations(users_interests_map: dict[int, list[int]]) -> None:
    """Расчет рекомендаций для пользователей.

    :param users_interests_map: Маппинг интересов пользователей.
    """
    user_id_position_map = {
        i: user_id
        for i, user_id in enumerate(users_interests_map)
    }

    user_interests_list = list(users_interests_map.values())
    user_interests_array = np.array(user_interests_list)

    processor = RecommendationsProcessor(
        user_interests_array,
        **recommendation_settings.model_dump(mode='python', include={'k', 'steps', 'alpha', 'reg_param', 'verbose'}),
    )
    stored_recommendations = processor.P

    async with redis.Redis(connection_pool=taskiq_broker.connection_pool) as cache_client:
        await cache_client.set('recommendations', json.dumps(stored_recommendations.tolist()))
        await cache_client.set('user_map', json.dumps(user_id_position_map))


@taskiq_broker.task
async def process_users_info() -> None:
    """Обработка пользовательской информации."""
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
