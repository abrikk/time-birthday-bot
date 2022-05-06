from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.lang_middleware import _

manual_data = CallbackData("manual", "button")


def help_manual():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = {
        _("Возможности бота"): "ability",
        _("Информация о боте"): "botinfo",
        _("Доступные форматы"): "formats",
        _("Список команд"): "commands",
        _("Оценить бота"): "rate"
    }

    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text,
                callback_data=manual_data.new(button=data),
            )
        )

    return markup


ability_data = CallbackData("instruction", "page", "action")


def help_ability(max_pages: int, page: int = 1):
    markup = InlineKeyboardMarkup()
    previous_page = page - 1
    previous_page_text = "<<"

    current_page_text = _("{page} из {max_pages}").format(page=page, max_pages=max_pages)

    next_page = page + 1
    next_page_text = ">>"

    markup.insert(
        InlineKeyboardButton(
            text=previous_page_text,
            callback_data=ability_data.new(page=previous_page, action="left")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=ability_data.new(page=page, action="just_answer")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=next_page_text,
            callback_data=ability_data.new(page=next_page, action="right")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data=ability_data.new(page="back", action="back_manual")
        )
    )

    return markup


date_order_cb = CallbackData("preferred_date_order", "order")


def help_back_manual(where: str = None, preferred_date_order: str = None,
                     page: int = 1):
    markup = InlineKeyboardMarkup()
    if where == "avl_formats":
        markup.add(
            InlineKeyboardButton(
                text=_("Предпочитаемый формат: {date_order}").format(date_order=preferred_date_order),
                callback_data=date_order_cb.new(order=page)
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data="back_manual"
        )
    )

    return markup


rate_data = CallbackData("rating", "rate")


def help_rate():
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5"
    }

    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text,
                callback_data=rate_data.new(rate=data),
            )
        )

    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data="back_manual"
        )
    )

    return markup
