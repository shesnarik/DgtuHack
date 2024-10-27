<<<<<<< HEAD
=======
import re
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
from bot.bot import dp
from aiogram.types import Message
from status_machine.user import User
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, Client
<<<<<<< HEAD
from kb.reply_key.user.sign_user import start_keyboard
=======
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f


@dp.message_handler(text="Войти как клиент ТТК")
async def sign_user(message: Message):
    await message.answer(
<<<<<<< HEAD
        text="✍ Введите Ваш номер Договора:"
=======
        text="Введите Ваш номер Договора:"
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
    )
    await User.contract.set()


@dp.message_handler(state=User.contract)
async def contract_input(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['contract'] = message.text

    await state.finish()

<<<<<<< HEAD
    contract_number = message.text

    if contract_number:
=======
    contract_number = message.text.strip()

    if re.match(r"^516\d{7}$", contract_number):
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract == contract_number).first()
            if client:
                await message.answer(
<<<<<<< HEAD
                    f"Добро пожаловать!\nВаш контактный номер: {client.phone}, адрес: {client.address}.")
            else:
                await message.answer(
                    text="Номер договора не найден.\nПопробуйте войти ещё раз!",
                    reply_markup=start_keyboard
                )
    else:
        await message.answer(
            text="Неверный формат номера договора.Попробуйте еще раз",
            reply_markup=start_keyboard
        )
=======
                    f"Добро пожаловать! Ваш контактный номер: {client.contact_number}, адрес: {client.address}.")
            else:
                await message.answer("Номер договора не найден.")
    else:
        await message.answer("Неверный формат номера договора.")
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
