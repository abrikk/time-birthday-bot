from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text, Command
from aiogram.utils.markdown import hbold
from dateutil import relativedelta

from tgbot.functions.case_conjugation_func import whom_conjuction
from tgbot.keyboards.reply import bd_today_list, bd_data
from tgbot.middlewares.lang_middleware import __, _


def get_page(array, page: int = 1):
    index = page - 1
    return array[index]


bd_text_today = __("Сегодня день рождение у {user_name}.\n\n"
                   "{whom} исполнилось {age} лет.\n\n")


async def whose_bd_is_today(message: types.Message, db_commands):
    all_users_bd = await db_commands.select_all_users_bd_today()
    if len(all_users_bd) != 0:
        await message.answer(_("Сегодня день рождение у {n} {p}!").format(n=hbold(len(all_users_bd)),
                                                                          p=hbold(_("человек"))))
        user_id = get_page(all_users_bd)
        user = await db_commands.get_user(user_id=user_id)
        today = date.today()
        age = relativedelta.relativedelta(today, user.user_bd)
        whom = whom_conjuction(user.sex)

        await message.answer(bd_text_today.format(user_name=user.first_name, whom=whom, age=age.years),
                             reply_markup=bd_today_list(max_pages=len(all_users_bd)))
    else:
        await message.answer(_("Увы, сегодня ни у кого нету дня рождения 😕"))


async def show_chosen_page(call: types.CallbackQuery, callback_data: dict, db_commands):
    await call.answer(cache_time=5)
    all_users_bd = await db_commands.select_all_users_bd_today()
    current_page = int(callback_data.get("page"))
    if current_page > len(all_users_bd):
        current_page = 1
    elif current_page < 1:
        current_page = len(all_users_bd)
    user_id = get_page(all_users_bd, page=current_page)
    user = await db_commands.get_user(user_id=user_id)
    today = date.today()
    age = relativedelta.relativedelta(today, user.user_bd)
    whom = whom_conjuction(user.sex)
    markup = bd_today_list(max_pages=len(all_users_bd), page=current_page)
    await call.message.edit_text(bd_text_today.format(user_name=user.first_name, whom=whom, age=age.years),
                                 reply_markup=markup)


async def congratz_user(call: types.CallbackQuery, callback_data: dict, db_commands):
    await call.answer(cache_time=60)
    all_users_bd = await db_commands.select_all_users_bd_today()
    current_page = int(callback_data.get("page"))
    user_id = get_page(all_users_bd, page=current_page)
    user = await db_commands.get_user(user_id=user_id)
    congratulator = call.from_user
    await call.bot.send_message(chat_id=user_id, text=_("Вас поздравил пользователь "
                                                        "{user_name} "
                                                        "с днем рождения!", locale=user.lang_code).format(
        user_name=congratulator.get_mention(as_html=True)))
    await call.message.answer(_("Поздравление пользователю {user_name} отправлено успешно!").format(
        user_name=user.first_name))


async def bd_current_page_btn(call: types.CallbackQuery):
    await call.answer(cache_time=86400)


def register_bd_today(dp: Dispatcher):
    dp.register_message_handler(whose_bd_is_today, Command("bday_today") | Text(contains=__("🎊 У кого сегодня день "
                                                                                            "рождение")))
    dp.register_callback_query_handler(congratz_user, bd_data.filter(action="gratz"))
    dp.register_callback_query_handler(bd_current_page_btn, bd_data.filter(action="current_page"))
    dp.register_callback_query_handler(show_chosen_page, bd_data.filter())
