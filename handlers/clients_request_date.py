from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from datetime import datetime, timedelta
from collections import defaultdict

from database.request_for_date import get_clients_by_date_range
from keyboards.keyboards import kb_registered_client

async def clients_date(message: types.Message):
    await message.answer('На какой период показать записи?', reply_markup=kb_registered_client)

async def format_clients_message(clients):
    if not clients:
        return "Нет клиентов на выбранный период."

    clients_by_day = defaultdict(list)
    for client in clients:
        client_date = datetime.strptime(client[4], '%Y-%m-%d')
        formatted_date = client_date.strftime('%d.%m.%Y')
        client = client[:4] + (formatted_date,) + client[5:]
        clients_by_day[formatted_date].append(client)

    message = ""
    for date, clients in clients_by_day.items():
        message += f"——————————————\n<b>Дата: {date}</b>\n"
        for client in clients:
            name = client[1]
            username = client[2]
            appointment_time = client[3]
            appointment_date = client[4]
            message += f"{name}, {username},\nВремя записи: {appointment_time}\n\n"
    return message

async def client_today(callback_query: CallbackQuery):
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        clients_today = get_clients_by_date_range(today, today)
        message = await format_clients_message(clients_today)
        await callback_query.message.answer(f'Клиенты на сегодня:\n{message}', parse_mode='HTML')
    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка при получении данных: {e}")

async def client_week(callback_query: CallbackQuery):
    today = datetime.now().strftime('%Y-%m-%d')
    next_7_days = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    try:
        clients_next_7_days = get_clients_by_date_range(today, next_7_days)
        message = await format_clients_message(clients_next_7_days)
        await callback_query.message.answer(f'Клиенты на неделю:\n{message}', parse_mode='HTML')
    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка при получении данных: {e}")

async def client_month(callback_query: CallbackQuery):
    today = datetime.now().strftime('%Y-%m-%d')
    next_31_days = (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d')
    try:
        clients_this_month = get_clients_by_date_range(today, next_31_days)
        message = await format_clients_message(clients_this_month)
        await callback_query.message.answer(f'Клиенты на месяц:\n{message}', parse_mode='HTML')
    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка при получении данных: {e}")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(clients_date, text='Клиенты')
    dp.register_callback_query_handler(client_today, text='clients_today')
    dp.register_callback_query_handler(client_week, text='clients_week')
    dp.register_callback_query_handler(client_month, text='clients_month')
