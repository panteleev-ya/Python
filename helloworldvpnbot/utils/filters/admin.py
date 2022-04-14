from aiogram import types
from aiogram.dispatcher.filters import Filter

from utils.locals.data.admins import is_admin


# Filters for admin commands

# Manually applying user payment filter
class AdminApplyPayment(Filter):
    key = "admin_apply"

    async def check(self, message: types.Message):
        commands = ['/apply']
        return is_admin(message.from_user.username) and message.text.split()[0] in commands
