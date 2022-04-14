from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Cancel button
cancel_text = "Отмена"


# Creating ReplyKeyboardMarkup
def create_reply_keyboard(texts, has_cancel=False, width=1):
    buttons = [
        KeyboardButton(text) for text in texts
    ]

    if has_cancel:
        # Adding cancel button if required to
        buttons.append(KeyboardButton(cancel_text))

    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=width).add(*buttons)


# Creating InlineKeyboardMarkup
def create_inline_keyboard(texts_urls):
    buttons = []
    for _text, _url in texts_urls:
        buttons.append(InlineKeyboardButton(text=_text, url=_url))
    keyboard = InlineKeyboardMarkup().add(*buttons)
    return keyboard
