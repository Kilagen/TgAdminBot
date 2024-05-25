import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from filters import SentByAdminFilter

admin_router = Router()


@admin_router.message(F.text.lower() == "бан", SentByAdminFilter())
async def handle_ban(message: types.Message, state: FSMContext):
    if message.reply_to_message is None:
        return
    await message.reply_to_message.reply("You're banned :(")
    bad_user = message.reply_to_message.from_user
    ban_until = message.date + datetime.timedelta(seconds=30)
    chat = message.chat
    permissions = types.chat_permissions.ChatPermissions(can_send_messages=False)
    await chat.restrict(bad_user.id, permissions=permissions, until_date=ban_until)
