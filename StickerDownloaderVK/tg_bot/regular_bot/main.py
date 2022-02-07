import telebot
from downloader import *
from url_generators import *
from messages import *
from reply_keyboard_markups import *

token = open("token.txt", "r").read()
# print(token)
bot = telebot.TeleBot(token, parse_mode=None)
markups = KeyboardMarkup(bot)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, send_welcome_message)
    bot.send_message(message.from_user.id, "Для начала выбери, как ты хочешь скачать стикеры",
                     reply_markup=markups.choose_stickers_type(message))


@bot.message_handler(func=lambda m: m.text == "Скачать стикер-пак целиком", content_types=['text'])
def download_stickers_by_range(message):
    pass


@bot.message_handler(func=lambda m: m.text == "Скачать отдельные стикеры", content_types=['text'])
def download_stickers_by_list(message):
    pass


bot.infinity_polling()
