<<<<<<< HEAD
from bot.bot import dp
from aiogram.types import Message
from kb.reply_key.user.sign_user import start_keyboard


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(
        text="Здравствуйте, Вас приветствует компания ТрансТелеКом."
    )
    await message.answer("Выберите что вам нужно", reply_markup=start_keyboard)
=======
from aiogram.dispatcher.filters import Command
from bot.bot import dp
from aiogram.types import Message
from keyboards.reply_key.user.sign_user import start_keyboard


@dp.message_handler(Command('start'))
async def start(message: Message):
    await message.answer(
        text="Здравствуйте,вас приветствует компания 'ТрансТелеКом'"
    )
    await message.answer("Ввыберите что вам нужно", reply_markup=start_keyboard)
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
