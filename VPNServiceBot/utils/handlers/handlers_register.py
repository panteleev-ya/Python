from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import filters
import datetime
from datetime import timedelta

from utils.keyboards import *
from utils.local_variable.prices import *
from utils.local_variable.subscription_durations import *
from utils.generate_promo import generate_promo

from utils.storage.storage import storage, store_json
from utils.local_variable.promos import promos
from utils.local_variable.accounts import get_account, accounts


class FSMRegisterUser(StatesGroup):
    choose_server = State()  # Step 1: Choose server
    choose_sub_dur = State()  # Step 2: Choose subscription duration
    use_promo = State()  # Step 3: Use PROMO if you have it
    input_promo = State()  # If Step 3 result is "I do have promo!" - input promo
    payment = State()  # Step 4: Pay for subscription


# /register
# Задаем состояние "Выбор сервера"
async def register_user_handler(message: types.Message, state: FSMContext):
    # Создаем запись в базе данных для нового пользователя
    async with state.proxy() as data:
        username = str(message.from_user.username)
        if username in storage:
            await message.reply(user_already_exist_message)
        else:
            data[username] = {
                'login': '',
                'password': '',
                'server': '',
                'exp_year': '',
                'exp_month': '',
                'exp_day': '',
                'referral_from_code': '',
                'referral_code': '',
                'price_next_time': default_price
            }
            await FSMRegisterUser.choose_server.set()
            await message.reply(register_user_message, reply_markup=servers_keyboard)


# Выбрали сервер.
# Записываем выбор в бд и задаем состояние "Выбор продолжительности подписки"
# Если выбор некорректен - сообщаем пользователю
async def choose_server_handler(message: types.Message, state: FSMContext):
    if message.text in servers_texts:
        username = str(message.from_user.username)
        async with state.proxy() as data:
            data[username]['server'] = message.text
        await FSMRegisterUser.choose_sub_dur.set()
        await message.reply(choose_sub_dur_message, reply_markup=sub_dur_keyboard)
    else:
        await message.reply(not_a_option_message)


# Выбрали продолжительность подписки.
# Записываем выбор в бд и задаем состояние "Ввод промокода"
async def choose_sub_dur_handler(message: types.Message, state: FSMContext):
    if message.text in sub_dur_texts:
        username = str(message.from_user.username)
        async with state.proxy() as data:
            now = datetime.datetime.now()
            delta = timedelta(days=durations[message.text])
            expiration_date = now + delta
            data[username]['exp_year'] = str(expiration_date.year)
            data[username]['exp_month'] = str(expiration_date.month)
            data[username]['exp_day'] = str(expiration_date.day)
        await FSMRegisterUser.use_promo.set()
        await message.reply(use_promo_message, reply_markup=promo_keyboard)
    else:
        await message.reply(not_a_option_message)


# Выбираем вводить ли промокод
#   Если вводим - состояние "Ввод промокода"
#   Если не вводим - состояние "Оплатить"
async def use_promo_handler(message: types.Message, state: FSMContext):
    if message.text in promo_texts:
        if message.text == i_have_promo:
            await FSMRegisterUser.input_promo.set()
            await message.reply(input_promo_message)
        else:
            await FSMRegisterUser.payment.set()
            await message.reply(payment_requisites)
    else:
        await message.reply(not_a_option_message)


# Вводим промокод
# Если промокод валидный - применяем и переходим в состояние "Оплата"
# Если промокод не существует - предлагаем пользователю ввести другой промокод, либо пропустить данный шаг.
# Если шаг пропускается командой /skip - переходим в состояние "Оплата"
async def input_promo_handler(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await FSMRegisterUser.payment.set()
        await message.reply(payment_requisites)
    elif message.text in promos["users"]:
        username = str(message.from_user.username)
        async with state.proxy() as data:
            data[username]['referral_from_code'] = message.text
            data[username]['price_next_time'] = 330
        await FSMRegisterUser.payment.set()
        # await state.finish()
        await message.reply(input_promo_success_message)
        await message.answer(payment_requisites)
    else:
        await message.reply(input_promo_failed_message)


# Оплачиваем подписку
# Пока что просто выводим текст о необходимости произвести оплату (еще на предыдущем шаге)
async def payment_handler(message: types.Message, state: FSMContext):
    username = str(message.from_user.username)
    async with state.proxy() as data:
        promo = generate_promo(username)

        data[username]['referral_code'] = promo
        # account = get_account()
        # data[username]['login'] = account[0]
        # data[username]['password'] = account[1]

        promos["users"].append(promo)
        storage[username] = data[username]
        store_json("utils/storage/storage.json", storage)
        store_json("utils/storage/promos.json", promos)
        # store_json("utils/storage/accounts.json", accounts)

    await state.finish()

    msg = """
    Оплата прошла успешно! Регистрация завершена, ваши логин и пароль будут высланы позднее
    """
    # msg = """
    # """
    await message.reply(msg, reply_markup=types.ReplyKeyboardRemove())


# Если пользователь передумал или хочет начать заново
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.reply(option_canceled_message, reply_markup=types.ReplyKeyboardRemove())


# /status
async def register_status_handler(message: types.Message):
    await message.reply(register_status_message)


def register_handlers_register(_dp: Dispatcher):
    # Состояния нет (None)
    _dp.register_message_handler(register_user_handler, commands=['register'], state=None)

    # Отмена любого состояния - перевод его в None
    _dp.register_message_handler(cancel_handler, commands=['cancel'], state="*")

    # Обработка состояний регистрации пользователя
    _dp.register_message_handler(choose_server_handler, content_types=['text'], state=FSMRegisterUser.choose_server)
    _dp.register_message_handler(choose_sub_dur_handler, content_types=['text'], state=FSMRegisterUser.choose_sub_dur)
    _dp.register_message_handler(use_promo_handler, content_types=['text'], state=FSMRegisterUser.use_promo)
    _dp.register_message_handler(input_promo_handler, content_types=['text'], state=FSMRegisterUser.input_promo)
    _dp.register_message_handler(payment_handler, content_types=['text'], state=FSMRegisterUser.payment)


register_user_message = """
Какой сервер предпочтете?
"""

user_already_exist_message = """
Вы уже зарегистрированы!
"""

choose_sub_dur_message = """
На какой срок вы хотите оформить подписку?
"""

register_status_message = """
Ваш статус заявки:
"""

use_promo_message = """
У вас есть реферальный промокод?
"""

input_promo_message = """
Введите реферальный промокод
"""

input_promo_success_message = """
Промокод применен!
"""

input_promo_failed_message = """
Такого промокода не существует! Введите валидный промокод или /skip для пропуска данного шага
"""

payment_requisites = """
Пожалуйста, оплатите подписку по следующим реквизитам. 
В комментарии к оплате укажите свой ник в Телеграм. 
После оплаты вам будут высланы логин и пароль для доступа к сервису!
"""

option_canceled_message = """
Операция успешно отменена!
"""

not_a_option_message = """
Такого варианта ответа не существует!
Пожалуйста, выберите один из ответов на встроенной клавиатуре и нажмите на него
Либо отмените операцию командой /cancel
"""


