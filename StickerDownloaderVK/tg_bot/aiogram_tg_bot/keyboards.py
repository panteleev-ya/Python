from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# /download клавиатура
range_download_text = "Скачать стикер-пак целиком"
list_download_text = "Скачать стикеры по-одиночке"
start_download_buttons = [
    KeyboardButton(range_download_text),
    KeyboardButton(list_download_text)
]
start_download_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*start_download_buttons)

# size_input клавиатура
img_sizes = ["64x64", "128x128", "256x256", "512x512"]
img_sizes_hash = {img_sizes[0]: 64, img_sizes[1]: 128, img_sizes[2]: 256, img_sizes[3]: 512}
size_input_buttons = [
    KeyboardButton(s) for s in img_sizes
]
size_input_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*size_input_buttons)
