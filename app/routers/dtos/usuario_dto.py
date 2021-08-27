from typing import Optional
from .model_base_dto import ModelBaseDto


class UsuarioDto(ModelBaseDto):
    email: Optional[str]
    senha: Optional[str]

    class Config:
        orm_mode = True


class UsuarioLoginDto(ModelBaseDto):
    username: Optional[str]
    senha: Optional[str]

    class Config:
        orm_mode = True