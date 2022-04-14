from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.locals.data.keyboards import *

from utils.messages.support import *
from utils.messages.other import not_an_option_message

from utils.locals.data.users import users, save_users

from utils.filters.paid import UserPaid, UserDidNotPaid, UserDidNotRenew


class GuideFSM(StatesGroup):
    get_guide = State()  # Only state with getting a guide


# /certificate
# Sending CA-certificate to user
async def get_cert_handler(message: types.Message):
    await message.answer_document(open("utils/new_cert.pem", "rb"), caption="Ваш сертификат доступа")


# /faq
async def faq_handler(message: types.Message):
    await message.answer("Нет вопросов - нет ответов🤠🤠🤠.\nВопросы задавайте [администратору](t.me/monokumato)🥳🥳🥳", parse_mode='markdown')


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
    await message.answer(info_message, parse_mode="markdown")


# /connect
# Setting State=Getting guide
# Asking user what OS does he wants guide for
async def ask_connection_guides_handler(message: types.Message, state: FSMContext):
    await GuideFSM.get_guide.set()
    await message.reply(ask_guide_message, reply_markup=os_keyboard)


# Guide messages for iOS, Android and Windows
# Linux and macOS soon
async def get_connection_guides_handler(message: types.Message, state: FSMContext):
    os = {
        "iOS": ios_guide_message,
        "Android": android_guide_message,
        "Windows": windows_guide_message
    }
    if message.text in os:
        await state.finish()
        await message.answer(os[message.text], reply_markup=types.ReplyKeyboardRemove(), parse_mode='markdown')
    else:
        await message.answer(not_an_option_message)


# No access to commands handler
async def no_access_handler(message: types.Message, state: FSMContext):
    await message.reply(no_access_message)


def register_handlers_support(_dp: Dispatcher):
    # Everybody has access to /faq
    _dp.register_message_handler(faq_handler, commands=['faq'], state=None)

    # User didn't pay or didn't renew the subscription - he has no access
    _dp.register_message_handler(no_access_handler, UserDidNotPaid(), commands=['certificate', 'info', 'connect'], state=None)
    _dp.register_message_handler(no_access_handler, UserDidNotRenew(), commands=['certificate', 'info', 'connect'], state=None)

    # Otherwise, he does have it
    _dp.register_message_handler(get_cert_handler, UserPaid(), commands=['certificate'], state=None)
    _dp.register_message_handler(get_info_handler, UserPaid(), commands=['info'], state=None)
    _dp.register_message_handler(ask_connection_guides_handler, UserPaid(), commands=['connect'], state=None)

    # Getting guide
    _dp.register_message_handler(get_connection_guides_handler, UserPaid(), content_types=['text'], state=GuideFSM.get_guide)


