from aiogram.types import ReplyKeyboardMarkup


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
        '📖 Реєстрація', '🔐 Вхід'
    ).add('💁🏻 Допомога')

    return kb


def get_tech_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('➡ Додати дефект')

    return kb


def get_repair_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.row('📂 Відкриті дефекти', '📘 Список дефектів')

    return kb
