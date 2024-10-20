from httpx import AsyncClient
from bs4 import BeautifulSoup


async def get_avatar_url(telegram_link: str) -> str | None:
    """Получение URL аватара из telegram.

    :param telegram_link: URL Telegram.
    :return: URL аватара пользователя.
    """
    async with AsyncClient() as client:
        response = await client.get(telegram_link)
        html = str(response.content)

        soup = BeautifulSoup(html)
        image_meta = soup.find('meta', property='og:image')

        if image_meta:
            return image_meta['content']
