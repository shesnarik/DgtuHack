from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


yes_no = ReplyKeyboardMarkup(resize_keyboard=True)
yes_no.add(
    KeyboardButton(
        "Да",
    )
)
yes_no.add(
    KeyboardButton(
        "Нет"
    )
)
