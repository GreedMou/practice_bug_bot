from aiogram import types
from sqlalchemy.orm.session import Session as ConnectedSession

from bot.database.main import Session
from bot.database.models.main import User


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
