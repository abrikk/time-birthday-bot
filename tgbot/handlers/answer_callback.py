from aiogram import types, Dispatcher

from tgbot.handlers.main_menu_keyb.help.help_keyb import ability_data
from tgbot.keyboards.reply import inter_hol_cb


async def just_answer(call: types.CallbackQuery):
    await call.answer(cache_time=255)
    print("Ответ на колбэк принят")


def register_just_answer(dp: Dispatcher):
    dp.register_callback_query_handler(
        just_answer,
        inter_hol_cb.filter(action='just_answer') |
        ability_data.filter(action='just_answer')
    )
