from fastapi import APIRouter

from config import get_auth_settings
from dependencies.auth import AuthUser
from schemas.users import UserInfoSchema

auth_settings = get_auth_settings()

auth_api_router = APIRouter(
    prefix='/auth',
)


@auth_api_router.put(
    '/',
    response_model=UserInfoSchema,
    status_code=200,
)
async def auth(user: AuthUser) -> None:
    """Авторизация пользователя.

    :param user: Пользователь, выполнивший авторизацию.
    """
    return user
