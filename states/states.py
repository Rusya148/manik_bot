from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_link = State()
    waiting_for_time = State()
    waiting_for_date = State()

class DeleteForm(StatesGroup):
    waiting_for_delete = State()
    waiting_for_link = State()

class SalaryForm(StatesGroup):
    waiting_for_salary = State()
