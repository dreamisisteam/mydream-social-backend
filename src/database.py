from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from tortoise.contrib.fastapi import RegisterTortoise

from config import get_db_settings

if TYPE_CHECKING:
    from fastapi import FastAPI

db_settings = get_db_settings()

TORTOISE_ORM = {
    'connections': {'default': db_settings.url},
    'apps': {
        'mydream_social': {
            'models': [
                'models.models',
                'models.signals',
                'aerich.models',
            ],
            'default_connection': 'default',
        },
    },
}


@asynccontextmanager
async def init_db(app: 'FastAPI'):
    """Инициализация подключения к БД."""
    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM,
    ):
        yield
