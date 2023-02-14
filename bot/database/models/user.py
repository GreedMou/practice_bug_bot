import sqlalchemy as sa
from sqlalchemy.dialects import mssql

from bot.database.main import Base


class Users(Base):
    __tablename__ = 'Users'
    User_id = sa.Column(sa.Integer, primary_key=True)
    Tg_id = sa.Column(sa.Integer)
    Role_id = sa.Column(sa.Integer, sa.ForeignKey('Roles.Role_id'))
    Is_available = sa.Column(mssql.BIT)
