import logging
from aiogram import Router, types
from aiogram.filters import BaseFilter

from config import admin_config
from methods import chat


class GeneralAdminFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: types.Message) -> bool:
        logging.debug(f"Check User {message.from_user} is admin")
        return (
                message.chat.id == message.from_user.id
                and
                message.from_user.id in admin_config.general_admins
        )


dm_router = Router()


@dm_router.message(GeneralAdminFilter())
async def handle_admin_message(message: types.Message):
    logging.info("Received admin message")
    command, *data = message.text.splitlines()
    data = '\n'.join(data)
    if command.startswith('addChat'):
        response = await chat.add_chat(data)
    elif command.startswith('getChat'):
        response = await chat.get_chat(data)
    elif command.startswith('removeChat'):
        response = await chat.remove_chat(data)
    elif command.startswith('updateChat'):
        response = await chat.update_chat(data)
    else:
        response = "Unknown command"
    await message.reply(response)
