from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command


async def test_1(message: types.Message):
    pass


def register_test_1(dp: Dispatcher):
    dp.register_message_handler(test_1, Command("test_1"))
