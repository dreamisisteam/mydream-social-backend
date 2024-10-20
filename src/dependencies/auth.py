import datetime
from typing import Annotated, TypeAlias

from fastapi import Request, Response, Depends, HTTPException

import models
from config import get_auth_settings
from models import User
from schemas.auth import UserAuthSchema
from utils.auth import generate_password_hash, Token

auth_settings: TypeAlias = get_auth_settings()


async def authenticate_user(
        response: Response,
        auth_info: UserAuthSchema,
) -> User:
    """Авторизация пользователя.

    :param response: Ответ на запрос.
    :param auth_info: Данные для авторизации пользователя.
    :raises HTTPException: Некорректные учетные данные.
    :return: Токен авторизации, пользователь
    """
    user = await User.get_or_none(
        username=auth_info.username,
        password=generate_password_hash(auth_info.password),
    )

    if not user:
        raise HTTPException(status_code=401, detail='Некорректные учетные данные.')

    auth_token = Token.generate_token(user.username)
    expiry = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=auth_settings.TOKEN_EXPIRY)
    response.set_cookie(
        key=auth_settings.AUTH_COOKIE_KEY,
        value=auth_token,
        expires=expiry,
        httponly=True,
    )

    return user


AuthUser = Annotated[User, Depends(authenticate_user)]


async def get_request_user(request: Request) -> User:
    """Получение пользователя.

    :param request: Запрос.
    :raises HTTPException: Авторизация не выполнена.
    :return: Пользователь.
    """
    auth_token = request.cookies.get(auth_settings.AUTH_COOKIE_KEY)
    if not auth_token:
        raise HTTPException(status_code=401, detail='Авторизация не выполнена.')

    # try:
    username = Token(auth_token).username
    # except Exception:
    #     raise HTTPException(status_code=401, detail='Некорректные авторизационные данные.')

    user = await models.User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=401, detail='Некорректные авторизационные данные.')

    return user


RequestUser = Annotated[User, Depends(get_request_user)]
