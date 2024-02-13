from aiogram import types, Router
from storage.chats import *
from util import Commander

stats_router = Router()


stats_commands = [
]

stats_commander = Commander(commands=stats_commands, router=stats_router)


@stats_router.message()
async def handle_message(msg: types.Message):
    print(msg)