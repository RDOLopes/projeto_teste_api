from typing import List

from fastapi import Depends
from starlette import status
from starlette.responses import JSONResponse

from app.routers.dtos.usuario_dto import UsuarioDto
from app.collections.usuario import collection_usuario
from app.settings import SUCESSO_OPERACAO
from app.tools import retorna_json, retorna_sucesso_operacao, retorna_erro_nao_encontrado, retorna_erro_operacao, \
    busca_por_id, verificar_existencia, retorna_json_busca_id, retorna_json_update
from app.util import AuthHandler, get_router

router = get_router("/usuarios", ["Usuario"])
autenticador = AuthHandler()


def retorna_usuario_dto(usuario):
    return UsuarioDto(id=usuario["id"], email=usuario["email"], senha=usuario["senha"])


@router.get("/")
async def buscar(token=Depends(autenticador.auth_wrapper)) -> List[UsuarioDto]:
    usuarios = collection_usuario.find({})
    if usuarios.count() > 0:
        array_usuarios_dto = [retorna_usuario_dto(usuario) for usuario in usuarios]
        return retorna_sucesso_operacao(array_usuarios_dto)
    retorna_erro_nao_encontrado()


@router.get("/{usuario_id}")
async def buscar(usuario_id, token=Depends(autenticador.auth_wrapper)) -> List[UsuarioDto]:
    try:
        usuario = busca_por_id(usuario_id, collection_usuario)
    except Exception:
        raise retorna_erro_operacao()
    if verificar_existencia(usuario):
        return retorna_sucesso_operacao(retorna_usuario_dto(usuario))
    retorna_erro_nao_encontrado()


@router.post("/")
# async def criar(usuario_dto: UsuarioDto, token=Depends(autenticador.auth_wrapper)) -> UsuarioDto:
async def criar(usuario_dto: UsuarioDto) -> UsuarioDto:
    try:
        usuario_dto.senha = autenticador.encriptar_senha(usuario_dto.senha)
        collection_usuario.insert_one(retorna_json(usuario_dto))
        return retorna_sucesso_operacao(usuario_dto)
    except Exception:
        retorna_erro_operacao()


@router.put("/")
async def alterar(usuario_dto: UsuarioDto, token=Depends(autenticador.auth_wrapper)) -> UsuarioDto:
    if verificar_existencia(busca_por_id(usuario_dto.id, collection_usuario)):
        try:
            collection_usuario.update_one(retorna_json_busca_id(usuario_dto.id), retorna_json_update(usuario_dto))
            return retorna_sucesso_operacao(usuario_dto)
        except Exception:
            retorna_erro_operacao()
    retorna_erro_nao_encontrado()


@router.delete("/")
async def delete(usuario_id: int, token=Depends(autenticador.auth_wrapper)):
    if verificar_existencia(busca_por_id(usuario_id, collection_usuario)):
        try:
            collection_usuario.delete_one(retorna_json_busca_id(usuario_id))
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO})
        except Exception:
            retorna_erro_operacao()
    retorna_erro_nao_encontrado()

