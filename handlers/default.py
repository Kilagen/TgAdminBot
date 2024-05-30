import logging
from aiogram import Router, types


default_router = Router()


@default_router.message()
async def handleMessage(message: types.Message):
    logging.info(f"reached default router {message.from_user} {message.chat}")
