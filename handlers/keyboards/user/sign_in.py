import re
from bot.bot import dp
from aiogram.types import Message
from status_machine.user import User
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, Client


@dp.message_handler(text="Войти как клиент ТТК")
async def sign_user(message: Message):
    await message.answer(
        text="Введите Ваш номер Договора:"
    )
    await User.contract.set()


@dp.message_handler(state=User.contract)
async def contract_input(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['contract'] = message.text

    await state.finish()

    contract_number = message.text.strip()

    if re.match(r"^516\d{7}$", contract_number):
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract == contract_number).first()
            if client:
                await message.answer(
                    f"Добро пожаловать! Ваш контактный номер: {client.contact_number}, адрес: {client.address}.")
            else:
                await message.answer("Номер договора не найден.")
    else:
        await message.answer("Неверный формат номера договора.")