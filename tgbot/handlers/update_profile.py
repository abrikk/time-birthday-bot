from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from dateutil.parser import parse, ParserError

from tgbot.keyboards.reply import main_keyb, upd_profile, cancel_keyb, choosing_sex, sex_data
from tgbot.middlewares.lang_middleware import _


async def edit_name(call: Union[types.CallbackQuery, types.Message], state: FSMContext):
    text = _("Отправьте новое имя")
    if isinstance(call, types.CallbackQuery):
        await call.message.answer(text, reply_markup=cancel_keyb())
    elif isinstance(call, types.Message):
        await call.answer(text, reply_markup=cancel_keyb())
    await state.set_state("edit_name")


async def editing_name(message: types.Message, state: FSMContext, session, db_commands):
    new_name = message.text

    await db_commands.update_user_name(user_id=message.from_user.id, new_name=new_name)
    await session.commit()
    await message.answer(_("Успешно! Имя обновлено."), reply_markup=main_keyb())
    await state.reset_state()


async def edit_date(call: Union[types.CallbackQuery, types.Message], state: FSMContext):
    text = _("Отправьте новую дату")
    if isinstance(call, types.CallbackQuery):
        await call.message.answer(text, reply_markup=cancel_keyb())
    elif isinstance(call, types.Message):
        await call.answer(text, reply_markup=cancel_keyb())
    await state.set_state("edit_date")


async def editing_date(message: types.Message, state: FSMContext, session, db_commands):
    new_date = message.text
    try:
        new_date_parsed = parse(new_date, dayfirst=True)

        await db_commands.update_user_date(user_id=message.from_user.id, date=new_date_parsed)
        await session.commit()
        await message.answer(_("Успешно! Дата обновлена."), reply_markup=main_keyb())
        await state.reset_state()

    except ParserError:
        await message.answer(_("Введите корректно вашу дату рождения."))


async def edit_sex(call: Union[types.CallbackQuery, types.Message]):
    text = _("Укажите ваш пол:")
    if isinstance(call, types.CallbackQuery):
        await call.message.answer(text, reply_markup=choosing_sex(where="main"))
    elif isinstance(call, types.Message):
        await call.answer(text, reply_markup=choosing_sex(where="main"))


async def editing_sex(call: types.CallbackQuery, session, db_commands, callback_data: dict):
    sex = callback_data.get("sex")
    await db_commands.update_user_sex(call.from_user.id, sex)
    await session.commit()
    await call.answer(cache_time=60)
    await call.message.answer(_("Успешно! Пол обновлен."))


def register_update(dp: Dispatcher):
    dp.register_message_handler(edit_name, Command("setname"))
    dp.register_callback_query_handler(edit_name, upd_profile.filter(profile="name"))
    dp.register_message_handler(editing_name, state="edit_name")
    dp.register_message_handler(edit_date, Command("setdate"))
    dp.register_callback_query_handler(edit_date, upd_profile.filter(profile="bd"))
    dp.register_message_handler(editing_date, state="edit_date")
    dp.register_message_handler(edit_sex, Command("setsex"))
    dp.register_callback_query_handler(edit_sex, upd_profile.filter(profile="sex"))
    dp.register_callback_query_handler(editing_sex, sex_data.filter(where="main"))
