from datetime import date

from aiogram import types, Dispatcher
from dateutil.parser import parse, ParserError

from tgbot.functions.gettext_func import get_echo_text, get_weekday_name
from tgbot.middlewares.lang_middleware import _


async def count_life(message: types.Message):
    user_date = message.text
    try:
        parsed_date = parse(user_date, dayfirst=True).date()
        print(parsed_date)
        today = date.today()
        if today > parsed_date:
            days = today - parsed_date
            day_of_the_week = get_weekday_name(parsed_date)
            date_text_info = _("Сегодня {days} день с момента Вашего рождения.\n"
                               "День недели в который вы родились: "
                               "{day_of_the_week}").format(days=days.days,
                                                           day_of_the_week=day_of_the_week.capitalize())
            await message.answer(date_text_info)
        else:
            await message.answer(get_echo_text())
    except ParserError:

        await message.answer(get_echo_text())


def register_count_life(dp: Dispatcher):
    dp.register_message_handler(count_life)
