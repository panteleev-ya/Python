from aiogram import types, Dispatcher
# from aiogram.types import ContentType

from utils.locals.data.accounts import get_account
from utils.locals.data.bot_init import bot
from utils.locals.data.users import users, save_users
from utils.locals.data.admins import admin_chat_id

from utils.messages.admin import *


# Manually applying user payment
async def apply_payment_handler(message: types.Message):
    # Getting list of users to apply their payments
    users_to_apply = message.get_args().split()
    for username in users_to_apply:
        if username in users:
            # Getting account
            account = get_account()
            login = account[0]
            password = account[1]

            # Getting current user
            user = users[username]

            # Giving him an account
            user['login'] = login
            user['password'] = password

            # Applying payment
            user['paid'] = 1

            # Sending message that current user payment got applied
            # ... to current user
            await bot.send_message(users[username]['user_id'], payment_applied_message)

            # ... to admins chat
            await bot.send_message(admin_chat_id, f"`{username}`\n-> Платеж успешно подтвержден", reply_markup=types.ReplyKeyboardRemove(), parse_mode='markdown')
        else:
            await bot.send_message(admin_chat_id, f"`{username}`\n-> Нет в списке пользователей!", reply_markup=types.ReplyKeyboardRemove(), parse_mode='markdown')

    # Saving result
    save_users(users)


# # Returning photo ID if photo got sent
# async def return_photo_id(message: types.Message):
#     photo_id = max(message.photo, key=lambda x: x.height).file_id
#     await message.answer(f"Photo ID is: `{photo_id}`", parse_mode='markdown')
#     await message.delete()
#
#
# # Sending photo by id
# async def send_photo_by_id(message: types.Message):
#     photo_id = "AgACAgIAAx0CaVbYGQADAmJcSi3MdR8e0y9Kv-A9Zvmr81CSAAJ-vDEb_HDgSnmSqKwyMpEYAQADAgADeQADJAQ"
#     await message.answer_photo(photo_id)


# Registering handlers function
def register_handlers_admin(_dp: Dispatcher):
    _dp.register_message_handler(apply_payment_handler, commands=['apply'])
    # _dp.register_message_handler(send_photo_by_id, commands=['send_photo'])
    # _dp.register_message_handler(return_photo_id, content_types=[ContentType.PHOTO])
