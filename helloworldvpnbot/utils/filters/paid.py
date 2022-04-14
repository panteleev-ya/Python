from aiogram import types
from aiogram.dispatcher.filters import Filter

from utils.locals.data.users import users


# "User paid" filter
class UserPaid(Filter):
    key = "user_paid"

    async def check(self, message: types.Message):
        username = str(message.from_user.username)
        if username in users and users[username]['paid'] == 1:
            return True
        return False


# "User didn't pay" filter
class UserDidNotPaid(Filter):
    key = "user_did_not_paid"

    async def check(self, message: types.Message):
        username = str(message.from_user.username)
        if username in users and users[username]['paid'] == 1:
            return False
        return True


# "User didn't renew subscription" filter
class UserDidNotRenew(Filter):
    key = "user_did_not_renew"

    async def check(self, message: types.Message):
        username = str(message.from_user.username)
        if username in users and users[username]['paid'] != 1:
            return True
        return False
