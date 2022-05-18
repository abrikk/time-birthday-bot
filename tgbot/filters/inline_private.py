from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class PrivateInlineFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        via = message.via_bot
        if not via:
            return False
        bot = await message.bot.me
        return via.username == bot.username



