from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Reading TOKEN from file
token = open("utils/token.txt", "r").read()

# Storage initializing
storage = MemoryStorage()

# Global variable initialization
# servers_list = [server[:-1] for server in open("servers_list.txt", "r").readlines()]

# Initializing Bot and Dispatcher
bot = Bot(token, parse_mode=None)
dp = Dispatcher(bot, storage=storage)
