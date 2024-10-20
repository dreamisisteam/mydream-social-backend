from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Базовый класс конфигурации приложения."""

    SRC_DIR: Path = Path(__file__).parent.parent
    BASE_DIR: Path = SRC_DIR.parent
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


class CacheSettings(BaseAppSettings):
    """Конфигурация подключения к Redis."""

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str = ''
    REDIS_USER: str = ''
    REDIS_PASSWORD: str = ''

    @computed_field
    @property
    def url(self) -> str:
        return f'redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@' \
               f'{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'


class DbSettings(BaseAppSettings):
    """Конфигурация подключения к базе данных."""

    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    modules: dict[str, list[str]] = {'models': ['models.models']}

    @computed_field
    @property
    def url(self) -> str:
        return f'asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


class AuthSettings(BaseAppSettings):
    """Конфигурация приложения в части авторизация."""

    SALT: str
    SECRET_KEY: str
    TOKEN_EXPIRY: int = 15
    ALGORITHM: str = 'HS256'
    AUTH_COOKIE_KEY: str = 'auth'


class RecommendationsSettings(BaseAppSettings):
    """Конфигурация работы алгоритма рекомендаций."""

    k: int = 5
    steps: int = 500
    alpha: float = 1e-4
    reg_param: float = 0.8


class Settings(BaseAppSettings):
    """Конфигурация приложения."""

    BASE_API_PREFIX: str = '/api'
    INTERESTS_KEYS: list[str] = [
        'travel',
        'music',
        'sport',
        'films',
        'student_community',
        'social_interaction',
        'entertainment',
        'technologies',
        'science',
        'ai',
    ]

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    PAGE_SIZE: int = 10


@lru_cache
def get_cache_settings() -> CacheSettings:
    """Получение конфигурации подключения к Redis."""
    return CacheSettings()


cache_settings: CacheSettings = get_cache_settings()


@lru_cache
def get_db_settings() -> DbSettings:
    """Получение конфигурации подключения к базе данных."""
    return DbSettings()


db_settings: DbSettings = get_db_settings()


@lru_cache
def get_auth_settings() -> AuthSettings:
    """Получение настроек авторизации."""
    return AuthSettings()


auth_settings: AuthSettings = get_auth_settings()


@lru_cache
def get_recommendations_settings() -> RecommendationsSettings:
    """Получение настроек рекомендаций."""
    return RecommendationsSettings()


recommendations_settings: RecommendationsSettings = get_recommendations_settings()


@lru_cache
def get_settings() -> Settings:
    """Получение конфигурации приложения."""
    return Settings()


settings: Settings = get_settings()
