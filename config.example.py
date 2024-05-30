import json
import typing as tp
from dataclasses import dataclass

BOT_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"


@dataclass
class ChatData:
    id: int
    redirect_to: int
    admins: tp.List[int]


@dataclass
class Config:
    general_admins: tp.List[int]
    chats: tp.List[ChatData]


def file_to_config(path='config.json') -> Config:
    config_data = json.load(open(path, 'r'))
    general_admins = config_data['general_admins']
    chats = config_data['chats']
    config = Config(general_admins, [])
    for chat in chats:
        config.chats.append(ChatData(chat['id'], chat['redirect_to'], chat['admins']))
    return config


def config_to_file(config: Config, path='config.json') -> None:
    mapping = {
        'general_admins': config.general_admins,
        'chats': [{'id': chat.id, 'redirect_to': chat.redirect_to, 'admins': chat.admins} for chat in config.chats]
    }
    json.dump(mapping, open(path, 'w'))


config = file_to_config()