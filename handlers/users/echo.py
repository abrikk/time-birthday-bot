from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import quote_html

from data.config import CHAT_ID
from loader import dp, bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Упс... Вы ввели что-то не понятное.\n\n"
                         f"Подробная информация о боте по команде /help")
    text = f"Сообщение от пользователя " \
           f"{message.from_user.get_mention(as_html=True)} : {quote_html(message.text)}"
    await bot.send_message(chat_id=CHAT_ID, text=text)


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Упс... Вы ввели что-то не понятное.\n\n"
                         f"Подробная информация о боте по команде /help\n"
                         f"Вы в состоянии <code>{state}</code>.")
    text = f"Сообщение от пользователя " \
           f"{message.from_user.get_mention(as_html=True)} : {quote_html(message.text)}"
    await bot.send_message(chat_id=CHAT_ID, text=text)
