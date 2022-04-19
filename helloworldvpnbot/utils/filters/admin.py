from aiogram import types
from aiogram.dispatcher.filters import Filter

from utils.locals.data.admins import is_admin


# Filters for admin commands

# Manually applying user payment filter
class NotAdmin(Filter):
    key = "not_admin"

    async def check(self, message: types.Message):
        return not is_admin(message.from_user.username)
