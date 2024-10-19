from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    """Схема для авторизации пользователя."""

    username: str
    password: str


class UserInfoSchema(BaseModel):
    """Схема для отображения пользователя."""

    username: str
    name: str
    surname: str
