from aiogram.utils import executor
from create_bot_and_dp import dp
from handlers_other import register_handlers_other

register_handlers_other(dp)

# Running Bot by LongPolling => infinity looping the program
# skip_updates=True means that bot will not answer on messages, that he got while being offline
executor.start_polling(dp, skip_updates=True)
