from bot.bot import dp
from aiogram.types import Message
from base.config import SessionLocal, Client


@dp.message_handler(text="Вывести Пользователей")
async def all_user(message: Message):
    with SessionLocal() as session:
        clients = session.query(Client).all()

    if not clients:
        await message.answer("Нет зарегистрированных пользователей.")
        return

    response_text = "Список пользователей:\n\n"

    for client in clients:
        response_text += (
            f"Номер договора: {client.contract}\n"
            f"Контактный номер: {client.phone}\n"
            f"Адрес: {client.address}\n"
            f"Услуга: {client.service}\n"
            f"Цель: {client.intent}\n"
            f"{'-' * 19}\n"
        )

    await message.answer(response_text)