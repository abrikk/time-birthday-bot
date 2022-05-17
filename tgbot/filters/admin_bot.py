from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class AdminOfBot(BoundFilter):
    """Checks whether the user is an admin of the bot"""
    async def check(self, obj) -> bool:
        print("TEXT FROM FILTER")
        data = ctx_data.get()
        return data.get("role") == "admin"
