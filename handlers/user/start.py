from bot.bot import dp
from aiogram.types import Message
from kb.reply_key.user.sign_user import start_keyboard


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(
        text="Здравствуйте, Вас приветствует компания ТрансТелеКом."
    )
    await message.answer("Выберите что вам нужно", reply_markup=start_keyboard)
