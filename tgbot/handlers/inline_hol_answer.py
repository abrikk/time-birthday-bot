from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.filters.inline_private import PrivateInlineFilter
from tgbot.functions.holidays_func import holiday_days_left, get_time_left
from tgbot.handlers.others.holidays.holidays_keyb import change_hol_keyb
from tgbot.middlewares.lang_middleware import _


async def show_chosen_holiday(message: types.Message, db_commands, state: FSMContext, morph):
    user = await db_commands.get_user(user_id=message.from_user.id)
    all_uids = await db_commands.get_all_holidays_uid(user.lang_code)
    hol_uid = message.text.rsplit(' ', 1)[-1]
    current_hol_page = all_uids.index(hol_uid) + 1
    holiday_name, holiday_date, time_left, photo_id = \
        await holiday_days_left(hol_uid, db_commands)
    if user.role == "admin":
        sett_data = {"uid": hol_uid, "holiday_name": holiday_name,
                     "holiday_date": holiday_date}
        await state.update_data(sett_data=sett_data)
    text = _("До {hol_name} осталось {time_left}!").format(
        hol_name=holiday_name, time_left=get_time_left(time_left, morph))
    await message.answer_photo(photo=photo_id, caption=text,
                               reply_markup=change_hol_keyb(
                                   max_pages=len(all_uids),
                                   page=current_hol_page,
                                   admin=user.role == 'admin'
                               ))


def register_inline_hol_answer(dp: Dispatcher):
    dp.register_message_handler(show_chosen_holiday, PrivateInlineFilter())
