import datetime

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.database.methods import get, create, update
from bot.database.models.main import Defect
from bot.keyboards import reply, inline
from bot.misc.util import callback_wrapper


class DefectForm(StatesGroup):
    insert_room_number = State()
    insert_desc = State()
    is_insert_photo = State()
    wait_for_photo = State()


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


async def add_defect_command(msg: types.Message, state: FSMContext):
    await msg.answer(text='Введіть номер кімнати')
    await state.set_state(DefectForm.insert_room_number)


async def room_number_choosen(msg: types.Message, state: FSMContext):
    await msg.answer(text='Опишіть поломку')
    await state.update_data(room_number=msg.text)
    await state.set_state(DefectForm.insert_desc)


async def desc_written(msg: types.Message, state: FSMContext):
    await msg.answer('Завантажити фото?', reply_markup=inline.get_photo_kb())
    await state.update_data(desc=msg.text)
    await state.set_state(DefectForm.is_insert_photo)


@callback_wrapper
async def photo_sending(callback: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    await callback.message.edit_text('Відправте фото')
    await state.set_state(DefectForm.wait_for_photo)


@callback_wrapper
async def defect_endpoint(data: types.CallbackQuery | types.Message, state: FSMContext, *args, **kwargs):
    if type(data) == types.Message:
        msg = data

    elif type(data) == types.CallbackQuery:
        msg = data.message

    else:
        msg = 'DEFINE ME'

    user_data = await state.get_data()

    defect_data = dict()
    defect_data['author_id'] = get.user_by_tg_id(str(msg.chat.id))[0].User_id
    defect_data['desc'] = user_data['desc']
    defect_data['room_number'] = user_data['room_number']

    defect = create.new_defect(defect_data)

    if type(data) == types.Message:
        photo = await data.photo[1].download(destination_dir='temp/')
        print('MSG')
        with open(photo.name, "rb") as image:
            f = image.read()
            photo_bytes = bytearray(f)
        defect_photo = create.new_defect_photo(defect.Defect_id, photo_bytes)

    await msg.answer('Дефект успішно збережено', reply_markup=reply.get_tech_kb())

    repair_users = get.users_by_role_id(3)
    message_text = f"З'явився новий дефект\n" \
                   f"Номер кімнати: {defect_data['room_number']}\n\n" \
                   f"Опис: {defect_data['desc']}"

    photos = get.defectphoto_by_id(defect.Defect_id)

    for rep_user in repair_users:
        if len(photos) != 0:
            await data.bot.send_photo(rep_user.Tg_id, photos[0].ImageData)
        await data.bot.send_message(rep_user.Tg_id, message_text, reply_markup=inline.get_defect_accept_kb(defect))

    await state.finish()
    await state.reset_data()


@callback_wrapper
async def accept_defect_endpoint(data: types.CallbackQuery, *args, **kwargs):
    callback_tuple = data.data.split()
    defect_id = int(callback_tuple[1])
    defect = get.defect_by_id(defect_id)

    if len(defect) == 0:
        await data.message.answer("Некоректний дефект, зв'яжіться з адміністратором")
        return

    defect: Defect = defect[0]

    if defect.Repairman_id:
        await data.message.edit_text('Дефект вже отриманий іншим працівником')
        return

    repairman_id = get.user_by_tg_id(data.from_user.id)[0].User_id
    res = update.defect_info(defect_id, {'Repairman_id': repairman_id, 'Status_id': 2})
    print(f'DEFECT {defect_id} UPDATE: {res}')
    if res == 1:
        await data.message.answer(f'Дефект {defect_id} в кімнаті {defect.Room_number} успішно взятий.')
    else:
        await data.message.answer("Некоректний дефект, зв'яжіться з адміністратором")


async def open_defect_list(msg: types.Message):
    defects = get.defects_by_status_id(1)

    if len(defects) == 0:
        await msg.answer('Відкриті дефекти відсутні')
        return

    for defect in defects:
        text = f"Дефект №{defect.Defect_id}\n" \
               f"Номер кімнати: {defect.Room_number}\n" \
               f"Опис: {defect.Description}\n"
        await msg.answer(text, reply_markup=inline.get_open_defect_kb(defect))


async def defect_list(msg: types.Message):
    user = get.user_by_tg_id(msg.from_id)[0]
    defects = get.defects_by_repairman_id(user.User_id)
    defect_count = 0
    if len(defects) == 0:
        await msg.answer('У вас немає дефектів в обробці')
        return

    for defect in defects:
        if defect.Status_id in [2, 3]:
            continue

        text = f"Дефект №{defect.Defect_id}\n" \
               f"Номер кімнати: {defect.Room_number}\n" \
               f"Опис: {defect.Description}\n"
        await msg.answer(text, reply_markup=inline.get_defect_kb(defect))
        defect_count += 1

    if defect_count == 0:
        await msg.answer('У вас немає дефектів в обробці')


async def get_defect_photo(data: types.CallbackQuery):
    defect_id = int(data.data.split()[1])
    photo = get.defectphoto_by_id(defect_id)

    if len(photo) == 0:
        await data.message.reply('Нема фото')
    else:
        await data.message.reply_photo(photo[0].ImageData)


@callback_wrapper
async def defect_complete(data: types.CallbackQuery, *args, **kwargs):
    defect_id = int(data.data.split()[1])
    query_dict = {
        'Status_id': 3,
        'Date_close': datetime.datetime.utcnow()
    }
    update.defect_info(defect_id, query_dict)

    await data.message.edit_text(data.message.text + '\n\n<b>Дефект виправлений</b>')


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_callback_query_handler(photo_sending, lambda x: x.data == 'defect_photo_yes',
                                       state=DefectForm.is_insert_photo)
    dp.register_callback_query_handler(defect_endpoint, lambda x: x.data == 'defect_photo_no',
                                       state=DefectForm.is_insert_photo)
    dp.register_callback_query_handler(accept_defect_endpoint, lambda x: x.data.split()[0] == 'defect_accept')
    dp.register_callback_query_handler(get_defect_photo, lambda x: x.data.split()[0] == 'defect_photo')
    dp.register_callback_query_handler(defect_complete, lambda x: x.data.split()[0] == 'defect_complete')

    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(register_command, Text('📖 Реєстрація'))
    dp.register_message_handler(login_command, Text('🔐 Вхід'))
    dp.register_message_handler(add_defect_command, Text('➡ Додати дефект'))
    dp.register_message_handler(defect_list, Text('📘 Список дефектів'))
    dp.register_message_handler(open_defect_list, Text('📂 Відкриті дефекти'))
    dp.register_message_handler(room_number_choosen, state=DefectForm.insert_room_number, regexp='^[0-9]*$')
    dp.register_message_handler(desc_written, state=DefectForm.insert_desc)
    dp.register_message_handler(defect_endpoint, state=DefectForm.wait_for_photo, content_types=['photo'])
