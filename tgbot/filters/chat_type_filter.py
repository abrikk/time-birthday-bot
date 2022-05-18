import typing
import warnings
from typing import Union

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery, InlineQuery, ChatType, ChatMemberUpdated


class ChatTypeFilter(BoundFilter):
    key = 'chat_type'

    def __init__(self, chat_type: typing.Container[Union[ChatType, str]]):
        if isinstance(chat_type, str):
            chat_type = {chat_type}

        self.chat_type: typing.Set[str] = set(chat_type)

    async def check(self, obj: Union[Message, CallbackQuery, ChatMemberUpdated, InlineQuery]):
        if isinstance(obj, Message):
            chat_type = obj.chat.type
        elif isinstance(obj, CallbackQuery):
            chat_type = obj.message.chat.type
        elif isinstance(obj, ChatMemberUpdated):
            chat_type = obj.chat.type
        elif isinstance(obj, InlineQuery):
            chat_type = obj.chat_type
        else:
            warnings.warn("ChatTypeFilter doesn't support %s as input", type(obj))
            return False

        return chat_type in self.chat_type
