from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
say_hi_button = KeyboardButton('Привет!')
markup_1.row(*[say_hi_button, say_hi_button, say_hi_button, say_hi_button])
markup_1.add(say_hi_button, say_hi_button)

