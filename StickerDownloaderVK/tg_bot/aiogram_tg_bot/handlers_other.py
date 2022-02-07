from aiogram import types, Dispatcher
from keyboards import *


async def send_help_message(message: types.Message):
    await message.reply("Привет! Чем я могу помочь? Вот мой список команд:", reply_markup=markup_1)


async def no_filters_handler(message: types.Message):
    await message.reply("Просто текст")


def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_help_message, commands=['help'])
    _dp.register_message_handler(no_filters_handler)
