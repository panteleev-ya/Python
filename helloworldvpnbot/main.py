from aiogram.utils import executor  # Import bot executor
from utils.locals.data.bot_init import dp  # Import bot dispatcher

# Import custom filters
from utils.filters.admin import NotAdmin
from utils.filters.paid import UserPaid, UserDidNotPaid, UserDidNotRenew

# Handlers import
from utils.handlers.other import register_handlers_other
from utils.handlers.subscribe import register_handlers_subscribe
from utils.handlers.admin import register_handlers_admin
from utils.handlers.user_account import register_handlers_user_account
from utils.handlers.check_access import register_handlers_check_access
from utils.handlers.connection_guides import register_handlers_connection_guides


if __name__ == '__main__':
    # Binding custom filters
    custom_filters = [
        NotAdmin,
        UserPaid,
        UserDidNotPaid,
        UserDidNotRenew
    ]
    for custom_filter in custom_filters:
        dp.bind_filter(custom_filter)

    # Registering handlers
    # Check access always first
    register_handlers_check_access(dp)

    # Handlers
    register_handlers_admin(dp)
    register_handlers_subscribe(dp)
    register_handlers_user_account(dp)
    register_handlers_connection_guides(dp)

    # Handlers other always last (has "no filters" handler)
    register_handlers_other(dp)

    # Running Bot by LongPolling => infinity looping the program
    # skip_updates=True means that bot will not answer on messages, that he got while being offline
    executor.start_polling(dp, skip_updates=True)
