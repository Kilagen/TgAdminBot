from aiogram import Router, types


default_router = Router()


@default_router.message()
async def handleMessage(message: types.Message):
    print(message)
