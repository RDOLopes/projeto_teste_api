from pymongo import MongoClient

from app.settings import DB_NAME

DATABASE_URL = "mongodb://mongo:root@127.0.0.1:27017/projetoTesteDB"
client_mongo = MongoClient(DATABASE_URL)
mongo_database = client_mongo[DB_NAME]


