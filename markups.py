from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# --- Main Menu ---
btnprice = KeyboardButton('/OZON_FBS')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnprice)

# --- POD Menu OZON ---
btncobr = KeyboardButton('/Сборки_OZON')
btnotprav = KeyboardButton('/Отгрузки_OZON')
btnback = KeyboardButton('/Назад')
menuzakaz = ReplyKeyboardMarkup(resize_keyboard=True).add(btncobr, btnotprav)

def genmarkup(data): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(InlineKeyboardButton(text=f"Собрать заказ: {data}", callback_data=data)) #Создаём кнопки, data - название, data - каллбек дата
    return markup #возвращаем клавиатуру

def markupp(data): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.add(InlineKeyboardButton(text=f"Документы для: {data}", callback_data=data)) #Создаём кнопки, data - название, data - каллбек дата
    return markup #возвращаем клавиатуру