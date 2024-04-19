import asyncio
import requests
from aiogram import Bot, Dispatcher, types
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

field_mapper = {
    "cost": "entry.1441644747",
    "category": "entry.767764842",
    "card_number": "entry.1727782915",
    "bank": "entry.412290270",
    "owner": "entry.873461443",
    "purpose": "entry.1063838522",
}

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


class RegisterPurchaseFSM(StatesGroup):
    input_cost = State()
    select_category = State()
    input_card_number = State()
    select_bank = State()
    input_purpose = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await message.reply("Привет! Для регистрации покупки отправь /purchase")


# Обработчик команды /purchase
@dp.message_handler(commands=['purchase'], state=None)
async def register_purchase(message: types.Message, state: FSMContext):
    await RegisterPurchaseFSM.input_cost.set()
    await message.reply("Давайте зарегистрируем покупку. Введите стоимость в $:")
    # async with state.proxy() as data:
    #     username = str(message.from_user.username)
    #     data[username] = {
    #         "username": username
    #     }
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for category in categories:
    #     keyboard.add(category)
    # await message.reply("Категория:", reply_markup=keyboard)


# Обработчик ввода стоимости покупки
@dp.message_handler(state=RegisterPurchaseFSM.input_cost)
async def input_cost(message: types.Message, state: FSMContext):
    # FIXME
    await message.reply("Введена стоимость покупки")
    # try:
    #     cost = float(message.text)
    #     user_id = message.from_user.id
    #     # Получаем данные пользователя
    #     data = await dp.storage.get_data()
    #     bank = data.get('bank')
    #     category = data.get('category')
    #     # Заполняем данные для Google формы
    #     form_data = {
    #         "entry.1441644747": str(cost),
    #         "entry.767764842": category,
    #         "entry.1727782915": "",  # Пока пустое, так как нет поля для номера карты
    #         "entry.412290270": bank,
    #         "entry.873461443": str(user_id),  # Используем chat_id в качестве owner
    #         "entry.1063838522": "",  # Пока пустое, так как нет поля для назначения платежа
    #     }
    #     user_agent = {
    #         "Referer": form_view_url,
    #         "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    #     }
    #     # Отправляем данные в Google форму
    #     requests.post(form_response_url, data=form_data, headers=user_agent)
    #     await message.reply("Покупка зарегистрирована")
    # except ValueError:
    #     await message.reply("Некорректная стоимость. Пожалуйста, отправьте число.")


# Обработчик выбора категории
@dp.message_handler(state=RegisterPurchaseFSM.select_category)
async def select_category(message: types.Message, state: FSMContext):
    # FIXME
    await message.reply("Выбрана категория")
    # category = message.text
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for bank in banks:
    #     keyboard.add(bank)
    # await message.reply(f"Категория выбрана: {category}. Теперь выбери банк:", reply_markup=keyboard)


# Обработчик ввода номера карты
@dp.message_handler(state=RegisterPurchaseFSM.input_card_number)
async def input_card_number(message: types.Message, state: FSMContext):
    # FIXME
    await message.reply("Введен номер карты")


# Обработчик выбора банка
@dp.message_handler(state=RegisterPurchaseFSM.select_bank)
async def select_bank(message: types.Message, state: FSMContext):
    # FIXME
    await message.reply("Выбран банк")
    # bank = message.text
    # user_id = message.from_user.id
    # await message.reply(f"Банк выбран: {bank}. Теперь отправь стоимость покупки:")
    # # Сохраняем состояние выбора банка и chat_id пользователя
    # await dp.storage.update_data(user_id=user_id, bank=bank)


# Обработчик ввода причины
@dp.message_handler(state=RegisterPurchaseFSM.input_purpose)
async def input_purpose(message: types.Message, state: FSMContext):
    # FIXME
    await message.reply("Введена причина")


# Функция для обработки ошибок
async def error_handler(_, exception):
    print(f"Exception while handling an update: {exception}")


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


async def on_startup(_dp):
    await bot.set_webhook("")
    await _dp.storage.connect()


async def on_shutdown(_dp):
    await bot.session.close()
    await _dp.storage.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
