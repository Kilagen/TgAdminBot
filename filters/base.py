from typing import Union
from aiogram import filters, types


class SentByAdminFilter(filters.BaseFilter):
    """
    Checks if the message sender is a chat admin
    """
    async def __call__(self, message: types.Message) -> bool:
        admins = await message.chat.get_administrators()
        admin_ids = (admin.user.id for admin in admins)
        return message.from_user.id in admin_ids


class ChatTypeFilter(filters.BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class SentInSuperGroupFilter(ChatTypeFilter):
    def __init__(self):
        super().__init__(chat_type="supergroup")