from bot.bot import dp
from aiogram.types import Message
from status_machine.user import User
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, Client
from kb.reply_key.user.sign_user import start_keyboard


@dp.message_handler(text="Войти как клиент ТТК")
async def sign_user(message: Message):
    await message.answer(
        text="✍ Введите Ваш номер Договора:"
    )
    await User.contract.set()


@dp.message_handler(state=User.contract)
async def contract_input(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['contract'] = message.text

    await state.finish()

    contract_number = message.text

    if contract_number:
        with SessionLocal() as session:
            client = session.query(Client).filter(Client.contract == contract_number).first()
            if client:
                await message.answer(
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