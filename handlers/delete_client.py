from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from database.delete_client import delete_client
from states.states import DeleteForm
from keyboards.keyboards import kb_exit_delete

async def delete_client_text(message: Message):
    await message.answer('Какого клиента вы хотите удалить?\nВведите ссылку на него:', reply_markup=kb_exit_delete)
    await DeleteForm.waiting_for_delete.set()

async def handle_delete_client_link(message: Message, state):
    client_link = message.text.strip()
    try:

        result = delete_client(client_link)

        if result:
            await message.answer('Клиент удален.')
        else:
            await message.answer('Клиент с такой ссылкой не найден или не был удален.')

    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')

    await state.finish()

def register_delete_client(dp: Dispatcher):
    dp.register_message_handler(delete_client_text, text='Удалить клиента')
    dp.register_message_handler(handle_delete_client_link, state=DeleteForm.waiting_for_delete)
