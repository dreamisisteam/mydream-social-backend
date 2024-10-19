from fastapi import APIRouter, Response

from config import get_auth_settings
from dependencies.auth import AuthUserToken
from schemas.auth import UserInfoSchema

auth_settings = get_auth_settings()

auth_api_router = APIRouter(
    prefix='/auth',
)


@auth_api_router.put(
    '/',
    response_model=UserInfoSchema,
    status_code=200,
)
async def auth(
    auth_info: AuthUserToken,
    response: Response,
) -> None:
    """Регистрация пользователя."""
    token, user = auth_info

    response.set_cookie(
        key=auth_settings.AUTH_COOKIE_KEY,
        value=token,
        httponly=True,
    )

    return user
