from aiogram import types, Router, Dispatcher, Bot


class Commander:
    def __init__(self, commands: list[types.BotCommand], router: Router):
        self.commands = commands
        self.router = router

    def add_to(self, consumer: 'Consumer'):
        consumer.add_commands(self.commands)
        consumer.include_router(self.router)


class Consumer:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.dispatcher = dispatcher
        self.bot = bot
        self.commands: list[types.BotCommand] = []

    def add_commands(self, commands: list[types.BotCommand]):
        self.commands.extend(commands)

    def include_router(self, router: Router):
        self.dispatcher.include_router(router)

    async def set_my_commands(self):
        await self.bot.set_my_commands(self.commands)
