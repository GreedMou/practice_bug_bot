import sqlalchemy as sa
from sqlalchemy.dialects import mssql

from bot.database.main import Base


class User(Base):
    __tablename__ = 'Users'
    User_id = sa.Column(sa.Integer, primary_key=True)
    Tg_id = sa.Column(sa.Integer)
    Name = sa.Column(sa.String)
    Role_id = sa.Column(sa.Integer, sa.ForeignKey('Roles.Role_id'), default=1)
    Is_available = sa.Column(mssql.BIT, default=0)

    def __repr__(self):
        return f'{self.__class__.__name__} with tg_id {self.Tg_id}'


class Status(Base):
    __tablename__ = 'Statuses'
    Status_id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String)


class Role(Base):
    __tablename__ = 'Roles'
    Role_id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String)


class Defect(Base):
    __tablename__ = 'Defects'
    Defect_id = sa.Column(sa.Integer, primary_key=True)
    Description = sa.Column(sa.String)
    Room_number = sa.Column(sa.Integer)
    Image_path = sa.Column(sa.String)
    Status_id = sa.Column(sa.Integer, sa.ForeignKey('Statuses.Status_id'))
    Date_open = sa.Column(mssql.DATETIME2)
    Date_close = sa.Column(mssql.DATETIME2)
    Author_id = sa.Column(sa.Integer, sa.ForeignKey('Users.User_id'))
    Repairman_id = sa.Column(sa.Integer, sa.ForeignKey('Users.User_id'))
