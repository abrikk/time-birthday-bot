import math

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.markdown import hide_link

from tgbot.functions.holidays_days_left_func import holiday_days_left, get_time_left
from tgbot.handlers.main_menu_keyb.whose_birthday_is_today.whose_birthday_is_today import get_page
from tgbot.handlers.others.holidays.holidays_keyb import hol_settings_keyboard, holidays_keyb, inter_holidays_keyb, \
    change_hol_keyb, hol_pag_cb, inter_hol_cb, hol_cb
from tgbot.middlewares.lang_middleware import _, __


# 1 LEVEL SECTION
async def show_all_holidays(message: types.Message):
    text = _("Нажми на кнопку, чтобы узнать сколько дней осталось до праздника.\n\n")
    await message.answer(text, reply_markup=holidays_keyb())


async def back_holidays(call: types.CallbackQuery):
    await call.answer()
    text = _("Нажми на кнопку, чтобы узнать сколько дней осталось до праздника.\n\n")
    await call.message.edit_text(text, reply_markup=holidays_keyb())


async def show_inter_holidays(call: types.CallbackQuery, db_commands):
    await call.answer()
    all_holidays = await db_commands.get_10_holidays(lang=await db_commands.get_user_language(call.from_user.id))
    number_of_hols = await db_commands.count_all_holidays()

    holidays_name = [hn for hn, dt, cb, hl in all_holidays]
    holidays_cb = [cb for hn, dt, cb, hl in all_holidays]
    buttons = {name: cb for name, cb in zip(holidays_name, holidays_cb)}

    text = _("Популярные праздники в мире. Нажми на кнопку, чтобы узнать сколько дней осталось"
             "до праздника.")
    await call.message.delete()
    await call.message.answer(text, reply_markup=inter_holidays_keyb(
        buttons=buttons,
        max_pages=math.ceil(number_of_hols / 9)
    ))


async def holiday_answer(call: types.CallbackQuery):
    await call.answer(text="ФУНКЦИЯ ЕЩЁ НЕ ГОТОВА", show_alert=True)


def register_all_holidays(dp: Dispatcher):
    dp.register_message_handler(show_all_holidays, Command("holidays") |
                                Text(contains=__("🎊 Праздники")))
    dp.register_callback_query_handler(back_holidays, hol_cb.filter(hol_type_name="back_holiday") |
                                       inter_hol_cb.filter(hol_uid="back_holiday"))
    dp.register_callback_query_handler(show_inter_holidays, hol_cb.filter(hol_type_name="ih") |
                                       hol_pag_cb.filter(action="back_inter"))
    dp.register_callback_query_handler(holiday_answer, hol_cb.filter())

