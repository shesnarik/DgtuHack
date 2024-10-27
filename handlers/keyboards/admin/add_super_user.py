from bot.bot import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from base.config import SessionLocal, People
from status_machine.admin import AddSuperUser


@dp.message_handler(text="Добавить супер пользователя")
async def add_super_user(message: Message):
    await message.answer(
        text="Введите новый <b>логин</b> для супер пользователя 🕴",
        parse_mode="HTML"
    )
    await AddSuperUser.login.set()


@dp.message_handler(state=AddSuperUser.login)
async def login(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await message.answer(
        text="<b>Теперь введите Роль:</b>\n\t1) Admin\n\t2) Editor",
        parse_mode="HTML"
    )

    await AddSuperUser.next()


@dp.message_handler(state=AddSuperUser.role)
async def role(message: Message, state: FSMContext):
    if message.text not in ["Admin", "Editor"]:
        await message.answer("Пожалуйста, введите корректную роль: Admin или Editor.")
        return

    async with state.proxy() as data:
        data['role'] = message.text

    await message.answer(
        text=f"Теперь введите пароль для нового <b>{data['role']}</b> пользователя ",
        parse_mode="HTML"
    )

    await AddSuperUser.next()


@dp.message_handler(state=AddSuperUser.password)
async def password(message: Message, state: FSMContext):
    role_user = ''

    async with state.proxy() as data:
        data['password'] = message.text

    await state.finish()

    if data['role'] == 'Admin':
        role_user = 'Администратор'
    else:
        role_user = 'Редактор'

    new_client = People(
        login=data['login'],
        role=data['role'],
        password=data['password'],
    )

    with SessionLocal() as session:
        session.add(new_client)
        session.commit()

    await message.answer(
        text=f"Новый {role_user} Пользователь создан"
    )