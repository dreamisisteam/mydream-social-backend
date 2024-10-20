import json

import redis.asyncio as redis
import numpy as np

from config import get_recommendations_settings
from broker import taskiq_broker
from processors.matrix_factorization import RecommendationsProcessor

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
