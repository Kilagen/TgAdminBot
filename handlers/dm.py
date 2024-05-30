import json
from dataclasses import asdict

from aiogram.methods.send_message import SendMessage
from aiogram import F, Router, types
from aiogram.filters import BaseFilter

from config import config, ChatData, config_to_file


class GeneralAdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return (
                message.from_user.id in config.general_admins
                and
                message.chat.id == message.from_user.id
        )


dm_router = Router()


async def addChat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_data = ChatData(**chat_dict)

        # Check if the chat id already exists
        if any(chat.id == chat_data.id for chat in config.chats):
            return "Chat with this ID already exists."

        config.chats.append(chat_data)
        config_to_file(config)
        return "Chat added successfully."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error adding chat: {str(e)}"


async def removeChat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_id = chat_dict['id']

        for chat in config.chats:
            if chat.id == chat_id:
                config.chats.remove(chat)
                config_to_file(config)
                return "Chat removed successfully."

        return "Chat not found."
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error removing chat: {str(e)}"


async def updateChat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_data = ChatData(**chat_dict)

        for idx, chat in enumerate(config.chats):
            if chat.id == chat_data.id:
                config.chats[idx] = chat_data
                config_to_file(config)
                return "Chat updated successfully."

        return "Chat not found."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error updating chat: {str(e)}"


async def getChat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_id = chat_dict['id']

        for chat in config.chats:
            if chat.id == chat_id:
                return json.dumps(asdict(chat))

        return "Chat not found."
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error retrieving chat: {str(e)}"


@dm_router.message(GeneralAdminFilter())
async def handleAdminMessage(message: types.Message):
    command, *data = message.text.splitlines()
    data = '\n'.join(data)
    if command.startswith('addChat'):
        response = await addChat(data)
    elif command.startswith('getChat'):
        response = await getChat(data)
    elif command.startswith('removeChat'):
        response = await removeChat(data)
    elif command.startswith('updateChat'):
        response = await updateChat(data)
    else:
        response = "Unknown command"
    await message.reply(response)
