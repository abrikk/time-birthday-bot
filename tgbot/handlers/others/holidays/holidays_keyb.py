from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from tgbot.middlewares.lang_middleware import _

# HOLIDAYS KEYBOARD
hol_cb = CallbackData("holidays", "hol_type_name")


def holidays_keyb():
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = {
        _("Международные праздники"): "ih",
        _("Праздник сегодня"): "todayh",
        _("smth"): "ny",
    }

    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=hol_cb.new(hol_type_name=data)
            )
        )
    return markup


# INTERNATIONAL HOLIDAYS KEYBOARD
inter_hol_cb = CallbackData("inter_holidays", "action", "page", "hol_uid")


def inter_holidays_keyb(buttons: dict, max_pages: int, page: int = 1):
    markup = InlineKeyboardMarkup(row_width=5)

    for text, data in buttons.items():
        markup.add(
            InlineKeyboardButton(
                text=text,
                callback_data=inter_hol_cb.new(action="show_hol", page="hol_page", hol_uid=data)
            )
        )

    markup.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=inter_hol_cb.new(action="switch_page", page=page - 9, hol_uid="nleft")
        )
    )
    another_data = {
        "<": ("switch_page", page - 1, "oleft"),
        _("{page}/{max_pages}").format(page=page, max_pages=max_pages):
            ("just_answer", "current_page", "none"),
        ">": ("switch_page", page + 1, "oright"),
        ">>": ("switch_page", page + 9, "nright")
    }
    for text, data in another_data.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=inter_hol_cb.new(action=data[0], page=data[1], hol_uid=data[2])
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data=inter_hol_cb.new(action="back_inter", page="back_hol_page",
                                           hol_uid="back_holiday")
        )
    )
    return markup


# HOLIDAY DETAILS KEYBOARD
hol_pag_cb = CallbackData("hol_pg", "action", "page")


def change_hol_keyb(max_pages: int, page: int = 1, admin: bool = False):
    markup = InlineKeyboardMarkup(row_width=5)
    markup.add(
        InlineKeyboardButton(
            text="👍",
            callback_data=hol_pag_cb.new(page="none", action="like")
        ),
        InlineKeyboardButton(
            text=_("{page} из {max_pages}").format(page=page, max_pages=max_pages),
            callback_data=hol_pag_cb.new(page="current_page", action="switch_page")
        ),
        InlineKeyboardButton(
            text="👎",
            callback_data=hol_pag_cb.new(page="none", action="dislike")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=hol_pag_cb.new(action="nleft", page=page - 9)
        )
    )
    buttons = {
        "<": ("oleft", page - 1),

        ">": ("oright", page + 1),
        ">>": ("nright", page + 9),
    }
    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=hol_pag_cb.new(action=data[0], page=data[1])
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=_("Поделиться"),
            callback_data=hol_pag_cb.new(action="share_message", page=page)
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data=hol_pag_cb.new(action="back_inter", page=page)
        )
    )
    if admin:
        markup.add(
            InlineKeyboardButton(
                text=_("Настройки"),
                callback_data=hol_pag_cb.new(action="settings", page=page)
            )
        )

    return markup


# SETTINGS BUTTON
sett_cb = CallbackData("hol_sett", "action", "page")


def hol_settings_keyboard(page: int):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=_("Изменить изображение"),
            callback_data=sett_cb.new(action="img", page=page)
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data=sett_cb.new(action="back", page=page)
        )
    )
    return markup


def confirm_chane():
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text="❌",
            callback_data="cancel_pic_change"
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="✅",
            callback_data="confirm_pic_change"
        )
    )
    return markup
