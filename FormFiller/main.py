import asyncio

import requests
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from sqlite_manager import *

BOT_TOKEN = open("token.txt", "r").read().strip()

form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLSfGxx6rqHDIjujNeSCr-NBLxry_ZmnVT6s5oWvFmu_-y0sQMQ"
form_response_url = f"{form_url_base}/formResponse"
form_view_url = f"{form_url_base}/viewForm"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class RegisterPurchaseFSM(StatesGroup):
    input_cost = State()
    select_category = State()
    input_card_number = State()
    select_bank = State()
    input_purpose = State()


async def delete_previous_messages(chat_id: int):
    message_ids = await get_all_bot_message_ids(chat_id)
    for message_id in message_ids:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await delete_all_bot_message_ids(chat_id)


async def before_reply(message: types.Message):
    await before_reply(message)


# Обработчик команды /start
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    await before_reply(message)
    user_id = str(message.from_user.id)
    if user_id not in known_users:
        await message.reply("Я не знаю такого пользователя как вы, команды недоступны")
    else:
        sent_message = await message.reply("Привет! Для регистрации покупки отправь /purchase")
        await add_bot_message(sent_message)


# Обработчик команды /purchase
@dp.message_handler(commands=['purchase'], state="*")
async def register_purchase(message: types.Message):
    await before_reply(message)
    await RegisterPurchaseFSM.input_cost.set()
    sent_message = await message.reply("Давайте зарегистрируем покупку. Введите стоимость в $")
    await add_bot_message(sent_message)


# Обработчик ввода стоимости покупки
@dp.message_handler(state=RegisterPurchaseFSM.input_cost)
async def input_cost(message: types.Message, state: FSMContext):
    await before_reply(message)
    try:
        cost = float(str(message.text).replace(",", "."))
        await RegisterPurchaseFSM.next()
        await state.update_data(cost=cost)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            keyboard.add(category)
        sent_message = await message.reply("Выберите категорию", reply_markup=keyboard)
        await add_bot_message(sent_message)
    except ValueError:
        sent_message = await message.reply("Некорректная стоимость. Пожалуйста, отправьте число.",
                                           reply_markup=types.ReplyKeyboardRemove())
        await add_bot_message(sent_message)


# Обработчик выбора категории
@dp.message_handler(lambda message: message.text in categories, state=RegisterPurchaseFSM.select_category)
async def select_category(message: types.Message, state: FSMContext):
    await before_reply(message)
    category = message.text
    await state.update_data(category=category)
    await RegisterPurchaseFSM.next()
    sent_message = await message.reply("Введите номер карты", reply_markup=types.ReplyKeyboardRemove())
    await add_bot_message(sent_message)


# Обработчик ввода номера карты
@dp.message_handler(state=RegisterPurchaseFSM.input_card_number)
async def input_card_number(message: types.Message, state: FSMContext):
    await before_reply(message)
    card_number = message.text
    await state.update_data(card_number=card_number)

    bank = await determine_bank_by_card_number(card_number)
    if bank is not None:
        sent_message = await message.reply(f"Банк {bank} автоматически определен по номеру карты {card_number}.")
        await add_bot_message(sent_message)
        sent_message = await message.reply("Введите цель покупки", reply_markup=types.ReplyKeyboardRemove())
        await add_bot_message(sent_message)
        await state.update_data(bank=bank)
        await RegisterPurchaseFSM.input_purpose.set()
    else:
        await RegisterPurchaseFSM.next()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for bank in banks:
            keyboard.add(bank)
        sent_message = await message.reply("Выберите банк", reply_markup=keyboard)
        await add_bot_message(sent_message)


# Обработчик выбора банка
@dp.message_handler(lambda message: message.text in banks, state=RegisterPurchaseFSM.select_bank)
async def select_bank(message: types.Message, state: FSMContext):
    await before_reply(message)
    bank = message.text
    await state.update_data(bank=bank)
    await RegisterPurchaseFSM.next()

    card_number = (await state.get_data()).get('card_number')
    if card_number:
        await map_card_number_to_bank(card_number, bank)

    sent_message = await message.reply(f"Выбран банк: {bank}. Он будет выбираться автоматически для этой карты")
    await add_bot_message(sent_message)
    sent_message = await message.reply("Введите цель покупки", reply_markup=types.ReplyKeyboardRemove())
    await add_bot_message(sent_message)


# Обработчик ввода цели покупки
@dp.message_handler(state=RegisterPurchaseFSM.input_purpose)
async def input_purpose(message: types.Message, state: FSMContext):
    await before_reply(message)
    purpose = message.text
    user_id = str(message.from_user.id)
    user = known_users[user_id] if user_id in known_users else user_id
    data = await state.get_data()
    cost = data.get('cost')
    category = data.get('category')
    card_number = data.get('card_number')
    bank = data.get('bank')

    form_data = {
        "entry.1441644747": str(cost),
        "entry.767764842": str(category),
        "entry.1727782915": str(card_number),
        "entry.412290270": str(bank),
        "entry.873461443": str(user),
        "entry.1063838522": str(purpose),
    }

    user_agent = {
        "Referer": form_view_url,
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }

    _ = requests.post(form_response_url, data=form_data, headers=user_agent)
    sent_message = await message.reply("Покупка зарегистрирована!")
    await add_bot_message(sent_message)
    await state.finish()


async def error_handler(_, exception):
    print(f"Exception while handling an update: {exception}")


async def on_shutdown(_dp):
    await bot.session.close()
    await _dp.storage.close()
    await conn.close()


def main():
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
