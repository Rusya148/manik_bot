from aiogram import types
from aiogram.dispatcher import Dispatcher
from states.states import Form
from keyboards.keyboards import kb_back_inline
from states.states import DeleteForm

async def exit_state_delete(callback_query: types.CallbackQuery, state):
    current_state = await state.get_state()

    if current_state == DeleteForm.waiting_for_delete.state:
        await callback_query.message.edit_text('Вы вышли из удаления клиента')
        await state.finish()

    await callback_query.answer()


async def back_to_previous_state(callback_query: types.CallbackQuery, state):
    current_state = await state.get_state()

    if current_state == Form.waiting_for_name.state:
        await callback_query.message.edit_text("Вы вышли из записи клиента.")
        await state.finish()
    else:
        if current_state == Form.waiting_for_link.state:
            await callback_query.message.edit_text("Введите имя клиента", reply_markup=kb_back_inline)
            await Form.waiting_for_name.set()

        elif current_state == Form.waiting_for_date.state:
            await callback_query.message.edit_text("Введите ссылку/id на клиента.", reply_markup=kb_back_inline)
            await Form.waiting_for_link.set()

    await callback_query.answer()

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_previous_state, text='back', state='*')
    dp.register_callback_query_handler(exit_state_delete, text='exit_delete', state='*')

