from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
import sqlite3 as sq
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text

TOKEN_API = "6383122397:AAFJB5h-pW8EjVPFfLeRkaPtAuyV1BKoIHU"
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

id_admin_data = ['340371976', '453800399', '452083843']
is_admin = False
# is_reg = False
ID = 0


con = sq.connect("test2.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS photos (
                    url TEXT
                    )""")
cur.execute("""CREATE TABLE IF NOT EXISTS photos_akcii (
                    url TEXT
                    )""")
# cur.execute("""CREATE TABLE IF NOT EXISTS users (
#                     name TEXT,
#                     surname TEXT,
#                     number INTEGER,
#                     id INTEGER,
#                     balance INTEGER
#                     )""")
cur.execute("""CREATE TABLE IF NOT EXISTS caption_tur (
                    caption TEXT
                    )""")
cur.execute("""CREATE TABLE IF NOT EXISTS caption_akcii (
                   caption TEXT
                    )""")
cur.execute("""CREATE TABLE IF NOT EXISTS clubs (
                   id INTEGER,
                   price TEXT,
                   accessories TEXT,
                   akcii TEXT, 
                   price_des TEXT,
                   accessories_des TEXT,
                   akcii_des TEXT, 
                   main TEXT
                    )""")

cur.execute("""CREATE TABLE IF NOT EXISTS users_all (
                   id INTEGER
                    )""")
cur.execute("""CREATE TABLE IF NOT EXISTS start_media_info (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   media TEXT,
                   caption TEXT, 
                   type INTEGER
                   )""")
con.commit()

cur.execute("SELECT * FROM start_media_info")
res_all = cur.fetchall()
if (len(res_all)==0):
    cur.execute("INSERT INTO start_media_info(media, type) VALUES ('AgACAgIAAxkBAAIMAWTKUoFLx39nip1CeNrEMjTsMJNhAAJAyTEb8CRQSgNeqXlK_avRAQADAgADeQADLwQ', 0)")
    con.commit()

cur.execute("SELECT * FROM photos")
res_all = cur.fetchall()
if (len(res_all)==0):
    cur.execute("INSERT INTO photos(url) VALUES ('AgACAgIAAxkBAAIMAWTKUoFLx39nip1CeNrEMjTsMJNhAAJAyTEb8CRQSgNeqXlK_avRAQADAgADeQADLwQ')")
    con.commit()

cur.execute("SELECT * FROM photos_akcii")
res_all = cur.fetchall()
if (len(res_all)==0):
    cur.execute("INSERT INTO photos_akcii(url) VALUES ('AgACAgIAAxkBAAIMAWTKUoFLx39nip1CeNrEMjTsMJNhAAJAyTEb8CRQSgNeqXlK_avRAQADAgADeQADLwQ')")
    con.commit()

cur.execute("SELECT * FROM caption_akcii")
res_all = cur.fetchall()
if (len(res_all)==0):
    cur.execute("INSERT INTO caption_akcii(caption) VALUES ('описание')")
    con.commit()

cur.execute("SELECT * FROM caption_tur")
res_all = cur.fetchall()
if (len(res_all)==0):
    cur.execute("INSERT INTO caption_tur(caption) VALUES ('описание')")
    con.commit()



def create_ikb(is_admin, ID):
    cur.execute("SELECT COUNT(*) FROM clubs")
    result = cur.fetchone()[0]
    start_menu_buttons = {}
    ikb = InlineKeyboardMarkup()
    kb1 = InlineKeyboardButton(text="Турниры", callback_data="Турниры")
    kb2 = InlineKeyboardButton(text="Акции", callback_data="Акции")
    ikb.add(kb1, kb2)
    if (result != 0):
        for i in range(1, result + 1):
            start_menu_buttons[f"Клуб {i}"] = f'Клуб {i}'
        for key, value in start_menu_buttons.items():
            ikb.add(InlineKeyboardButton(text=key, callback_data=value))
    # kb5 = InlineKeyboardButton(text="Мой баланс", callback_data="Мой баланс")
    # ikb.add(kb5)
    # cur.execute("SELECT id FROM users WHERE id = ?", (ID,))
    # result_reg = cur.fetchone()
    # if (result_reg == None):
    #     kb6 = InlineKeyboardButton(text = "Зарегистрироваться", callback_data="Зарегистрироваться")
    #     ikb.add(kb6)
    if (is_admin):
        kb7 = InlineKeyboardButton(text = "Режим админа", callback_data="Режим админа")
        ikb.add(kb7)
    return ikb


@dp.message_handler(commands = ['start'])
async def start_commmand(message: types.Message):
    global ID
    ID = message.from_user.id
    global is_admin
    # global is_reg
    for i in id_admin_data:
        if ID == int(i):
            is_admin = True
            break
    ikb = create_ikb(is_admin, ID)
    cur.execute("SELECT id FROM users_all")
    result = cur.fetchall()
    est = False
    for i in range(0, len(result)):
        if ID == result[i][0]:
            est = True
            break

    if (not(est)):
        cur.execute("INSERT INTO users_all(id) VALUES (?)", (ID,))
        con.commit()
    cur.execute("SELECT type FROM start_media_info WHERE id = 1")
    res_type = cur.fetchone()[0]
    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
    res_media = cur.fetchone()[0]
    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
    res_caption = cur.fetchone()[0]
    if (res_type == 1):
        await bot.send_video(chat_id=message.chat.id, video = res_media, caption = res_caption, reply_markup=ikb)
    elif (res_type == 0):
        await bot.send_photo(chat_id = message.chat.id, photo =res_media, caption=res_caption, reply_markup=ikb)
    elif (res_type == 2):
        await bot.send_animation(chat_id = message.chat.id, animation =res_media, caption=res_caption, reply_markup=ikb)


async def start_command_back(callback: types.CallbackQuery):
    global ID, is_admin
    ikb = create_ikb(is_admin, ID)
    cur.execute("SELECT type FROM start_media_info WHERE id = 1")
    res_type = cur.fetchone()[0]
    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
    res_media = cur.fetchone()[0]
    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
    res_caption = cur.fetchone()[0]
    if (res_type == 1):
        await callback.message.edit_media(types.InputMedia(media = res_media, type = 'video', caption = res_caption), reply_markup=ikb)
    elif (res_type == 0):
        await callback.message.edit_media(types.InputMedia(media = res_media, type = 'photo', caption = res_caption), reply_markup=ikb)
    elif (res_type == 2):
        await callback.message.edit_media(types.InputMedia(media = res_media, type = 'animation', caption = res_caption), reply_markup=ikb)




async def start_command_back2(callback: types.CallbackQuery):
    global is_admin, ID
    ikb = create_ikb(is_admin, ID)
    await callback.message.delete()

    cur.execute("SELECT type FROM start_media_info WHERE id = 1")
    res_type = cur.fetchone()[0]
    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
    res_media = cur.fetchone()[0]
    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
    res_caption = cur.fetchone()[0]
    if (res_type == 1):
        await bot.send_video(chat_id=callback.message.chat.id, video=res_media, caption=res_caption, reply_markup=ikb)
    elif (res_type == 0):
        await bot.send_photo(chat_id=callback.message.chat.id, photo=res_media, caption=res_caption, reply_markup=ikb)
    elif (res_type == 2):
        await bot.send_animation(chat_id=callback.message.chat.id, animation=res_media, caption=res_caption, reply_markup=ikb)


async def ikbadmin_back(callback: types.CallbackQuery):
    cur.execute("SELECT type FROM start_media_info WHERE id = 1")
    res_type = cur.fetchone()[0]
    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
    res_media = cur.fetchone()[0]
    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
    res_caption = cur.fetchone()[0]
    if (res_type == 1):
        await callback.message.edit_media(types.InputMedia(media=res_media, type='video', caption=res_caption),
                                          reply_markup=ikbadmin)
    elif (res_type == 0):
        await callback.message.edit_media(types.InputMedia(media=res_media, type='photo', caption=res_caption),
                                          reply_markup=ikbadmin)
    elif (res_type == 2):
        await callback.message.edit_media(types.InputMedia(media=res_media, type='animation', caption=res_caption),
                                          reply_markup=ikbadmin)


async def ikbadmin_back2(callback: types.CallbackQuery):
    await callback.message.delete()

    cur.execute("SELECT type FROM start_media_info WHERE id = 1")
    res_type = cur.fetchone()[0]
    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
    res_media = cur.fetchone()[0]
    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
    res_caption = cur.fetchone()[0]
    if (res_type == 1):
        await bot.send_video(chat_id=callback.message.chat.id, video=res_media, caption=res_caption, reply_markup=ikbadmin)
    elif (res_type == 0):
        await bot.send_photo(chat_id=callback.message.chat.id, photo=res_media, caption=res_caption, reply_markup=ikbadmin)
    elif (res_type == 2):
        await bot.send_animation(chat_id=callback.message.chat.id, animation=res_media, caption=res_caption,
                                 reply_markup=ikbadmin)

@dp.callback_query_handler()
async def cb_start(callback: types.CallbackQuery):
    global is_admin, ID
    if callback.data == 'Турниры':
        try:
            cur.execute("SELECT COUNT(*) FROM photos")
            result = cur.fetchone()
            cur.execute("SELECT * FROM photos LIMIT 1 OFFSET ?", (result[0] - 1,))
            photo_path_turnir = cur.fetchone()
            photo_path_turnir = f'{photo_path_turnir[0]}'
            cur.execute("SELECT COUNT(*) FROM caption_tur")
            result = cur.fetchone()
            cur.execute("SELECT * FROM caption_tur LIMIT 1 OFFSET ?", (result[0] - 1,))
            caption_path_turnir = cur.fetchone()[0]
            await callback.message.edit_media(types.InputMedia(media = photo_path_turnir, type = 'photo', caption = caption_path_turnir), reply_markup=ikb2)
        except:
            await callback.answer("Попробуйте немного позже")
            await bot.send_message(chat_id="340371976",
                                   text="Ошибка загрузки изображения или описания в разделе турниры. Загрузите другое изображение или описание.")
    elif callback.data == 'Акции':
        try:
            cur.execute("SELECT COUNT(*) FROM photos_akcii")
            result = cur.fetchone()
            cur.execute("SELECT * FROM photos_akcii LIMIT 1 OFFSET ?", (result[0] - 1,))
            photo_path_akcii = cur.fetchone()
            photo_path_akcii = f'{photo_path_akcii[0]}'
            cur.execute("SELECT COUNT(*) FROM caption_akcii")
            result = cur.fetchone()
            cur.execute("SELECT * FROM caption_akcii LIMIT 1 OFFSET ?", (result[0] - 1,))
            caption_path_akcii = cur.fetchone()[0]
            await callback.message.edit_media(types.InputMedia(media=photo_path_akcii, type='photo', caption=caption_path_akcii),
                                              reply_markup=ikb3)
        except:
            await callback.answer("Попробуйте немного позже")
            await bot.send_message(chat_id = "340371976", text = "Ошибка загрузки изображения или описания в разделе акции. Загрузите другое изображение или описание.")
    # elif callback.data == 'Мой баланс':
    #     async def your_balance(callback: types.CallbackQuery):
    #         global ID
    #         cur.execute("SELECT balance FROM users WHERE id = ?  ", (ID,))
    #         user_balance = cur.fetchone()
    #         if (user_balance == None):
    #             await callback.message.answer("Зарегистрируйтесь, чтобы узнать баланс")
    #         else:
    #             await callback.message.delete()
    #             await callback.bot.send_message(chat_id=callback.message.chat.id, text =f"Ваш баланс {user_balance[0]} рублей", reply_markup=ikb3)
    #     await your_balance(callback)

    # elif callback.data == 'Зарегистрироваться':
    #     global ID
    #     cur.execute("INSERT INTO users (id) VALUES (?)", (ID,))
    #     con.commit()
    #     global is_reg
    #     if (is_reg):
    #         await callback.message.answer("Вы зарегистрированы")
    #         return
    #     else:
    #         class REGISTRATION(StatesGroup):
    #             name = State()
    #             surname = State()
    #             number = State()
    #         await REGISTRATION.name.set()
    #         await callback.message.answer("Введите свое имя")
    #         @dp.message_handler(state = REGISTRATION.name)
    #         async def reg_name(message: types.Message, state = FSMContext):
    #             global ID
    #             if message.text.isalpha() == True:
    #                 cur.execute("UPDATE users SET name = ? WHERE id = ? ", (message.text, ID))
    #                 con.commit()
    #                 await message.answer("Введите свою фамилию")
    #                 await REGISTRATION.next()
    #             else:
    #                 await message.answer("Введите имя в текстовом формате")
    #                 return
    #         @dp.message_handler(state = REGISTRATION.surname)
    #         async def reg_surname(message: types.Message, state = FSMContext):
    #             global ID
    #             if message.text.isalpha() == True:
    #                 cur.execute("UPDATE users SET surname = ? WHERE id = ? ", (message.text, ID))
    #                 con.commit()
    #                 await message.answer("Введите свой номер телефона")
    #                 await REGISTRATION.next()
    #             else:
    #                 await message.answer("Введите фамилию в текстовом формате")
    #                 return
    #
    #         @dp.message_handler(state = REGISTRATION.number)
    #         async def reg_number(message: types.Message, state = FSMContext):
    #             global ID
    #             if message.text.isdigit() == True:
    #                 global is_reg
    #                 is_reg = True
    #                 cur.execute("UPDATE users SET number = ? WHERE id = ? ", (message.text, ID))
    #                 cur.execute("UPDATE users SET balance = 300 WHERE id = ? ", (ID,))
    #                 con.commit()
    #                 await message.answer("Вы успешно зарегистрировались!")
    #                 await start_commmand(message)
    #                 await state.finish()
    #             else:
    #                 await message.answer("Введите номер телефона цифрами")
    #                 return

    elif callback.data == "Назад1":
        try:
            await start_command_back(callback)
        except:
            await start_command_back2(callback)
    elif callback.data == "Назад2":
        try:
            await ikbadmin_back(callback)
        except:
            await ikbadmin_back2(callback)

    elif callback.data == "Зарегистрироваться!":
        await callback.answer("Здесь будет ссылка")

    elif callback.data == "Режим админа":
        if is_admin:
            await callback.message.edit_caption(caption = "",  reply_markup=ikbadmin)
        else:
            await callback.answer(text = "У вас нет прав")
    elif callback.data == "Изменить информацию по турнирам":
        if is_admin:
            await callback.message.edit_reply_markup(reply_markup=ikbadmin_tur)
        else:
            await callback.answer(text = "У вас нет прав")
    elif callback.data == "Изменить информацию по акциям":
        if is_admin:
            await callback.message.edit_reply_markup(reply_markup=ikbadmin_akcii)
        else:
            await callback.answer(text = "У вас нет прав")
    elif callback.data == "Изменить информацию по клубам":
        if is_admin:
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            ikbadmin_choose_club = InlineKeyboardMarkup()
            for i in range(1, int(result)+1):
                ikbadmin_choose_club.add(InlineKeyboardButton(text = f'Клуб {i}', callback_data=f'ИзменитьКлуб{i}'))
            ikbadmin_choose_club.add(InlineKeyboardButton(text = "Добавить клуб", callback_data="Добавить клуб"))
            ikbadmin_choose_club.add(InlineKeyboardButton(text="Удалить клуб", callback_data="Удалить клуб"))
            ikbadmin_choose_club.add(InlineKeyboardButton(text = "Назад", callback_data="Назад2"))
            await callback.message.edit_reply_markup(reply_markup = ikbadmin_choose_club)

        else:
            await callback.answer(text = "У вас нет прав")

    elif callback.data.startswith("ИзменитьКлуб"):
        try:
            i_club = callback.data[-1]
            change_club = InlineKeyboardMarkup()
            change_club.add(InlineKeyboardButton(text = "Изменить основное изображение клуба",
                                                 callback_data=f'MAIN{i_club}'))
            change_club.add(InlineKeyboardButton(text = "Изменить изображение/описание Цен",
                                                 callback_data= f'PRICE{i_club}'))
            change_club.add(InlineKeyboardButton(text = "Изменить изображение/описание Железа",
                                                 callback_data= f'METAL{i_club}'))
            change_club.add(InlineKeyboardButton(text="Изменить изображение/описание Акций",
                                                 callback_data= f'ACTIONS{i_club}'))
            change_club.add(InlineKeyboardButton(text = "Назад", callback_data="Назад2"))
            await callback.message.edit_reply_markup(reply_markup = change_club)
        except:
            await callback.message.answer("Ошибка")

    elif callback.data.startswith('MAIN'):
        if is_admin:

            class ClubEditPrice(StatesGroup):
                change_photo = State()

            i_club = callback.data[-1]
            await callback.message.answer("Пришлите изображение.\n"
                                          "Для отмены действий введите 'отмена'")
            await ClubEditPrice.change_photo.set()

            @dp.message_handler(Text(equals="отмена", ignore_case=True), state = ClubEditPrice.change_photo)
            @dp.message_handler(commands=["отмена"], state = ClubEditPrice.change_photo)
            async def club_otmena(message: types.Message, state = FSMContext):
                await message.answer("Действие отменено!", reply_markup=ikbadmin)
                await state.finish()

            @dp.message_handler(content_types=ContentType.PHOTO, state = ClubEditPrice.change_photo)
            async def club_1(message: types.Message, state = FSMContext):
                try:
                    photo = message.photo[-1].file_id
                    cur.execute("UPDATE clubs SET main = ? WHERE id = ?", (photo, i_club))
                    con.commit()
                    await message.answer("Изменения сохранены!", reply_markup=ikbadmin)
                    await state.finish()
                except:
                    await message.answer("Пришлите фото в явном виде (не файлом)\n"
                                         "Для отмены действий введите 'отмена'")
                    return

            @dp.message_handler(content_types=ContentType.ANY, state=ClubEditPrice.change_photo)
            async def club_2(message: types.Message, state=FSMContext):
                await message.answer("Пришлите фото в явном виде (не файлом)\n"
                                         "Для отмены действий введите 'отмена'")
        else:
            await callback.message.answer("У вас нет прав!")





    elif callback.data.startswith('PRICE'):
        if is_admin:
            photo_1 = ""
            class ClubEditPrice(StatesGroup):
                change_photo = State()
                photo = State()
                change_description = State()
                description = State()
            i_club = callback.data[-1]
            await ClubEditPrice.change_photo.set()
            await callback.message.answer('Вы хотите изменить <b>изображение</b>? Ответьте "да" или "нет".\n'
                                          ' (если вы хотите отменить действия, введите "отмена")', parse_mode='HTML')

            @dp.message_handler(commands=["отмена"], state="*")
            @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
            async def ClubEditPrice_otmena(message: types.Message, state=FSMContext):
                await callback.message.answer("Действие отменено!", reply_markup=ikbadmin)
                await state.finish()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditPrice.change_photo)
            async def ClubEditPrice_first(message: types.Message, state=ClubEditPrice.change_photo):
                await callback.message.answer('Пришлите фото, на которое хотите заменить текущее.\n'
                                              ' (для отмены действий введите "отмена")')
                await ClubEditPrice.next()

            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditPrice.change_photo)
            async def ClubEditPrice_second(message: types.Message, state=ClubEditPrice.change_photo):
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              '(для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditPrice.change_description.set()

            @dp.message_handler(content_types=ContentType.ANY, state=ClubEditPrice.photo)
            async def ClubEditPrice_third(message: types.Message, state=FSMContext):
                if message.photo:
                    async with state.proxy() as data:
                        data['photo_1'] = message.photo[-1].file_id
                else:
                    await message.answer('Пришлите фотографию, а не другое сообщение.\n'
                                         ' (для отмены действий введите "отмена")')
                    return
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              ' (для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditPrice.change_description.set()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditPrice.change_description)
            async def ClubEditPrice_fourth(message: types.Message, state=ClubEditPrice.change_description):
                await callback.message.answer('Пришлите описание.\n'
                                              '(для отмены действий введите "отмена")')
                await ClubEditPrice.description.set()

            @dp.message_handler(content_types=ContentType.TEXT, state=ClubEditPrice.description)
            async def ClubEditPrice_fifth(message: types.Message, state=FSMContext):
                try:
                    try:
                        description = message.text
                        cur.execute("UPDATE clubs SET price_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET price = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT price FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT price_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description, reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        description = message.text
                        cur.execute("UPDATE clubs SET price_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT price FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT price_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()

                except:
                    await message.answer('Произошла ошибка. Пришлите описание заново.\n')
                    return


            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditPrice.change_description)
            async def ClubEditPrice_sixth(message: types.Message, state=FSMContext):
                try:
                    try:
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET price = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT price FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT price_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description, reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT price FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT price_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()

                except:
                    await callback.message.answer("Произошла ошибка. Возможно, проблемы с фотографией.\n"
                                                  "Заполните поля заново.",
                                                  reply_markup=ikbadmin)
                    await state.finish()
        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data.startswith('METAL'):
        if is_admin:
            photo_1 = ""

            class ClubEditMetal(StatesGroup):
                change_photo = State()
                photo = State()
                change_description = State()
                description = State()

            i_club = callback.data[-1]
            await ClubEditMetal.change_photo.set()
            await callback.message.answer('Вы хотите изменить <b>изображение</b>? Ответьте "да" или "нет".\n'
                                          ' (если вы хотите отменить действия, введите "отмена")', parse_mode='HTML')

            @dp.message_handler(commands=["отмена"], state="*")
            @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
            async def ClubEditMetal_otmena(message: types.Message, state=FSMContext):
                await callback.message.answer("Действие отменено!", reply_markup=ikbadmin)
                await state.finish()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditMetal.change_photo)
            async def ClubEditMetal_first(message: types.Message, state=ClubEditMetal.change_photo):
                await callback.message.answer('Пришлите фото, на которое хотите заменить текущее.\n'
                                              ' (для отмены действий введите "отмена")')
                await ClubEditMetal.next()

            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditMetal.change_photo)
            async def ClubEditMetal_second(message: types.Message, state=ClubEditMetal.change_photo):
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              '(для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditMetal.change_description.set()

            @dp.message_handler(content_types=ContentType.ANY, state=ClubEditMetal.photo)
            async def ClubEditMetal_third(message: types.Message, state=FSMContext):
                if message.photo:
                    async with state.proxy() as data:
                        data['photo_1'] = message.photo[-1].file_id
                else:
                    await message.answer('Пришлите фотографию, а не другое сообщение.\n'
                                         ' (для отмены действий введите "отмена")')
                    return
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              ' (для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditMetal.change_description.set()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditMetal.change_description)
            async def ClubEditMetal_fourth(message: types.Message, state=ClubEditMetal.change_description):
                await callback.message.answer('Пришлите описание.\n'
                                              '(для отмены действий введите "отмена")')
                await ClubEditMetal.description.set()

            @dp.message_handler(content_types=ContentType.TEXT, state=ClubEditMetal.description)
            async def ClubEditMetal_fifth(message: types.Message, state=FSMContext):
                try:
                    try:
                        description = message.text
                        cur.execute("UPDATE clubs SET accessories_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET accessories = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT accessories FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT accessories_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        description = message.text
                        cur.execute("UPDATE clubs SET accessories_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT accessories FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT accessories_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()

                except:
                    await message.answer('Произошла ошибка. Пришлите описание заново.')
                    return

            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditMetal.change_description)
            async def ClubEditMetal_sixth(message: types.Message, state=FSMContext):
                try:
                    try:
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET accessories = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT accessories FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT accessories_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT accessories FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT accessories_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                except:
                    await callback.message.answer("Произошла ошибка. Возможно, проблемы с фотографией.\n"
                                                  "Заполните поля заново.",
                                                  reply_markup=ikbadmin)
                    await state.finish()
        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data.startswith('ACTIONS'):
        if is_admin:
            photo_1 = ""

            class ClubEditActions(StatesGroup):
                change_photo = State()
                photo = State()
                change_description = State()
                description = State()

            i_club = callback.data[-1]
            await ClubEditActions.change_photo.set()
            await callback.message.answer('Вы хотите изменить <b>изображение</b>? Ответьте "да" или "нет".\n'
                                          ' (если вы хотите отменить действия, введите "отмена")', parse_mode='HTML')

            @dp.message_handler(commands=["отмена"], state="*")
            @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
            async def ClubEditActions_otmena(message: types.Message, state=FSMContext):
                await callback.message.answer("Действие отменено!", reply_markup=ikbadmin)
                await state.finish()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditActions.change_photo)
            async def ClubEditActions_first(message: types.Message, state=ClubEditActions.change_photo):
                await callback.message.answer('Пришлите фото, на которое хотите заменить текущее.\n'
                                              ' (для отмены действий введите "отмена")')
                await ClubEditActions.next()

            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditActions.change_photo)
            async def ClubEditActions_second(message: types.Message, state=ClubEditActions.change_photo):
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              '(для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditActions.change_description.set()

            @dp.message_handler(content_types=ContentType.ANY, state=ClubEditActions.photo)
            async def ClubEditActions_third(message: types.Message, state=FSMContext):
                if message.photo:
                    async with state.proxy() as data:
                        data['photo_1'] = message.photo[-1].file_id
                else:
                    await message.answer('Пришлите фотографию, а не другое сообщение.\n'
                                         ' (для отмены действий введите "отмена")')
                    return
                await callback.message.answer('Вы хотите изменить <b>описание</b>? Ответьте "да" или "нет".\n'
                                              ' (для отмены действий введите "отмена")', parse_mode='HTML')
                await ClubEditActions.change_description.set()

            @dp.message_handler(Text(equals="да", ignore_case=True), state=ClubEditActions.change_description)
            async def ClubEditActions_fourth(message: types.Message, state=ClubEditActions.change_description):
                await callback.message.answer('Пришлите описание.\n'
                                              '(для отмены действий введите "отмена")')
                await ClubEditActions.description.set()

            @dp.message_handler(content_types=ContentType.TEXT, state=ClubEditActions.description)
            async def ClubEditActions_fifth(message: types.Message, state=FSMContext):
                try:
                    try:
                        description = message.text
                        cur.execute("UPDATE clubs SET akcii_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET akcii = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT akcii FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT akcii_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        description = message.text
                        cur.execute("UPDATE clubs SET akcii_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT akcii FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT akcii_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()

                except:
                    await message.answer('Произошла ошибка. Пришлите описание заново.\n')
                    return

            @dp.message_handler(Text(equals="нет", ignore_case=True), state=ClubEditActions.change_description)
            async def ClubEditActions_sixth(message: types.Message, state=FSMContext):
                try:
                    try:
                        async with state.proxy() as data:
                            cur.execute("UPDATE clubs SET akcii = ? WHERE id = ?", (data['photo_1'], i_club))
                            con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT akcii FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT akcii_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                    except:
                        description = message.text
                        cur.execute("UPDATE clubs SET akcii_des = ? WHERE id = ?", (description, i_club))
                        con.commit()
                        await message.answer("Изменения сохранены. Вот, как выглядит ваш пост:")
                        cur.execute("SELECT akcii FROM clubs WHERE id = ?", (i_club,))
                        photo = cur.fetchone()[0]
                        cur.execute("SELECT akcii_des FROM clubs WHERE id = ?", (i_club,))
                        description = cur.fetchone()[0]
                        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=description,
                                                     reply_markup=ikbadmin)
                        await state.finish()
                except:
                    await callback.message.answer("Произошла ошибка. Возможно, проблемы с фотографией.\n"
                                                  "Заполните поля заново.",
                                                  reply_markup=ikbadmin)
                    await state.finish()
        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data == "Изменить изображение турниров":
        if is_admin:
            class EditPhotoAdmin_TUR(StatesGroup):
                photo = State()

            await EditPhotoAdmin_TUR.photo.set()
            await callback.message.answer("Пришлите новое изображение.\n"
                                  "(если вы хотите отменить изменение изображения, введите 'отмена')")

            @dp.message_handler(state=EditPhotoAdmin_TUR.photo, commands=['отмена'])
            @dp.message_handler(Text(equals='отмена', ignore_case=True), state=EditPhotoAdmin_TUR.photo)
            async def handle_otmena(message: types.Message, state: FSMContext):
                await state.finish()
                await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin, parse_mode='HTML')

            @dp.message_handler(state=EditPhotoAdmin_TUR.photo, content_types=ContentType.PHOTO)
            async def load_photo(message: types.Message, state: FSMContext):
                photo_path_tur = message.photo[-1].file_id
                cur.execute("INSERT INTO photos(url) VALUES (?)", (photo_path_tur,))
                con.commit()
                await message.answer("<b>Фото успешно загружено!</b>", reply_markup=ikbadmin, parse_mode='HTML')
                await state.finish()

            @dp.message_handler(state=EditPhotoAdmin_TUR.photo, content_types=ContentType.ANY)
            async def handle_non_text_content(message: types.Message, state: FSMContext):
                await message.answer("Пожалуйста, пришлите изображение.\n"
                                     "(если вы хотите отменить изменение изображения, введите 'отмена')")
                return

        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data == "Изменить изображение акций":
        if is_admin:
            class EditPhotoAdmin_ACT(StatesGroup):
                photo = State()

            await EditPhotoAdmin_ACT.photo.set()
            await callback.message.answer("Пришлите новое изображение.\n"
                                  "(если вы хотите отменить изменение изображения, введите 'отмена')")

            @dp.message_handler(state=EditPhotoAdmin_ACT.photo, commands=['отмена'])
            @dp.message_handler(Text(equals='отмена', ignore_case=True), state=EditPhotoAdmin_ACT.photo)
            async def handle_otmena(message: types.Message, state: FSMContext):
                await state.finish()
                await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin, parse_mode='HTML')

            @dp.message_handler(state=EditPhotoAdmin_ACT.photo, content_types= ContentType.PHOTO)
            async def load_photo(message: types.Message, state: FSMContext):
                photo_path_akcii = message.photo[-1].file_id
                cur.execute("INSERT INTO photos_akcii(url) VALUES (?)", (photo_path_akcii,))
                con.commit()
                await message.answer("<b>Фото успешно загружено!</b>", reply_markup=ikbadmin, parse_mode='HTML')
                await state.finish()

            @dp.message_handler(state=EditPhotoAdmin_ACT.photo, content_types=ContentType.ANY)
            async def handle_non_text_content(message: types.Message, state: FSMContext):
                await message.answer("Пожалуйста, пришлите изображение.\n"
                                     "(если вы хотите отменить изменение изображения, введите 'отмена')")
                return

        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data == "Изменить описание турниров":
        if is_admin:
            class EditCaptionAdmin_TUR(StatesGroup):
                caption = State()
            await EditCaptionAdmin_TUR.caption.set()
            await callback.message.answer("Пришлите новое описание.\n"
                                          "(если вы хотите отменить изменение описания, введите 'отмена')")

            @dp.message_handler(state=EditCaptionAdmin_TUR.caption, commands=['отмена'])
            @dp.message_handler(Text(equals='отмена', ignore_case=True), state=EditCaptionAdmin_TUR.caption)
            async def handle_otmena_caption_tur(message: types.Message, state: FSMContext):
                await state.finish()
                await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin, parse_mode='HTML')

            @dp.message_handler(state=EditCaptionAdmin_TUR.caption, content_types= ContentType.TEXT)
            async def load_caption_tur(message: types.Message, state: FSMContext):
                photo_path_caption_tur = message.text
                cur.execute("INSERT INTO caption_tur (caption) VALUES (?)", (photo_path_caption_tur,))
                con.commit()
                await message.answer("<b>Описание успешно загружено!</b>", reply_markup=ikbadmin, parse_mode='HTML')
                await state.finish()

            @dp.message_handler(state = EditCaptionAdmin_TUR.caption, content_types=ContentType.ANY)
            async def load_caption_tur_non_text(message: types.Message, state: FSMContext):
                await message.answer(text = "Пожалуйста, пришлите описание в текстовом формате")
                return

        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data == "Изменить описание акций":
        if is_admin:
            class EditCaptionAdmin_ACT(StatesGroup):
                caption = State()
            await EditCaptionAdmin_ACT.caption.set()
            await callback.message.answer("Пришлите новое описание.\n"
                                          "(если вы хотите отменить изменение описания, введите 'отмена')")

            @dp.message_handler(state=EditCaptionAdmin_ACT.caption, commands=['отмена'])
            @dp.message_handler(Text(equals='отмена', ignore_case=True), state=EditCaptionAdmin_ACT.caption)
            async def handle_otmena_caption_akcii(message: types.Message, state: FSMContext):
                await state.finish()
                await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin, parse_mode='HTML')

            @dp.message_handler(state=EditCaptionAdmin_ACT.caption, content_types=ContentType.TEXT)
            async def load_caption_akcii(message: types.Message, state: FSMContext):
                photo_path_caption_akcii = message.text
                cur.execute("INSERT INTO caption_akcii (caption) VALUES (?)", (photo_path_caption_akcii,))
                con.commit()
                await message.answer("<b>Описание успешно загружено!</b>", reply_markup=ikbadmin, parse_mode='HTML')
                await state.finish()

            @dp.message_handler(state=EditCaptionAdmin_ACT.caption, content_types=ContentType.ANY)
            async def load_caption_tur_non_text(message: types.Message, state: FSMContext):
                await message.answer(text="Пожалуйста, пришлите описание в текстовом формате")
                return
        else:
            await callback.answer(text="У вас нет прав")

    elif callback.data == "Добавить клуб":
        cur.execute("SELECT COUNT(*) FROM clubs")
        result = cur.fetchone()[0]
        class AddClubAdmin(StatesGroup):
            price = State()
            accessories = State()
            akcii = State()
            main = State()
        await AddClubAdmin.price.set()
        await callback.message.answer("Пришлите изображение для раздела цены.\n"
                                      "(если вы хотите отменить добавление клуба, введите 'отмена')")

        @dp.message_handler(state=AddClubAdmin.price,
                            commands=['отмена'])
        @dp.message_handler(Text(equals='отмена', ignore_case=True), state=AddClubAdmin.price)
        async def handle_otmena_delete_club(message: types.Message, state: FSMContext):
            await state.finish()
            await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin,
                                 parse_mode='HTML')

        @dp.message_handler(state=[AddClubAdmin.akcii, AddClubAdmin.accessories, AddClubAdmin.main],
                            commands=['отмена'])
        @dp.message_handler(Text(equals='отмена', ignore_case=True), state=[AddClubAdmin.akcii, AddClubAdmin.accessories])
        async def handle_otmena_delete_club_1(message: types.Message, state: FSMContext):
            await state.finish()
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            cur.execute("DELETE FROM clubs WHERE id = ?", (result, ))
            con.commit()
            await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin,
                                 parse_mode='HTML')

        @dp.message_handler(state=AddClubAdmin.price, content_types=ContentType.PHOTO)
        async def load_photo_1(message: types.Message, state: FSMContext):
            photo_add_club = message.photo[-1].file_id
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            cur.execute("INSERT INTO clubs (id, price) VALUES (?, ?) ", (result+1, photo_add_club))
            con.commit()
            await message.answer("Пришлите изображение для раздела железо.\n"
                                      "(если вы хотите отменить добавление клуба, введите 'отмена')")
            await AddClubAdmin.next()
            return

        @dp.message_handler(state=AddClubAdmin.accessories, content_types=ContentType.PHOTO)
        async def load_photo_2(message: types.Message, state: FSMContext):
            photo_add_club = message.photo[-1].file_id
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            cur.execute("UPDATE clubs SET accessories = ? WHERE id = ? ", (photo_add_club, result))
            con.commit()
            await message.answer("Пришлите изображение для раздела акции.\n"
                                 "(если вы хотите отменить добавление клуба, введите 'отмена')")
            await AddClubAdmin.next()
            return

        @dp.message_handler(state=AddClubAdmin.akcii, content_types=ContentType.PHOTO)
        async def load_photo_3(message: types.Message, state: FSMContext):
            photo_add_club = message.photo[-1].file_id
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            cur.execute("UPDATE clubs SET akcii = ? WHERE id = ? ", (photo_add_club, result))
            con.commit()
            await message.answer("Пришлите изображение для основного раздела клуба.\n"
                                 "(если вы хотите отменить добавление клуба, введите 'отмена')")
            await AddClubAdmin.next()
            return

        @dp.message_handler(state=AddClubAdmin.main, content_types=ContentType.PHOTO)
        async def load_photo_4(message: types.Message, state: FSMContext):
            photo_add_club = message.photo[-1].file_id
            cur.execute("SELECT COUNT(*) FROM clubs")
            result = cur.fetchone()[0]
            cur.execute("UPDATE clubs SET main = ? WHERE id = ? ", (photo_add_club, result))
            con.commit()
            await message.answer("<b>Клуб добавлен!</b>", reply_markup=ikbadmin, parse_mode='HTML')
            await state.finish()
            return


        @dp.message_handler(state=[AddClubAdmin.price, AddClubAdmin.akcii, AddClubAdmin.accessories, AddClubAdmin.main], content_types=ContentType.ANY)
        async def handle_non_text_content(message: types.Message, state: FSMContext):
            await message.answer("Пожалуйста, пришлите именно изображение.\n"
                                 "(если вы хотите отменить добавление клуба, введите 'отмена')")
            return

    elif callback.data.startswith("Клуб "):
        i_club = callback.data[-1]
        cur.execute("SELECT main FROM clubs WHERE id = ?", (i_club,))
        res_main = cur.fetchone()[0]
        ikb_clubs = InlineKeyboardMarkup()
        ikb_clubs_1 = InlineKeyboardButton(text="Цены", callback_data=f'ЦеныКлуб{i_club}')
        ikb_clubs_2 = InlineKeyboardButton(text="Железо", callback_data=f'ЖелезоКлуб{i_club}')
        ikb_clubs_3 = InlineKeyboardButton(text="Акции", callback_data=f'АкцииКлуб{i_club}')
        ikb_clubs_4 = InlineKeyboardButton(text="Назад", callback_data="Назад1")
        ikb_clubs.add(ikb_clubs_1).add(ikb_clubs_2).add(ikb_clubs_3).add(ikb_clubs_4)
        await callback.message.edit_media(types.InputMedia(media= res_main, type='photo'), reply_markup=ikb_clubs)


    elif callback.data.startswith("НазадКлуб"):
        i_club = callback.data[-1]
        cur.execute("SELECT main FROM clubs WHERE id = ?", (i_club,))
        res_main = cur.fetchone()[0]
        ikb_clubs = InlineKeyboardMarkup()
        ikb_clubs_1 = InlineKeyboardButton(text="Цены", callback_data=f'ЦеныКлуб{i_club}')
        ikb_clubs_2 = InlineKeyboardButton(text="Железо", callback_data=f'ЖелезоКлуб{i_club}')
        ikb_clubs_3 = InlineKeyboardButton(text="Акции", callback_data=f'АкцииКлуб{i_club}')
        ikb_clubs_4 = InlineKeyboardButton(text="Назад", callback_data="Назад1")
        ikb_clubs.add(ikb_clubs_1).add(ikb_clubs_2).add(ikb_clubs_3).add(ikb_clubs_4)
        await callback.message.edit_media(types.InputMedia(media=res_main, type='photo'),
                                          reply_markup=ikb_clubs)

    elif callback.data.startswith("ЦеныКлуб"):
        i_club = callback.data[-1]
        cur.execute("SELECT price FROM clubs WHERE id = ?", (i_club, ))
        photo_path = cur.fetchone()[0]
        cur.execute("SELECT price_des FROM clubs WHERE id = ?", (i_club,))
        des_path = cur.fetchone()[0]
        i_clubs_back = InlineKeyboardMarkup()
        i_clubs_back1 = InlineKeyboardButton(text = "Назад", callback_data=f'НазадКлуб{i_club}')
        i_clubs_back.add(i_clubs_back1)
        try:
            await callback.message.edit_media(types.InputMedia(media=photo_path, type='photo', caption = des_path),
                                              reply_markup=i_clubs_back)

        except:
            await callback.answer("Попробуйте позже")
            await callback.bot.send_message(chat_id = '340371976', text = f'Ошибка в разделе "Цены" клуба номер {i_club}')

    elif callback.data.startswith("ЖелезоКлуб"):
        i_club = callback.data[-1]
        cur.execute("SELECT accessories FROM clubs WHERE id = ?", (i_club, ))
        photo_path = cur.fetchone()[0]
        cur.execute("SELECT accessories_des FROM clubs WHERE id = ?", (i_club,))
        des_path = cur.fetchone()[0]
        i_clubs_back = InlineKeyboardMarkup()
        i_clubs_back1 = InlineKeyboardButton(text = "Назад", callback_data=f'НазадКлуб{i_club}')
        i_clubs_back.add(i_clubs_back1)
        try:
            await callback.message.edit_media(types.InputMedia(media=photo_path, type='photo', caption = des_path),
                                              reply_markup=i_clubs_back)
        except:
            await callback.answer("Попробуйте позже")
            await callback.bot.send_message(chat_id = '340371976', text = f'Ошибка в разделе "Железо" клуба номер {i_club}')

    elif callback.data.startswith("АкцииКлуб"):
        i_club = callback.data[-1]
        cur.execute("SELECT akcii FROM clubs WHERE id = ?", (i_club, ))
        photo_path = cur.fetchone()[0]
        cur.execute("SELECT akcii_des FROM clubs WHERE id = ?", (i_club,))
        des_path = cur.fetchone()[0]
        i_clubs_back = InlineKeyboardMarkup()
        i_clubs_back1 = InlineKeyboardButton(text = "Назад", callback_data=f'НазадКлуб{i_club}')
        i_clubs_back.add(i_clubs_back1)
        try:
            await callback.message.edit_media(types.InputMedia(media=photo_path, type='photo', caption = des_path),
                                              reply_markup=i_clubs_back)
        except:
            await callback.answer("Попробуйте позже")
            await callback.bot.send_message(chat_id = '340371976', text = f'Ошибка в разделе "Акции" клуба номер {i_club}')


    elif callback.data == "Удалить клуб":
        class Delete_Club(StatesGroup):
            nomer = State()
        await Delete_Club.nomer.set()
        await callback.message.answer('Введите номер клуба, который вы хотите удалить (если хотите отменить действие, введите "отмена")')

        @dp.message_handler(Text(equals='отмена', ignore_case=True), state=Delete_Club.nomer)
        @dp.message_handler(commands=["отмена"], state=Delete_Club.nomer)
        async def delete_club_admin_cancel(message: types.Message, state=FSMContext):
            await message.answer("<b>Действие отменено</b>", reply_markup=ikbadmin, parse_mode='HTML')
            await state.finish()

        @dp.message_handler(state = Delete_Club.nomer, content_types=ContentType.TEXT)
        async def delete_club_admin(message: types.Message, state = FSMContext):
            if message.text.isdigit() == True:
                club = message.text
                cur.execute("SELECT COUNT(*) FROM clubs")
                result = cur.fetchone()[0]
                if (int(club) <= int(result) and int(club) > 0):
                    cur.execute("DELETE FROM clubs WHERE id = ?", (club, ))
                    con.commit()
                    await message.answer("<b>Клуб удален!</b>", reply_markup=ikbadmin, parse_mode='HTML')
                    await state.finish()
                    for i in range(int(club)+1, int(result)+1):
                        cur.execute("UPDATE clubs SET id = ? WHERE id = ?", (i-1, i))
                        con.commit()
                else:
                    await message.answer('Введите верный номер клуба (если хотите отменить действие, введите "отмена"')
                    return
            else:
                await message.answer("Введите номер клуба цифрами")
                return

    elif callback.data == "Сделать рассылку":
        flag_rassilka = 0
        media_add = ""
        description_rassilka = ""
        class Rassilka(StatesGroup):
            photo_or_video = State()
            media = State()
            description = State()
            sure = State()

        await Rassilka.photo_or_video.set()
        await callback.message.answer('Прикрепить к посту видео или фото?\n'
                                      'Ответьте "видео" или "фото".\n'
                                      'Если медиа не будет, отправьте "нет медиа"')

        @dp.message_handler(state = Rassilka.photo_or_video, content_types=ContentType.TEXT)
        async def rassilka_first(message: types.Message, state: FSMContext):
            text = message.text.lower().strip()
            if (text == "видео"):
                await message.answer("Пришлите видео")
                await Rassilka.next()
                async with state.proxy() as data:
                    data['flag_rassilka'] = 2
            elif (text == "фото"):
                await message.answer("Пришлите фото")
                await Rassilka.next()
                async with state.proxy() as data:
                    data['flag_rassilka'] = 1
            elif (text == "нет медиа"):
                await message.answer("Пришлите описание к посту")
                await Rassilka.description.set()
                async with state.proxy() as data:
                    data['flag_rassilka'] = 0
            else:
                await message.answer("Нет такого варианта ответа")
                return
        @dp.message_handler(state = Rassilka.media, content_types=[ContentType.PHOTO])
        async def rassilka_second(message: types.Message, state: FSMContext):
            try:
                async with state.proxy() as data:
                    data['media_add'] = message.photo[-1].file_id
                await message.answer("Теперь пришлите описание к посту")
                await Rassilka.next()
            except:
                await message.answer("Пришлите изображение в явном виде (не файлом)")
                return


        @dp.message_handler(state=Rassilka.media, content_types=[ContentType.VIDEO, ContentType.VIDEO_NOTE, ContentType.ANIMATION])
        async def rassilka_second(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['media_add'] = data['media_add'] = message.video.file_id if message.video else message.animation.file_id
            await message.answer("Теперь пришлите описание к посту")
            await Rassilka.next()

        @dp.message_handler(state = Rassilka.description, content_types=ContentType.TEXT)
        async def rassilka_third(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['description_rassilka'] = message.text
            try:
                await message.answer("Вот, как будет выглядеть пост:")
                async with state.proxy() as data:
                    if (data['flag_rassilka'] == 2):
                        await message.bot.send_video(chat_id=message.chat.id, video=data['media_add'], caption=data['description_rassilka'])

                    elif (data['flag_rassilka'] == 1):
                        await message.bot.send_photo(chat_id = message.chat.id, photo = data['media_add'], caption=data['description_rassilka'])
                    elif (data['flag_rassilka'] == 0):
                        await message.bot.send_message(chat_id=message.chat.id, text = data['description_rassilka'])
                    await message.answer('Все верно? (Ответьте "да" или "нет")')
                    await Rassilka.next()
            except:
                await message.answer("Возникла ошибка, скорее всего, проблема в медиа. Попробуйте заново заполнить пост",
                                     reply_markup=ikbadmin)
                await state.finish()

        @dp.message_handler(Text(equals="да", ignore_case=True), state =Rassilka.sure)
        async def rassilka_fourth(message: types.Message, state = FSMContext):
            try:
                cur.execute("SELECT id FROM users_all")
                result = cur.fetchall()
                for i in range(0, len(result)):
                    id = result[i][0]
                    async with state.proxy() as data:
                        if (data['flag_rassilka'] == 2):
                            await message.bot.send_video(chat_id=id, video=data['media_add'],
                                                         caption=data['description_rassilka'])
                        elif (data['flag_rassilka'] == 1):
                            await message.bot.send_photo(chat_id=id, photo=data['media_add'], caption=data['description_rassilka'])
                        elif (data['flag_rassilka'] == 0):
                            await message.bot.send_message(chat_id=id, text=data['description_rassilka'])
                await message.answer("Рассылка выполнена успешно!", reply_markup=ikbadmin)
                await state.finish()
            except:
                await message.answer("Произошла ошибка в рассылке, попробуйте еще раз", reply_markup=ikbadmin)
                await state.finish()

        @dp.message_handler(Text(equals="нет", ignore_case=True), state=Rassilka.sure)
        async def rassilka_fourth(message: types.Message, state=FSMContext):
            await message.answer("Тогда попробуйте еще раз заполнить пост.", reply_markup=ikbadmin)
            await state.finish()

    elif callback.data == "Изменить информацию по /start":
        media_start_1 = ""
        description_1 = ""
        type = 0
        class EditStartAdmin(StatesGroup):
            what = State()
            change_media = State()
            change_des = State()
            sure_media = State()
            sure_des = State()
        await EditStartAdmin.what.set()
        await callback.message.answer("Вы хотите изменить медиа или описание?\n"
                                      "(ответьте 'медиа' или 'описание')")

        @dp.message_handler(commands=["отмена"], state="*")
        @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
        async def EditStartAdmin_otmena(message: types.Message, state = FSMContext):
            await callback.message.answer("Действие отменено!", reply_markup=ikbadmin)
            await state.finish()

        @dp.message_handler(Text(equals="медиа", ignore_case=True), state = EditStartAdmin.what)
        async def EditAdmin_first(message: types.Message, state = FSMContext):
            await message.answer("Пришлите видео или фото в явном виде (не файлом)\n"
                                 "Для отмены действий введите 'отмена'")
            await EditStartAdmin.change_media.set()

        @dp.message_handler(Text(equals="описание", ignore_case=True), state=EditStartAdmin.what)
        async def EditAdmin_second(message: types.Message, state=FSMContext):
            await message.answer("Пришлите описание в текстовом формате.\n"
                                 "Для отмены действий введите 'отмена'")
            await EditStartAdmin.change_des.set()

        @dp.message_handler(content_types=[ContentType.VIDEO, ContentType.PHOTO, ContentType.ANIMATION], state=EditStartAdmin.change_media)
        async def EditAdmin_third(message: types.Message, state = FSMContext):
            async with state.proxy() as data:
                if (message.photo):
                    media_start = message.photo[-1].file_id
                    await message.answer("Вот, как будет выглядеть пост:")
                    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_photo(chat_id = message.from_user.id, photo = media_start, caption= cap)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['media_start_1'] = media_start
                    data['type'] = 0
                    await EditStartAdmin.sure_media.set()
                elif (message.video):
                    media_start = message.video.file_id
                    await message.answer("Вот, как будет выглядеть пост:")
                    print("Видео")
                    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_video(chat_id = message.from_user.id, video=media_start, caption=cap)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['media_start_1'] = media_start
                    data['type'] = 1
                    await EditStartAdmin.sure_media.set()
                elif (message.animation):
                    media_start = message.animation.file_id
                    await message.answer("Вот, как будет выглядеть пост:")
                    print("Анимация")
                    cur.execute("SELECT caption FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_animation(chat_id = message.from_user.id, animation=media_start, caption=cap)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['media_start_1'] = media_start
                    data['type'] = 2
                    await EditStartAdmin.sure_media.set()

        @dp.message_handler(content_types=ContentType.ANY, state = EditStartAdmin.change_media)
        async def EditAdmin_fourth(message: types.Message, state: FSMContext):
            await message.answer("Пришлите медиа в явном виде (не файлом).\n"
                                 "Для отмены действий введите 'отмена'")

        @dp.message_handler(Text(equals="да", ignore_case=True), state = EditStartAdmin.sure_media)
        async def EditAdmin_fifth(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                cur.execute("UPDATE start_media_info SET media = ? WHERE id = 1", (data['media_start_1'],))
                cur.execute("UPDATE start_media_info SET type = ? WHERE id = 1", (data['type'], ))
                con.commit()
            await message.answer("Изменения сохранены!", reply_markup=ikbadmin)
            await state.finish()

        @dp.message_handler(Text(equals="нет", ignore_case=True), state=EditStartAdmin.sure_media)
        async def EditAdmin_sixth(message: types.Message, state: FSMContext):
            await message.answer("Действия отменены!", reply_markup=ikbadmin)
            await state.finish()


        @dp.message_handler(content_types=ContentType.TEXT, state = EditStartAdmin.change_des)
        async def EditAdmin_seventh(message: types.Message, state: FSMContext):

            des_start = message.text
            cur.execute("SELECT type FROM start_media_info WHERE id = 1")
            result = cur.fetchone()[0]

            async with state.proxy() as data:
                if (result == 0):
                    await message.answer("Вот, как будет выглядеть пост:")
                    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_photo(chat_id=message.from_user.id, photo=cap, caption=des_start)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['description_1'] = des_start
                    await EditStartAdmin.sure_des.set()
                elif (result == 1):
                    await message.answer("Вот, как будет выглядеть пост:")
                    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_video(chat_id=message.from_user.id, video=cap, caption=des_start)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['description_1'] = des_start
                    await EditStartAdmin.sure_des.set()
                elif (result == 2):
                    await message.answer("Вот, как будет выглядеть пост:")
                    cur.execute("SELECT media FROM start_media_info WHERE id = 1")
                    cap = cur.fetchone()[0]
                    await bot.send_animation(chat_id=message.from_user.id, animation=cap, caption=des_start)
                    await message.answer("Все верно? (ответьте 'да' или 'нет')")
                    data['description_1'] = des_start
                    await EditStartAdmin.sure_des.set()

        @dp.message_handler(Text(equals="да", ignore_case=True), state = EditStartAdmin.sure_des)
        async def EditAdmin_eighth(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                cur.execute("UPDATE start_media_info SET caption = ? WHERE id = 1", (data['description_1'],))
                con.commit()
            await message.answer("Изменения сохранены!", reply_markup=ikbadmin)
            await state.finish()

        @dp.message_handler(Text(equals="нет", ignore_case=True), state=EditStartAdmin.sure_media)
        async def EditAdmin_nineth(message: types.Message, state: FSMContext):
            await message.answer("Действия отменены!", reply_markup=ikbadmin)
            await state.finish()





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)














