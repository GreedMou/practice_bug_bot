from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm.session import Session as ConnectedSession
from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select as ConnectedSelect

from bot.database.main import Session
from bot.database.models.main import User, Defect, DefectPhoto


def user_by_tg_id(tg_id: str | int):
    tg_id = str(tg_id)
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


def user_by_user_id(user_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(User)
        statement = statement.where(User.User_id == user_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result


def users_by_role_id(role_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(User)
        statement = statement.where(User.Role_id == role_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result


def defect_by_id(defect_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(Defect)
        statement = statement.where(Defect.Defect_id == defect_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result


def defects_by_status_id(status_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(Defect)
        statement = statement.where(Defect.Status_id == status_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result


def defects_by_repairman_id(repairman_id: int) -> list[Defect]:
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(Defect)
        statement = statement.where(Defect.Repairman_id == repairman_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result


def defectphoto_by_id(defect_id: int):
    with Session() as __session:
        __session: ConnectedSession
        statement: ConnectedSelect = select(DefectPhoto)
        statement = statement.where(DefectPhoto.Defect_id == defect_id)
        res: ScalarResult = __session.scalars(statement)
        result = res.all()
        __session.flush()
        __session.expunge_all()
        __session.commit()
    return result
