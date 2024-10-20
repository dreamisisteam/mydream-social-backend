from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError, ValidationError

from models import User
from dependencies.users import RegisterUser
from schemas.users import GetUserSchema

users_api_router = APIRouter(
    prefix='/users',
)


@users_api_router.post(
    '/register/',
    response_model=None,
    status_code=204,
)
async def register(register_user: RegisterUser) -> None:
    """Регистрация пользователя.

    :param register_user: Информация о регистрируемом пользователе.
    :return: 204
    """
    try:
        await register_user.save()
    except (IntegrityError, ValidationError):
        raise HTTPException(status_code=400)


@users_api_router.get(
    '/{username}',
    response_model=GetUserSchema,
)
async def get_user(username: str) -> User:
    """Получение информации о пользователе

    :param username:
    :return: 200, GetUserSchema
    """
    user = await User.get_or_none(username=username)

    if not user:
        raise HTTPException(status_code=404)

    return user
