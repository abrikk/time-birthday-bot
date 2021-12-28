from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import CHAT_ID
from loader import dp, bot
from states.how_many_days_state import HMD


@dp.message_handler(Command("howmanydays"))
async def days_left(message: types.Message):
    await message.answer("Отправьте дату, чтобы узнать разницу между текущей датой "
                         "и датой отправленной вами (например 01.01.2077 или 01.07.2003):")

    await HMD.DATE.set()


@dp.message_handler(state=HMD.DATE)
async def days_left_before_the_date(message: types.Message, state: FSMContext):
    user_date = message.text
    try:
        parsed_date = datetime.strptime(user_date, "%d.%m.%Y")
        today = datetime.today()

        if parsed_date > today:
            difference = parsed_date - today
            await message.answer(f"До {user_date} осталось {difference.days} дней")
        elif today > parsed_date:
            difference = today - parsed_date
            await message.answer(f"С {user_date} прошло {difference.days} дней")
    except ValueError as ex:
        await message.answer("Вы некорректно ввели дату.")
        text = f"Ошибка от пользователя : " \
               f"{message.from_user.get_mention(as_html=True)} : {ex} : {message.text}"
        await bot.send_message(chat_id=CHAT_ID, text=text)
        await state.reset_state()

    await state.reset_state()
