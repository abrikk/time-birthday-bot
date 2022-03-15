from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from tgbot.functions.gettext_func import get_botinfo_text
from tgbot.handlers.admin_handlers.update_botinfo.update_botinfo_keyb import update_bot_info
from tgbot.keyboards.reply import help_back_manual
from tgbot.middlewares.lang_middleware import _


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
    dp.register_callback_query_handler(update_updated, Text(contains="update_date_info"))
