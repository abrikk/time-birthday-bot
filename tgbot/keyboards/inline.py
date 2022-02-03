from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

from tgbot.functions.birthday_func import birthday_btn
from tgbot.functions.case_conjugation_func import day_conjugation, left_conjunction
from tgbot.functions.newyear_func import newyear_time
from tgbot.keyboards.reply import switch_to_bot
from tgbot.middlewares.lang_middleware import _, __


async def all_queries(query: types.InlineQuery, db_commands):
    # New Year
    newyear_d, newyear_h, newyear_m, newyear_s = newyear_time()
    user = await db_commands.get_user(user_id=query.from_user.id)
    # Birthday
    days_left = await birthday_btn(query.from_user.id, db_commands)
    day = day_conjugation(days_left)
    left = left_conjunction(days_left)
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="newyear",
                title=_("Количество дней оставшееся до Нового Года."),
                description=_("Нажмите чтобы отправить сколько дней осталось до Нового Года в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=_("До Нового Года осталось {d} дней, {h} часов, {m} минут "
                                   "и {s} секунд! ☃").format(d=hbold(newyear_d),
                                                             h=hbold(newyear_h),
                                                             m=hbold(newyear_m),
                                                             s=hbold(newyear_s))
                ),
                reply_markup=switch_to_bot()
            ),
            types.InlineQueryResultArticle(
                id="share",
                title=_("До вашего дня рождения {left}: {days_left} {day}").format(days_left=days_left, day=day,
                                                                                   left=left),
                description=_("Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=_("До моего дня рождения {left} {days_left} {day} 😏").format(
                        days_left=days_left, day=day, left=left)
                ),
                reply_markup=switch_to_bot()
            )
        ],
        cache_time=10,
        is_personal=True
    )


async def newyear_query(query: types.InlineQuery):
    newyear_d, newyear_h, newyear_m, newyear_s = newyear_time()
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="newyear",
                title=_("Количество дней оставшееся до Нового Года."),
                description=_("Нажмите чтобы отправить сколько дней осталось до Нового Года в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=_("До Нового Года осталось {d} дней, {h} часов, {m} минут "
                                   "и {s} секунд! ☃").format(d=hbold(newyear_d),
                                                             h=hbold(newyear_h),
                                                             m=hbold(newyear_m),
                                                             s=hbold(newyear_s))
                ),
                reply_markup=switch_to_bot()
            )
        ],
        cache_time=10
    )


async def bd_query(query: types.InlineQuery, db_commands):
    days_left = await birthday_btn(query.from_user.id, db_commands)
    day = day_conjugation(days_left)
    left = left_conjunction(days_left)
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="share",
                title=_("До вашего дня рождения {left}: {days_left} {day}").format(days_left=days_left, day=day,
                                                                                   left=left),
                description=_("Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=_("До моего дня рождения {left} {days_left} {day} 😏").format(
                        days_left=days_left, day=day, left=left)
                ),
                reply_markup=switch_to_bot()
            )
        ],
        is_personal=True
    )


def register_inline_mode(dp: Dispatcher):
    dp.register_inline_handler(bd_query, Text(contains=__("my birthday"), ignore_case=True))
    dp.register_inline_handler(newyear_query, Text(contains=__("new year"), ignore_case=True))
    dp.register_inline_handler(all_queries)
