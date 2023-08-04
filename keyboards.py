from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb2 = InlineKeyboardMarkup()
ikb21 = InlineKeyboardButton(text = "Зарегистрироваться!", callback_data="Зарегистрироваться!")
ikb22 = InlineKeyboardButton(text = "Назад", callback_data="Назад1")
ikb2.add(ikb21).add(ikb22)

ikb3 = InlineKeyboardMarkup()
ikb31 = InlineKeyboardButton(text= "Назад", callback_data="Назад1")
ikb3.add(ikb31)

ikbadmin = InlineKeyboardMarkup()
ikbadmin1 = InlineKeyboardButton(text = "Изменить информацию по турнирам", callback_data="Изменить информацию по турнирам")
ikbadmin2 = InlineKeyboardButton(text = "Изменить информацию по акциям", callback_data="Изменить информацию по акциям")
ikbadmin3 = InlineKeyboardButton(text = "Изменить информацию по клубам", callback_data="Изменить информацию по клубам")
ikbadmin5 =  InlineKeyboardButton(text = "Сделать рассылку", callback_data="Сделать рассылку")
ikbadmin6 = InlineKeyboardButton(text = "Изменить информацию по /start", callback_data= "Изменить информацию по /start")
ikbadmin4 = InlineKeyboardButton(text = "Назад", callback_data="Назад1")
ikbadmin.add(ikbadmin1).add(ikbadmin2).add(ikbadmin3).add(ikbadmin6).add(ikbadmin5).add(ikbadmin4)

ikb_admin_start = InlineKeyboardMarkup()
ikb_admin_start_1 = InlineKeyboardButton(text = "Изменить видео", callback_data= "Изменить видео start")
ikb_admin_start_2 = InlineKeyboardButton(text = "Изменить описание", callback_data="Изменить описание start")
ikb_admin_start_3 = InlineKeyboardButton(text = "Назад", callback_data="Назад2")
ikb_admin_start.add(ikb_admin_start_1).add(ikb_admin_start_2).add(ikb_admin_start_3)


ikbadmin_tur = InlineKeyboardMarkup()
ikbadmin_tur1 = InlineKeyboardButton(text = "Изменить изображение", callback_data="Изменить изображение турниров")
ikbadmin_tur2 = InlineKeyboardButton(text = "Изменить описание", callback_data="Изменить описание турниров")
ikbadmin_tur3 = InlineKeyboardButton(text = "Назад", callback_data="Назад2")
ikbadmin_tur.add(ikbadmin_tur1).add(ikbadmin_tur2).add(ikbadmin_tur3)

ikbadmin_akcii = InlineKeyboardMarkup()
ikbadmin_akcii1 = InlineKeyboardButton(text = "Изменить изображение", callback_data="Изменить изображение акций")
ikbadmin_akcii2 = InlineKeyboardButton(text = "Изменить описание", callback_data="Изменить описание акций")
ikbadmin_akcii3 = InlineKeyboardButton(text = "Назад", callback_data="Назад2")
ikbadmin_akcii.add(ikbadmin_akcii1).add(ikbadmin_akcii2).add(ikbadmin_akcii3)



