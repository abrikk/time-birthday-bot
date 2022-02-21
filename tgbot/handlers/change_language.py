from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text

from tgbot.functions.minor_functions import get_date_order
from tgbot.keyboards.reply import lang_keyb, lang_cb, main_keyb
from tgbot.middlewares.lang_middleware import _, __, i18n
from tgbot.misc.set_bot_commands import set_default_commands


async def set_language(message: types.Message):
    await message.answer(_("🌐 Выберите язык:"), reply_markup=lang_keyb)


async def setting_language(call: types.CallbackQuery, callback_data: dict, db_commands, session):
    lang = callback_data.get("name")
    i18n.ctx_locale.set(lang)
    await call.answer(text=_("🇷🇺 Вы поменяли язык на русский").format(lang=lang))
    await call.message.delete()

    await call.message.answer(_("Ваш язык был изменен успешно!"), reply_markup=main_keyb())
    await set_default_commands(call.bot)
    await db_commands.update_language(user_id=call.from_user.id, lang=lang)
    await session.commit()


def register_change_language(dp: Dispatcher):
    dp.register_message_handler(set_language, Command("setlanguage") | Text(contains=__("🌐 Поменять язык"),
                                                                                ignore_case=True))
    dp.register_callback_query_handler(setting_language, lang_cb.filter())
