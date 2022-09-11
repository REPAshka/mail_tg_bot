from aiogram import Router, html, Bot, types
from aiogram.filters import CommandObject
from aiogram.utils.markdown import hide_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
# from aiogram.dispatcher.filters import Text

user_router = Router()


@user_router.message(commands=["start"])
async def user_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


# @user_router.message(Text(text="С пюрешкой"))
# async def with_puree(message: types.Message):
#     await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
#
#
# @user_router.message(lambda message: message.text == "Без пюрешки")
# async def without_puree(message: types.Message):
#     await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())


@user_router.message(commands=["special_buttons"]) # специальные конпки с геолокацией, контактом и викториной
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    # ... а второй из одной
    builder.row(types.KeyboardButton(
        text="Создать викторину",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@user_router.message(commands=["inline_url"]) # Инлайн конпки с переходом по ссылке
async def cmd_inline_url(message: types.Message, bot: Bot):
    # При попытке создать URL-кнопку с ID юзера, у которого отключен переход по форварду,
    # бот получит ошибку Bad Request: BUTTON_USER_PRIVACY_RESTRICTED.
    # Соответственно, прежде чем показывать такую кнопку, необходимо выяснить состояние упомянутой настройки.
    # Для этого можно вызвать метод getChat и в ответе проверить состояние поля has_private_forwards.
    # Если оно равно True, значит, попытка добавить URL-ID кнопку приведёт к ошибке.
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards
    user_id = 1234567890
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Какой-то пользователь",
            url=f"tg://user?id={user_id}")
        )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


@user_router.message(commands=["dice"]) # бросить кубик
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@user_router.message(commands=["name"]) # отделить строку от команды
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}")
    else:
        await message.answer(f"Пожалуйста, укажи своё имя после команды /name!")


@user_router.message(content_types="text") # вычленить ссылку, имейл, пароль(стиль написания Monospace) из строки
async def extract_data(message: types.Message):
    data = {
        "url": "<N/A>",
        "email": "<N/A>",
        "code": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    await message.reply(
        "Вот что я нашёл:\n"
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Пароль: {html.quote(data['code'])}"
    )


@user_router.message(content_types=[types.ContentType.ANIMATION]) # ответить присланной анимацией на анимацию
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@user_router.message(content_types="photo") # сохранить картинку к себе на пк не более 20мб (Telegram Client API - Telethon - если более 20мб)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"/Programming_Learning/Mail_bot/temp/photo/{message.photo[-1].file_id}.jpg"
    )
    await message.answer(f"Картинка сохранена")


@user_router.message(content_types=types.ContentType.STICKER) # сохранить стикер к себе на пк не более 20мб
async def download_sticker(message: types.Message, bot: Bot):
    await bot.download(
        message.sticker,
        destination=f"/Programming_Learning/Mail_bot/temp/stickers/{message.sticker.file_id}.webp"
    )
    await message.answer(f"Стикер сохранен")


@user_router.message(commands=["hidden_link"]) # спрятать ссылку в сообщении и вывести только картинку
async def cmd_hidden_link(message: types.Message):
    await message.answer(
        f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
        f"Документация Telegram: *существует*\n"
        f"Пользователи: *не читают документацию*\n"
        f"Груша:"
    )
