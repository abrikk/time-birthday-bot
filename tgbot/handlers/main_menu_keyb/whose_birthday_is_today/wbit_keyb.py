from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.lang_middleware import _

bd_data = CallbackData("bd_people", "page", "action")


def bd_today_list(max_pages: int, page: int = 1):
    markup = InlineKeyboardMarkup()
    previous_page = page - 1
    previous_page_text = "<<"

    current_user_text = _("Поздравить")
    current_page_text = _("{page} из {max_pages}").format(page=page, max_pages=max_pages)

    next_page = page + 1
    next_page_text = ">>"

    markup.insert(
        InlineKeyboardButton(
            text=previous_page_text,
            callback_data=bd_data.new(page=previous_page, action="left")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=bd_data.new(page=page, action="current_page")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=next_page_text,
            callback_data=bd_data.new(page=next_page, action="right")
        )
    )

    markup.add(
        InlineKeyboardButton(
            text=current_user_text,
            callback_data=bd_data.new(page=page, action="gratz")
        )
    )

    return markup
