from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from messages import *
from url_generators import *
from downloader import *
from file_manager import *


class FSMDownloadStickers(StatesGroup):
    sticker_collect_mode = State()  # Step 1: Range or list
    id_start_input = State()        # Range -> Step 2
    id_end_input = State()          # Range -> Step 2
    id_first_input = State()        # List -> Step 2
    id_input = State()              # List -> Step 2
    size_input = State()            # Step 3
    # done = State()                # Done!


# /download - задаем состояние "выбор способа", предлагаем варианты для выбора
async def start_download_handler(message: types.Message):
    await FSMDownloadStickers.sticker_collect_mode.set()
    await message.answer(start_download_message, reply_markup=start_download_keyboard)


# Выбираем режим:
#   Если "Скачать стикер-пак целиком" - состояние "Ввод id_start"
#   Если "Скачать стикеры по-одиночке" - состояние "Ввод id первого стикера"
async def sticker_collect_mode_handler(message: types.Message, state: FSMContext):
    # "Скачать стикер-пак целиком" - просим ввести id_start
    if message.text == range_download_text:
        # Записываем в хранилище FSM тип операции
        async with state.proxy() as data:
            data['type'] = 0
        await FSMDownloadStickers.id_start_input.set()
        await message.answer(id_start_input_message)

    # "Скачать стикеры по-одиночке" - просим ввести первый id
    elif message.text == list_download_text:
        # Записываем в хранилище FSM тип операции
        async with state.proxy() as data:
            data['type'] = 1
        await FSMDownloadStickers.id_first_input.set()
        await message.answer(id_first_input_message)

    # Что-то другое, что не подходит нам - пишем, что пользователь ошибся и отправляем ему клавиатуру обратно
    else:
        await message.reply(not_an_option_message, reply_markup=start_download_keyboard)


# Вводим ID первого стикера в стикер-паке
async def id_start_input_handler(message: types.Message, state: FSMContext):
    # Если было введено целое число
    if message.text.isdigit():
        # Записываем в хранилище FSM ID первого стикера в стикер-паке
        async with state.proxy() as data:
            data['id_start'] = int(message.text)

        # Задаем новое состояние - "Ввод ID последнего стикера в стикер-паке"
        await FSMDownloadStickers.id_end_input.set()
        await message.answer(id_end_input_message)

    # Если ID введен некорректно
    else:
        await message.reply(id_wrong_input_message)


async def id_first_input_handler(message: types.Message, state: FSMContext):
    # Если было введено целое число
    if message.text.isdigit():
        # Записываем в хранилище FSM ID первого стикера в списке на скачивание
        async with state.proxy() as data:
            data['id'] = [int(message.text)]

        # Задаем новое состояние - "Ввод последующих ID либо конец ввода"
        await FSMDownloadStickers.id_input.set()
        await message.answer(id_input_message)

    # Если ID введен некорректно
    else:
        await message.reply(id_wrong_input_message)


async def id_end_input_handler(message: types.Message, state: FSMContext):
    # Если было введено целое число
    if message.text.isdigit():
        # Записываем в хранилище FSM ID последнего стикера в стикер-паке
        async with state.proxy() as data:
            data['id_end'] = int(message.text)

        # Задаем новое состояние - "Ввод размера скачиваемой картинки"
        await FSMDownloadStickers.size_input.set()
        await message.answer(size_input_message, reply_markup=size_input_keyboard)

    # Если ID введен некорректно
    else:
        await message.reply(id_wrong_input_message)


async def id_input_handler(message: types.Message, state: FSMContext):
    # Если было введено целое число
    if message.text.isdigit():
        # Записываем в хранилище FSM ID следующего стикера в списке на скачивание
        async with state.proxy() as data:
            data['id'].append(int(message.text))

        # Оставляем прежнее состояние, выводим то же самое сообщение
        await message.answer(id_input_message)

    elif message.text == "/done":
        # Задаем новое состояние - "Ввод размера скачиваемой картинки"
        await FSMDownloadStickers.size_input.set()
        await message.answer(size_input_message, reply_markup=size_input_keyboard)

    # Если ID введен некорректно и это не команда /done
    else:
        await message.reply(id_wrong_input_message)


async def size_input_handler(message: types.Message, state: FSMContext):
    # Если пользователь случайно не ввел вручную какую-нибудь дичь
    if message.text in img_sizes_hash:
        img_size = img_sizes_hash[message.text]

        # Достаём из хранилища собранные данные
        async with state.proxy() as data:
            # data_hash = data.values()
            data_hash = data

        # Генерируем URL-адреса
        urls = []
        # Если нужно скачать стикер-пак
        if data_hash['type'] == 0:
            id_start = data_hash['id_start']
            id_end = data_hash['id_end']
            urls = generate_urls_from_range(id_start, id_end, size=img_size)

        # Если нужно скачать отдельные стикеры
        elif data_hash['type'] == 1:
            id_list = data_hash['id']
            urls = generate_urls_from_list(id_list, size=img_size)

        # Если что-то не то, или не так?????
        else:
            await message.answer("Что-то пошло не так!")

        # Скачиваем стикеры
        directory = "stickers"
        download_images_from_list(urls, directory=directory)

        # Собираем архив
        archive_name = "vk_stickers"
        archive_zip = archive_name + ".zip"
        make_zip_archive(archive_name, directory)

        # Отправляем этот архив пользователю
        await message.answer_document(open(archive_zip, "rb"), caption="Ваш архив со стикерами!")

        # Удаляем папку со стикерами и архив с ними из памяти
        rm(archive_zip)
        rm_rf_dir(directory)

        # Заканчиваем выполнение и задаем состояние "Сделано"
        # await message.answer(finish_message)
        await state.finish()

    # Если все же дичь
    else:
        await message.reply(size_wrong_input_message, reply_markup=size_input_keyboard)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.reply("Операция успешно отменена!")


def register_handlers_download_sticker(_dp: Dispatcher):
    _dp.register_message_handler(start_download_handler, commands=['download'], state=None)
    _dp.register_message_handler(sticker_collect_mode_handler, content_types=['text'], state=FSMDownloadStickers.sticker_collect_mode)
    _dp.register_message_handler(id_start_input_handler, content_types=['text'], state=FSMDownloadStickers.id_start_input)
    _dp.register_message_handler(id_first_input_handler, content_types=['text'], state=FSMDownloadStickers.id_first_input)
    _dp.register_message_handler(id_end_input_handler, content_types=['text'], state=FSMDownloadStickers.id_end_input)
    _dp.register_message_handler(id_input_handler, content_types=['text'], state=FSMDownloadStickers.id_input)
    _dp.register_message_handler(size_input_handler, content_types=['text'], state=FSMDownloadStickers.size_input)
    _dp.register_message_handler(cancel_handler, commands=['cancel'], state="*")
