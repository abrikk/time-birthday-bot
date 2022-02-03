from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.functions.gettext_func import get_botinfo_text


async def bot_info(message: types.Message, db_commands):
    return await message.answer(await get_botinfo_text(message, db_commands),
                                disable_web_page_preview=True)


def register_bot_info(dp: Dispatcher):
    dp.register_message_handler(bot_info, Command("botinfo"))
