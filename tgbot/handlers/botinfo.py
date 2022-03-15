from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from tgbot.functions.gettext_func import get_botinfo_text
from tgbot.handlers.admin_handlers.update_botinfo.update_botinfo_keyb import update_bot_info


async def bot_info(message: types.Message, db_commands, session):
    user = await db_commands.get_user(user_id=message.from_user.id)
    return await message.answer(await get_botinfo_text(message, db_commands, session),
                                disable_web_page_preview=True,
                                reply_markup=update_bot_info(where="msg_cmnd")
                                if user.role == 'admin' else None)


def register_bot_info(dp: Dispatcher):
    dp.register_message_handler(bot_info, Command("botinfo"))
