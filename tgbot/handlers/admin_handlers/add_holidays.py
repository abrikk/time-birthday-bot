import hashlib

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from ics import Calendar


def make_id(sentence: str) -> str:
    return hashlib.shake_256(sentence.encode('utf-8')).hexdigest(5)


async def add_holidays(message: types.Message, session, db_commands):
    await message.answer("OK")
    url = r"/home/abror/Загрузки/ical-wholeworld.ics"
    with open(url, 'r') as f:
        c = Calendar(f.read())
    list_of_events = list(c.events)
    await message.answer("Получение данных из файла")
    for h in list_of_events:
        await db_commands.add_hol(make_id(h.name), h.name, h.begin.date())

    await session.commit()
    await message.answer("Все праздники записаны в базу.")


def register_add_holidays(dp: Dispatcher):
    dp.register_message_handler(add_holidays, Command("add_holidays"))
