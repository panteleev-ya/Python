from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
from datetime import timedelta

from utils.locals.data.keyboards import *
from utils.locals.data.subscription_options import prices, subscription_durations
from utils.locals.data.admins import admin_chat_id
from utils.locals.data.bot_init import bot

from utils.locals.data.users import users, save_users


# /certificate
# Sending CA-certificate to user
async def get_cert_handler(message: types.Message):
    await message.answer_document(open("utils/new_cert.pem", "rb"), caption="Ваш сертификат доступа")

# TODO add handlers for /connect, /info, /faq


def register_handlers_support(_dp: Dispatcher):
    _dp.register_message_handler(get_cert_handler, commands=['certificate'])
