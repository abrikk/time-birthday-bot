from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.functions.gettext_func import get_echo_text
from tgbot.middlewares.lang_middleware import _


async def admin_stat(message: types.Message, db_commands):
    user = await db_commands.get_user(user_id=message.from_user.id)
    if user.role == 'admin':
        count_users = await db_commands.count_users()
        await message.answer(_("Всего пользователей: {count_users}").format(count_users=count_users))
    else:
        await message.answer(get_echo_text())


def register_stat(dp: Dispatcher):
    dp.register_message_handler(admin_stat, Command("statistics"))
