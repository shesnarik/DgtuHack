from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_editor_panel = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text="Вывести Пользователей")
btn2 = KeyboardButton(text="Изменить Триггеры (ключевые слова)")
start_editor_panel.row(btn1, btn2)
