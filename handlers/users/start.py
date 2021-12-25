from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n\n"
                         f"Этот бот считает количество прожитых дней с момента твоего "
                         f"дня рождения. Просто отправь дату рождения (например: 22.07.2006)")
