from utils.locals.scripts.keyboards_creator import create_inline_keyboard, create_reply_keyboard

# ReplyKeyboards

# Yes or No keyboard
yes_no_texts = [
    "Да",
    "Нет"
]
yes_no_keyboard = create_reply_keyboard(texts=yes_no_texts)

# Choosing server keyboard + cancel
servers_texts = [
    "Вильнюс, Литва",
    # "Франкфурт, Германия"
]
servers_keyboard = create_reply_keyboard(texts=servers_texts, has_cancel=True)

# Choosing subscription duration keyboard + cancel
subscription_durations_texts = [
    "30 дней",
    # "90 дней"
]
subscription_durations_keyboard = create_reply_keyboard(texts=subscription_durations_texts, has_cancel=True)

# Payment keyboard
payment_buttons = [
    ["Оплатить картой", "https://www.tinkoff.ru/rm/panteleev.yaroslav8/j6ZHY46844"],
    # ["Оплатить криптовалютой", "кошелек"]
]
payment_inline_keyboard = create_inline_keyboard(texts_urls=payment_buttons)

# Choosing OS type
os_texts = [
    "iOS",
    "Android",
    "Windows"
]
os_keyboard = create_reply_keyboard(texts=os_texts)
