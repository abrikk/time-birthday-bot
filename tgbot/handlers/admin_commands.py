from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove

from tgbot.functions.gettext_func import get_echo_text
from tgbot.middlewares.lang_middleware import _, __


async def delete_keyboard(message: types.Message, db_commands):
    user = await db_commands.get_user(user_id=message.from_user.id)
    if user.role == 'admin':
        await message.answer(_("Клавиатура была успешно удалена"), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(get_echo_text())


async def delete_me_from_db(message: types.Message, db_commands, session):
    user = await db_commands.get_user(user_id=message.from_user.id)
    if user.role == 'admin':
        await db_commands.delete_me_from_db(message.from_user.id)
        await session.commit()
    else:
        await message.answer(get_echo_text())


def register_admin_commands(dp: Dispatcher):
    dp.register_message_handler(delete_keyboard, Command("delete_keyboard"))
    dp.register_message_handler(delete_me_from_db, Command("delete_me"))

