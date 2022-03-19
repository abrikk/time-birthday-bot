from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.markdown import hide_link

from tgbot.functions.holidays_days_left_func import holiday_days_left, get_holiday_name, get_time_left
from tgbot.functions.next_holiday_func import get_next_holiday
from tgbot.handlers.main_menu_keyb.whose_birthday_is_today.whose_birthday_is_today import get_page
from tgbot.keyboards.reply import holidays_keyb, hol_cb, inter_holidays_keyb, change_hol_keyb, hol_pag_cb, inter_hol_cb
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


async def show_chosen_holiday(call: types.CallbackQuery, db_commands, morph, callback_data):
    await call.answer()
    hol_name = callback_data.get("hol_name")
    all_hol_codes = await db_commands.get_all_holidays_code()
    current_hol_page = all_hol_codes.index(hol_name)
    holiday_name, holiday_date, time_left, hide_photo = \
        await holiday_days_left(hol_name, db_commands, morph)
    text = _("До {hol_name} осталось {time_left}!").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph))
    await call.message.edit_text(hide_link(hide_photo) + text, reply_markup=change_hol_keyb(current_hol_page+1))


async def change_hol_page(call: types.CallbackQuery, callback_data: dict, db_commands, morph):
    await call.answer()
    all_hol_codes = await db_commands.get_all_holidays_code()
    current_hol_page = int(callback_data.get("page"))
    if current_hol_page > len(all_hol_codes):
        current_hol_page = 1
    elif current_hol_page < 1:
        current_hol_page = len(all_hol_codes)
    current_hol_code = get_page(all_hol_codes, page=current_hol_page)
    holiday_name, holiday_date, time_left, hide_photo = \
        await holiday_days_left(current_hol_code, db_commands, morph)
    text = _("До {hol_name} осталось {time_left}!").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph))
    await call.message.edit_text(hide_link(hide_photo) + text, reply_markup=change_hol_keyb(current_hol_page))


async def share_holiday(call: types.CallbackQuery):
    await call.answer(cache_time=255)


async def back_inter_holidays(call: types.CallbackQuery):
    await call.answer(cache_time=255)


def register_all_holidays(dp: Dispatcher):
    dp.register_message_handler(show_all_holidays, Command("holidays") |
                                Text(contains=__("🎊 Праздники")))
    dp.register_callback_query_handler(show_inter_holidays, hol_cb.filter(hol_name="ih") |
                                       hol_pag_cb.filter(action="back_inter"))
    dp.register_callback_query_handler(back_holidays, hol_cb.filter(hol_name="back_holiday") |
                                       inter_hol_cb.filter(hol_name="back_holiday"))
    dp.register_callback_query_handler(show_chosen_holiday, inter_hol_cb.filter())
    dp.register_callback_query_handler(share_holiday, hol_pag_cb.filter(action="share_message"))
    dp.register_callback_query_handler(change_hol_page, hol_pag_cb.filter())


