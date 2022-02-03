from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command

from tgbot.keyboards.reply import main_keyb, additional_keyb
from tgbot.middlewares.lang_middleware import _, __


async def cancel_action(message: types.Message, state: FSMContext):
    await state.reset_state()
    if message.text == "/cancel":
        await message.answer(_("Что бы там ни было - отменено. Что еще я могу сделать для вас?"))
    else:
        await message.answer(_("• Главное меню •"), reply_markup=main_keyb())


async def cancel_other_action(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(_("• Прочее •"), reply_markup=additional_keyb())


def register_cancel_action(dp: Dispatcher):
    dp.register_message_handler(cancel_action, Command("cancel") | Text(contains=__("↪️ Назад в главное меню"),
                                                                        ignore_case=True), state="*")
    dp.register_message_handler(cancel_other_action, Text(contains=__("↪️ Назад"),
                                                                        ignore_case=True), state="*")
