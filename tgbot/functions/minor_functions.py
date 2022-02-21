def get_date_order(user_lang: str) -> str:
    date_order = "MDY"
    if user_lang in ["ru", "uz", "uk"]:
        date_order = "DMY"
    elif user_lang in ["en"]:
        date_order = "YMD"
    return date_order
