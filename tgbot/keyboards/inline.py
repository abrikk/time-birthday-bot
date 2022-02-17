from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from tgbot.functions.birthday_func import birthday_btn
from tgbot.functions.gettext_func import get_newyear_time, until_bd
from tgbot.keyboards.reply import switch_to_bot, switch_or_gratz
from tgbot.middlewares.lang_middleware import _, __


async def all_queries(query: types.InlineQuery, db_commands):
    user = await db_commands.get_user(user_id=query.from_user.id)
    days_left, age = await birthday_btn(user)
    if user.user_bd == date.today():
        inline_message_text = _("Я сегодня родился!!! 🥳🥳")
    else:
        inline_message_text = await until_bd(days_left, age, "inline_text")
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="newyear",
                title=_("Количество дней оставшееся до Нового Года."),
                description=_("Нажмите чтобы отправить сколько дней осталось до Нового Года в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=get_newyear_time()
                ),
                reply_markup=switch_to_bot()
            ),
            types.InlineQueryResultArticle(
                id="share",
                title=await until_bd(days_left, age, where="title"),
                description=_("Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=inline_message_text
                ),
                reply_markup=switch_to_bot() if days_left != 0 else switch_or_gratz(query.from_user.id)
            )
        ],
        cache_time=5,
        is_personal=True
    )


async def newyear_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="newyear",
                title=_("Количество дней оставшееся до Нового Года."),
                description=_("Нажмите чтобы отправить сколько дней осталось до Нового Года в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=get_newyear_time()
                ),
                reply_markup=switch_to_bot()
            )
        ],
        cache_time=10
    )


async def bd_query(query: types.InlineQuery, db_commands):
    user = await db_commands.get_user(user_id=query.from_user.id)
    days_left, age = await birthday_btn(user)
    if user.user_bd == date.today():
        inline_message_text = _("Я сегодня родился!!! 🥳🥳")
    else:
        inline_message_text = await until_bd(days_left, age, "inline_text")
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="share",
                title=await until_bd(days_left, age, where="title"),
                description=_("Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=inline_message_text
                ),
                reply_markup=switch_to_bot() if days_left != 0 else switch_or_gratz(query.from_user.id)
            )
        ],
        cache_time=5,
        is_personal=True
    )


def register_inline_mode(dp: Dispatcher):
    dp.register_inline_handler(bd_query, Text(contains=__("my birthday"), ignore_case=True))
    dp.register_inline_handler(newyear_query, Text(contains=__("new year"), ignore_case=True))
    dp.register_inline_handler(all_queries)
