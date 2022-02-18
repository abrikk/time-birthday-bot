from pathlib import Path

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import toml


async def test_1(message: types.Message, state: FSMContext):
    state = await state.get_state()
    print(state)
    await message.answer(f"state = {state}")
    # data = toml.load(Path("pyproject.toml").absolute())
    # raw_version: str = data["tool"]["poetry"]["CREATED_ON"]
    # await message.answer(raw_version)
    # print(type(raw_version))


def register_test_1(dp: Dispatcher):
    dp.register_message_handler(test_1, Command("test_1"))
