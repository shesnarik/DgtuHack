from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    contract = State()

class UserRegistration(StatesGroup):
    phone = State()
    address = State()
    service = State()
<<<<<<< HEAD
    intent = State()
=======
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f
