from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text

from tgbot.functions.holidays_days_left_func import holiday_days_left
from tgbot.functions.next_holiday_func import get_next_holiday
from tgbot.keyboards.reply import holidays_keyb
from tgbot.middlewares.lang_middleware import _, __


async def show_all_holidays(message: types.Message):
    next_holiday: dict = get_next_holiday()
    text = _("Нажми на кнопку, чтобы узнать сколько дней осталось до праздника.\n\n"
             "P.S. Скоро праздник - {hol_name} 😃").format(hol_name=next_holiday["name"])
    await message.answer(text, reply_markup=holidays_keyb())


async def get_time_left_before_holiday(message: types.Message):
    holiday_name = message.text
    holiday_name, days_left = holiday_days_left(holiday_name)
    text = _("До {hol_name} осталось {days_left} дней!").format(hol_name=holiday_name,
                                                                days_left=days_left)
    await message.answer(text)

all_holidays = [__("🌹 Международный женский день"), __("🌱 Навруз")]


def register_all_holidays(dp: Dispatcher):
    dp.register_message_handler(show_all_holidays, Command("holidays") |
                                Text(contains=__("🎊 Праздники")))
    dp.register_message_handler(get_time_left_before_holiday, Text(contains=__("🌹 Международный женский день")))
