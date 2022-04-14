from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Reading bot TOKEN from file
token = open("utils/token.txt", "r").read()

# Memory storage initializing
memory_storage = MemoryStorage()

# Initializing Bot and Dispatcher
bot = Bot(token, parse_mode=None)
dp = Dispatcher(bot, storage=memory_storage)
