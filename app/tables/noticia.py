from sqlalchemy import Column, String, DateTime

from .connection.database import Base
from .connection.model_base import ModelBase


class Noticia(Base, ModelBase):
    __tablename__ = "noticia"

    titulo = Column(String)
    conteudo = Column(String)
    data_publicacao = Column(DateTime)
