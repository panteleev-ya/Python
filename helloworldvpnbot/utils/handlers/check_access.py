from aiogram import types, Dispatcher

from utils.messages.check_access import *

from utils.filters.admin import NotAdmin
from utils.filters.paid import UserDidNotPaid, UserDidNotRenew

# Paid only commands
paid_only_commands = ['certificate', 'info', 'renew', 'connect']

# Admin commands
admin_commands = ['apply', 'photo_id', 'send_photo']


# No access to commands handler
async def no_access_handler(message: types.Message):
    await message.reply(no_access_message, parse_mode='markdown')


def register_handlers_check_access(_dp: Dispatcher):
    # User didn't pay or didn't renew the subscription - he has no access
    _dp.register_message_handler(no_access_handler, UserDidNotPaid(), commands=list(paid_only_commands))
    _dp.register_message_handler(no_access_handler, UserDidNotRenew(), commands=list(paid_only_commands))

    # User is not admin
    _dp.register_message_handler(no_access_handler, NotAdmin(), commands=list(admin_commands))
