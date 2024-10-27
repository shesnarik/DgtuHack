import requests
from os import getenv
from bot.bot import dp
from dotenv import load_dotenv
from aiogram.types import Message
from status_machine.admin import Admin
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, People
from kb.reply_key.admin.start_admin_key import start_admin_panel
from kb.reply_key.editor.start_editor_key import start_editor_panel

load_dotenv()

admin_email = getenv("ADMIN_EMAIL")

@dp.message_handler(commands='admin')
async def admin(message: Message):
    await message.answer(
        text="Введите Логин "
    )
    await Admin.login.set()

@dp.message_handler(state=Admin.login)
async def process_login(message: Message, state: FSMContext):
    login = message.text

    async with state.proxy() as data:
        data['login'] = login

    await message.answer(
        text="Введите Пароль"
    )
    await Admin.password.set()

@dp.message_handler(state=Admin.password)
async def process_password(message: Message, state: FSMContext):
    password = message.text

    async with state.proxy() as data:
        login = data['login']

    with SessionLocal() as session:
        user = session.query(People).filter(People.login == login).first()

        if user and user.password == password:
            await state.finish()
            role_user = user.role

            if role_user == 'Admin':
                await message.answer(
                    text="Добро пожаловать в админ-панель",
                    reply_markup=start_admin_panel
                )
                await message.answer(
                    text="Выберите команду из менб кнопок"
                )

            elif role_user == 'Editor':
                await message.answer(
                    text="Добро пожаловать в панель редактора",
                    reply_markup=start_editor_panel
                )
            else:
                await message.answer("Неизвестная роль пользователя.")
        else:
            await message.answer(
                text="Неверный логин или пароль. Попробуйте снова."
                     "\n\nЧтобы отменить операцию введите /cancel"
            )
            await state.finish()