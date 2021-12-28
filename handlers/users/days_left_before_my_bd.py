from datetime import datetime, date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import CHAT_ID
from loader import dp, bot
from states.your_bd import BD


@dp.message_handler(Command("mybd"))
async def my_bd(message: types.Message):
    await message.answer("Введите день и месяц вашего рождения, например \"22.07\": ")

    await BD.DAY.set()


@dp.message_handler(state=BD.DAY)
async def days_left_before_my_bd(message: types.Message, state: FSMContext):
    mybd = message.text
    try:
        parse_dt = datetime.strptime(mybd, "%d.%m")
        today = date.today()

        bd = date.today().replace(month=parse_dt.month, day=parse_dt.day)

        if today > bd:
            bd = bd.replace(year=date.today().year + 1)
            days_left = bd - today
            await message.answer(f"До вашего дня рождения осталось: {days_left.days} дней")
        else:
            days_left = bd - today
            await message.answer(f"До вашего дня рождения осталось: {days_left.days} дней")
    except ValueError as ex:
        await message.answer("Вы некорректно ввели дату.")
        text = f"Ошибка от пользователя : " \
               f"{message.from_user.get_mention(as_html=True)} : {ex} : {message.text}"
        await bot.send_message(chat_id=CHAT_ID, text=text)
        await state.reset_state()

    await state.reset_state()
