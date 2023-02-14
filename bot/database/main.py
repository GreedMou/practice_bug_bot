from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_url = URL.create(
    "mssql+pyodbc",
    username="sqlserver",
    password="iXnPsxt1/G]f<:JK",
    host="34.154.100.212",
    port=1433,
    database="DefectsServiceDB",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes"
    },
)

engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
