from tortoise import fields
from tortoise.validators import MinLengthValidator

from models.base import BaseModel


class User(BaseModel):
    """Пользователь."""

    username = fields.CharField(
        max_length=16,
        unique=True,
        null=False,
        validators=[MinLengthValidator(3)],
    )
    telegram_link = fields.CharField(
        max_length=128,
        unique=True,
        null=False,
        validators=[MinLengthValidator(3)],
    )
    avatar_url = fields.CharField(
        max_length=1024,
        null=True
    )
    name = fields.CharField(
        max_length=16,
        null=False,
        validators=[MinLengthValidator(1)],
    )
    surname = fields.CharField(
        max_length=32,
        null=True,
    )
    password = fields.CharField(
        max_length=128,
        null=True,
    )
    interests = fields.JSONField(
        null=False,
    )
