from functools import cached_property
import hashlib
import jwt

from config import get_auth_settings

auth_settings = get_auth_settings()


def generate_password_hash(raw_password: str) -> str:
    """Генерация хэша пароля.

    :param raw_password: Сырой пароль.
    :return: Захэшированный пароль.
    """
    return hashlib.md5(
        (raw_password + auth_settings.SECRET_KEY).encode('utf-8')
    ).hexdigest()


class Token:
    """Логика для токена авторизации."""

    token: str

    def __init__(self, token: str):
        self.token = token

    @classmethod
    def generate_token(cls, username: str):
        """Генерация токена.

        :param username: Имя пользователя.
        :return: Авторизационный токен.
        """
        token_data = {'exp': auth_settings.TOKEN_EXPIRY, 'sub': username}
        return jwt.encode(token_data, auth_settings.SECRET_KEY, auth_settings.ALGORITHM)

    @cached_property
    def body(self):
        """Получение наполнения токена."""
        return jwt.decode(self.token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])

    @property
    def username(self):
        """Получение имени пользователя обладателя токена."""
        return self.body['sub']
