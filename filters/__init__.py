from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsSentByAdmin(BaseFilter):
    """
    Checks if the message sender is a chat admin
    """
    async def __call__(self, message: Message) -> bool:
        admins = await message.chat.get_administrators()
        admin_ids = [admin.user.id for admin in admins]
        return message.from_user.id in admin_ids
