from datetime import datetime, date

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("newyear"))
async def days_left_before_new_year(message: types.Message):
    NEWYEAR = datetime(year=date.today().year, month=1, day=1)
    today = datetime.today()

    if today > NEWYEAR:
        NEWYEAR = NEWYEAR.replace(year=date.today().year + 1)

        days_left = NEWYEAR - today
        hours_left = today.hour - NEWYEAR.hour
        minutes_left = today.minute - NEWYEAR.minute
        await message.answer(f"До Нового Года осталось {days_left.days} дней, "
                             f"{24 - hours_left} "
                             f"часов и {60 - minutes_left} минуты!")
    else:
        days_left = NEWYEAR - today
        hours_left = today.hour - NEWYEAR.hour
        minutes_left = today.minute - NEWYEAR.minute
        await message.answer(f"До Нового Года осталось {days_left.days} дней, "
                             f"{24 - hours_left} часов и "
                             f"{60 - minutes_left} минуты!")