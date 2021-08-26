from typing import Optional
from .model_base_dto import ModelBaseDto


class UsuarioDto(ModelBaseDto):
    email: Optional[str]
    senha: Optional[str]

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    class Config:
        orm_mode = True