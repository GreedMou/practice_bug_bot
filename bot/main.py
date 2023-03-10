from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.utils import executor

from bot.filters import register_all_filters
from bot.handlers import register_all_handlers
from bot.misc import TgKeys


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=JSONStorage('memory.json'))
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
