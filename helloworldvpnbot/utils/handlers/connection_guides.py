from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils.handlers.user_account import get_cert_handler, get_info_handler
from utils.locals.data.keyboards import *
from utils.messages.connection_guides import *
from utils.locals.data.photos_id import *

# Info for sending and deleting guide messages
from utils.messages.other import not_an_option_message

current_step_id = -1
current_steps_number = -1
current_guide_messages = []
current_guide_photos = []
cert_msg = None
info_msg = None
prev_guide_text_msg = None
prev_guide_screenshots_msg = None


class ChooseOSTypeFSM(StatesGroup):
    choosing_os_type = State()


class ShowGuideFSM(StatesGroup):
    show = State()


async def connect_command_handler(message: types.Message, state: FSMContext):
    await ChooseOSTypeFSM.choosing_os_type.set()
    await message.reply(ask_guide_message, reply_markup=os_keyboard, parse_mode='markdown')


async def choose_os_guide_handler(message: types.Message, state: FSMContext):
    global current_step_id, current_guide_messages, current_guide_photos, current_steps_number
    global cert_msg, info_msg, prev_guide_text_msg, prev_guide_screenshots_msg
    current_step_id = 0

    # Parsing argument to get OS type
    # Setting states, messages and screenshots by OS type
    if message.text == "Windows":
        # current_states = list(WindowsConnectionGuideFSM.states)
        current_guide_messages = windows_guide_messages
        current_guide_photos = windows_guide_photos
        current_steps_number = 8
    elif message.text == "Android":
        # current_states = list(AndroidConnectionGuideFSM.states)
        current_guide_messages = android_guide_messages
        current_guide_photos = android_guide_photos
        current_steps_number = 6
    elif message.text == "iOS":
        # current_states = list(IOSConnectionGuideFSM.states)
        current_guide_messages = ios_guide_messages
        current_guide_photos = ios_guide_photos
        current_steps_number = 4
    else:
        await message.answer(not_an_option_message, parse_mode='markdown')
        return

    # Setting ShowGuide state
    await ShowGuideFSM.show.set()

    # Sending certificate
    cert_msg = await get_cert_handler(message=message)

    # Sending /info
    info_msg = await get_info_handler(message=message)

    # Sending first step of the guide
    prev_guide_text_msg, prev_guide_screenshots_msg = await send_guide_step(message=message, state_index=0, state_keyboard=next_menu_keyboard, guide_messages=current_guide_messages, guide_photos=current_guide_photos)


async def show_guide_handler(message: types.Message, state: FSMContext):
    global current_step_id, current_guide_messages, current_guide_photos
    global prev_guide_text_msg, prev_guide_screenshots_msg

    # Setting prev or next state
    if message.text == prev_step_text:
        if current_step_id > 0:
            current_step_id -= 1
        else:
            # Closing guide
            await cancel_guide_handler(message=message, state=state)
            return
    elif message.text == next_step_text:
        if current_step_id < current_steps_number - 1:
            current_step_id += 1
        else:
            # Closing guide
            await cancel_guide_handler(message=message, state=state)
            return

    # Setting keyboard
    if current_step_id == 0:
        current_state_keyboard = next_menu_keyboard
    elif current_step_id == current_steps_number - 1:
        current_state_keyboard = prev_menu_keyboard
    else:
        current_state_keyboard = prev_next_menu_keyboard

    # Deleting prev step text and screenshots messages
    if prev_guide_text_msg is not None and prev_guide_screenshots_msg is not None:
        for screenshot_msg in prev_guide_screenshots_msg:
            await screenshot_msg.delete()
        await prev_guide_text_msg.delete()
        await message.delete()

    # Sending message and screenshots
    prev_guide_text_msg, prev_guide_screenshots_msg = await send_guide_step(message, current_step_id, current_state_keyboard, current_guide_messages, current_guide_photos)


async def send_guide_step(message, state_index, state_keyboard, guide_messages, guide_photos):
    # Send text and reply keyboard
    text_msg = await message.answer(f"***Шаг {state_index + 1}***:\n\n" + guide_messages[state_index + 1], reply_markup=state_keyboard, parse_mode='markdown')

    # Send screenshots
    attached_screenshots = types.MediaGroup()
    for photo in guide_photos[state_index]:
        attached_screenshots.attach_photo(photo)
    screenshots_msg = await message.answer_media_group(media=attached_screenshots)
    return text_msg, screenshots_msg


async def cancel_guide_handler(message: types.Message, state: FSMContext):
    global prev_guide_text_msg, prev_guide_screenshots_msg, cert_msg, info_msg
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        if prev_guide_text_msg is not None and prev_guide_screenshots_msg is not None:
            for screenshot_msg in prev_guide_screenshots_msg:
                await screenshot_msg.delete()
            await prev_guide_text_msg.delete()
            # await message.delete()
        if cert_msg is not None and info_msg is not None:
            await cert_msg.delete()
            await info_msg.delete()
        await message.reply(guide_finish_message, reply_markup=types.ReplyKeyboardRemove(), parse_mode='markdown')


def register_handlers_connection_guides(_dp: Dispatcher):
    # Stop using guide
    _dp.register_message_handler(cancel_guide_handler, filters.Text(contains=[cancel_guide_text], ignore_case=True), state=ShowGuideFSM.show)

    # Choose OS
    _dp.register_message_handler(connect_command_handler, commands=['connect'], state=None)
    _dp.register_message_handler(choose_os_guide_handler, content_types=['text'], state=ChooseOSTypeFSM.choosing_os_type)

    # Show guide
    _dp.register_message_handler(show_guide_handler, filters.Text(contains=[next_step_text], ignore_case=True) | filters.Text(contains=[prev_step_text], ignore_case=True), state=ShowGuideFSM.show)
