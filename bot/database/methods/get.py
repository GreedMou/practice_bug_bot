from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm.session import Session as ConnectedSession
from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select as ConnectedSelect

from bot.database.main import Session
from bot.database.models.main import User


def user_by_tg_id(tg_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(User)
        statement = statement.where(User.Tg_id == tg_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result
