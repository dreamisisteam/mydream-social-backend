from pydantic import BaseModel, field_validator

from config import get_settings

settings = get_settings()


class RegisterUserSchema(BaseModel):
    """Схема для регистрации пользователя."""

    username: str
    telegram_link: str
    name: str
    surname: str | None
    password: str
    interests: dict[str, int]

    @field_validator('interests')
    def validate_interests(cls, value: dict[str, int]) -> dict[str, int]:
        """Валидация поля интересов."""
        if set(value.keys()) != set(settings.INTERESTS_KEYS):
            raise ValueError('Не все интересы указаны!')

        return value


class GetUserSchema(BaseModel):
    """Схема для репрезентации пользователя."""

    username: str
    name: str
    surname: str | None
    avatar_url: str | None
    telegram_link: str
    interests: dict[str, int]


class UserInfoSchema(BaseModel):
    """Схема для отображения пользователя."""

    username: str
    name: str
    surname: str
    avatar_url: str | None


class RecommendationUserSchema(UserInfoSchema):
    """Схема для репрезентации пользователя для рекомендации."""

    rating: str
