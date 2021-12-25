from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHAT_ID
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n\n"
                         f"Этот бот считает количество прожитых дней с момента твоего "
                         f"дня рождения. Просто отправь дату рождения (например: 22.07.2006)")
    text = f"Новый пользователь {message.from_user.get_mention(as_html=True)}"
    await bot.send_message(chat_id=CHAT_ID, text=text)
