from tgbot.handlers.admin_handlers.add_holidays import register_add_holidays
from tgbot.handlers.admin_handlers.admin_commands import register_admin_commands
from tgbot.handlers.admin_handlers.show_all_jobs import register_show_all_tasks
from tgbot.handlers.admin_handlers.statistics import register_stat
from tgbot.handlers.admin_handlers.test import register_test_1
from tgbot.handlers.admin_handlers.update_botinfo.update_botinfo import register_update_botinfo
from tgbot.handlers.admin_handlers.update_hide_links import register_upd_hide_links
from tgbot.handlers.admin_handlers.update_holidays_names import register_update_hols
from tgbot.handlers.answer_callback import register_just_answer
from tgbot.handlers.botinfo import register_bot_info
from tgbot.handlers.cancel_handler import register_cancel_action
from tgbot.handlers.inline_hol_answer import register_inline_hol_answer
from tgbot.handlers.is_active_user import register_is_active_user
from tgbot.handlers.life_counter import register_count_life
from tgbot.handlers.main_menu_keyb.additional_keyboard import register_add_keyb
from tgbot.handlers.main_menu_keyb.change_language import register_change_language
from tgbot.handlers.main_menu_keyb.help.help import register_help
from tgbot.handlers.main_menu_keyb.whose_birthday_is_today.whose_birthday_is_today import register_bd_today
from tgbot.handlers.newyear import register_newyear
from tgbot.handlers.others.birthday import register_my_bd
from tgbot.handlers.others.day_number_in_the_year import register_day_num_year
from tgbot.handlers.others.holidays.holidays import register_all_holidays
from tgbot.handlers.others.holidays.hols_inter import register_inter_holidays
from tgbot.handlers.others.how_many_days import register_hmd
from tgbot.handlers.profile.profile import register_profile
from tgbot.handlers.profile.update_profile import register_update
from tgbot.handlers.start import register_start
from tgbot.keyboards.inline import register_inline_mode


def register_all_handlers(dp):
    register_inline_mode(dp)
    register_cancel_action(dp)
    register_update(dp)
    register_just_answer(dp)
    register_test_1(dp)
    register_update_hols(dp)
    register_show_all_tasks(dp)
    register_upd_hide_links(dp)
    register_my_bd(dp)

    register_add_holidays(dp)
    register_all_holidays(dp)
    register_inter_holidays(dp)

    register_profile(dp)
    register_add_keyb(dp)
    register_stat(dp)
    register_day_num_year(dp)
    register_bd_today(dp)
    register_hmd(dp)
    register_bot_info(dp)
    register_update_botinfo(dp)
    register_newyear(dp)
    register_change_language(dp)
    register_admin_commands(dp)
    register_help(dp)
    register_start(dp)
    register_inline_hol_answer(dp)
    register_count_life(dp)
    register_is_active_user(dp)
