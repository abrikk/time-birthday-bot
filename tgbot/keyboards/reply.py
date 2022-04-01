from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.lang_middleware import _


def main_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    my_profile = _("👤 Мой профиль")
    markup.add(KeyboardButton(my_profile))

    buttons = [[_('🎊 У кого сегодня день рождение'), _('🌐 Поменять язык')],
               [_('🌀 Прочее'), _('❔ Помощь')]]

    for text_1, text_2 in buttons:
        markup.add(KeyboardButton(text_1),
                   KeyboardButton(text_2))

    return markup


def additional_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [[_('🥳 Моё день рождение'), _('🎊 Праздники [beta]')],
               [_('🔢 Номер дня в году'), _('⏳ Сколько дней')]]
    for text_1, text_2 in buttons:
        markup.add(KeyboardButton(text_1),
                   KeyboardButton(text_2))

    markup.add(KeyboardButton(text=_("↪️ Назад в главное меню")))
    return markup


hol_cb = CallbackData("holidays", "hol_name")


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
                callback_data=hol_cb.new(hol_name=data)
            )
        )
    return markup


inter_hol_cb = CallbackData("inter_holidays", "hol_name")


def inter_holidays_keyb(buttons: dict):
    markup = InlineKeyboardMarkup(row_width=1)

    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=inter_hol_cb.new(hol_name=data)
            )
        )
    markup.add(InlineKeyboardButton(text=_("Назад"),
                                    callback_data=inter_hol_cb.new(hol_name="back_holiday")))
    return markup


hol_pag_cb = CallbackData("hol_pg", "page", "action")


def change_hol_keyb(page: int = 1):
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text="<<",
            callback_data=hol_pag_cb.new(page=page - 1, action="left")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=_("Поделиться"),
            callback_data=hol_pag_cb.new(page=page, action="share_message")
        )
    )

    markup.insert(
        InlineKeyboardButton(
            text=">>",
            callback_data=hol_pag_cb.new(page=page + 1, action="right")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data=hol_pag_cb.new(page=page, action="back_inter")
        )
    )
    return markup


def back_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text=_("↪️ Назад")))
    return markup


def cancel_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text=_("↪️ Назад в главное меню")))
    return markup


lang_cb = CallbackData("language", "name")

lang_keyb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data=lang_cb.new(name="en")),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data=lang_cb.new(name="ru"))
        ],
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data=lang_cb.new(name="uz")),
            InlineKeyboardButton(text="🇺🇦 Український", callback_data=lang_cb.new(name="uk"))
        ],
        [
            InlineKeyboardButton(text="🇪🇸 Español", callback_data=lang_cb.new(name="es")),
            InlineKeyboardButton(text="🇫🇷 Français", callback_data=lang_cb.new(name="fr"))
        ]
    ]
)


def share_message(action: str):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(
        text=_("Поделиться сообщением"),
        switch_inline_query=action
    ))

    return markup


def switch_to_bot():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(
        text=_("Перейти к боту"),
        url="t.me/totalyclearbot"
    ))

    return markup


switch_or_gratz_cb = CallbackData("gratz", "birthday_man_id")


def switch_or_gratz(user_bday: int):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Поздравить"),
            callback_data=switch_or_gratz_cb.new(birthday_man_id=str(user_bday))
        ),
        InlineKeyboardButton(
            text=_("Перейти к боту"),
            url="t.me/totalyclearbot"
        )
    )

    return markup


def profile_back_manual():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data="back_profile"
        )
    )

    return markup
