from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart

from bot.database.methods import get, create
from bot.keyboards import reply


async def bot_start(msg: types.Message):
    await msg.answer('Виберіть дію', reply_markup=reply.get_start_kb())


async def register_command(msg: types.Message):
    user = get.user_by_tg_id(msg.from_id)

    if user:
        user = user[0]
        if user.Role_id == 1:
            await msg.answer('Ваш запит оброблюється. Очікуйте на відповідь.')
        else:
            await msg.answer('Ви вже зареєстровані.')
    else:
        create.new_user(msg)
        await msg.answer('Ваш запит вислано на підтвердженння. Очікуйте на відповідь.')


async def login_command(msg: types.Message):
    user = get.user_by_tg_id(msg.from_id)

    if user:
        user = user[0]
        if user.Role_id == 1:
            await msg.answer('Ваш запит оброблюється. Очікуйте на відповідь.')
            return

        if not user.Is_available:
            await msg.answer('Ваш акаунт виключений.')
            return

        if user.Role_id == 2:
            await msg.answer('Виберіть дію', reply_markup=reply.get_tech_kb())
            return

        if user.Role_id == 3:
            await msg.answer('Виберіть дію', reply_markup=reply.get_repair_kb())
            return

        await msg.answer('Ваша роль не визначена.')
    else:
        await msg.answer('Ви ще не зареєстровані.')


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(register_command, Text('📖 Реєстрація'))
    dp.register_message_handler(login_command, Text('🔐 Вхід'))
