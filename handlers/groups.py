import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from spam_detection import LogRegDetector

group_router = Router()
detector = LogRegDetector()


@group_router.message()
async def message_handler(message: types.Message, state: FSMContext) -> None:
    is_spam = await detector(message.text)
    if is_spam:
        await message.reply(f"Message\n{message.text}\nfrom {message.from_user.full_name} looks like spam")
        await message.delete()
        bad_user = message.from_user
        ban_until = message.date + datetime.timedelta(seconds=30)
        chat = message.chat
        permissions = types.chat_permissions.ChatPermissions(can_send_messages=False)
        await chat.restrict(bad_user.id, permissions=permissions, until_date=ban_until)
