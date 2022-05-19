from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatType
from dateparser import parse as dp_parse

from tgbot.filters.chat_type_filter import ChatTypeFilter
from tgbot.functions.gettext_func import get_echo_text, get_weekday_name
from tgbot.functions.holidays_func import holiday_days_left, get_time_left
from tgbot.functions.minor_functions import get_locale_date_order
from tgbot.handlers.others.holidays.holidays_keyb import change_hol_keyb
from tgbot.middlewares.lang_middleware import _


async def count_life(message: types.Message, db_commands):
    user_date = message.text
    user = await db_commands.get_user(user_id=message.from_user.id)
    try:
        parsed_date = dp_parse(user_date, date_formats=get_locale_date_order(user.preferred_date_order),
                               languages=[user.lang_code],
                               settings={'DATE_ORDER': user.preferred_date_order}).date()
        await message.answer(parsed_date)
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
    except AttributeError:
        await message.answer(get_echo_text())


def register_count_life(dp: Dispatcher):
    dp.register_message_handler(count_life, ChatTypeFilter(ChatType.PRIVATE))
