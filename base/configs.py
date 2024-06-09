import json
import typing as tp

from dataclasses import dataclass, asdict


@dataclass
class ChatData:
    id: int
    redirect_to: int
    admins: tp.List[int]


@dataclass
class ChatConfig:
    chats: tp.List[ChatData]

    @staticmethod
    def load(path='chats_config.json') -> 'ChatConfig':
        config_data = json.load(open(path, 'r'))
        chats = config_data['chats']
        config = ChatConfig([])
        for chat in chats:
            config.chats.append(ChatData(chat['id'], chat['redirect_to'], chat['admins']))
        return config

    def dump(self, path='chats_config.json') -> None:
        json.dump(asdict(self), open(path, 'w'))

    def add_chat(self, chat: ChatData) -> 'ChatConfig':
        self.chats.append(chat)
        self.dump()
        return self

    def update_chat(self, new_chat: ChatData) -> 'ChatConfig':
        try:
            old_chat = next(chat for chat in self.chats if chat.id == new_chat.id)
        except StopIteration:
            raise KeyError("Chat with id {} not found".format(new_chat.id))
        old_chat.admins = new_chat.admins
        old_chat.redirect_to = new_chat.redirect_to

        self.dump()
        return self

    def remove_chat(self, chat_id: int) -> 'ChatConfig':
        try:
            chat = next(chat for chat in self.chats if chat.id == chat_id)
        except StopIteration:
            raise KeyError("Chat with id {} not found".format(chat_id))
        self.chats = [chat for chat in self.chats if chat.id != chat_id]

        self.dump()
        return self

    def get_chat(self, chat_id: int) -> ChatData:
        try:
            chat = next(chat for chat in self.chats if chat.id == chat_id)
        except StopIteration:
            raise KeyError("Chat with id {} not found".format(chat_id))
        return chat
