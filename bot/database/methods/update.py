from sqlalchemy.orm.query import Query as ConnectedQuery
from sqlalchemy.orm.session import Session as ConnectedSession

from bot.database.main import Session
from bot.database.models.main import Defect


def defect_info(defect_id: int, querry_dict: dict) -> int:
    """
    Update user info

    Only for related use

    :param engine: instance of sqlalchemy.engine.base.Engine
    :param __tg_id: user telegram id
    :param __info_tuple: tuple(faculty, form, course, group)
    :return: count of updated users (normal value is 1)
    """
    with Session() as __session:
        __session: ConnectedSession
        __query: ConnectedQuery = __session.query(Defect).filter(Defect.Defect_id == defect_id)
        __update_count = __query.update(
            querry_dict
        )
        __session.commit()
    return __update_count
