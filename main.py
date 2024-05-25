import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import (
admin_router,
command_router,
dm_router,
group_router
)
from storage import SqliteStorage

ROUTERS = [admin_router, command_router, dm_router, group_router]
print("Before storage...")
STORAGE = SqliteStorage()
print("After storage...")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher(storage=STORAGE)
    dispatcher.include_routers(*ROUTERS)
    print("Before polling...")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
