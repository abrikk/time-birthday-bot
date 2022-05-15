from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.lang_middleware import _

bd_data = CallbackData("bd_people", "page", "action")


def bd_today_list(max_pages: int, page: int = 1):
    markup = InlineKeyboardMarkup()
    buttons = {
        "<<": (page - 1, 'left'),
        _("{page} из {max_pages}").format(page=page, max_pages=max_pages): (page, 'just_answer'),
        ">>": (page + 1, 'right'),
        _("Поздравить"): (page, 'gratz')
    }
    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=bd_data.new(page=data[0], action=data[1])
            )
        )

    return markup
