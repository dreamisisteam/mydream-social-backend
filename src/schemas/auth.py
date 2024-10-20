from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    """Схема для авторизации пользователя."""

    username: str
    password: str
