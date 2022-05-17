from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from tgbot.filters.admin_bot import AdminOfBot
from tgbot.functions.gettext_func import get_echo_text
from tgbot.middlewares.lang_middleware import _


async def delete_keyboard(message: types.Message):
    await message.answer(_("Клавиатура была успешно удалена"), reply_markup=ReplyKeyboardRemove())


async def delete_me_from_db(message: types.Message, db_commands, session, scheduler):
    await db_commands.delete_me_from_db(message.from_user.id)
    await db_commands.delete_me_from_bd_stat_r(message.from_user.id)
    await db_commands.delete_me_from_bd_stat_g(message.from_user.id)
    scheduler.remove_job(str(message.from_user.id))

    await session.commit()


async def delete_all_jobs(message: types.Message, scheduler):
    scheduler.remove_all_jobs()
    await message.answer("All jobs have been deleted.\n\n"
                         f"The jobstore is: {scheduler.get_jobs()}")


def register_admin_commands(dp: Dispatcher):
    dp.register_message_handler(delete_keyboard, Command("delete_keyboard"), AdminOfBot())
    dp.register_message_handler(delete_me_from_db, Command("delete_me"), AdminOfBot())
    dp.register_message_handler(delete_all_jobs, Command("delete_all_jobs"), AdminOfBot())

