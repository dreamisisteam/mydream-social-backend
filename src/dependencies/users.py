from typing import Annotated

from fastapi import Depends

from models import User
from schemas.users import RegisterUserSchema

from utils.auth import generate_password_hash
from utils.avatar import get_avatar_url


async def register_user_info(
    user_info: RegisterUserSchema,
) -> User:
    """Данные для регистрации пользователя."""
    user = User(**user_info.model_dump(mode='python'))
    user.password = generate_password_hash(user.password)
    user.avatar_url = await get_avatar_url(user.telegram_link)
    return user


RegisterUser = Annotated[User, Depends(register_user_info)]
