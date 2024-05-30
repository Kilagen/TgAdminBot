import datetime

from aiogram.filters import BaseFilter
from aiogram import Router, types
from aiogram.utils.formatting import TextMention, TextLink
from config import config

from spam_detection import LogRegDetector, MixedAbcDetector

group_router = Router()
detector = MixedAbcDetector()
detector.set_next(LogRegDetector())


class ChatIsWatchedFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return any(message.chat.id == chat.id for chat in config.chats)


@group_router.message(ChatIsWatchedFilter())
async def message_handler(message: types.Message) -> None:
    print(message)
    forward_chat_id = next(chat.redirect_to for chat in config.chats if chat.id == message.chat.id)
    is_spam = await detector(message.text)
    if not is_spam:
        return

    forward = await message.forward(forward_chat_id)
    forward_url = forward.get_url()
    await message.delete()
    await message.answer(
        f"{TextMention(message.from_user).as_html()} restricted. {TextLink("Reason", url=forward_url).as_html()}"
    )

    bad_user = message.from_user
    ban_until = message.date + datetime.timedelta(seconds=15)
    chat = message.chat
    permissions = types.chat_permissions.ChatPermissions(can_send_messages=False)
    await chat.restrict(bad_user.id, permissions=permissions, until_date=ban_until)
