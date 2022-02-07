# Написание Telegram-бота на aiogram (python)
##Полезные ссылки
Видео-курс на YouTube - [ссылка](https://youtu.be/TYs3-uyjC30)  
Официальная документация - [ссылка](https://docs.aiogram.dev/en/latest/index.html)
## Режимы работы бота
### LongPolling
Позволяет запустить бота на локальном устройстве. Бот постоянно посылает запросы на сервера Телеграма для проверки наличия новых сообщений.  
**Плюсы:** Бота легко запустить локально, без каких-либо требований к нему  
**Минусы:** Бот часто вылетает, такой способ не подходит для продакшна
### Webhook
Бот запускается на сервере (необходима реализация API для данного бота), а схема работы такая:
1. Пользователь отправляет сообщение боту
2. Телеграм "ловит" это сообщение и отправляет боту запрос (через его API) с этим сообщением

**Плюсы:** Бот работает стабильно, сервера Телеграма меньше нагружаются, сам бот меньше нагружает систему  
**Минусы:** Необходима реализация API, а также запуск бота удаленно на сервере
##Подключение необходимых библиотек
```Python
from aiogram import Bot, types  # Подключает класс Бота и "типы"
from aiogram.dispatcher import Dispatcher  # Подключает диспетчера сообщений для бота
from aiogram.utils import executor  # Подключает класс "запускателя" бота
```
##Инициализация бота и диспетчера
```Python
bot = Bot(token, parse_mode=None)
dp = Dispatcher(bot)  # Отвечает за отлавливание сообщений
```
##Message handlers
"Отловщики" (хэндлеры) полученных сообщений в *aiogram* создаются следующим образом
```Python
@dp.message_handler(filters)
async def function_name(message: types.Message):
    do_something
    await something_to_do
    do_something
    await something_to_do
    ...
```
, где  
+ `async` - означает, что функция асинхронная.  
То есть, пока выполнение этой функции "заморожено" каким-либо ожиданием (например, пользовательского ввода) - сам бот продолжает работать 
и может выполнять какие-то другие функции, чтобы вернуться к данной когда ожидание закончится
+ `"filters"` - какие-либо фильтры, установленные для этого хэндлера.  
То есть, сообщения будут отлавливаться именно этим хэндолером только если они подходят под все фильтры.  
Подробнее про фильтры хэндлеров - [ссылка на документацию](https://docs.aiogram.dev/en/latest/dispatcher/index.html#aiogram.Dispatcher.message_handler)
+ `dp` - созданный ранее диспетчер.
+ `"function_name"` - название функции хэндлера, никаких особых ограничений на название функции нет, от названия никак 
не зависит функционал бота
+ `message: types.Message` - ДОПИСАТЬ
+ `await` - "подождать пока не появится свободное время и выполнить" ДОПИСАТЬ
+ `"something_to_do"` - какая-либо команда по отправке сообщений пользователю, например
  + message.answer("message text", _optional_argument_) - отправляет обычное сообщение пользователю ("в ответ на его сообщение").
  Некоторые полезные опциональные аргументы: `parse_mode=`, `disable_notification=`, `reply_markup=`  
  Подробнее - [ссылка на документацию](https://docs.aiogram.dev/en/latest/telegram/types/message.html#aiogram.types.message.Message.answer)
  + message.reply("message text", some_options)  
    Подробнее - [ссылка на документацию](https://docs.aiogram.dev/en/latest/telegram/types/message.html#aiogram.types.message.Message.reply)  

Если сообщение было отловлено одним хэндлером, то в другие оно уже точно не попадет (аналогично конструкции `if-elif-else`).  
Желательно иметь один хэндлер **без фильтров** - для ответа на сообщения, которые бот не знает как обрабатывать (такой хэндлер будет тем самым `else` у нашего бота)
## Как вынести хэндлеры в отдельный файл?
1. Создаем файл `create_bot_and_dp.py`, в который переносим создание бота (`bot`) и диспетчера (`dp`)
2. Создаем файлы для хранения хэндлеров по группам  - `handlers_<group_name>.py`, либо один файл для всех хэндлеров
3. Переносим в них (в него) хэндлеры из основного файла
4. Адаптируем перенесенные хэндлеры:
   1. В каждом файле с хэндлерами создаем функцию `def register_handlers_<group_name>(_dp: Dispatcher)`,  
   где `<group_name>` - название группы хэндлеров
   2. В созданной функции для каждого хэндлера пишем строчку `_dp.register_message_handler(<name>, <filters>)`,  
   где `<name>` - название хэндлера, а `<filters>` - фильтры из его декоратора
   3. Удаляем декораторы у всех перенесенных хэндлеров
5. В мэйн-файле импортируем функции регистрации хэндлеров из всех созданных `.py-файлов` командами вида  
`from handlers_<group_name> import register_handlers_<group_name>` 

Пример кода (файл `handlers_other.py`):
```Python
from aiogram import types, Dispatcher

async def send_help_message(message: types.Message):
    await message.reply("Привет! Чем я могу помочь? Вот мой список команд:")

async def no_filters_handler(message: types.Message):
    await message.reply("Просто текст")

def register_handlers_other(_dp: Dispatcher):
    _dp.register_message_handler(send_help_message, commands=['help'])
    _dp.register_message_handler(no_filters_handler)
```
##Создание клавиатур
Раздел по теме в официальной документации [ссылка](https://docs.aiogram.dev/en/latest/telegram/types/reply_keyboard.html)  
Статья по созданию клавиатур - [ссылка](https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html)  
Клавиатуры делятся на `ReplyKeyboardMarkup` и `InlineKeyboardMarkup`
###Подключение библиотек
```Python
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
```
###ReplyKeyboardMarkup
Нужны для более простой отправки боту команд или сообщений.  
Т.е. не нужно угадывать команду и набирать ее вручную - просто нажимаешь на подходящую кнопку и все  
Раздел по теме в [официальной документации](https://docs.aiogram.dev/en/latest/telegram/types/reply_keyboard.html)
####Создание объекта клавиатуры
```Python
keyboard_hi = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=5)
# Размер клавиатуры будет подстроен под необходимый, клавиатура исчезнет после нажатия на ее кнопку
# Максимальное количество кнопок в одном ряду клавиатуры будет равно 5 (по дефолту - 3)
```
####Создание кнопки
```Python
button_hi = KeyboardButton('Привет!')
```
####Добавление кнопок
**.add(\*args)**
```Python
keyboard_hi.add(button_hi)
# Создаст новый ряд и добавит в него одну кнопку
```
```Python
# Либо
keyboard_hi.add(button_hi, button_hi)
# Либо
buttons_row = [button_hi, button_hi]
keyboard_hi.add(*buttons_row)
# Создаст новый ряд и добавит в него все перечисленные кнопки
# Если в списке будет больше кнопок, чем вмещает в себя один ряд, то будет создано столько рядов, сколько необходимо
```
**.row(\*args)**
```Python
# Либо
keyboard_hi.row(button_hi, button_hi)
# Либо
buttons_row = [button_hi, button_hi]
keyboard_hi.row(*buttons_row)
# То же самое, что и .add, но если кнопок больше, чем может быть - ограничение будет проигнорировано.  
# То есть если row_width=5, а количество кнопок в ряду - 6 или больше, то все они будут добавлены в один ряд
```
**.insert(*button*)**
```Python
keyboard_hi.insert(button_hi)
# Добавляет к клавиатуре еще одну кнопку. Если последний ее ряд не заполнен целиком, то добавляет туда,
# если же он уже заполнен, то создает новый ряд и помещает кнопку в него
```
####Отправка данных через кнопки
Отправка своего телефонного номера
```Python
button_send_phone_number = KeyboardButton('Отправить свой контакт', request_contact=True)
```
Отправка своей локации (местоположения)
```Python
button_send_location = KeyboardButton('Отправить свое местоположение', request_location=True)
```
###InlineKeyboardMarkup
В отличие от **ReplyKeyboardMarkup**, не только отправляют сообщение с текстом, указанным на кнопке,  
но и отправляют боту `callback_data`  
Раздел по теме в [официальной документации](https://docs.aiogram.dev/en/latest/telegram/types/inline_keyboard.html)  
Будут рассмотрены позже