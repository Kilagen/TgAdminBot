from aiogram import F, Router, types
from filters import IsSentByAdmin
from methods.user import ban_user

admin_router = Router()


@admin_router.message(F.text.lower() in ("бан", "ban", "/ban", "/бан"), IsSentByAdmin())
async def handle_ban(message: types.Message):
    try:
        if message.reply_to_message is not None:
            await ban_user(message.reply_to_message, notify_about_ban=False)
    finally:
        await message.delete()
