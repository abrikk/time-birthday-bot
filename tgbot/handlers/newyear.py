from datetime import datetime, date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.markdown import hbold

from tgbot.functions.newyear_func import newyear_time
from tgbot.keyboards.reply import share_message
from tgbot.middlewares.lang_middleware import _, __


async def days_left_before_new_year(message: types.Message):
    days_left, hours_left, minutes_left, seconds_left = newyear_time()

    await message.answer(_("До Нового Года осталось {d} дней, {h} "
                           "часов, {m} минут и {s} секунд! ☃").format(
        d=hbold(days_left),
        h=hbold(hours_left),
        m=hbold(minutes_left),
        s=hbold(seconds_left)),
        reply_markup=share_message("new year"))


def register_newyear(dp: Dispatcher):
    dp.register_message_handler(days_left_before_new_year, Command("newyear") | Text(contains=__("⛄️ Новый Год")))
