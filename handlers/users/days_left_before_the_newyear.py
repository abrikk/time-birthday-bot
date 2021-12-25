from datetime import datetime, date

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils import emoji

from loader import dp


@dp.message_handler(Command("newyear"))
async def days_left_before_new_year(message: types.Message):
    NEWYEAR = datetime(year=date.today().year, month=12, day=31, hour=23,
                       minute=59, second=59, microsecond=999999)
    today = datetime.today()

    if NEWYEAR > today:
        days_left = NEWYEAR - today
        hours_left = NEWYEAR.hour - datetime.now().hour
        minutes_left = NEWYEAR.minute - today.minute
        await message.answer(f"До Нового Года осталось {days_left.days} дней, {hours_left} "
                             f"часов и {minutes_left} минут!{emoji.emojize(':snowman:')}")
    else:
        days_left = today - NEWYEAR
        hours_left = NEWYEAR.hour - datetime.now().hour
        minutes_left = NEWYEAR.minute - today.minute
        await message.answer(f"До Нового Года осталось {days_left.days} дней, {hours_left} "
                             f"часов и {minutes_left} минут!{emoji.emojize(':snowman:')}")
