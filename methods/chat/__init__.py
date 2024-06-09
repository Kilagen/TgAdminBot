import json
from config import chats_config
from base import ChatData
from dataclasses import asdict


async def add_chat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_data = ChatData(**chat_dict)

        # Check if the chat id already exists
        if any(chat.id == chat_data.id for chat in chats_config.chats):
            return "Chat with this ID already exists."

        chats_config.add_chat(chat_data)
        return "Chat added successfully."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error adding chat: {str(e)}"


async def remove_chat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_id = chat_dict['id']

        chats_config.remove_chat(chat_id)
        return "Chat not found."
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error removing chat: {str(e)}"


async def update_chat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_data = ChatData(**chat_dict)
        chats_config.update_chat(chat_data)
        return "Chat updated successfully."
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error updating chat: {str(e)}"


async def get_chat(data: str) -> str:
    try:
        chat_dict = json.loads(data)
        chat_id = chat_dict['id']
        return json.dumps(
            asdict(chats_config.get_chat(chat_id))
        )
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error retrieving chat: {str(e)}"
