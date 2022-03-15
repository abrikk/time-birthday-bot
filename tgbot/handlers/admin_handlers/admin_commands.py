from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from tgbot.functions.gettext_func import get_echo_text
from tgbot.middlewares.lang_middleware import _


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
        await db_commands.delete_me_from_bd_stat_r(message.from_user.id)
        await db_commands.delete_me_from_bd_stat_g(message.from_user.id)

        await session.commit()
    else:
        await message.answer(get_echo_text())


async def delete_all_jobs(message: types.Message, db_commands, scheduler):
    # user_ids = await db_commands.get_all_users_with_date()
    # for user_id in user_ids:
    scheduler.remove_all_jobs()
    await message.answer("All jobs have been deleted.\n\n"
                         f"The jobstore is: {scheduler.get_jobs()}")


def register_admin_commands(dp: Dispatcher):
    dp.register_message_handler(delete_keyboard, Command("delete_keyboard"))
    dp.register_message_handler(delete_me_from_db, Command("delete_me"))
    dp.register_message_handler(delete_all_jobs, Command("delete_all_jobs"))

