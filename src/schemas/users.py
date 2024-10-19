from pydantic import BaseModel


class RegisterUserSchema(BaseModel):
    """Схема для регистрации пользователя."""

    username: str
    telegram_link: str
    name: str
    surname: str | None
    password: str
    interests: dict[str, int]


class GetUserSchema(BaseModel):
    """Схема для репрезентации пользователя."""

    username: str
    name: str
    surname: str | None
    telegram_link: str
    interests: dict[str, int]
