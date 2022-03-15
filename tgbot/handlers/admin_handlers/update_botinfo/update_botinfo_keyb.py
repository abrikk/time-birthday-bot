from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.middlewares.lang_middleware import _


def update_bot_info(where: str = "call_help"):
    markup = InlineKeyboardMarkup()
    if where == "call_help":
        markup.add(
            InlineKeyboardButton(
                text=_("Назад"),
                callback_data="back_manual"
            ),
            InlineKeyboardButton(
                text=_("Обновить"),
                callback_data="update_date_info"
            )
        )
    elif where == "msg_cmnd":
        markup.add(
            InlineKeyboardButton(
                text=_("Обновить"),
                callback_data="update_date_info"
            )
        )

    return markup
