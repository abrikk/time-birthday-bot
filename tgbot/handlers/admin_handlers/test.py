from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hide_link


async def test_1(message: types.Message, state: FSMContext):
    await message.answer("Text with hide link {hide_link}".format(hide_link=hide_link("https://www.ixbt.com/img/n1"
                                                                                      "/news/2022/0/4/tesla-roadster_large.jpg")))


def register_test_1(dp: Dispatcher):
    dp.register_message_handler(test_1, Command("test_1"))
