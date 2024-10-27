from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text="Добавить супер пользователя")
btn2 = KeyboardButton(text="Вывести Пользователей")
btn3 = KeyboardButton(text="Изменить Триггеры (ключевые слова)")
start_admin_panel.row(btn1, btn2)
start_admin_panel.add(btn3)
