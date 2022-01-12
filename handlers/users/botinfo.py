from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hcode, hlink

from loader import dp


@dp.message_handler(Command("botinfo"))
async def bot_info(message: types.Message):
    return await message.answer(f"About this {hlink('bot', url='t.me/countthetimebot')}:\n\n"
                                f"Beta version {hcode('0.0.1')}\n"
                                "Updated on Jan 9, 2022\n"
                                "Released on Dec 25, 2021\n"
                                "Developer @JustAbrik", disable_web_page_preview=True)
