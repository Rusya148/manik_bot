from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from datetime import datetime

from keyboards.keyboards import kb_salary, get_continue_keyboard, get_months_keyboard
from states.states import SalaryForm
from database.database import add_salary_to_db, get_total_salary_for_month, remove_last_salary_from_db

months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]


async def salary(message: Message):
    await message.answer('Выберите пункт меню: ', reply_markup=kb_salary)


async def salary_month_selection(callback_query: CallbackQuery):
    await callback_query.message.answer("Выберите месяц, чтобы посмотреть зарплату:", reply_markup=get_months_keyboard())
    await callback_query.answer()


async def salary_for_selected_month(callback_query: CallbackQuery):
    try:
        data = callback_query.data
        month_index = int(data.split("_")[1])

        today = datetime.today()
        year = today.year

        month_year = f"{year}-{month_index:02d}"
        total_salary = get_total_salary_for_month(month_year)

        month_name = months[month_index - 1]
        await callback_query.message.answer(
            f"Зарплата за {month_name}: {total_salary} руб."
        )
        await callback_query.answer()
    except Exception as e:
        print(f"Ошибка при обработке выбора месяца: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке месяца.")
        await callback_query.answer()

async def add_salary(callback_query: CallbackQuery):
    await callback_query.message.answer("Сколько нужно добавить?", reply_markup=None)
    await SalaryForm.waiting_for_salary.set()

async def process_salary(message: Message, state):
    try:
        salary_amount = int(message.text)
        if salary_amount <= 0:
            await message.answer("Пожалуйста, введите положительное значение зарплаты.")
            return

        today = datetime.today()
        month_year = today.strftime("%Y-%m")

        add_salary_to_db(salary_amount, month_year)

        total_salary = get_total_salary_for_month(month_year)

        month_name = months[today.month - 1]

        await message.answer(f"Зарплата за {month_name}: {total_salary} руб.")
        await message.answer(f"Сумма добавлена. Хотите продолжить добавление или удалить последнюю сумму?",
                             reply_markup=get_continue_keyboard())

        await state.finish()

    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для зарплаты.")
    except Exception as e:
        print(f"Ошибка при обработке зарплаты: {e}")
        await message.answer("Произошла ошибка при добавлении зарплаты.")

async def handle_continue_add(callback_query: CallbackQuery):
    await callback_query.message.answer("Введите следующую сумму для добавления или нажмите 'Отменить'.")
    await SalaryForm.waiting_for_salary.set()

async def handle_cancel_add(callback_query: CallbackQuery):
    await callback_query.message.answer("Добавление суммы отменено.")
    await callback_query.answer()

async def handle_remove_last_add(callback_query: CallbackQuery):
    today = datetime.today()
    month_year = today.strftime("%Y-%m")

    try:
        remove_last_salary_from_db(month_year)
        total_salary = get_total_salary_for_month(month_year)
        month_name = months[today.month - 1]
        await callback_query.message.answer(
            f"Последняя сумма удалена. Текущая зарплата за {month_name}: {total_salary} руб.")
    except Exception as e:
        print(f"Ошибка при удалении последней суммы: {e}")
        await callback_query.message.answer("Произошла ошибка при удалении последней суммы.")

    await callback_query.answer()

def register_salary(dp: Dispatcher):
    dp.register_message_handler(salary, text='Зарплата')
    dp.register_callback_query_handler(salary_month_selection, text="salary")
    dp.register_callback_query_handler(salary_for_selected_month, text_startswith="month_")
    dp.register_callback_query_handler(add_salary, text="add")
    dp.register_message_handler(process_salary, state=SalaryForm.waiting_for_salary)
    dp.register_callback_query_handler(handle_continue_add, text="continue_add")
    dp.register_callback_query_handler(handle_cancel_add, text="cancel_add")
    dp.register_callback_query_handler(handle_remove_last_add, text="remove_last_add")
