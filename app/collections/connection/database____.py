import sqlalchemy
import databases

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings import DB_PROTOCOL, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, DB_NAME

# DATABASE_URL = DB_PROTOCOL + "://?" + DB_USER + ":" +DB_PASSWORD+"@" +DB_HOST+ ":" +DB_PORT+ "/" + DB_NAME
DATABASE_URL = "mongodb://mongo:root@127.0.0.1:27017/projetoTesteDB"


engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def return_databases():
    return databases.Database(DATABASE_URL)
