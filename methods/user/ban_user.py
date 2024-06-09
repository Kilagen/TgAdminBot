import asyncio
import logging
import datetime

from aiogram.types import Message, ChatPermissions, LinkPreviewOptions
from aiogram.utils.formatting import TextLink

from config import chats_config
from util.functions import delay


async def ban_user(message: Message, notify_about_ban: bool = False) -> None:
    try:
        forward_chat_id = next(chat.redirect_to for chat in chats_config.chats if chat.id == message.chat.id)

        forward = await message.forward(forward_chat_id)
        forward_url = forward.get_url()
    except StopIteration:
        logging.error("Chat config not found")
        return

    await message.delete()

    bad_user = message.from_user
    ban_until = message.date + datetime.timedelta(seconds=15)
    chat = message.chat
    permissions = ChatPermissions(can_send_messages=False)
    if chat.type == 'supergroup':
        result = await chat.restrict(bad_user.id, permissions=permissions, until_date=ban_until)
    else:
        result = await chat.ban(bad_user.id, until_date=ban_until)
    if result and notify_about_ban:
        answer = await message.answer(
            f"{message.from_user.mention_html()} restricted. "
            f"{TextLink("Reason", url=forward_url).as_html()}",
            parse_model='html',
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )
        task = asyncio.create_task(delay(answer.delete(), 180))
