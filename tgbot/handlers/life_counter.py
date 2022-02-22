from datetime import date

from aiogram import types, Dispatcher
from dateparser import parse as dp_parse
from tgbot.functions.gettext_func import get_echo_text, get_weekday_name
from tgbot.middlewares.lang_middleware import _


async def count_life(message: types.Message, db_commands):
    user_date = message.text
    try:
        user = await db_commands.get_user(user_id=message.from_user.id)
        parsed_date = dp_parse(user_date, languages=[user.lang_code],
                               settings={'DATE_ORDER': user.preferred_date_order}).date()
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
    dp.register_message_handler(count_life)
