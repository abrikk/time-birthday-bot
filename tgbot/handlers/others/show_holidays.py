from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text

from tgbot.functions.holidays_days_left_func import holiday_days_left, get_holiday_name
from tgbot.functions.next_holiday_func import get_next_holiday
from tgbot.keyboards.reply import holidays_keyb, hol_cb, inter_holidays_keyb, change_hol_keyb, hol_pag_cb
from tgbot.middlewares.lang_middleware import _, __


async def show_all_holidays(message: types.Message):
    next_holiday: dict = get_next_holiday()
    text = _("Нажми на кнопку, чтобы узнать сколько дней осталось до праздника.\n\n"
             "P.S. Скоро {hol_name} 😃").format(hol_name=next_holiday["name"])
    await message.answer(text, reply_markup=holidays_keyb())


async def back_holidays(call: types.CallbackQuery):
    await call.answer()
    next_holiday: dict = get_next_holiday()
    text = _("Нажми на кнопку, чтобы узнать сколько дней осталось до праздника.\n\n"
             "P.S. Скоро праздник - {hol_name} 😃").format(hol_name=next_holiday["name"])
    await call.message.edit_text(text, reply_markup=holidays_keyb())


async def show_inter_holidays(call: types.CallbackQuery, db_commands):
    await call.answer()
    all_holidays = await db_commands.get_all_holidays()
    holidays_name = [get_holiday_name(cb) for d, cb, hl in all_holidays]
    holidays_cb = [i[1] for i in all_holidays]
    buttons = {name: cb for name, cb in zip(holidays_name, holidays_cb)}
    text = _("Популярные праздники в мире. Нажми на кнопку, чтобы узнать сколько дней осталось"
             "до праздника.")
    await call.message.edit_text(text, reply_markup=inter_holidays_keyb(buttons))


async def show_chosen_holiday(call: types.CallbackQuery, callback_data):
    await call.answer()
    hol_name = callback_data.get("hol_name")
    holiday_name, holiday_namec, holiday_date, days_left = holiday_days_left(hol_name)
    text = _("До {hol_name} осталось {days_left} дней!").format(hol_name=holiday_namec,
                                                                days_left=days_left)
    await call.message.edit_text(text, reply_markup=change_hol_keyb())


def register_all_holidays(dp: Dispatcher):
    dp.register_message_handler(show_all_holidays, Command("holidays") |
                                Text(contains=__("🎊 Праздники")))
    dp.register_callback_query_handler(show_inter_holidays, hol_cb.filter(hol_name="ih") |
                                       hol_pag_cb.filter(action="back_inter"))
    dp.register_callback_query_handler(back_holidays, hol_cb.filter(hol_name="back_holiday"))
    dp.register_callback_query_handler(show_chosen_holiday, hol_cb.filter())

