from aiogram import types, filters, Router
from util.filters import IsAdmin
from util import Commander
from config import FORWARD_SPAM_CHAT_ID

ban_router = Router()


ban_commands = [
    types.BotCommand(command="ban", description="Ban"),
    types.BotCommand(command="banspam", description="Ban For Spam")
]

ban_commander = Commander(commands=ban_commands, router=ban_router)


@ban_router.message(filters.Command("ban"), IsAdmin())
async def ban_user(msg: types.Message):
    chat = msg.chat
    ban_message = msg.reply_to_message
    user_to_be_banned = ban_message.from_user
    ban_chat_member = chat.ban(user_to_be_banned.id, revoke_messages=True)
    await msg.delete()
    await ban_chat_member


@ban_router.message(filters.Command("banspam"), IsAdmin())
async def ban_user_for_spam(msg: types.Message):
    ban_message = msg.reply_to_message
    await ban_message.forward(FORWARD_SPAM_CHAT_ID)
    await ban_user(msg)
