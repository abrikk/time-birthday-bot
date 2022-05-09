from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hide_link


async def test_1(message: types.Message, db_commands):
    names = await db_commands.get_test_names()
    print(names)
    print(len(names) == len(set(names)))
    repeated = []
    list_t = []
    for i in names:
        if i not in list_t:
            list_t.append(i)
        else:
            repeated.append(i)
    print(repeated)


def register_test_1(dp: Dispatcher):
    dp.register_message_handler(test_1, Command("test_1"))
