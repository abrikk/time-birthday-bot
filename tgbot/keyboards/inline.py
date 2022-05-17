from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from tgbot.filters.admin_bot import BotAdmin
from tgbot.functions.birthday_func import birthday_btn
from tgbot.functions.gettext_func import get_newyear_time, until_bd
from tgbot.keyboards.reply import switch_to_bot, switch_or_gratz
from tgbot.middlewares.lang_middleware import _, __


def get_fake_results(start_num: int, size: int = 50):
    overall_items = 195
    # Если результатов больше нет, отправляем пустой список
    if start_num >= overall_items:
        return []
    # Отправка неполной пачки (последней)
    elif start_num + size >= overall_items:
        return list(range(start_num, overall_items + 1))
    else:
        return list(range(start_num, start_num + size))


async def all_queries(query: types.InlineQuery, db_commands):
    user = await db_commands.get_user(user_id=query.from_user.id)
    if user.role == 'admin':
        query_offset = int(query.offset) if query.offset else 0
        print(query.query)
        holidays = await db_commands.get_holidays(lang=user.lang_code, like=query.query,
                                                  offset=query_offset)
        # await query.answer(results=[], switch_pm_text="Press me",
        #                    switch_pm_parameter="press_me", cache_time=3, is_personal=True, next_offset="")
        results = [
            types.InlineQueryResultArticle(
                id=data[2],
                title=data[0],
                description=_("Дата празднования: {hol_date}").format(hol_date=data[1].strftime("%d.%m.%Y")),
                input_message_content=types.InputTextMessageContent(
                    message_text=_("Праздник {hol}: {uid}").format(hol=data[0], uid=data[2])
                )
            )
            for data in holidays
        ]
        if len(holidays) < 50:
            print("LESS")
            await query.answer(results=results, cache_time=3, is_personal=True, next_offset="")
        else:
            print("MORE")
            await query.answer(results, cache_time=3, is_personal=True, next_offset=str(query_offset + 50))
    else:
        days_left, age = await birthday_btn(user)
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
                    title=await until_bd(days_left, age, where="title", user_bd=user.user_bd),
                    description=_(
                        "Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                    input_message_content=types.InputTextMessageContent(
                        message_text=await until_bd(days_left, age, "inline_text", user_bd=user.user_bd)
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

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="share",
                title=await until_bd(days_left, age, where="title", user_bd=user.user_bd),
                description=_("Нажмите чтобы отправить сколько дней осталось до вашего дня рождения в текущий чат."),
                input_message_content=types.InputTextMessageContent(
                    message_text=await until_bd(days_left, age, "inline_text", user_bd=user.user_bd)
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
    dp.register_inline_handler(all_queries, BotAdmin())
