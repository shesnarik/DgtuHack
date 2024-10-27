from aiogram import executor
from handlers import dp


__all__ = ["dp"]


if __name__ == '__main__':
    print('Бот запущен!\nВсе обновления пропущена: ', end=' ')
    executor.start_polling(dp, skip_updates=True)
    print("Бот остановлен!")
