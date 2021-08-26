from typing import List

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.routers.dtos.usuario_dto import UsuarioDto
from app.collections.usuario import collection_usuario
from app.settings import ERRO_OPERACAO, SUCESSO_OPERACAO
from app.tools import retorna_json, retorna_sucesso_operacao, retorna_erro_nao_encontrado, retorna_erro_operacao, \
    busca_por_id, verificar_existencia, retorna_json_busca_id
from app.util import AuthHandler, get_router, get_db

router = get_router("/usuarios", ["Usuario"])
autenticador = AuthHandler()


@router.get("/")
async def buscar(token=Depends(autenticador.auth_wrapper)) -> List[UsuarioDto]:
    try:
        usuarios = collection_usuario.find()
        if usuarios:
            array_usuarios_dto = [UsuarioDto(usuario.email) for usuario in
                                  usuarios]
            return retorna_sucesso_operacao(array_usuarios_dto)
        else:
            retorna_erro_nao_encontrado()
    except Exception:
        retorna_erro_operacao()


@router.get("/")
async def buscar(usuario_id, token=Depends(autenticador.auth_wrapper)) -> List[UsuarioDto]:
    try:
        usuario = busca_por_id(usuario_id)
        if verificar_existencia(usuario):
            return retorna_sucesso_operacao(usuario)
        retorna_erro_nao_encontrado()
    except Exception:
        raise retorna_erro_operacao()


@router.post("/")
async def criar(usuario_dto: UsuarioDto, token=Depends(autenticador.auth_wrapper)) -> UsuarioDto:
    try:
        usuario_json = retorna_json(usuario_dto)
        collection_usuario.insert_one(usuario_json)
        return retorna_sucesso_operacao(usuario_dto)
    except Exception:
        retorna_erro_operacao()


@router.put("/")
async def alterar(usuario_dto: UsuarioDto, token=Depends(autenticador.auth_wrapper)) -> UsuarioDto:
    try:
        if verificar_existencia(busca_por_id(usuario_dto.id, collection_usuario)):
            usuario_json = retorna_json(usuario_dto)
            collection_usuario.update_one(retorna_json_busca_id(usuario_dto.id), usuario_json)
            return retorna_sucesso_operacao(usuario_dto)
        retorna_erro_nao_encontrado(usuario_dto.id)
    except Exception:
        retorna_erro_operacao()


@router.delete("/")
async def delete(usuario_id: int, token=Depends(autenticador.auth_wrapper)):
    try:
        if verificar_existencia(busca_por_id(usuario_id)):
            collection_usuario.delete_one(retorna_json_busca_id(usuario_id))
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO})
        retorna_erro_nao_encontrado(usuario_id)
    except Exception:
        retorna_erro_operacao()
