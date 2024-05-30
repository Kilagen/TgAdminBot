import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import (
    dm_router,
    group_router,
    default_router
)
ROUTERS = [dm_router, group_router, default_router]


async def main():
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(*ROUTERS)
    logging.info("begin polling")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("start asyncio")
    asyncio.run(main())
