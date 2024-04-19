import asyncio

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Замените на ваш токен бота
BOT_TOKEN = open("token.txt", "r").read().strip()

# Замените на ссылку на вашу Google форму
form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLSfGxx6rqHDIjujNeSCr-NBLxry_ZmnVT6s5oWvFmu_-y0sQMQ"
form_response_url = f"{form_url_base}/formResponse"
form_view_url = f"{form_url_base}/viewForm"

categories = [
    "Miscellaneous", "Dining", "Bills",
    "Grocery and disposables", "Gas",
    "Buying something", "Entertainments",
    "Beauty products",
]

banks = [
    "Sber", "Tinkoff", "Alpha",  # russian
    "Chase", "AmEx", "Capital One", "Discover",  # american credit cards
    "TD Bank", "BofA",  # american debit cards
    "BNB", "Statusbank",  # belarus
]

known_users = {
    "370021575": "Yarik",
    "908892026": "Yana"
}

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class RegisterPurchaseFSM(StatesGroup):
    input_cost = State()
    select_category = State()
    input_card_number = State()
    select_bank = State()
    input_purpose = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in known_users:
        await message.reply("Я не знаю такого пользователя как вы, команды недоступны")
    else:
        await message.reply("Привет! Для регистрации покупки отправь /purchase")


# Обработчик команды /purchase
@dp.message_handler(commands=['purchase'], state="*")
async def register_purchase(message: types.Message):
    await RegisterPurchaseFSM.input_cost.set()
    await message.reply("Давайте зарегистрируем покупку. Введите стоимость в $:")


# Обработчик ввода стоимости покупки
@dp.message_handler(state=RegisterPurchaseFSM.input_cost)
async def input_cost(message: types.Message, state: FSMContext):
    try:
        cost = float(str(message.text).replace(",", "."))
        await RegisterPurchaseFSM.next()
        await state.update_data(cost=cost)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            keyboard.add(category)
        await message.reply("Выберите категорию:", reply_markup=keyboard)
    except ValueError:
        await message.reply("Некорректная стоимость. Пожалуйста, отправьте число.",
                            reply_markup=types.ReplyKeyboardRemove())


# Обработчик выбора категории
@dp.message_handler(lambda message: message.text in categories, state=RegisterPurchaseFSM.select_category)
async def select_category(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await RegisterPurchaseFSM.next()
    await message.reply("Введите номер карты:", reply_markup=types.ReplyKeyboardRemove())


# Обработчик ввода номера карты
@dp.message_handler(state=RegisterPurchaseFSM.input_card_number)
async def input_card_number(message: types.Message, state: FSMContext):
    card_number = message.text
    await state.update_data(card_number=card_number)
    await RegisterPurchaseFSM.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for bank in banks:
        keyboard.add(bank)
    await message.reply("Выберите банк:", reply_markup=keyboard)


# Обработчик выбора банка
@dp.message_handler(lambda message: message.text in banks, state=RegisterPurchaseFSM.select_bank)
async def select_bank(message: types.Message, state: FSMContext):
    bank = message.text
    await state.update_data(bank=bank)
    await RegisterPurchaseFSM.next()
    await message.reply("Введите цель покупки:", reply_markup=types.ReplyKeyboardRemove())


# Обработчик ввода цели покупки
@dp.message_handler(state=RegisterPurchaseFSM.input_purpose)
async def input_purpose(message: types.Message, state: FSMContext):
    purpose = message.text
    user_id = str(message.from_user.id)
    user = known_users[user_id] if user_id in known_users else user_id
    data = await state.get_data()
    cost = data.get('cost')
    category = data.get('category')
    card_number = data.get('card_number')
    bank = data.get('bank')

    # Заполняем данные для Google формы
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

    # Отправляем данные в Google форму
    _ = requests.post(form_response_url, data=form_data, headers=user_agent)
    await message.reply("Покупка зарегистрирована!")
    await state.finish()


# Функция для обработки ошибок
async def error_handler(_, exception):
    print(f"Exception while handling an update: {exception}")


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
