import os
import pymorphy2
from bot.bot import dp
from pydub import AudioSegment
import speech_recognition as sr
from aiogram.dispatcher import FSMContext
from text_file_download import my_list_str
from base.config import SessionLocal, Client
from status_machine.user import UserRegistration
from kb.reply_key.user.yes_no import yes_no
from kb.reply_key.user.sign_user import start_keyboard
from aiogram.types import Message, ReplyKeyboardRemove, ContentType


morph = pymorphy2.MorphAnalyzer()

@dp.message_handler(text="Заключить новый договор")
async def registration_user(message: Message):
    await message.answer(
        text="Укажите Ваш номер телефона",
        reply_markup=ReplyKeyboardRemove()
    )
    await UserRegistration.phone.set()

@dp.message_handler(state=UserRegistration.phone)
async def user_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply(
        text="Введите адрес",
        reply_markup=ReplyKeyboardRemove()
    )
    await UserRegistration.next()

@dp.message_handler(state=UserRegistration.address)
async def user_address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    await message.answer(
        text="<b>Предлагаемые нами тарифы и услуги:\n</b>"
             "\n<b>Список тарифов:\n</b>"
             "\tМаксимальный - 1000 Гбит 800р в месяц\n"
             "\tМощный - 100 Мбит 400р в месяц\n"
             "\tЧестный - 10 Мбит 100р в месяц\n"
             "\n\n<b>Список услуг:</b>\n"
             "\tАнтиВирус Касперский - 100р в месяц\n"
             "\tВыделенный IP - 100р в месяц\n"
             "\tПерсональный менеджер - 100р в месяц\n"
             "\tФирменный роутер - 100р в месяц\n",
        parse_mode="HTML"
    )

    await message.answer(
        text="Выберите интересующие вас опции из нашего списка продуктов"
             "\nИ Сообщите нам об этом с помощью текстового или голосового сообщения"
    )

    await UserRegistration.next()

@dp.message_handler(content_types=ContentType.VOICE, state=UserRegistration.service)
async def user_provider_service(message: Message, state: FSMContext):
    file_id = message.voice.file_id
    file_info = await dp.bot.get_file(file_id)
    downloaded_file = await dp.bot.download_file(file_info.file_path)

    # Сохраняем файл во временное хранилище
    with open("sound_user/user_gs_start.ogg", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())

    # Проверяем наличие ffmpeg
    if not os.system("ffmpeg -version >nul 2>nul"):
        recognizer = sr.Recognizer()

        # Конвертируем OGG в WAV
        audio = AudioSegment.from_ogg("sound_user/user_gs_start.ogg")
        audio.export("sound_user/user_gs_finish.wav", format="wav")

        with sr.AudioFile("sound_user/user_gs_finish.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")

                # Лемматизация текста
                lemmatized_text = ' '.join([morph.parse(word)[0].normal_form for word in text.split()])

                # Проверяем наличие триггеров и выводим описание
                found_descriptions = []
                key_list = []
                for key, value in my_list_str.items():
                    if any(trigger in lemmatized_text for trigger in value["триггеры"]):
                        found_descriptions.append(f"{value['описание']}")
                        key_list.append(key)

                async with state.proxy() as data:
                    # Добавляем распознанный текст в user_text
                    data['user_text'] = data.get('user_text', '') + ' ' + text

                if found_descriptions:
                    await message.answer(
                        text="Правильно ли я Вас понял?",
                        reply_markup=yes_no
                    )
                    await message.answer("\n".join(found_descriptions))

                    async with state.proxy() as data:
                        data['service'] = key_list
                        data['intent'] = found_descriptions

                else:
                    await message.answer(
                        f"К сожалению я Вас не понял, попробуйте еще раз "
                        f"записать голосовое сообщение или напишите текстом"
                        f"\nЧтобы отменить операцию введите /cancel",
                        reply_markup=start_keyboard
                    )
                    await state.finish()
            except sr.UnknownValueError:
                await message.answer(
                    "Не удалось распознать речь.",
                )
                await state.finish()
            except sr.RequestError as e:
                await message.answer(
                    f"Ошибка сервиса: {e}",
                )
                await state.finish()
    else:
        await message.answer(
            "FFmpeg не найден. Пожалуйста, установите FFmpeg.",
        )
        await state.finish()

    await UserRegistration.next()

@dp.message_handler(content_types=ContentType.TEXT, state=UserRegistration.service)
async def user_provider_service_text(message: Message, state: FSMContext):
    user_text = message.text

    async with state.proxy() as data:
        data['user_text'] = data.get('user_text', '') + ' ' + user_text

    input_lemmatized_text = ' '.join([morph.parse(word)[0].normal_form for word in user_text.split()])

    found_descriptions = []
    key_list = []
    for key, value in my_list_str.items():
        if any(trigger in input_lemmatized_text for trigger in value["триггеры"]):
            found_descriptions.append(f"{value['описание']}")
            key_list.append(key)

    if found_descriptions:
        await message.answer(
            text="Правильно ли я Вас понял? ",
            reply_markup=yes_no
        )
        await message.answer("\n".join(found_descriptions))

        async with state.proxy() as data:
            data['service'] = key_list
            data['intent'] = found_descriptions

        await UserRegistration.next()
    else:
        await message.answer(
            f"К сожалению, я Вас не понял. "
            f"Попробуйте написать текстом или используйте голосовое сообщение \n"
            f"\nЧтобы отменить операцию введите /cancel",
            reply_markup=start_keyboard
        )
        await state.finish()


@dp.message_handler(text="Да", state=UserRegistration.intent)
async def yes_user_otvet(message: Message, state: FSMContext):
    async with state.proxy() as data:
        service = ', '.join(data['service'])
        intent = ', '.join(data['intent'])

        await state.finish()

        await message.answer(
            text="Данные успешно переданы"
                 "\nСкоро с Вами свяжутся специалисты",
            reply_markup=start_keyboard
        )

        with SessionLocal() as session:
            max_contract = session.query(Client.contract).order_by(Client.contract.desc()).first()
            if max_contract:
                contract_number = str(int(max_contract[0]) + 1)
            else:
                contract_number = "516111111"

        new_client = Client(
            contract=contract_number,
            phone=data['phone'],
            address=data['address'],
            service=service,
            intent=intent,
            user_text=data['user_text']
        )

        with SessionLocal() as session:
            session.add(new_client)
            session.commit()


@dp.message_handler(text="Нет", state=UserRegistration.intent)
async def no_user_otvet(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
            text="Пожалуйста, Если возникла проблема, напишите "
                 "текстовое сообщение, которое отправится администратору",
            reply_markup=start_keyboard
    )


@dp.message_handler(commands='cancel', state='*')
async def cancel_command(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Операция отменена.")
