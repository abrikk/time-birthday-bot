from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text

from tgbot.functions.gettext_func import get_newyear_time
from tgbot.keyboards.reply import share_message
from tgbot.middlewares.lang_middleware import __


async def days_left_before_new_year(message: types.Message):
    await message.answer(get_newyear_time(), reply_markup=share_message("new year"))


def register_newyear(dp: Dispatcher):
    dp.register_message_handler(days_left_before_new_year, Command("newyear") | Text(contains=__("⛄️ Новый Год")))
