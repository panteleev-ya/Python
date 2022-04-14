from aiogram.utils import executor  # Import bot executor

from utils.locals.data.bot_init import dp  # Import bot dispatcher
from utils.filters.admin import AdminApplyPayment
from utils.handlers.other import register_handlers_other  # Import handlers (other)
from utils.handlers.subscribe import register_handlers_subscribe  # Import handlers (register)
from utils.handlers.admin import register_handlers_admin  # Import handlers (admin)
from utils.handlers.support import register_handlers_support


if __name__ == '__main__':
    # Binding filters
    custom_filters = [
        AdminApplyPayment,
    ]
    for custom_filter in custom_filters:
        dp.bind_filter(custom_filter)

    # Registering handlers
    register_handlers_admin(dp)
    register_handlers_subscribe(dp)
    register_handlers_other(dp)
    register_handlers_support(dp)

    # Running Bot by LongPolling => infinity looping the program
    # skip_updates=True means that bot will not answer on messages, that he got while being offline
    executor.start_polling(dp, skip_updates=True)
