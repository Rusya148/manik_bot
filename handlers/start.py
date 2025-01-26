from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.keyboards import kb_start

async def start(message: types.Message):
    await message.answer('ky', reply_markup=kb_start)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
