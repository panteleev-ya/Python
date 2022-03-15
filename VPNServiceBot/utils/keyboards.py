from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора сервера
frankfurt = "Германия, Франкфурт"
london = "Великобритания, Лондон"
servers_texts = [
    frankfurt
]
servers_buttons = [
    KeyboardButton(text) for text in servers_texts
]
servers_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*servers_buttons)

# Клавиатура выбора срока подписки
month = "30 дней"
three_month = "90 дней"
sub_dur_texts = [
    month
]
sub_dur_buttons = [
    KeyboardButton(dur) for dur in sub_dur_texts
]
sub_dur_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*sub_dur_buttons)

# Клавиатура выбора наличия промокода
i_have_promo = "Да, ввести промокод"
i_do_not_have_promo = "Нет, у меня нет промокода"
promo_texts = [
    i_have_promo,
    i_do_not_have_promo
]
promo_buttons = [
    KeyboardButton(promo_option) for promo_option in promo_texts
]
promo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*promo_buttons)
