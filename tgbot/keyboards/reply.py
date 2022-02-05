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

    # rate_button = _("🌟 Оценить этого бота")
    # markup.add(KeyboardButton(rate_button))

    return markup


def additional_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = [[_('🥳 Моё день рождение'), _('⛄️ Новый Год')],
               [_('🔢 Номер дня в году'), _('⏳ Сколько дней')]]
    for text_1, text_2 in buttons:
        markup.add(KeyboardButton(text_1),
                   KeyboardButton(text_2))

    markup.add(KeyboardButton(text=_("↪️ Назад в главное меню")))
    return markup


def choose_dy_keyb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = [[_('Текущая дата'), _('Конкретная дата')]]
    for text_1, text_2 in buttons:
        markup.add(KeyboardButton(text_1),
                   KeyboardButton(text_2))
    markup.add(KeyboardButton(text=_("↪️ Назад")))
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

upd_profile = CallbackData("update", "profile")


def update_profile():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Изменить Имя"),
            callback_data=upd_profile.new(profile="name")
        ),
        InlineKeyboardButton(
            text=_("Изменить дату"),
            callback_data=upd_profile.new(profile="bd")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=_("Изменить Пол"),
            callback_data=upd_profile.new(profile="sex")
        ),
        InlineKeyboardButton(
            text=_("Статистика"),
            callback_data=upd_profile.new(profile="statistics")
        )
    )

    return markup


def update_bot_info():
    markup = InlineKeyboardMarkup()

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

    return markup


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


def switch_or_gratz():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Поздравить"),
            callback_data=bd_data.new(page="None", action="gratz")
        ),
        InlineKeyboardButton(
            text=_("Перейти к боту"),
            url="t.me/totalyclearbot"
        )
    )


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


sex_data = CallbackData("choose", "sex", "where")


def choosing_sex(where):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Мужской 👨"),
            callback_data=sex_data.new(sex="1", where=where)
        ),
        InlineKeyboardButton(
            text=_("Женский 👩"),
            callback_data=sex_data.new(sex="2", where=where)
        )
    )

    return markup


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
            callback_data=ability_data.new(page=page, action="current_page")
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


def help_back_manual():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text=_("Назад"),
            callback_data="back_manual"
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
