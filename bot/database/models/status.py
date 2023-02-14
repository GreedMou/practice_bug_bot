import sqlalchemy as sa

from bot.database.main import Base


class Statuses(Base):
    __tablename__ = 'Statuses'
    Status_id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String)
