from aiogram import types, Dispatcher

from utils.locals.data.accounts import get_account
from utils.locals.data.bot_init import bot
from utils.locals.data.users import users, save_users
from utils.locals.data.admins import admin_chat_id

from utils.filters.admin import AdminApplyPayment


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
            user_msg = f"""
            Ваш платеж подтвержден!\nНапишите /info чтобы узнать все о вашей подписке
            """
            await bot.send_message(users[username]['user_id'], user_msg)

            # ... to admins chat
            msg = f"""
            {username} : платеж успешно подтвержден
            """
            await bot.send_message(admin_chat_id, msg, reply_markup=types.ReplyKeyboardRemove())
        else:
            msg = f"""
            {username} нет в списке пользователей!
            """
            await bot.send_message(admin_chat_id, msg, reply_markup=types.ReplyKeyboardRemove())

    # Saving result
    save_users(users)


# Registering handlers function
def register_handlers_admin(_dp: Dispatcher):
    _dp.register_message_handler(apply_payment_handler, AdminApplyPayment())
