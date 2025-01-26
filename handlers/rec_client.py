import re
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from states.states import Form
from keyboards.keyboards import kb_back_inline
from database.database import save_client

DATE_REGEX = r'^\d{2}\.\d{2}\.\d{4}$'

async def rec_client(message: types.Message):
    await message.answer('Введите имя клиента:', reply_markup=kb_back_inline)
    await Form.waiting_for_name.set()

async def process_name(message: types.Message, state):
    client_name = message.text.strip()
    await message.answer('Введите ссылку/id на клиента: ', reply_markup=kb_back_inline)
    await state.update_data(name=client_name)
    await Form.waiting_for_link.set()

async def process_link(message: types.Message, state):
    client_link = message.text.strip()
    await message.answer('Введите время, на которое записан клиент: ', reply_markup=kb_back_inline)
    await state.update_data(link=client_link)
    await Form.waiting_for_time.set()

async def process_time(message: types.Message, state):
    client_time = message.text.strip()
    await message.answer('Введите дату записи клиента (формат: DD.MM.YYYY): ', reply_markup=kb_back_inline)
    await state.update_data(time=client_time)
    await Form.waiting_for_date.set()

async def process_request_for_data(message: types.Message, state):
    client_date = message.text.strip()

    if not re.match(DATE_REGEX, client_date):
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате DD.MM.YYYY.", reply_markup=kb_back_inline)
        return

    user_data = await state.get_data()
    client_name = user_data['name']
    client_link = user_data['link']
    client_time = user_data['time']

    day, month, year = client_date.split('.')
    formatted_date = f"{year}-{month}-{day}"

    try:
        save_client(client_name, client_link, client_time, formatted_date)
        await message.answer('Клиент успешно записан!')
    except Exception as e:
        await message.answer(f"Произошла ошибка при записи клиента: {e}")

    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(rec_client, Text(equals='Записать клиента'))
    dp.register_message_handler(process_name, state=Form.waiting_for_name)
    dp.register_message_handler(process_link, state=Form.waiting_for_link)
    dp.register_message_handler(process_time, state=Form.waiting_for_time)
    dp.register_message_handler(process_request_for_data, state=Form.waiting_for_date)
