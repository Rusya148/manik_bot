from aiogram import executor

from bot.bot import dp
from bot.register_dp import register

if __name__ == '__main__':
    register(dp)
    executor.start_polling(dp, skip_updates=True)
