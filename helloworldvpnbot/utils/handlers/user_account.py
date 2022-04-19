from aiogram import types, Dispatcher

from utils.locals.data.users import users
from utils.messages.user_account import *


# /certificate
# Sending CA-certificate to user
async def get_cert_handler(message: types.Message):
    cert_msg = await message.answer_document(open("utils/vpn_cert.pem", "rb"), caption="Ваш сертификат доступа")
    return cert_msg


# /faq
async def faq_handler(message: types.Message):
    await message.answer(faq_message, parse_mode='markdown')


# /info
# Sending subscription information to user
async def get_info_handler(message: types.Message):
    # Getting username and user from users storage
    username = str(message.from_user.username)
    user = users[username]

    # Getting expiration date
    month = str(user['exp_month'])
    month = "0" + month if len(month) < 2 else month
    day = str(user['exp_day'])
    day = "0" + day if len(day) < 2 else day
    exp_date = f"{day}.{month}.{user['exp_year']}"

    # Getting server name, server IP, login and password
    server_name = user['server']
    ip = user['server_ip']
    login = user['login']
    password = user['password']

    # Generating full message
    seven_spaces = "       "
    info_message = f"Информация об подписке\n\n🗓Дата окончания подписки🗓\n{seven_spaces}{exp_date}\n\n" \
                   f"🌍Регион сервера🌍\n{seven_spaces}{server_name}\n\n💻IP сервера💻\n{seven_spaces}`{ip}`\n\n" \
                   f"🔑Логин🔑\n{seven_spaces}{login}\n\n🔑Пароль🔑\n{seven_spaces}{password} "
    info_msg = await message.answer(info_message, parse_mode="markdown")
    return info_msg


def register_handlers_user_account(_dp: Dispatcher):
    # Everybody has access to /faq
    _dp.register_message_handler(faq_handler, commands=['faq'])

    # Otherwise, he does have it
    _dp.register_message_handler(get_cert_handler, commands=['certificate'])
    _dp.register_message_handler(get_info_handler, commands=['info'])
