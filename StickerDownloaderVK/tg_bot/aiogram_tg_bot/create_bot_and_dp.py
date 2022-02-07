from aiogram import Bot
from aiogram.dispatcher import Dispatcher

# Reading TOKEN from file
token = open("token.txt", "r").read()

# Initializing Bot and Dispatcher
bot = Bot(token, parse_mode=None)
dp = Dispatcher(bot)
