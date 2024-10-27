from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()

bot = Bot(token=getenv('API_TOKEN_BOT'))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
