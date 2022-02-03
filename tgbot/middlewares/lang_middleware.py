from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from typing import Tuple, Any
from aiogram import types

I18N_DOMAIN = 'multilang'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / '../../locales'


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        user = types.User.get_current()
        db_commands = args[1]['db_commands']
        lang = await db_commands.get_user_language(user_id=int(user.id))
        return lang or user.locale


i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)

_ = i18n.gettext
__ = i18n.lazy_gettext
