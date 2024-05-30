import json
from dataclasses import asdict

from aiogram import F, Router, types
from aiogram.filters import BaseFilter

from config import config, ChatData, config_to_file


default_router = Router()


@default_router.message()
async def handleMessage(message: types.Message):
    print(message)

