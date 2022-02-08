from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Reading TOKEN from file
token = open("token.txt", "r").read()

# Storage initializing
storage = MemoryStorage()

# Initializing Bot and Dispatcher
bot = Bot(token, parse_mode=None)
dp = Dispatcher(bot, storage=storage)
