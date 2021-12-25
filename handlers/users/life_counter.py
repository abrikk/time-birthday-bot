from datetime import datetime, date, time, timedelta
import locale

from aiogram import types
from aiogram.dispatcher import filters

from loader import dp

regexp = r'\d{1,2}(\.|-)\d{1,2}(\.|-)\d{4}'


@dp.message_handler(filters.Regexp(regexp))
async def count_life(message: types.Message):
    locale.setlocale(locale.LC_ALL, "")

    your_bd = message.text
    parse_dt = datetime.strptime(your_bd, "%d.%m.%Y")
    days = datetime.today() - parse_dt
    day_of_the_week = datetime(parse_dt.year, parse_dt.month, parse_dt.day).strftime('%A')
    text = f"Сегодня {days.days} день с момента Вашего рождения.\n" \
           f"День недели в который вы родились: " \
           f"{day_of_the_week.capitalize()}"
    await message.answer(text)

