from typing import Annotated

from fastapi import Depends

from models import User
from schemas.users import RegisterUserSchema

from utils.auth import generate_password_hash


def register_user_info(
    user_info: RegisterUserSchema,
) -> User:
    """Данные для регистрации пользователя."""
    user = User(**user_info.model_dump(mode='python'))
    user.password = generate_password_hash(user.password)
    return user


RegisterUser = Annotated[User, Depends(register_user_info)]
