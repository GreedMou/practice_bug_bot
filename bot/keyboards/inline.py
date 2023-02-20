from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_photo_kb() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton('Так', callback_data='defect_photo_yes')
    btn2 = InlineKeyboardButton('Ні', callback_data='defect_photo_no')
    kb = InlineKeyboardMarkup().row(btn1, btn2)

    return kb


def get_defect_accept_kb(defect) -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton('Взяти дефект', callback_data=f'defect_accept {defect.Defect_id}')
    kb = InlineKeyboardMarkup().add(btn1)

    return kb


def get_defect_kb(defect) -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton('Отримати фото', callback_data=f'defect_photo {defect.Defect_id}')
    btn2 = InlineKeyboardButton('Позначити як виконане', callback_data=f'defect_complete {defect.Defect_id}')
    kb = InlineKeyboardMarkup().row(btn1, btn2)

    return kb


def get_open_defect_kb(defect) -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton('Отримати фото', callback_data=f'defect_photo {defect.Defect_id}')
    btn2 = InlineKeyboardButton('Взяти дефект', callback_data=f'defect_accept {defect.Defect_id}')
    kb = InlineKeyboardMarkup().row(btn1, btn2)

    return kb
