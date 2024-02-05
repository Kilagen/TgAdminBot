import asyncio
from aiogram import Bot, Dispatcher
from ban import ban_commander
from config import BOT_TOKEN
from util import Consumer


async def main():
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()
    consumer = Consumer(dispatcher, bot)

    ban_commander.add_to(consumer)
    
    await consumer.set_my_commands()
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
