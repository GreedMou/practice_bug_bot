from aiogram import types
from sqlalchemy.orm.session import Session as ConnectedSession

from bot.database.main import Session
from bot.database.models.main import User, Defect, DefectPhoto


def new_user(msg: types.Message):
    with Session() as __session:
        __session: ConnectedSession
        __instance = User(
            Tg_id=msg.from_id,
            Name=msg.from_user.full_name,

        )
        __session.add(__instance)
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return __instance


def new_defect(data: dict):
    with Session() as __session:
        __session: ConnectedSession
        __instance = Defect(
            Description=data['desc'],
            Room_number=data['room_number'],
            Author_id=data['author_id']
        )
        __session.add(__instance)
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return __instance


def new_defect_photo(def_id: int, image_data):
    with Session() as __session:
        __session: ConnectedSession
        __instance = DefectPhoto(
            Defect_id=def_id,
            ImageData=image_data
        )
        __session.add(__instance)
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return __instance
