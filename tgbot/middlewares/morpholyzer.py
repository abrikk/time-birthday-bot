from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from pymorphy2 import MorphAnalyzer


class MorphMiddleware(LifetimeControllerMiddleware):

    def __init__(self, morph: MorphAnalyzer):
        super().__init__()
        self._morph = morph

    async def pre_process(self, obj: TelegramObject, data: Dict[str, Any], *args: Any):
        data["morph"] = self._morph
