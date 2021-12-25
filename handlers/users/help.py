from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Запустить бота",
            "/help - Помощь",
            "/mybd - Количество дней до дня рождения",
            "/newyear - Количество дней до Нового Года",
            "/howmanydays - Подсчёт дней в определённом промежутке времени")

    await message.answer("\n".join(text))
