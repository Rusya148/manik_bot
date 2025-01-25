from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import token

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())