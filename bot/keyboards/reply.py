from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_kb():
    button1 = KeyboardButton('📖 Реєстрація')
    button2 = KeyboardButton('🔐 Вхід')
    button3 = KeyboardButton('💁🏻 Допомога')

    start_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
        button1, button2
    ).add(button3)

    return start_kb
