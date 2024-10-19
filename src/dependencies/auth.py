from typing import Annotated, TypeAlias

from fastapi import Depends, HTTPException

from models import User
from schemas.auth import UserAuthSchema

from utils.auth import generate_password_hash, Token

AuthToken: TypeAlias = str
AuthInfo: TypeAlias = tuple[AuthToken, User]

async def authenticate_user(
    auth_info: UserAuthSchema,
) -> AuthInfo:
    """Данные для регистрации пользователя.

    :param auth_info:
    :raises HTTPException: Некорректные учетные данные.
    :return:
    """
    user = await User.get_or_none(
        username=auth_info.username,
        password=generate_password_hash(auth_info.password),
    )

    if not user:
        raise HTTPException(status_code=401, detail="Некорректные учетные данные.")

    auth_token = Token.generate_token(user.username)
    return auth_token, user


AuthUserToken = Annotated[AuthInfo, Depends(authenticate_user)]
