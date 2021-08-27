from datetime import datetime
from typing import Optional

from .model_base_dto import ModelBaseDto


class NoticiaDto(ModelBaseDto):
    titulo: Optional[str]
    conteudo: Optional[str]
    data_publicacao: Optional[datetime]

    class Config:
        orm_mode = True