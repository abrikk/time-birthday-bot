from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.functions.gettext_func import get_echo_text


async def create_bot_info(message: types.Message, db_commands, session):
    user = await db_commands.get_user(user_id=message.from_user.id)
    if user.role == 'admin':
        bot_user = await message.bot.me
        if await db_commands.get_bot_info(bot_user.username) is None:
            await db_commands.add_bot(username=bot_user.username)
            await session.commit()
            await message.answer("Добавил бота в базу")
        else:
            await message.answer("Бот уже находится в базе")
    else:
        await message.answer(get_echo_text())


def register_botinfo_create(dp: Dispatcher):
    dp.register_message_handler(create_bot_info, Command("create_bot"))
