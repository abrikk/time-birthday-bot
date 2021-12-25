from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("mybd"))
async def my_bd(message: types.Message):
    await message.answer("Введите день и месяц вашего рождения, например \"22.07\": ")

    await BD.DAY.set()
