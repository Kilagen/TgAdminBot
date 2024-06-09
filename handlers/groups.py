import logging

from aiogram.filters import BaseFilter
from aiogram import Router, types
from config import chats_config

from spam_detection import LogRegDetector, MixedAbcDetector
from methods.user import ban_user

group_router = Router()
detector = MixedAbcDetector()
detector.set_next(LogRegDetector())


class ChatIsWatchedFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: types.Message) -> bool:
        logging.info(f"Check Chat {message.chat.id} Is Watched")
        return any(message.chat.id == chat.id for chat in chats_config.chats)


@group_router.message(ChatIsWatchedFilter())
async def message_handler(message: types.Message) -> None:
    logging.info("Received chat message")
    is_spam = detector(message.text)
    if is_spam:
        await ban_user(message, notify_about_ban=True)

