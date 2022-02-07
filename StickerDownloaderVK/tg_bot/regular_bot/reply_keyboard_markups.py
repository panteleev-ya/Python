import telebot


class KeyboardMarkup:
    def __init__(self, bot):
        self.bot = bot

    def choose_stickers_type(self, message):
        stickers_type_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        stickers_type_markup.row("Скачать стикер-пак целиком")
        stickers_type_markup.row("Скачать отдельные стикеры")
        return stickers_type_markup
