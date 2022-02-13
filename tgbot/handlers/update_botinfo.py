from datetime import date, datetime
from pathlib import Path

import toml
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text
from dateutil.parser import parse

from tgbot.functions.gettext_func import get_botinfo_text
from tgbot.keyboards.reply import help_back_manual, update_bot_info
from tgbot.middlewares.lang_middleware import _


async def update_lang(message: types.Message, db_commands, session):
    message_lang = int(message.get_args())
    bot_user = await message.bot.me
    await db_commands.update_botinfo_lang(bot_user.username, message_lang)
    await session.commit()
    await message.answer(text=_("Язык был успешно обновлен!"))


async def update_version(message: types.Message, db_commands, session):
    message_version = message.get_args()
    bot_user = await message.bot.me
    await db_commands.update_botinfo_version(bot_user.username, message_version)
    await session.commit()
    await message.answer(text=_("Версия бота была успешно обновлена!"))


async def update_updated(call: types.CallbackQuery, db_commands, session):
    bot_user = await call.bot.me
    bot_info = await db_commands.get_bot_info(bot_user.username)
    updated_date = bot_info.updated_at.date()
    date_today = datetime.now()

    if updated_date != date_today.date():
        await db_commands.update_botinfo_date(bot_user.username, date_today)
        await session.commit()
        await call.answer(text=_("Дата была успешно обновлена!"), cache_time=43200)
        user = await db_commands.get_user(user_id=call.from_user.id)
        await call.message.edit_text(await get_botinfo_text(call, db_commands, session),
                                     disable_web_page_preview=True,
                                     reply_markup=help_back_manual() if user.role != 'admin'
                                     else update_bot_info())
    else:
        await call.answer(_("Дата была уже обновлена!"))


def register_update_botinfo(dp: Dispatcher):
    dp.register_message_handler(update_lang, filters.Regexp(r'^/update_lang\s(([1-9][0-9])|[1-9])$'))
    dp.register_message_handler(update_version, filters.Regexp(r'^/update_version\s\d\.\d\.\d$'))
    dp.register_callback_query_handler(update_updated, Text(contains="update_date_info"))
