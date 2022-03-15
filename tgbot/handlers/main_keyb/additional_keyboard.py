from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text

from tgbot.keyboards.reply import additional_keyb
from tgbot.middlewares.lang_middleware import _, __


async def another_keyb(message: types.Message):
    await message.answer(_("Что будем делать? 🙂"), reply_markup=additional_keyb())


def register_add_keyb(dp: Dispatcher):
    dp.register_message_handler(another_keyb, Command("others") | Text(contains=__("🌀 Прочее")))
