from broker import taskiq_broker
from models import User
from utils.avatar import get_avatar_url


@taskiq_broker.task
async def update_users_avatars():
    """Обновление ссылок на пользовательские аватары."""
    updated_users = []
    async for user in User.filter():
        user: User
        user.avatar_url = await get_avatar_url(user.telegram_link)
        updated_users.append(user)

    await User.bulk_update(updated_users, fields=['avatar_url'])
