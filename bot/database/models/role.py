import sqlalchemy as sa

from bot.database.main import Base


class Roles(Base):
    __tablename__ = 'Roles'
    Role_id = sa.Column(sa.Integer, primary_key=True)
    Name = sa.Column(sa.String)
