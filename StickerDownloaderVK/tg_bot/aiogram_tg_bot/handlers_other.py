from aiogram import types, Dispatcher
from keyboards import *
from messages import *


# /start
async def send_welcome_handler(message: types.Message):
    await message.reply(send_welcome_message)


# /help
async def send_help_handler(message: types.Message):
    await message.reply(send_help_message)


# Неизвестная команда, либо случайное сообщение
async def no_filters_handler(message: types.Message):
    await message.reply(no_filters_message)


def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_welcome_handler, commands=['start'])
    _dp.register_message_handler(send_help_handler, commands=['help'])
    _dp.register_message_handler(no_filters_handler)
