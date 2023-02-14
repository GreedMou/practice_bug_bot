import sqlalchemy as sa
from sqlalchemy.dialects import mssql

from bot.database.main import Base


class Defects(Base):
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
