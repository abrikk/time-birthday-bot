from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hcode

from loader import dp


@dp.message_handler(Command("show_state"), state="*")
async def show_state(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Вы в состоянии {hcode(state)}.")