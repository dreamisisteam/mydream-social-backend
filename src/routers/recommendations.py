import json

import numpy as np
import redis.asyncio as redis
from fastapi import APIRouter, Request

from config import get_settings
from models import User
from dependencies.auth import RequestUser
from schemas.users import UserInfoSchema
from processors.matrix_factorization import RecommendationsProcessor

settings = get_settings()

recommendations_api_router = APIRouter(
    prefix='/recommendations',
)


@recommendations_api_router.get(
    '',
    response_model=list[UserInfoSchema],
)
async def get_recommendations(
        request: Request,
        user: RequestUser,
):
    """Получение рекомендаций для пользователя.

    :param request: Запрос.
    :param user: Пользователь, отправивший запрос.
    """
    cache_client: redis.Redis = request.app.state.cache

    recommendations_source: list[list[float]] = json.loads(await cache_client.get('recommendations'))
    user_id_map: dict[str, int] = json.loads(await cache_client.get('user_map'))

    recommendation_user_id = int(next(i for i in user_id_map if user_id_map[i] == user.id))

    recommendations_array = np.array(recommendations_source)
    recommendation_users_info: list[tuple[int, float]] = RecommendationsProcessor.predict(
        recommendations_array,
        user_id=recommendation_user_id,
        top_n=settings.PAGE_SIZE,
    )

    response_user_ids = [
        user_id_map[str(recommendation_user_info[0])]
        for recommendation_user_info in recommendation_users_info
        if str(recommendation_user_info[0]) in user_id_map
    ]
    return await User.filter(id__in=response_user_ids).order_by('-id').all()
