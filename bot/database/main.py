from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.misc import TgKeys

connection_url = URL.create(
    "mssql+pyodbc",
    username=TgKeys.DB_USER,
    password=TgKeys.DB_PASS,
    host=TgKeys.DB_HOST,
    port=1433,
    database=TgKeys.DB_NAME,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes"
    },
)

engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
