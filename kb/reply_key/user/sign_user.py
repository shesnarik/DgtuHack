from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(
    KeyboardButton(
        "Войти как клиент ТТК",
    )
)
start_keyboard.add(
    KeyboardButton(
        "Заключить новый договор"
    )
)
