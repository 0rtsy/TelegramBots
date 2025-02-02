import logging
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token="TOKEN", parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s] «%(filename)s» line %(lineno)s >>> %(message)s", datefmt='%H:%M:%S'
)