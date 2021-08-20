from datetime import datetime
from typing import Optional

from .model_base_dto import ModelBaseDto


class NoticiaDto(ModelBaseDto):
    titulo: Optional[str]
    conteudo: Optional[str]
    data_publicacao: Optional[datetime]

    def __init__(self, titulo, conteudo, data_publicacao):
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_publicacao = data_publicacao

    class Config:
        orm_mode = True