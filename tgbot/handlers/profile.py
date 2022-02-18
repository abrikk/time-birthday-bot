from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from dateutil.parser import parse, ParserError

from tgbot.functions.gettext_func import get_profile_text, get_profile_stat_text, get_user_turned_day_text
from tgbot.keyboards.reply import cancel_keyb, update_profile, main_keyb, choosing_sex, sex_data, \
    upd_profile, profile_back_manual
from tgbot.middlewares.lang_middleware import _, __


async def my_profile(message: types.Message, state: FSMContext, db_commands):
    user = await db_commands.get_user(user_id=message.from_user.id)
    if user.sex is None:
        if user.user_bd is None:
            await message.answer(_("Укажите ваш пол:"), reply_markup=choosing_sex(where="profile"))
        else:
            await message.answer(_("Укажите ваш пол:"), reply_markup=choosing_sex(where="sex"))
    elif user.user_bd is None:
        await message.answer(_("Хорошо. Теперь отправьте свою дату рождения.\n\n"
                               "Важно! Отправьте Вашу настоящую дату, чтобы не вводить пользователей в заблуждение."),
                             reply_markup=cancel_keyb())
        await state.set_state("setting_profile")
    else:
        await message.answer(get_profile_text(user), reply_markup=update_profile())


async def back_my_profile(call: types.CallbackQuery, db_commands):
    user = await db_commands.get_user(user_id=call.from_user.id)
    await call.message.edit_text(get_profile_text(user), reply_markup=update_profile())


async def my_date(call: types.CallbackQuery, state: FSMContext, session, db_commands, callback_data: dict):
    sex = callback_data.get("sex")
    await db_commands.update_user_sex(call.from_user.id, sex)
    await session.commit()
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(_("Хорошо. Теперь отправьте свою дату рождения.\n\n"
                                "Важно! Отправьте Вашу настоящую дату, чтобы не вводить пользователей в заблуждение."),
                              reply_markup=cancel_keyb())
    await state.set_state("setting_profile")


async def setting_profile_date(message: types.Message, state: FSMContext, db_commands, session,
                               scheduler):
    user_date = message.text
    try:
        user_date_parse = parse(user_date, dayfirst=True).date()
        await db_commands.update_user_date(message.from_user.id, user_date_parse)
        await session.commit()
        user = await db_commands.get_user(user_id=message.from_user.id)

        await message.answer(_("Готово!"), reply_markup=main_keyb())
        await message.answer(get_profile_text(user), reply_markup=update_profile())
        await state.reset_state()
        trigger = CronTrigger(hour=12, minute=30, jitter=10800)
        # trigger_3 = CronTrigger(hour=14, minute=23, second=55)
        # trigger_2 = IntervalTrigger(seconds=10)
        scheduler.add_job(user_turned_day, trigger,
                          id=str(message.from_user.id), replace_existing=True,
                          args=(message, db_commands))

    except ParserError:
        await message.answer(_("Введите корректно вашу дату рождения."))


async def user_turned_day(message: types.Message, db_commands):
    await message.answer(await get_user_turned_day_text(message.from_user.id, db_commands))


async def setting_profile_sex(call: types.CallbackQuery, session, db_commands, callback_data: dict):
    sex = callback_data.get("sex")
    await db_commands.update_user_sex(call.from_user.id, sex)
    await session.commit()
    await call.answer(cache_time=60)
    await call.message.delete()
    user = await db_commands.get_user(user_id=call.from_user.id)
    await call.message.answer(_("Готово!"), reply_markup=main_keyb())
    await call.message.answer(get_profile_text(user), reply_markup=update_profile())


async def show_profile_statistics(call: types.CallbackQuery, db_commands):
    await call.answer(cache_time=3)
    text = await get_profile_stat_text(call.from_user.id, db_commands)
    await call.message.edit_text(text, reply_markup=profile_back_manual())


def register_profile(dp: Dispatcher):
    dp.register_message_handler(my_profile, Command("profile") | Text(equals=__("👤 Мой профиль")))
    dp.register_callback_query_handler(back_my_profile, Text(contains="back_profile"), state="*")
    dp.register_callback_query_handler(my_date, sex_data.filter(where="profile"))
    dp.register_message_handler(setting_profile_date, state="setting_profile")
    dp.register_callback_query_handler(setting_profile_sex, sex_data.filter(where="sex"))
    dp.register_callback_query_handler(show_profile_statistics, upd_profile.filter(profile="statistics"), state="*")
