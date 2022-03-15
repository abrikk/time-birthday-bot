from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.lang_middleware import _

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


upd_profile = CallbackData("update", "profile")


def update_profile():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = {
        _("Изменить Имя"): "name",
        _("Изменить дату"): "bd",
        _("Изменить Пол"): "sex",
        _("Статистика"): "statistics",
        # _("Настройки"): "sett"
    }

    for text, data in buttons.items():
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=upd_profile.new(profile=data)
            )
        )
    # markup.add(
    #     InlineKeyboardButton(
    #         text=,
    #         callback_data=upd_profile.new(profile="name")
    #     ),
    #     InlineKeyboardButton(
    #         text=_("Изменить дату"),
    #         callback_data=upd_profile.new(profile="bd")
    #     )
    # )
    # markup.add(
    #     InlineKeyboardButton(
    #         text=,
    #         callback_data=upd_profile.new(profile="sex")
    #     ),
    #     InlineKeyboardButton(
    #         text=,
    #         callback_data=upd_profile.new(profile="statistics")
    #     )
    # )

    return markup
