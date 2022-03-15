from aiogram.utils import executor  # Import bot executor

from utils.create_bot import dp  # Import bot dispatcher
from utils.handlers.handlers_other import register_handlers_other  # Import handlers (other)
from utils.handlers.handlers_register import register_handlers_register  # Import handlers (register)


if __name__ == '__main__':
    # Registering handlers
    register_handlers_register(dp)
    register_handlers_other(dp)

    # Running Bot by LongPolling => infinity looping the program
    # skip_updates=True means that bot will not answer on messages, that he got while being offline
    executor.start_polling(dp, skip_updates=True)
