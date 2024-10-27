from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    contract = State()

class UserRegistration(StatesGroup):
    phone = State()
    address = State()
    service = State()
    intent = State()
