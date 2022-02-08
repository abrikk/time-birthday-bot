from aiogram import types, Dispatcher


async def all_answer(call: types.CallbackQuery):
    await call.answer(cache_time=5)


def register_all_cq_answer(dp: Dispatcher):
    dp.register_message_handler(all_answer, state="*")
