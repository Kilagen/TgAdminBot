from aiogram import types, filters


class IsAdmin(filters.BaseFilter):
    """
    Checks if the message sender is a chat admin
    """
    async def __call__(self, message: types.Message) -> bool:
        admins = await message.chat.get_administrators()
        return message.from_user in admins


class HasSpamBan(filters.BaseFilter):
    """
    Checks if user has ban for spam in any moderated chat
    NOT IMPLEMENTED
    """
    async def __call__(self, message: types.Message) -> bool:
        raise NotImplementedError


class HasBan(filters.BaseFilter):
    """
    Checks if user has ban in any moderated chat
    NOT IMPLEMENTED
    """
    async def __call__(self, message: types.Message) -> bool:
        raise NotImplementedError


__all__ = ["IsAdmin"]
