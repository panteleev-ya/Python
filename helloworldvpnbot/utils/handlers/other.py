from aiogram import types, Dispatcher
from aiogram.dispatcher import filters

from utils.messages.other import *


# Command /start handler
async def send_welcome_handler(message: types.Message):
    await message.reply(welcome_message, parse_mode='markdown')


# Command /help handler
async def send_help_handler(message: types.Message):
    # commands = available_commands_message
    # for command in commands_list:
    #     commands += command + "\n"
    # await message.reply(commands)
    await message.reply(help_message, parse_mode='markdown')


# Say "Your welcome!" to user if he tells "Thank you!" to the bot
async def be_polite_handler(message: types.Message):
    await message.reply(you_are_welcome_message, parse_mode='markdown')


# Unknown command handler
async def no_filters_handler(message: types.Message):
    await message.reply(unknown_command_message, parse_mode='markdown')


# Registering handlers function
def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_welcome_handler, commands=['start'])
    _dp.register_message_handler(send_help_handler, commands=['help'])
    _dp.register_message_handler(be_polite_handler, filters.Text(contains=['Спасибо'], ignore_case=True))
    _dp.register_message_handler(no_filters_handler)
