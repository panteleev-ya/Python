from aiogram import types, Dispatcher
from aiogram.dispatcher import filters


# Command /start handler
async def send_welcome_handler(message: types.Message):
    await message.reply(send_welcome_message)


# Command /help handler
async def send_help_handler(message: types.Message):
    commands = available_commands_message
    for command in commands_list:
        commands += command + "\n"
    await message.reply(commands)


# Say "Your welcome!" to user if he tells "Thank you!" to the bot
async def be_polite_handler(message: types.Message):
    await message.reply("Пожалуйста☺")


# Unknown command handler
async def no_filters_handler(message: types.Message):
    await message.reply(unknown_command_message)


# Registering handlers function
def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_welcome_handler, commands=['start'])
    _dp.register_message_handler(send_help_handler, commands=['help'])
    _dp.register_message_handler(be_polite_handler, filters.Text(contains=['Спасибо'], ignore_case=True))
    _dp.register_message_handler(no_filters_handler)


send_welcome_message = """
Здравствуйте!
Я - Telegram бот VPN-сервиса Hello world!. Вот что я умею:
1) Помогу с оформлением подписки
   --> /subscribe
2) Расскажу как настроить VPN-подключение с любого устройства
   --> /connect
3) Скажу ваши персональные данные и продолжительность подписки
   --> /info
4) Ответы на часто задаваемые вопросы
   --> /faq
5) Продлю вашу подписку
   --> /renew
Печатать и отправлять команду не обязательно - просто нажмите на нее☺
"""

commands_list = [
    "⚫ /subscribe\n  Оформление подписки",
    "⚫ /renew\n  Продлить подписку"
    "⚫ /connect\n  Расскажу как настроить VPN-подключение с любого устройства",
    "⚫ /info\n  Скажу ваши персональные данные и продолжительность подписки",
    "⚫ /faq\n  Ответы на часто задаваемые вопросы",
]

available_commands_message = """
Список возможных команд:
"""

unknown_command_message = """
Извините, команда не распознана! Напиши /help для получения списка возможных команд
"""
