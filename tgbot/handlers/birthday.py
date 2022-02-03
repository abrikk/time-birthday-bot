from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from dateutil.parser import parse, ParserError

from tgbot.functions.birthday_func import birthday_btn, birthday_cmnd
from tgbot.functions.gettext_func import until_bd
from tgbot.keyboards.reply import cancel_keyb, share_message, back_keyb
from tgbot.middlewares.lang_middleware import _, __


# async def my_bd_deeplink(message: types.Message):
#     birthdate = message.get_args()
#     try:
#         parsed_dt = parse(birthdate, dayfirst=True)
#         days_left, age = birthday_cmnd(parsed_dt)
#         await message.answer(until_bd(message, days_left, age, "cmnd"),
#                              reply_markup=share_message("my birthday"))
#     except ValueError:
#         await message.answer(get_echo_text())


async def my_bd_command(message: types.Message, state: FSMContext):
    await message.answer(_("Введите день и месяц рождения, например \"22.07\":"), reply_markup=cancel_keyb())

    await state.set_state("bd_command")


async def my_bd_command_state(message: types.Message, state: FSMContext):
    birthdate = message.text
    try:
        parsed_dt = parse(birthdate, dayfirst=True)
        days_left, age = birthday_cmnd(parsed_dt)
        await message.answer(until_bd(message, days_left, age, "cmnd"),
                             reply_markup=share_message("my birthday"))

        await state.reset_state()
    except ValueError:
        await message.answer(_("Вы некорректно ввели дату. Попробуйте еще раз"))


async def my_bd_button(message: types.Message, state: FSMContext, db_commands):
    days_left, age = await birthday_btn(message.from_user.id, db_commands)
    if days_left is None:
        await message.answer(_("Хорошо. Теперь отправьте свою дату рождения.\n\n"
                               "Важно! Отправьте Вашу настоящую дату, чтобы не вводить пользователей в заблуждение."),
                             reply_markup=back_keyb())
        await state.set_state("bd_button")
    else:
        if days_left != 0:
            await message.answer(until_bd(message, days_left, age, "btn"),
                                 reply_markup=share_message("my birthday"))
        else:
            await message.answer(until_bd(message, days_left, age, "btn"),
                                 reply_markup=share_message("my birthday"))


async def my_bd_date(message: types.Message, state: FSMContext, db_commands, session):
    user_date = message.text
    try:
        user_date_parse = parse(user_date, dayfirst=True)
        await db_commands.update_user_date(message.from_user.id, user_date_parse)
        await session.commit()
        days_left, age = await birthday_btn(message.from_user.id, db_commands)
        if days_left != 0:
            await message.answer(until_bd(message, days_left, age, "btn"),
                                 reply_markup=share_message("my birthday"))
        else:
            await message.answer(until_bd(message, days_left, age, "btn"),
                                 reply_markup=share_message("my birthday"))

        await state.reset_state()
    except ParserError:
        await message.answer(_("Введите корректно вашу дату рождения."))


def register_my_bd(dp: Dispatcher):
    dp.register_message_handler(my_bd_command, Command("mybd"))
    dp.register_message_handler(my_bd_command_state, state="bd_command")
    dp.register_message_handler(my_bd_button, Text(contains=__("🥳 Моё день рождение")))
    dp.register_message_handler(my_bd_date, state="bd_button")
