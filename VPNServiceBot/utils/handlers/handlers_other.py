from aiogram import types, Dispatcher
from aiogram.dispatcher import filters


# /start
async def send_welcome_handler(message: types.Message):
    await message.reply(send_welcome_message)


# /help
async def send_help_handler(message: types.Message):
    commands = ""
    for command in commands_list:
        commands += command + "\n"
    await message.reply(available_commands_message + commands)


# Сказать "Пожалуйста! Рад стараться :)"
async def be_polite_handler(message: types.Message):
    await message.reply("Пожалуйста :)")


# Неизвестная команда, либо случайное сообщение
async def no_filters_handler(message: types.Message):
    await message.reply(no_filters_message)


def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_welcome_handler, commands=['start'])
    _dp.register_message_handler(send_help_handler, commands=['help', 'info'])
    _dp.register_message_handler(be_polite_handler, filters.Text(contains=['Спасибо'], ignore_case=True))
    _dp.register_message_handler(no_filters_handler)


send_welcome_message = """
Здравствуйте!
Я - Telegram бот сервиса Hello world! VPN. 
Я помогу вам оформить подписку, расскажу как настроить подключение к сервису и подскажу, сколько еще длится ваша подписка ;)
Вы здесь впервые? Для регистрации и оформления подписки напишите мне /register <-- или нажмите прямо на эту синюю надпись и команда отправится автоматически <3
"""

available_commands_message = """
Список возможных команд:

"""

no_filters_message = """
Извините, команда не распознана! Напиши /help для получения списка возможных команд
"""

commands_list = [
    "/register - регистрация в сервисе и оформление подписки",
]
