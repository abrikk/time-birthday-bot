from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Запустить бота",
            "/help - Помощь",
            "/mybd - Сколько дней осталось до дня рождения",
            "/newyear - Сколько дней осталось до Нового Года",
            "/howmanydays - Находит разницу между отправленной вами датой и текущей датой")

    await message.answer("\n".join(text))
