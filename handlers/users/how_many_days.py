from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("howmanydays"))
async def days_left(message: types.Message):
    await message.answer("Эта команда находится в разработке. "
                         "Приносим прощения за временные не удобства.")
