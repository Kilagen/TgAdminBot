import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import (
    dm_router,
    group_router
)

ROUTERS = [dm_router, group_router]


async def main():
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(*ROUTERS)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
