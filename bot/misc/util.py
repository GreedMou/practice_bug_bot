from aiogram import types


def callback_wrapper(func):
    """Remove Inline Markup in message"""

    async def wrapper(*args, **kwargs):
        callback_query: types.CallbackQuery = args[0]
        if isinstance(callback_query, types.Message):
            await func(*args, **kwargs)
            return
        message: types.Message = callback_query.message
        __inline_dict = {}
        __inline_general_list = callback_query.message.reply_markup.inline_keyboard
        for __inline_list in __inline_general_list:
            for __item in __inline_list:
                __inline_dict[__item['callback_data']] = __item['text']
        __action = __inline_dict.get(callback_query.data, 'Не установлено')
        await message.edit_text(text=message.text, reply_markup=None)

        await func(*args, **kwargs)

    return wrapper
