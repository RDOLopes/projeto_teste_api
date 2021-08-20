import sqlalchemy
import databases

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings import DB_PROTOCOL, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

# engine = create_engine("mongodb:///?Server=MyServer&;Port=27017&Database=test&User=test&Password=Password")
DATABASE_URL = DB_PROTOCOL + ":///?Server=" + DB_HOST + "&;Port=" + DB_PORT + "&User=" + DB_USER + "&Password=" + DB_PASSWORD
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def return_databases():
    return databases.Database(DATABASE_URL)
